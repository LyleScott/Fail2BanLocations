from parsers import LocalLogParser


class RemoteLogParser(LocalLogParser):
    """Parse hosts from remote fail2ban log files."""

    SOURCE_TYPE = 'RemoteLog'