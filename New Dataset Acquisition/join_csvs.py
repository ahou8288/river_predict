import pandas as pd
from pathlib import Path
import os

print('Finding files to load.')
csv_folder = str(Path(__file__).parent.parent) + '/New Dataset/CSVs/'
csv_list = os.listdir(csv_folder)

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

    return df

# Read all the csvs
print('Loading all dataframes.')
dataframes = list(map(process_csv, sorted(csv_list)))

print('Joining all loaded dataframes.')
df = pd.concat(dataframes)
del dataframes # free memory

# Remove missing data
print('Removing missing values.')
df.dropna(how='all')

print(df.describe())
