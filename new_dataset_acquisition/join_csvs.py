import pandas as pd
from pathlib import Path
import os
import math
from multiprocessing import Pool

print('Finding files to load.')
csv_folder = str(Path(__file__).parent.parent) + '/New Dataset/CSVs/'
csv_list = os.listdir(csv_folder)


def fix_names(df):
    if 'Level (Metres)' in df.columns:
        df = df.rename(columns={'Level (Metres)': 'Level'})
    if 'Discharge (ML/d)' in df.columns:
        df = df.rename(columns={'Discharge (ML/d)': 'Discharge'})
    return df


def process_csv(filename):
    print('Loading: ' + filename)
    skip = [0, 1, 3]  # skip invalid header rows
    # Try to load in csv file using pandas
    try:
        df = pd.read_csv(csv_folder + filename, skiprows=skip, usecols=[
            'Date', 'Level (Metres)', 'Discharge (ML/d)'])
    except ValueError:  # Data does not have discharge volume
        df = pd.read_csv(csv_folder + filename, skiprows=skip, usecols=[
            'Date', 'Level (Metres)'])
    return fix_names(df)

# Read all the csvs
print('Loading all dataframes.')
dataframes = Pool(4).map(process_csv, sorted(csv_list))

print('Joining all loaded dataframes.')
df = pd.concat(dataframes)

print('Converting to date type.')
df['Date'] = pd.to_datetime(df.Date, format='%H:%M:%S %d/%m/%Y')

print('Sorting based on date.')

print('Writing to file')
pickle_path = str(Path(__file__).parent.parent) + \
    '/New Dataset/Pickles/combined_csvs.pickle'
df.to_pickle(pickle_path, compression='bz2')
