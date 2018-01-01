import pandas
pandas.set_option('display.width', 200)
from pathlib import Path


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
full_df['Rainfall'].interpolate(limit=95, inplace=True)
# only interpolate up to one day in advance


print('Creating new column.')
# Column will have a list with the previous river levels
previous_levels = 3
col_names = []
# Create columns 1 by one
for i in range(1, previous_levels + 1):
    col_name = 'previous' + str(i)
    # Store column names to use then remove them later.
    col_names.append(col_name)
    full_df = full_df.assign(**{col_name: full_df.Discharge.shift(i)})
# Aggregate columns into a list
full_df['past_levels'] = full_df[col_names].values.tolist()
# Drop temporary columns
full_df.drop(col_names, inplace=True, axis=1)
print('Columns created.')


print('Printing dataframe.')
print(full_df.iloc[1340:1400])
# print(full_df.describe())
