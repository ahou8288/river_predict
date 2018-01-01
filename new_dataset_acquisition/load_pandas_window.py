import pandas
pandas.set_option('display.width', 200)
pandas.set_option('display.max_rows', 500)
from pathlib import Path
steps_der_day = 96


def create_history_column(col_name, num_timesteps, input_df, verbose=False):
    if verbose:
        print('Creating column history for {} with {} time steps.'.format(
            col_name, num_timesteps))
    new_col_name = 'Past_' + col_name.lower()
    temp_names_list = []
    # Create columns 1 by one
    for i in range(1, previous_levels + 1):
        if verbose and i % 20 == 0:
            print('Created {} columns.'.format(i))
        temp_col_name = 'prev' + str(i)
        # Store column names to use then remove them later.
        temp_names_list.append(temp_col_name)
        input_df = input_df.assign(
            **{temp_col_name: input_df[col_name].shift(i)})
        input_df[temp_col_name] = input_df[temp_col_name].round(3)
    # Aggregate columns into a list
    input_df[new_col_name] = input_df[temp_names_list].values.tolist()
    # Drop temporary columns
    input_df.drop(temp_names_list, inplace=True, axis=1)
    return input_df

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


print('Creating new columns with history.')
# Column will have a list with the previous river levels
previous_levels = 500
previous_rainfalls = 500
full_df = create_history_column('Rainfall', previous_rainfalls, full_df, True)
full_df = create_history_column('Discharge', previous_levels, full_df, True)
print('Columns created.')

print('Printing dataframe.')
print(full_df.iloc[1000:1500])
# print(full_df.describe())
