# Lyle Scott, III  // lyle@digitalfoo.net // Copyright 2013

import imaplib
import email
import re
from operator import itemgetter

import pygeoip
from dateutil import parser

import constants


class Parser(object):

    KEYS = ['latitude', 'longitude', 'city', 'country_code', 'country_name']

    def __init__(self):
        self.geoip = pygeoip.GeoIP(constants.getConstant('GEOIP_CITY'))

    def get_locations(self, ips):
        locations = []
        for ip, date_ in ips:
            location = self.get_location(ip)
            location.update({
                'ip': ip,
                'date': parser.parse(date_).strftime('%Y-%m-%d')})
            locations.append(location)
        return sorted(locations, key=itemgetter('date'), reverse=True)

    def get_location(self, ip):
        record = self.geoip.record_by_addr(ip)
        return {key: record[key] for key in self.KEYS}

    def run(self, locations):
        return locations


class ParserEmail(Parser):

    def __init__(self):
        super(ParserEmail, self).__init__()
        self.host = constants.getConstant('EMAIL_HOST')
        self.is_ssl = constants.getConstant('EMAIL_HOST_SSL')
        self.user = constants.getConstant('EMAIL_USER')
        self.passwd = constants.getConstant('EMAIL_PASS')
        self.search = constants.getConstant('EMAIL_SEARCH')
        self.regex = constants.getConstant('EMAIL_IP_REGEX')

    def login(self):
        if self.is_ssl is True:
            handler = imaplib.IMAP4_SSL
        else:
            handler = imaplib.IMAP4

        handle = handler(self.host)
        handle.login(self.user, self.passwd)

        return handle

    def get_emails(self, handle):
        handle.select('inbox')
        _, uids = handle.uid('search', self.search)

        uids = uids[0].split()

        for uid in uids:
            _, data = handle.uid('fetch', uid, '(RFC822)')
            yield email.message_from_string(data[0][1])

    def extract_ips(self, emails):
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
        parser = cls()
        handle = parser.login()
        emails = parser.get_emails(handle)
        ips = parser.extract_ips(emails)
        locations = parser.get_locations(ips)

        return super(ParserEmail, parser).run(locations)


class ParserLog(Parser):

    def __init__(self):
        super(ParserEmail, self).__init__()
