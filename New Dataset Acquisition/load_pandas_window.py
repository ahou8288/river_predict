import pandas
from pathlib import Path

pickle_path = str(Path(__file__).parent.parent) + \
    '/New Dataset/Pickles/combined_csvs.pickle'
df = pandas.read_pickle(pickle_path, compression='bz2')
print('Finished loading')

print('Creating new column.')
# Column will have a list with the previous river levels
previous_levels = 3
col_names = []
# Create columns 1 by one
for i in range(1, previous_levels + 1):
    col_name = 'previous' + str(i)
    col_names.append(col_name) # Store column names to use then remove them later.
    df = df.assign(**{col_name: df.Discharge.shift(i)})
# Aggregate columns into a list
df['past_levels'] = df[col_names].values.tolist()
# Drop temporary columns
df.drop(col_names, inplace=True, axis=1)

print('Columns created.')
print(df.iloc[10:20])

df.set_index('Date', inplace=True)
