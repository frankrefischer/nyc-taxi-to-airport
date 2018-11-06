import pandas as pd
import numpy as np
import time
import os

def main():
    print('=== nyc taxi to airport - step 4 feature engineering')

    input_file = 'nyc-2017-yellow-taxi-trips-to-airport.pkl.gz'
    output_file = 'nyc-2017-yellow-taxi-trips-to-airport-expanded.pkl.gz'
    if os.path.exists(output_file):
        print("output file exists:", output_file)
        print("skipping")
        return

    print('loading file:', input_file)
    df = pd.read_pickle(input_file)

    df = expand_features(df)
    df.info(memory_usage='deep')
    
    save_dataset(df, output_file)
    print('done')

def expand_features(df):
    
    print("expanding location ids to zones")
    zone_lookup = pd.read_csv('nyc-taxi-zone-lookup.csv', index_col=0)[:263]
    df['pickup_borough'] = df.PULocationID.apply(zone_lookup.Borough.get).astype('category')
    df['pickup_zone'] = df.PULocationID.apply(zone_lookup.Zone.get).astype('category')
    df['pickup_service_zone'] = df.PULocationID.apply(zone_lookup.service_zone.get).astype('category')
    df['dropoff_zone'] = df.DOLocationID.apply(zone_lookup.Zone.get).astype('category')    
    df = df.drop(columns=['PULocationID', 'DOLocationID'])
    
    print("expanding datetimes")
    df = df.rename(columns={'tpep_pickup_datetime': 'pickup_datetime',
                            'tpep_dropoff_datetime': 'dropoff_datetime'})
    
    df['dropoff_month'] = df.dropoff_datetime.dt.month.astype('category')
    df['drop_off_week_of_year'] = df.dropoff_datetime.dt.weekofyear.astype('category')
    df['dropoff_day_of_year'] = df.dropoff_datetime.dt.dayofyear.astype('category')
    df['dropoff_day_of_month'] = df.dropoff_datetime.dt.day.astype('category')
    df['dropoff_hour'] = df.dropoff_datetime.dt.hour.astype('category')
    
    print("adding trip duration")
    df['trip_duration_minutes'] = (df.dropoff_datetime - df.pickup_datetime).dt.total_seconds() / 60
    
    print("one hot encoding")
    one_hot = pd.get_dummies(df[['pickup_borough', 'pickup_zone', 'pickup_service_zone',
                                 'dropoff_month', 'drop_off_week_of_year',
                                 'dropoff_day_of_year','dropoff_day_of_month',
                                 'dropoff_hour']])
    df = df.join(one_hot)
    
    return df

def save_dataset(df, filepath):
    print('saving file:', filepath)
    df.to_pickle(filepath, compression='gzip')

if __name__ == '__main__':
    main()
