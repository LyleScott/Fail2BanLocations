#!/usr/bin/env bash

GEOIP_ADDR="http://geolite.maxmind.com/download/geoip/database/"
script_dir="$(cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd)"

if [ $(type -P curl) ]; then
    curl $GEOIP_ADDR/GeoLiteCity.dat.gz | gzip -d > GeoLiteCity.dat
elif [ $(type -P wget) ]; then
    wget -O - $GEOIP_ADDR/GeoLiteCity.dat.gz | gzip -d > GeoLiteCity.dat
elif [ $(type -P fetch) ]; then
    fetch -o - $GEOIP_ADDR/GeoLiteCity.dat.gz | gzip -d > GeoLiteCity.dat
else
    echo "For some reason, the GeoIP dat files will not automagically download."
    echo "Get the file manually at "
    echo "${GEOIP_ADDR}/GeoLiteCity.dat.gz"
    echo "Put the file in ${script_dir}."
fi
