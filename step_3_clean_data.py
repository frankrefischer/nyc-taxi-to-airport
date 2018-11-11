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

    df = load_data(input_file)
    df = clean_data(df)
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
        'trip_distance',
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

def clean_data(df):
    
    any_location_id_missing = (df.PULocationID > 263) | (df.DOLocationID > 263)
    df = df.drop(df.index[any_location_id_missing])
    
    df = df[df.tpep_dropoff_datetime > df.tpep_pickup_datetime]

    df.PULocationID.replace([104, 105], 103)
    
    return df

def save_dataset(df, filepath):
    print('saving file:', filepath)
    df.to_pickle(filepath, compression='gzip')

if __name__ == '__main__':
    main()
