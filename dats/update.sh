#!/bin/sh

SITE="http://geolite.maxmind.com/download/geoip/database/"

#curl $SITE/GeoLiteCountry/GeoIP.dat.gz | gzip -d > GeoIP.dat
curl $SITE/GeoLiteCity.dat.gz | gzip -d > GeoLiteCity.dat
