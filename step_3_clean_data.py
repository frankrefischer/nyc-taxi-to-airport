import pandas as pd
import numpy as np
import time
import os

def main():
    print('=== nyc taxi to airport - step 3 clean data')

    input_file = 'nyc-2017-yellow-taxi-trips-to-airport.cvs.gz'
    output_file = 'nyc-2017-yellow-taxi-trips-to-airport.pkl.gz'
    if os.path.exists(output_file):
        print("output file exists:", output_file)
        print("skipping")
        return

    zone_lookup = pd.read_csv('nyc-taxi-zone-lookup.csv', index_col=0)[:263]

    df = load_data(input_file)
    df = clean_data(df, zone_lookup)
    save_dataset(df, output_file)
    print('done')

def make_show_progress():
    start_time = time.time()
    lines_read = 0

    def show_progress(chunk_length):
        nonlocal lines_read

        lines_read += chunk_length
        elapsed_time = int(time.time() - start_time)
        print('{:,} lines read | time {:,}s'.format(lines_read, elapsed_time))

    return show_progress

def load_data(input_file):
    print('loading file:', input_file)
    cols_to_use = [
        'Unnamed: 0',
        'tpep_pickup_datetime',
        'tpep_dropoff_datetime',
        'PULocationID',
        'DOLocationID',
    ]
    data_types = {
        'PULocationID': np.int16,
        'DOLocationID': np.int16,
    }
    dates_to_parse = ['tpep_pickup_datetime', 'tpep_dropoff_datetime']
    df = pd.DataFrame()
    show_progress = make_show_progress()
    chunk_iterator = pd.read_csv(input_file,
                                 compression='gzip',
                                 chunksize=100_000,
                                 index_col=0,
                                 usecols=cols_to_use,
                                 dtype=data_types,
                                 parse_dates=dates_to_parse,
                                 infer_datetime_format=True
                                )
    for chunk in chunk_iterator:
        df = pd.concat([df, chunk])
        show_progress(len(chunk))
    return df

def clean_data(df, zone_lookup):
    
    any_location_id_missing = (df.PULocationID > 263) | (df.DOLocationID > 263)
    df = df.drop(df.index[any_location_id_missing])

    df.PULocationID.replace([104, 105], 103)
    
    df['pickup_borough'] = df.PULocationID.apply(zone_lookup.Borough.get).astype('category')
    df['pickup_zone'] = df.PULocationID.apply(zone_lookup.Zone.get).astype('category')
    df['pickup_service_zone'] = df.PULocationID.apply(zone_lookup.service_zone.get).astype('category')
    df['dropoff_zone'] = df.DOLocationID.apply(zone_lookup.Zone.get).astype('category')
    
    df = df.drop(columns=['PULocationID', 'DOLocationID'])
    
    return df

def save_dataset(df, filepath):
    print('saving file:', filepath)
    df.to_pickle(filepath, compression='gzip')

if __name__ == '__main__':
    main()
