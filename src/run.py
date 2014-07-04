#!/usr/bin/env python

import json
import os
import sys


#path = os.path.dirname(os.path.realpath(__file__))
#sys.path.insert(0, '%s/src' % path)

try:
    import constants
except ImportError:
    print '''Problem importing src/constants.py. Make sure
src/constants.py.sample is copied to src/constants.py and is setup
properly.'''
    sys.exit(3)

from parsers import ParserEmail
from parsers import ParserLocalLog
from parsers import ParserRemoteLog


def usage():
    """Usage statement."""
    me = sys.argv[0]
    print 'USAGE: %s' % me
    sys.exit(1)


def sanity_checks():
    """Sanity checks to make sure the world is OK."""
    if not os.path.exists('src/constants.py'):
        print ('Copy constants.py.sample to constants.py and fill in the '
               'appropriate options.')
        exit(2)


def get_parsers():
    """Collect the enabled parsers."""
    objs = []

    if constants.getConstant('EMAIL_ENABLE'):
        objs.append(ParserEmail)

    if constants.getConstant('LOCALLOG_ENABLE'):
        objs.append(ParserLocalLog)

    if constants.getConstant('REMOTELOG_ENABLE'):
        objs.append(ParserRemoteLog)

    return objs


def run(args):
    """Run the parsers and write a unique list of hit dates and hosts."""
    sanity_checks()

    allresults = {}

    for parser in get_parsers():
        results = parser.run() or []

        for result in results:
            key = (result['ip'], result['date'])
            if key not in allresults:
                allresults[key] = result

    allresults = allresults.values()

    print len(allresults), 'locations about to be parsed.'

    with open('locations.json', 'w') as fp:
        fp.write('var locations = ')
        json.dump(allresults, fp)
        fp.write(';')


if __name__ == '__main__':
    run(get_parsers())
