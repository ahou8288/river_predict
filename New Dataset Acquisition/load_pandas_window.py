import pandas

pickle_path = str(Path(__file__).parent.parent) + '/New Dataset/Pickles/combined_csvs.pickle'
df = pandas.read_pickle(pickle_path)

# def newcol(inp,arr):
#     return inp+arr[0]
# print('Creating new column.')
# df = df.assign(Diff=lambda df:
#     newcol(
#         df.Level,
#         [df.Level.shift(1), df.Level.shift(2)]
#         )
#     )

# print('Sorting on date')
# print(df)
# df = df.sort_values('Date')
# print(df)

# first_valid_indices = df.apply(lambda series: series.first_valid_index())
# data_start_index = min(first_valid_indices.Level,first_valid_indices.Discharge)

# last_valid_indices = df.apply(lambda series: series.last_valid_index())
# data_end_index = max(last_valid_indices.Level,last_valid_indices.Discharge)

# # print(data_start_index)
# # print(df[data_start_index:])
# # print(data_end_index)
# print(df[:data_end_index])
# print(df[:data_end_index+10000])
