#!/usr/bin/env bash

echo '=== nyc taxi to airport - step 1 download taxi zone lookup'

URL='https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv'
FILE='nyc-taxi-zone-lookup.csv'

if [ -e $FILE ]
then
    echo "output file exists: $FILE"
    echo "skipping"
    exit 0
fi

curl "$URL" | gzip --best > $FILE
