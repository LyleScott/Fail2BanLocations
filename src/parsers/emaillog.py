import imaplib
import email
import re

from parsers import BaseParser


class EmailLogParser(BaseParser):
    """Parse hosts from an imap(s) inbox."""

    SOURCE_TYPE = 'Email'

    DEFAULT_SEARCH = '(HEADER Subject "[Fail2Ban] ssh: banned*")'
    DEFAULT_IP_REGEX = re.compile(
            r'The IP ([0-9]{1,3}(?:\.[0-9]+){3}) has just been banned .* against ([^.]+).')

    def __init__(self, user=None, password=None, host=None, host_ssl=False,
                 search=None, ip_regex=None, *args, **kwargs):
        """Initialization."""
        super(EmailLogParser, self).__init__(*args, **kwargs)
        self.user = user
        self.password = password
        self.host = host
        self.host_ssl = host_ssl
        self.search = search or self.DEFAULT_SEARCH
        self.ip_regex = ip_regex or self.DEFAULT_IP_REGEX

    def login(self):
        """Login to the imap(s) server with credentials.

        Returns:
          A handle to the imap server connection.
        """
        if self.host_ssl is True:
            handler = imaplib.IMAP4_SSL
        else:
            handler = imaplib.IMAP4

        sock = handler(self.host)
        sock.login(self.user, self.password)

        return sock

    def get_emails(self, handle):
        """Get the emails that satisfy the search criteria.

        Arguments:
          handle (imaplib_IMAP4[_SSL]): Handle to the imap connection.

        Returns:
          An iterator of email bodies.
        """
        handle.select('inbox')
        _, uids = handle.uid('search', self.search)

        uids = uids[0].split()

        for uid in uids:
            _, data = handle.uid('fetch', uid, '(RFC822)')
            yield email.message_from_string(data[0][1])

    def extract_ips(self, emails):
        """"Extract the IP addresses from the emails.

        Arguments:
          emails (seq): A sequence of emails to extract IPs from.

        Returns:
          An iterator of (date, ip, service) tuples.
        """
        r = re.compile(r'<(.*)>')

        for email_ in emails:
            msg = email_.get_payload()
            date_ = email_['Date']

            source = re.search(r, email_['From']).groups()
            if not source:
                source = 'unknown'
            else:
                source = source[0]

            ip = re.search(self.ip_regex, msg.replace('\n', ' '))
            if not ip:
                # TODO: how to handle?
                continue

            ip, service = ip.groups()
            yield (date_, ip, service, source, self.SOURCE_TYPE)

    def run(self):
        """Do work."""
        sock = self.login()
        emails = self.get_emails(sock)
        ips = self.extract_ips(emails)
        locations = self.get_locations(ips)

        return super(EmailLogParser, self).run(locations)