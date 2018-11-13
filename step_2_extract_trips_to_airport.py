import pandas as pd
import os
import time

def main():
    print('=== nyc taxi to airport - step 2 extract trips to airport')

    def select_trips_to_airport(df):
        newark, jfk, laguardia = 1, 132, 138
        nyc_airports = (newark, jfk, laguardia)

        return df[df.DOLocationID.isin(nyc_airports)]

    input_file = 'nyc-2017-yellow-taxi-trips.cvs.gz'
    output_file = 'nyc-2017-yellow-taxi-trips-to-airport.cvs.gz'

    if os.path.exists(output_file):
        print("output file exists:", output_file)
        print("skipping")
        return

    df = load_dataset(input_file, select_trips_to_airport)
    save_dataset(df, output_file)
    print('done')

def load_dataset(filepath, data_filter, chunksize=10_000_000):
    print('loading file:', filepath)
    df = pd.DataFrame()
    lines = 0
    start_time = time.time()
    chunk_iterator = pd.read_csv(filepath, chunksize=chunksize, memory_map=True)

    for df_chunk in chunk_iterator:
        lines += len(df_chunk)
        df = pd.concat([df, data_filter(df_chunk)])
        elapsed_time = int(time.time() - start_time)
        print("time {:,}s | {:,} lines read in | {:,} lines selected".format(
            elapsed_time, lines, len(df)))
    return df

def save_dataset(df, filepath):
    print('saving file:', filepath)
    df.to_csv(filepath, compression='gzip')

if __name__ == '__main__':
    main()