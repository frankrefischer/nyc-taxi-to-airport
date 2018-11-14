import pandas as pd
import numpy as np
import time
import os

input_file = 'nyc-2017-yellow-taxi-trips-to-airport.pkl.gz'
output_file = 'nyc-2017-yellow-taxi-trips-to-airport-transformed.pkl.gz'

def main():
    """Loads the cleaned data for taxi trips to airports from step 3, transforms it and saves the result.
    
    If output_file already exists, the function skips.
    Remove the output_file manually in that case.
    
    The input_file is loaded unchunked.
    
    After the whole file is loaded the function transform is applied.
    
    At the end the transformed dataset is saved as a gzipped pickle file.
    
    Remember: pickle files should only be used for temporary storage, since
    the format is not guaranteed to be stable between different lib versions.                   
    
    Keyword Arguments: -
    
    Returns: -
    """
    
    if os.path.exists(output_file):
        print("output file exists:", output_file)
        print("skipping")
        return

    print('loading file:', input_file)
    df = pd.read_pickle(input_file)

    df = transform(df)
    
    df.info(memory_usage='deep')
    
    save_as_pickle_gz(df, output_file)
    
    print('done')

def transform(df):
    """Transforms the passed dataframe.
    
    Actions done while transforming:
    - translating location ids to zone name categories
    - renaming datetime: get rid of the tpep_ prefix
    - add additional variables derived from the dropoff dateime
    - add trip duration in minutes and in hours
    - add trip velocity
    
    Keyword Arguments:
    df -- the dataframe to transform
    
    Returns: the transformed dataframe
    """
    
    print('=== nyc taxi to airport - step 4 transform')

    # zones
    df = translate_location_ids_to_zones(df)
    
    # datetimes
    df = rename_datetimes(df)
    df = add_additonal_datetime_variables(df)
    
    # duration
    df = add_trip_duration_in_minutes(df)
    df = add_trip_duration_in_hours(df)

    # velocity
    df = add_trip_velocity(df)
  
    return df
    
def translate_location_ids_to_zones(df):
    """Translating pick and dropoff location ids to zones, dropping PULocationId, DOLocationId"""
    
    print("translate location ids to zones")
    
    zone_lookup = pd.read_csv('nyc-taxi-zone-lookup.csv', index_col=0)[:263]
    lookup_borough = zone_lookup.Borough.get
    lookup_zone = zone_lookup.Zone.get
    lookup_service_zone = zone_lookup.service_zone.get

    as_cat = lambda loc_id, lookup: loc_id.apply(lookup).astype('category')
    
    df['pickup_borough'] = as_cat(df.PULocationID, lookup_borough)

    df['pickup_zone'] = as_cat(df.PULocationID, lookup_zone)
    df['dropoff_zone'] = as_cat(df.DOLocationID, lookup_zone)    

    df['pickup_service_zone'] = as_cat(df.PULocationID, lookup_service_zone)
    
    df = df.drop(columns=['PULocationID', 'DOLocationID'])
    
    return df

def rename_datetimes(df):
    """Renaming tpep_pickup_datetime and tpep_dropoff_datetime into pickup_datetime, dropoff_datetime"""
    
    print("renaming datetimes")
    df = df.rename(columns={'tpep_pickup_datetime': 'pickup_datetime',
                            'tpep_dropoff_datetime': 'dropoff_datetime'})
    
    return df

def add_additonal_datetime_variables(df): 
    """Adding variables derived from datetime: dropoff_month, *_week_of_year, *_day_of_year, *_day_of_month, *_weekday, *_is_weekend, *_hour"""
    
    print("adding additonal datetime variables")

    do_dt = df.dropoff_datetime.dt
    as_cat = lambda x: x.astype('category')
    
    df['dropoff_month'] = as_cat(do_dt.month)
    df['drop_off_week_of_year'] = as_cat(do_dt.weekofyear)
    df['dropoff_day_of_year'] = as_cat(do_dt.dayofyear)
    df['dropoff_day_of_month'] = as_cat(do_dt.day)
    df['dropoff_weekday'] = as_cat(do_dt.weekday)
    df['dropoff_is_weekend'] = as_cat(do_dt.weekday > 4)
    df['dropoff_hour'] = as_cat(do_dt.hour)
    
    return df


def add_trip_duration_in_minutes(df):
    """Adding new variable for trip duration in minutes."""
    
    print("adding trip duration in minutes")
    df['trip_duration_minutes'] = (df.dropoff_datetime - df.pickup_datetime).dt.total_seconds() / 60
    
    return df    

def add_trip_duration_in_hours(df):
    """Adding new variable for trip duration in hours."""

    print("adding trip duration in hours")
    df['trip_duration_hours'] = df.trip_duration_minutes / 60
    
    return df    


def add_trip_velocity(df):
    """Adding new variable for trip velocity (in miles per hour)."""

    print("adding trip velocity")
    df['trip_velocity'] = df.trip_distance / df.trip_duration_hours
    
    return df

def save_as_pickle_gz(df, filepath):
    """Saves a dataframe as a gzipped pickle file.
    
    Prints a simple message about the target filepath.
    
    Keyword Arguments:
    df       -- the dataframe to save
    filepath -- path with filename where the dataframe will be saved
    
    Returns: -
    """

    print('saving file:', filepath)
    df.to_pickle(filepath, compression='gzip')

if __name__ == '__main__':
    main()
