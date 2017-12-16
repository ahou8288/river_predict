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
while row_index < len(csv_data) - interpolation_limit - 1:
    for col_index in range(1, 3):
        # Check each of the next items for a missing value.
        # Stop if a non missing value is found.

        # Find out how many values are missing
        if not math.isnan(csv_data[row_index + 1][col_index]):
            print('No values are missing')
        elif not math.isnan(csv_data[row_index + 2][col_index]):
            print('1 missing')
            row_index+=1
        elif not math.isnan(csv_data[row_index + 3][col_index]):
            print('2 missing')
            row_index+=2
    row_index += 1
