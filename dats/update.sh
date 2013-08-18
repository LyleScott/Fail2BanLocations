#!/usr/bin/env bash

SITE="http://geolite.maxmind.com/download/geoip/database/"

curdir=`pwd`
if [ $(basename $curdir) != "dats" ]; then
    if [ -d dats ]; then
        pushd dats
    else
        echo "Be in the dats directory."
        exit 1
    fi
fi

if [ $(type -P curl) ]; then
    curl $SITE/GeoLiteCity.dat.gz | gzip -d > GeoLiteCity.dat
elif [ $(type -P wget) ]; then
    wget -O - $SITE/GeoLiteCity.dat.gz | gzip -d > GeoLiteCity.dat
elif [ $(type -P fetch) ]; then
    fetch -o - $SITE/GeoLiteCity.dat.gz | gzip -d > GeoLiteCity.dat
else
    echo "Couldn't figure out how to automagically download the file."
    echo "Down load the file manually and store in the 'dats' directory:"
    echo "${SITE}/GeoLiteCity.dat.gz"
    echo "...also, decompress it with 'gzip -d GeoLiteCity.dat.gz'"
fi
