import pandas
import numpy as np
import os
from tqdm import tqdm
steps_der_day = 96


def create_history_column(col_name, num_timesteps, input_df):
    # print('Creating column history for {} with {} time steps.'.format(
    #     col_name, num_timesteps))
    input_df = input_df.assign(**{col_name.lower() + '_' + str(i): input_df[
                               col_name].shift(i) for i in range(1, previous_levels + 1)})
    return input_df

pickle_path = '../new_dataset/Pickles/combined_csvs.pickle'
df = pandas.read_pickle(pickle_path, compression='bz2')
print('Finished loading')


print('Loading and creating rainfall data column.')
dateparse = lambda x: pandas.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
rain_df = pandas.read_csv(
    '../old_dataset/nymboida_rain.csv', parse_dates=[0], date_parser=dateparse)
print('Rainfall data loaded from csv.')


print('Merging rainfall and level data into one dataframe.')
full_df = pandas.merge(df, rain_df, how='left')


print('Interpolating missing rainfall data')
# assume rain fell at a constant rate over the whole time period
# only fill in gaps of up to one day
full_df['Rainfall'].fillna(
    method='bfill', inplace=True, limit=steps_der_day - 1)
# Adjust for 15 minute time period
full_df['Rainfall'] /= steps_der_day
full_df = full_df.round(3)

print('Creating new columns with history.')
# Column will have a list with the previous river levels
previous_levels = 100
previous_rainfalls = previous_levels

num_chunks = 40

csv_filename = '../new_dataset/nymboida_gaussian_week.csv'

# to make life easier
try:
    os.remove(csv_filename)
except OSError:
    pass

chunk_counter = 0
for small_df in tqdm(np.array_split(full_df, num_chunks), unit='chunks'):

    small_df = create_history_column(
        'Rainfall', previous_rainfalls, small_df)
    small_df = create_history_column(
        'Level', previous_levels, small_df)

    del small_df['Date']
    del small_df['Discharge']

    small_df.dropna(inplace=True)

    small_df.to_csv(csv_filename,
                    header=chunk_counter == 0, mode='a', index=False)
    chunk_counter += 1
