#!/usr/bin/env python
# Lyle Scott, III  // lyle@digitalfoo.net // Copyright 2013

import json
import sys

import constants
from parsers import ParserEmail
from parsers import ParserLog


def usage():
    """Usage statement."""
    me = sys.argv[0]
    print 'USAGE: %s' % me
    sys.exit(1)


def get_parsers():
    """Parse arguments."""
    objs = []

    if constants.getConstant('EMAIL_ENABLE'):
        objs.append(ParserEmail)

    if constants.getConstant('LOG_ENABLE'):
        objs.append(ParserLog)

    return objs


def run(args):
    """Do work."""
    with open('locations.json', 'w') as fp:
        fp.write('var locations = ')
        for parser in get_parsers():
            results = parser.run()
            if results:
                json.dump(list(results), fp)
        fp.write(';')        


if __name__ == '__main__':
    run(get_parsers())
