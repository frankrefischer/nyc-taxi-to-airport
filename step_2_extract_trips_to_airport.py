import pandas as pd
import os
import time

input_file = 'nyc-2017-yellow-taxi-trips.cvs.gz'
output_file = 'nyc-2017-yellow-taxi-trips-to-airport.cvs.gz'

def main():
    """Extracts trips to any airport and save the data to a gzipped csv file
    
    1) Loads file input_file
    2) Filters trips to one of the airports: Newark, JFK, LaGuardia
    3) Writes result to output_file
    
    If output_file already exists, the function skips.
    Remove the output_file manually in that case.
    
    Keyword arguments: -
    Returns: -
    """
    
    print('=== nyc taxi to airport - step 2 extract trips to airport')

    if os.path.exists(output_file):
        print("output file exists:", output_file)
        print("skipping")
        return

    df = load_dataset(input_file, filter_trips_to_airports)
    save_as_csv_gz(df, output_file)
    
    print('done')

def load_dataset(filepath, data_filter, chunksize=10_000_000):
    """Loads the dataset in chunks of chunksize from filepath, applying filter_trips_to_airports.
    
    The original dataset read in is quite big.
    To avoid to load it completely into RAM, filtering will be applied to every chunk.
    Simple progress info will be printed.
    
    Keyword Arguments:
    filepath    -- Path to the fill that will be loaded with pandas.read_csv
    data_filter -- Filters the loaded dataframe.
                   Should take an original dataframe and return the filtered dataframe.
    chunksize   -- Chunksize passed to read_csv
    
    Returns: filtered dataframe
    """
    
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

newark, jfk, laguardia = 1, 132, 138
nyc_airports = (newark, jfk, laguardia)
    
def filter_trips_to_airports(df):
    """Filters trips to any of the three airports in New York
    
    Keyword Arguments:
    df -- the dataframe to be filtered
    
    Returns:
    the filtered dataframe
    """
    
    trips_to_airports_index = df.DOLocationID.isin(nyc_airports)
    return df[ trips_to_airports_index ]
    
def save_as_csv_gz(df, filepath):
    """Saves a dataframe as a gzipped csv file.
    
    Prints a simple message about the target filepath.
    
    Keyword Arguments:
    df       -- the dataframe to save
    filepath -- path with filename where the dataframe will be saved
    
    Returns: -
    """

    print('saving file:', filepath)
    df.to_csv(filepath, compression='gzip')

if __name__ == '__main__':
    main()