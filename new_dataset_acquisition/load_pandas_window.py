import collections
import pandas
import math
import csv
from pathlib import Path
from tqdm import tqdm

steps_der_day = 96

print('Loading dataframes.')
pickle_path = str(Path(__file__).parent.parent) + \
    '/new_dataset/Pickles/combined_csvs.pickle'
df = pandas.read_pickle(pickle_path, compression='bz2')

dateparse = lambda x: pandas.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
rain_df = pandas.read_csv(
    '../old_dataset/nymboida_rain.csv', parse_dates=[0], date_parser=dateparse)

print('Merging rainfall and level data into one dataframe.')
full_df = pandas.merge(df, rain_df, how='left')

print('Interpolating missing rainfall data')
# assume rain fell at a constant rate over the whole time period
# only fill in gaps of up to one day
full_df['Rainfall'].fillna(
    method='bfill', inplace=True, limit=steps_der_day - 1)
# Adjust for 15 minute time period
full_df['Rainfall'] /= steps_der_day

print('Rounding data.')
full_df['Rainfall'] = full_df['Rainfall'].round(3)
full_df['Discharge'] = full_df['Discharge'].round(3)

print('Writing all gaussian estimation training data to file.')
# creating empty data structures to hold window.
num_stored_rain = 100
num_stored_lvl = 100
stored_rain = collections.deque(num_stored_rain * [math.nan], num_stored_rain)
stored_lvl = collections.deque(num_stored_lvl * [math.nan], num_stored_lvl)

outfile_name = '../new_dataset/nymboida_gaussian.csv'
with open(outfile_name, 'w') as f:
    # Write a header explaining the file format
    writer = csv.writer(f, delimiter=',')
    for index, row in tqdm(full_df.iterrows(),total = len(full_df), ncols = 140, unit='rows'):
        temp_row_data = [row.Discharge] + list(stored_rain) + list(stored_lvl)
        has_nan=False
        for i in temp_row_data:
            try:
                if math.isnan(i):
                    has_nan=True
                    break
            except:
                has_nan=True
                print(str(index)+' had an error.')
        if not has_nan:
            writer.writerow(temp_row_data)
        stored_rain.appendleft(row.Rainfall)
        stored_lvl.appendleft(row.Discharge)
