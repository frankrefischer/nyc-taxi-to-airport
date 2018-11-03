#!/usr/bin/env bash

URL='https://data.cityofnewyork.us/api/views/biws-g3hs/rows.csv?accessType=DOWNLOAD'
FILE='nyc-2017-yellow-taxi-trips.cvs.gz'

if [ -e $FILE ]
then
    echo "output file exists: $FILE"
    echo "skipping"
    exit 0
fi

curl "$URL" | gzip --best > $FILE