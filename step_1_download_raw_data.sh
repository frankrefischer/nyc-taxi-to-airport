#!/usr/bin/env bash

URL='https://data.cityofnewyork.us/api/views/biws-g3hs/rows.csv?accessType=DOWNLOAD'
FILE='nyc-2017-yellow-taxi-trips.cvs.gz'

curl "$URL" | gzip --best > $FILE