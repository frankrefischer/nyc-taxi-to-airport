#!/usr/bin/env bash

echo '=== nyc taxi to airport - step 1b download taxi zone lookup'
echo

URL='https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv'
FILE='nyc-taxi-zone-lookup.csv'

if [ -e $FILE ]
then
    echo "output file exists: $FILE"
    echo "skipping"
    exit 0
fi

echo "downloading from url: $URL"
echo "writing to file: $FILE"
echo

curl "$URL" > $FILE

echo
echo "done"
