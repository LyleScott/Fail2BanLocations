Fail2BanLocations
=================

Output the locations of hosts logged or emailed by fail2ban to a JSON file so
that they can easily be mapped. See the below example for more info.

I didn't create a proper installable module, so bare with me on the (still
quick) setup process.


Setup
-------------
pip install -r requirements.txt

...or manually install:
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
* system
* source
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

![Fail2Ban Cluster Map Screenshot 1](https://raw.github.com/LyleScott/Fail2BanGoogleMap/master/html/Fail2Ban_map1_screenshot.png)
![Fail2Ban Cluster Map Screenshot 2](https://raw.github.com/LyleScott/Fail2BanGoogleMap/master/html/Fail2Ban_map2_screenshot.png)
![Fail2Ban Cluster Map Screenshot 3](https://raw.github.com/LyleScott/Fail2BanGoogleMap/master/html/Fail2Ban_map3_screenshot.png)

TODO
----

I really don't plan to do too much more, unless I hear any interest otherwise.
This was really just for fun to see where folks were coming from that were in
my logs.

EDIT: It looks like the fail2ban folks might create a 3rd party directory and
this repository is making its way in there according to a pull request. So,
I will be cleaning things up a bit and atleast documenting items more closely
so someone can hack it easier. Let me know if you think of something
interesting.

I plan to finish a few more things and that is about it:
* make the infowindow look better.
* unittests... because engineering.
* add "source" column in infowindow (email vs logfile)
* use openauth to auth to email. or atleast don't store password in plain text.
* add remotelog ability.
* add a persistence layer
