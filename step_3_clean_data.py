import pandas as pd
import numpy as np
import time
import os

input_file = 'nyc-2017-yellow-taxi-trips-to-airport.cvs.gz'
output_file = 'nyc-2017-yellow-taxi-trips-to-airport.pkl.gz'

def main():
    """Loads the data for taxi trips to airports from step 2, cleans it and saves the result.
    
    If output_file already exists, the function skips.
    Remove the output_file manually in that case.
    
    The input_file is loaded in chunks of 100,000 lines.
    While loading simple progress info will be displayed.
    
    After the whole file is loaded the function clean_data is applied.
    That includes a transformation to efficient datatypes.
    
    At the end the cleaned dataset is saved as a gzipped pickle file,
    so that the datatypes are not lost.
    
    Remember: pickle files should only be used for temporary storage, since
    the format is not guaranteed to be stable between different lib versions.                   
    
    Keyword Arguments: -
    
    Returns: -
    """
    
    print('=== nyc taxi to airport - step 3 clean data')

    if os.path.exists(output_file):
        print("output file exists:", output_file)
        print("skipping")
        return

    df = load_data(input_file)
    df = clean_data(df)
    save_as_pickle_gz(df, output_file)
    
    print('done')


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


def load_data(input_file):
    """Loads the dataframe from input_file.

    The file will be loaded with pandas.read_csv with a chunksize of 100_000.
    Simple progress info will be displayed during loading.

    To speed up, the following transformations are done while loading:
       - only the columns in cols_to_use are loaded
       - data types are mapped as specified in dict data_types
       - the columns specified in dates_to_parse will be parsed

    Keyword Arguments:
    input_file -- the filepath of the input file to read
    
    Returns: the loaded dataframe
    """
    print('loading file:', input_file)
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

def make_show_progress():
    """Creates a helper function that generates progress info.
    
    Keyword Arguments: -
    
    Returns: a function that prints a progress line.
    
             Keyword Arguments:
             chunk_length -- the length of the last chunk read
             
             that
             
             Returns: -
    
    """
    
    start_time = time.time()
    lines_read = 0

    def show_progress(chunk_length):
        """Displays a progress line. Created by make_show_progress."""
        
        nonlocal lines_read

        lines_read += chunk_length
        elapsed_time = int(time.time() - start_time)
        print('{:,} lines read | time {:,}s'.format(lines_read, elapsed_time))

    return show_progress

def clean_data(df):
    """Cleans the passed dataframe.
    
    Actions done while cleaning:
    - dropping all rows with missing location ids
    - dropping all rows where dropoff time is before pickup time
    - consider all location ids that map to the same zone as equivalent and replace them with a single value
    
    Keyword Arguments:
    df -- the dataframe to clean
    
    Returns: the cleaned dataframe
    """
    
    any_location_id_missing = (df.PULocationID > 263) | (df.DOLocationID > 263)
    df = df.drop(df.index[any_location_id_missing])
    
    df = df[df.tpep_dropoff_datetime > df.tpep_pickup_datetime]

    df.PULocationID.replace([104, 105], 103)
    
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
