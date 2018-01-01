import collections
import pandas
import math
import numpy
from pathlib import Path
pandas.set_option('display.width', 200)
# pandas.set_option('display.max_rows', 500)

steps_der_day = 96

pickle_path = str(Path(__file__).parent.parent) + \
    '/new_dataset/Pickles/combined_csvs.pickle'
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

print('Rounding data.')
full_df['Rainfall'] = full_df['Rainfall'].round(3)
full_df['Discharge'] = full_df['Discharge'].round(3)

print('Writing all gaussian estimation training data to file.')
# creating empty data structures to hold window.
num_stored_rain = 5
num_stored_lvl = 5
stored_rain = collections.deque(num_stored_rain * [math.nan], num_stored_rain)
stored_lvl = collections.deque(num_stored_lvl * [math.nan], num_stored_lvl)

output = {
    'num_stored_rain': num_stored_rain,
    'num_stored_lvl': num_stored_lvl,
    'y_vals': [],
    'x_rainfalls': [],
    'x_levels': [],
}

for index, row in full_df.iterrows():
    if index % 5000 ==0:
        print('Index {}'.format(index))
    output['y_vals'].append(row.Discharge)
    output['x_rainfalls'].append(list(stored_rain))
    output['x_levels'].append(list(stored_lvl))
    stored_rain.appendleft(row.Rainfall)
    stored_lvl.appendleft(row.Discharge)
    # if index > 4:
    #     break

# import pprint
# pprint.pprint(output)

print('Saving file')
outfile_name = '../new_dataset/nymboida_gaussian.mat'
import scipy.io as sio
sio.savemat(outfile_name, output)
print('Finished.')
