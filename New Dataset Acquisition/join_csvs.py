import pandas as pd
from pathlib import Path
import os

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
            'Date', 'Level (Metres)', 'Discharge (ML/d)'], parse_dates=['Date'])
    except ValueError:  # Data does not have discharge volume
        df = pd.read_csv(csv_folder + filename, skiprows=skip, usecols=[
            'Date', 'Level (Metres)'], parse_dates=['Date'])
    return fix_names(df)

# Read all the csvs
print('Loading all dataframes.')
dataframes = list(map(process_csv, sorted(csv_list)))

print('Joining all loaded dataframes.')
df = pd.concat(dataframes)
del dataframes  # free memory

save_path = str(Path(__file__).parent.parent) + '/New Dataset/combined_csvs.pickle'
df.to_pickle(save_path)

# def newcol(inp,arr):
#     return inp+arr[0]
# print('Creating new column.')
# df = df.assign(Diff=lambda df:
#     newcol(
#         df.Level,
#         [df.Level.shift(1), df.Level.shift(2)]
#         )
#     )

# print('Sorting on date')
# print(df)
# df = df.sort_values('Date')
# print(df)

# first_valid_indices = df.apply(lambda series: series.first_valid_index())
# data_start_index = min(first_valid_indices.Level,first_valid_indices.Discharge)

# last_valid_indices = df.apply(lambda series: series.last_valid_index())
# data_end_index = max(last_valid_indices.Level,last_valid_indices.Discharge)

# # print(data_start_index)
# # print(df[data_start_index:])
# # print(data_end_index)
# print(df[:data_end_index])
# print(df[:data_end_index+10000])
