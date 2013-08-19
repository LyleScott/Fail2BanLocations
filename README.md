Fail2BanGoogleMap
=================

Map the locations of hosts logged or emailed by fail2ban.

I didn't create a proper installable module, so bare with me on the (still
quick) setup process.

Automated Setup
---------------

These need to be installed for the automated setup:
* virtualenv
* pip

Manual Setup
-------------

Install the folling Python libs:
* pygeoip
* python-dateutil

Configuration
-------------

Copy src/constants.py.sample to src/constants.py and edit the options as
necessary.


Example
-------

Once you have src/constants.py setup, you should be able to just execute run.sh
and, supposing there are no errors, locations.json will be generated in the
root directory of Fail2BanGoogleMap.

The locations.json sets a variable 'locations' to an array of dictionaries
containing location info about each IP parsed.

The dictionary has the following keys:
* ip
* date
* latitude
* longitude
* city
* country_code
* country_name

I have provided html/example.html that uses the Google Map API (v3) and the
[markerclustererplus javascript library](http://google-maps-utility-library-v3.googlecode.com/svn/trunk/markerclustererplus/)
as a simple example to map the IPs on a geographical map representing
"clusters" of IPs where you can drill down to be more specific about the
location. Basic Google Maps API foo, honestly.
