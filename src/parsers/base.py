from dateutil import parser
from operator import itemgetter

import pygeoip

import constants


class BaseParser(object):
    """The bare-bones base class for parses to be built from."""

    SOURCE_TYPE = 'Unknown'
    KEYS = ['latitude', 'longitude', 'city', 'country_code', 'country_name']

    def __init__(self):
        """Initialization."""
        self.geoip = pygeoip.GeoIP(constants.GEOIP_CITY)

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
        for date_, ip, service, source, source_type in ips:
            # TODO REFACTOR
            location = self.get_location(ip)
            location.update({
                'ip': ip,
                'date': parser.parse(date_).strftime('%Y-%m-%d'),
                'service': service,
                'source': source,
                'source_type': source_type,
            })
            locations.append(location)
        return sorted(locations, key=itemgetter('date'), reverse=True)

    def get_location(self, ip):
        """Get the location info for a single IP.

        Arguments:
          ip (str): The IP address to look up location info for.

        Returns:
          A dict containing the IP information specified in KEYS.
        """
        print 'IP', ip
        record = self.geoip.record_by_addr(ip)
        return {key: record[key] for key in self.KEYS}

    def run(self, locations):
        """Return the locations and do any things here that need to be done on
        all locations.
        """
        return locations
