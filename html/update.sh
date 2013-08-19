#!/usr/bin/env bash
# Lyle Scott, III  // lyle@digitalfoo.net // Copyright 2013

FILE="http://google-maps-utility-library-v3.googlecode.com/svn/trunk/markerclustererplus/src/markerclusterer_packed.js"

curdir=`pwd`
if [ $(basename $curdir) != "html" ]; then
    if [ -d html ]; then
        pushd html
    else
        echo "Be in the html directory or its parent directory to run update.sh."
        exit 1
    fi
fi

#if [ $(type -P curl) ]; then
#    curl -O $FILE
if [ $(type -P wget) ]; then
    wget -N $FILE
elif [ $(type -P fetch) ]; then
    fetch $FILE
else
    echo "Couldn't figure out how to automagically download the file."
    echo "Down load the file manually and store in the 'html' directory:"
    echo "${FILE}"
fi
