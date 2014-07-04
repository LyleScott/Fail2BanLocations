#!/usr/bin/env python

import json
import os
import sys

path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, '%s/src' % path)

try:
    import constants
except ImportError:
    print '''Problem importing src/constants.py. Make sure
src/constants.py.sample is copied to src/constants.py and is setup
properly.'''
    sys.exit(3)

from parsers import EmailLogParser
from parsers import LocalLogParser
from parsers import RemoteLogParser


def usage():
    """Usage statement."""
    print 'USAGE: %s' % sys.argv[0]
    sys.exit(1)


def get_enabled_parsers():
    """Collect the enabled parsers."""
    if constants.EMAILLOG_ENABLE:
        yield EmailLogParser, constants.EMAILLOG_ARGS

    if constants.LOCALLOG_ENABLE:
        yield LocalLogParser, constants.LOCALLOG_ARGS

    if constants.REMOTELOG_ENABLE:
        yield RemoteLogParser, constants.REMOTELOG_ARGS


def run():
    """Run the parsers and write a unique list of hit dates and hosts."""
    shit = {}

    for parser, parser_args in get_enabled_parsers():
        for args, kwargs in parser_args:
            for ip_info in parser(*args, **kwargs).run():
                ip = ip_info.pop('ip')
                date_ = ip_info.pop('date')

                if ip not in shit:
                    shit[ip] = (ip_info, [date_])
                else:
                    shit[ip][1].append(date_)

    with open('locations.json', 'w') as fp:
        fp.write('var locations = ')

        infos = []
        for ip in shit:
            info, dates = shit[ip]
            info.update({
                'ip': ip,
                'dates': dates
            })
            infos.append(info)

        json.dump(infos, fp, indent=2)
        fp.write(';')



if __name__ == '__main__':
    print 'HI'
    print run()
    run()