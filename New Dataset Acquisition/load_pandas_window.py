import pandas
from pathlib import Path

pickle_path = str(Path(__file__).parent.parent) + \
    '/New Dataset/Pickles/combined_csvs.pickle'
df = pandas.read_pickle(pickle_path, compression='bz2')
print('Finished loading')

def newcol(inp,arr):
    return inp+arr[0]
print('Creating new column.')
df = df.assign(Diff=lambda df:
    newcol(
        df.Discharge,
        [df.Discharge.shift(1), df.Discharge.shift(2)]
        )
    )

print(df.iloc[10:20])