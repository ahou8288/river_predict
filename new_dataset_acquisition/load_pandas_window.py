import pandas
import numpy as np
import os
from multiprocessing import Pool
from tqdm import tqdm
steps_der_day = 96

# The levels are stored in a pickle file
print('Loading level data from pickle.')
pickle_path = '../new_dataset/Pickles/combined_csvs.pickle'
df = pandas.read_pickle(pickle_path, compression='bz2')

# The rainfall data is stored in a csv file.
# Using a dateparse speeds up processing dates into a date format when
# using the read_csv function
print('Loading rainfall data from csv.')
dateparse = lambda x: pandas.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
rain_df = pandas.read_csv(
    '../old_dataset/nymboida_rain.csv', parse_dates=[0], date_parser=dateparse)

print('Merging rainfall and level data into one dataframe.')
full_df = pandas.merge(df, rain_df, how='left')

print('Interpolating missing rainfall data. (Limit 1 day gap)')
# assume rain fell at a constant rate over the whole time period
# only fill in gaps of up to one day
full_df['Rainfall'].fillna(
    method='bfill', inplace=True, limit=steps_der_day - 1)
# Adjust for 15 minute time period
print('Adjusting rainfall scale for 15 minute time period.')
full_df['Rainfall'] /= steps_der_day
# Round all values to 3 decimal places for easy display and remove all
# unused columns
print('Rounding values and removing unused columns')
del full_df['Date']
del full_df['Discharge']
full_df = full_df.round(3)

# Specify parameters for history window size.
# previous_levels says how many previous level measurements should be
# stored in the output
previous_levels = 96
previous_rainfalls = previous_levels
# Chunks are used to allow the calculations to fit into memory.
num_chunks = 100

# This is the output file
csv_filename = '../new_dataset/nymboida_gaussian_{}steps.csv'.format(
    previous_levels)
# write header row manually
print('Writing header to output csv file.')
with open(csv_filename, 'w') as f:
    col_list = ['Rainfall', 'Level', ] + \
        ['rainfall' + str(i) for i in range(1, previous_rainfalls + 1)] + \
        ['level' + str(i) for i in range(1, previous_levels + 1)]
    f.write(','.join(col_list)+'\n')


def create_history_column(col_name, num_timesteps, input_df):
    # Creates new columns with previous data from the column col_name.
    # the number of columns/ timesteps created is num_timesteps
    # input_df is returned after it is modified.
    input_df = input_df.assign(**{col_name.lower() + '_' + str(i): input_df[
                               col_name].shift(i) for i in range(1, previous_levels + 1)})
    return input_df


def write_chunk_to_csv(small_df):
    # Adds columns with the window data to a row
    small_df = create_history_column(
        'Rainfall', previous_rainfalls, small_df)
    small_df = create_history_column(
        'Level', previous_levels, small_df)
    # if data is missing from the window then discard the whole row.
    small_df.dropna(inplace=True)
    small_df.to_csv(csv_filename, header=False, mode='a', index=False)

# Split the data into chunks
print('Spliting dataframe into chunks.')
chunks = np.array_split(full_df, num_chunks)

print('Creating window and writing chunks to file.')
# Use a thead pool to work on multiple threads at once.
with Pool(4) as p:
    # Use tqdm to get a fancy progress bar
    # Pass every chunk to the write_chunk_to_csv function.
    # p.imap_unordered is a multithreaded map which sends the function chunks
    for _ in tqdm(p.imap_unordered(write_chunk_to_csv, chunks), total=num_chunks, unit='chunk'):
        pass
print('Finished.')
