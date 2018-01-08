import pandas
import os
import math

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
full_df = pandas.merge(rain_df, df, how='inner')
full_df = full_df.dropna()
full_df = full_df.sort_values('Date')
full_df = full_df.round(4)
del full_df['Discharge']

full_df = full_df.assign(
    **{'diff': full_df['Date'] - full_df['Date'].shift(1)})

longest_section = 0
longest_section_end = 0
current_section = 0

for ind, entry in full_df.iterrows():
    if entry['diff'] == pandas.Timedelta('1 days'):
        current_section += 1
    else:
        if current_section > longest_section:
            longest_section = current_section
            longest_section_end = ind
        current_section = 0

print('Longest section is {} long. Finishes at {}'.format(
    longest_section, longest_section_end))

cont = full_df.iloc[longest_section_end-longest_section:longest_section_end]

print(cont[cont['diff'] != pandas.Timedelta('1 days')])

# print(full_df)

# full_df.to_csv('../new_dataset/daily_nymbo.csv',header=False,index=False)
