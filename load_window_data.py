# imports
import csv
import math

# Load all rivers
# Do an interpolation pass
# Choose a window
# Find as much data that fits the window as possible
# Save in .mat format

# Loading rivers from csv
nymbo_file = open('nymbo.csv', 'r')
try:
    reader = csv.reader(nymbo_file)
    csv_data = [i for i in reader]
finally:
    nymbo_file.close()

# Converting data to correct format
for index, entry in enumerate(csv_data):
    csv_data[index][1] = float(entry[1])
    csv_data[index][2] = float(entry[2])
# print(csv_data)

# Interpolate missing data
interpolation_limit = 2
row_index = 0
should_interpolate = [False] * len(csv_data)
print(should_interpolate)
for col_index in range(1, 3):
    for row_index in range(1, len(csv_data)):
        for i in range(i, interpolation_limit + 1):
            if not math.isnan(csv_data[row_index][col_index]) and
            not math.isnan(csv_data[row_index + i][col_index])
                should_interpolate[row_index] = True
