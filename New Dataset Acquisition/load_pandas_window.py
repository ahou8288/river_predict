import pandas
from pathlib import Path

pickle_path = str(Path(__file__).parent.parent) + \
    '/New Dataset/Pickles/combined_csvs.pickle'
df = pandas.read_pickle(pickle_path, compression='bz2')

print(df.index.is_monotonic)
print(df.dtypes)
print(df)

# # Remove NANs at the front and back
# nan_rows = df[df.isnull().T.any().T]
# print(nan_rows)
# print(len(df.values.tolist()))
# print('All done.')



# def newcol(inp,arr):
#     return inp+arr[0]
# print('Creating new column.')
# df = df.assign(Diff=lambda df:
#     newcol(
#         df.Level,
#         [df.Level.shift(1), df.Level.shift(2)]
#         )
#     )
