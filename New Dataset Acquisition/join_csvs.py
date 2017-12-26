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
            'Date', 'Level (Metres)', 'Discharge (ML/d)'])  # , parse_dates=['Date'])
    except ValueError:  # Data does not have discharge volume
        df = pd.read_csv(csv_folder + filename, skiprows=skip, usecols=[
            'Date', 'Level (Metres)'])  # , parse_dates=['Date'])
    return fix_names(df)

# Read all the csvs
print('Loading all dataframes.')
dataframes = Pool(4).map(process_csv, sorted(csv_list))

# for i in dataframes:
#     print(i.describe())

print('Joining all loaded dataframes.')
df = pd.concat(dataframes)

counter = 0
for i in range(0,len(df)):
    entry = df.iloc[i]
    if entry.Level and entry.Discharge:
        print(entry.Level)
        print(entry.Discharge)
        counter+=1
    print('{} Valid {}'.format(entry.Date,not math.isnan(entry.Level) and not math.isnan(entry.Discharge)))
    break
print('counter {}'.format(counter))

# df2 = df.drop('Date', axis=1)
# print(df2.first_valid_index())
# print(df2.last_valid_index())
# print(len(df2))

# print(df2[1000000:1000500])

# print(df)
# print(df.describe())

# print('Writing to file')
# pickle_path = str(Path(__file__).parent.parent) + \
#     '/New Dataset/Pickles/combined_csvs.pickle'
# df.to_pickle(pickle_path, compression='bz2')
print('All done.')
