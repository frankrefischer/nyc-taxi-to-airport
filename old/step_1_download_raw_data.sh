#!/usr/bin/env bash

echo '=== nyc taxi to airport - step 1 download raw data'

URL='https://data.cityofnewyork.us/api/views/biws-g3hs/rows.csv?accessType=DOWNLOAD'
FILE='nyc-2017-yellow-taxi-trips.cvs.gz'
                                
if [ -e $FILE ]
then
    echo "output file exists: $FILE"
    echo "skipping"
    exit 0
fi

echo "downloading from url: $URL"
echo "compressing and writing to file: $FILE"

curl "$URL" | gzip --best > $FILE

echo "done"
    