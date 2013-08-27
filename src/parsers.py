# Lyle Scott, III  // lyle@digitalfoo.net // Copyright 2013

import imaplib
import email
import re
from glob import glob
from operator import itemgetter

import pygeoip
from dateutil import parser

import constants


class Parser(object):
    """The bare-bones base class for parses to be built from."""

    KEYS = ['latitude', 'longitude', 'city', 'country_code', 'country_name']

    def __init__(self):
        """Initialization."""
        self.geoip = pygeoip.GeoIP(constants.getConstant('GEOIP_CITY'))

    def get_locations(self, ips):
        """Get a list of dict objects that contain the location and hit-date
        for each ip in ips.

        Arguments:
          ips (sequence): A sequence of (ips, hit-date) tuples to iterate
            through and look up the location for. 

        Returns:
          A list of dicts containing the location info for each IP sorted by
            the hit-date in ascending order (most recent first).
        """
        locations = []
        for ip, date_ in ips:
            location = self.get_location(ip)
            location.update({
                'ip': ip,
                'date': parser.parse(date_).strftime('%Y-%m-%d')})
            locations.append(location)
        return sorted(locations, key=itemgetter('date'), reverse=True)

    def get_location(self, ip):
        """Get the location info for a single IP.

        Arguments:
          ip (str): The IP address to look up location info for.

        Returns:
          A dict containing the IP information specified in KEYS.
        """  
        record = self.geoip.record_by_addr(ip)
        return {key: record[key] for key in self.KEYS}

    def run(self, locations):
        """Return the locations and do any things here that need to be done on
        all locations.
        """
        return locations


class ParserEmail(Parser):
    """Parse hosts from an imap(s) inbox."""

    def __init__(self):
        """Initialization."""
        super(ParserEmail, self).__init__()
        self.host = constants.getConstant('EMAIL_HOST')
        self.is_ssl = constants.getConstant('EMAIL_HOST_SSL')
        self.user = constants.getConstant('EMAIL_USER')
        self.passwd = constants.getConstant('EMAIL_PASS')
        self.search = constants.getConstant('EMAIL_SEARCH')
        self.regex = constants.getConstant('EMAIL_IP_REGEX')

    def login(self):
        """Login to the imap(s) server with credentials.
        
        Returns:
          A handle to the imap server connection.
        """
        if self.is_ssl is True:
            handler = imaplib.IMAP4_SSL
        else:
            handler = imaplib.IMAP4

        handle = handler(self.host)
        handle.login(self.user, self.passwd)

        return handle

    def get_emails(self, handle):
        """Get the emails that satisfy the search criteria.

        Arguments:
          handle ():

        Returns:
          ...
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
          emails ():

        Returns:  
          ...
        """
        for email_ in emails:
            msg = email_.get_payload()
            date_ = email_['Date']
            ip = re.search(self.regex, msg)
            if not ip:
                # TODO: how to handle?
                continue
            yield (ip.groups()[0], date_)

    @classmethod
    def run(cls):
        """TODO"""
        parser = cls()
        handle = parser.login()
        emails = parser.get_emails(handle)
        ips = parser.extract_ips(emails)
        locations = parser.get_locations(ips)

        return super(ParserEmail, parser).run(locations)


class ParserLog(Parser):
    """Parse hosts from fail2ban log files."""

    def __init__(self):
        """Initialization."""
        super(ParserLog, self).__init__()
        self.regex = constants.getConstant('LOG_IP_REGEX')

    def extractIpsWithDates(self):
        """TODO"""
        ips = []
        for log in constants.getConstant('LOGS'):
            for file in glob(log):
                with open(log) as fp:
                    ips.extend(re.findall(self.regex, fp.read()))

        return [(ip[1], ip[0]) for ip in ips]

    @classmethod
    def run(cls):
        """TODO"""
        parser = cls()
        ips = parser.extractIpsWithDates()
        locations = parser.get_locations(ips)

        return super(ParserLog, parser).run(locations)
