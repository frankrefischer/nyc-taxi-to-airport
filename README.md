# Duration of Yellow Taxi Trips to Airports in NYC

## Motivation

Me and my wife stayed in NYC recently and missed our plane, since our taxi got stuck in traffix jam.
Could we have planned better? Or was it just bad luck?

## Summary of Results

99% of all yellow taxi rides in 2017 starting in Murray Hill (like us) and heading for Newark Airport (like us) at a Friday arriving target at 17:XX (like is) did not need more than 124 minutes. Our ride took >160 minutes. So yes, it was bad luck, not bad planning.

Further more if we plan to stay next time in Murray Hill, then it is helpful to know that taxi transfer to LaGuardia Airport is fastest: the 99-percentile duration for trips from Murray Hill to LaGuardua is only 65 minutes compared to 102 minutes for Newark Airport.

The other way around: if we need to take Newark Airport, then we should consider to choose a hotel in Manhattan, thats closer to the Holland Tunnel or George Washington Bridge, since these zones have the best transfer times to Newark Airport.

## Files

See [Overview_and_Business_Understanding.ipynb](Overview_and_Business_Understanding.ipynb)
There you find links to more notebooks. 

## command line tools

To download, clean and prepare the raw data, there are the following command line
tools available.

### [step_1a_download_raw_data.sh](step_1a_download_raw_data.sh)
### [step_1b_download_taxi_zone_lookup.sh](step_1b_download_taxi_zone_lookup.sh)
### [step_2_extract_trips_to_airport.py](step_2_extract_trips_to_airport.py)
### [step_3_clean_data.py](step_3_clean_data.py)
### [step_4_transform.py](step_4_transform.py)

You can find details, about their use in the notebooks
- [Data Understanding](Data_Understanding.ipynb)
- and [Prepare Data](Prepare_Data.ipynb)

## Libraries
- pandas
- numpy
- matplotlib
- seaborn

## Tools
- bash
- curl
- gzip

