import re
from glob import glob

import constants
from parsers import BaseParser


class LocalLogParser(BaseParser):
    """Parse hosts from fail2ban log files."""

    SOURCE_TYPE = 'LocalLog'

    DEFAULT_IP_REGEX = re.compile(
            r'(\d\d\d\d-\d\d-\d\d).* \[(.*?)\] Ban ([0-9]+(?:\.[0-9]+){3})')

    def __init__(self, files, ip_regex=None, *args, **kwargs):
        """Initialization."""
        super(LocalLogParser, self).__init__(*args, **kwargs)

        if files and not hasattr(files, '__iter__'):
            files = [files]

        self.files = files
        self.ip_regex = ip_regex or self.DEFAULT_IP_REGEX

    def extract_ips(self):
        """Extract (when, ip, service) tuples from fail2ban log file(s) or
        glob(s).
        """
        for glob_ in self.files:
            for file_ in glob(glob_):
                with open(file_) as fp:
                    for when, service, ip in re.findall(self.ip_regex, fp.read()):
                        yield (when, ip, service, 'localhost', self.SOURCE_TYPE)

    def run(self):
        """Do work."""
        ips = self.extract_ips()
        locations = self.get_locations(ips)

        return super(LocalLogParser, self).run(locations)
