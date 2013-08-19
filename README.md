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

I have provided [html/example.html](https://github.com/LyleScott/Fail2BanGoogleMap/blob/master/html/example.html)
which reads locations.json into the [Google Map API (v3)](https://developers.google.com/maps/documentation/javascript/) with the
[markerclustererplus javascript library](http://google-maps-utility-library-v3.googlecode.com/svn/trunk/markerclustererplus/)
leveraged as a simple example to map the IPs on a geographical map representing
"clusters" of IPs where you can drill down to be more specific about the
location. Basic Google Maps API foo, honestly.

!(Fail2Ban Cluster Map Screenshot 1)[https://raw.github.com/LyleScott/Fail2BanGoogleMap/master/html/Fail2Ban_map1_screenshot.png]
!(Fail2Ban Cluster Map Screenshot 2)[https://raw.github.com/LyleScott/Fail2BanGoogleMap/master/html/Fail2Ban_map2_screenshot.png]
!(Fail2Ban Cluster Map Screenshot 3)[https://raw.github.com/LyleScott/Fail2BanGoogleMap/master/html/Fail2Ban_map3_screenshot.png]

TODO
----

I really don't plan to do too much more, unless I hear any interest otherwise.
This was really just for run to see where folks were coming from that were in
my logs. I'll probably use the library in many other ways, anyways.

I do plan to finish a few things soon, though:
* show the ip/hostname of the box that logged the IP "hit" so you can
differentiate which box was getting attacked if you wanted to use multiple
log files or have >1 box sending fail2ban messages to the same inbox.
* make the infowindow look better.
* finish log parsing since email parsing it the only parser that works.
* unittests... because engineering.
