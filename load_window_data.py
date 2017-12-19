# This function loads data from a csv and converts it to small sections of
# data which don't have missing values.

# Imports
import csv
import math
import numpy as np
import scipy.io as sio
import pprint

# Process
# Load all rivers
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

# Choose a window
num_levels = 100
num_rainfalls = num_levels
output = {
    'window_num_levels': num_levels,
    'window_num_rainfalls': num_rainfalls,
    'y_vals': [],
    'x_rainfalls': [],
    'x_levels': [],
    'readme': 'y_vals contains the next days level.\nx_rainfalls contains 5 rainfall values for the past 5 days (with the most recent rainfall as the first element of the list).\nx_levels contains 3 level values for the past 3 days (with the most recent level as the first element of the list).'
}

# Utility function for finding if an array of numbers has a nan value in a
# specific column


def has_nan(arr, col):
    for i in arr:
        if math.isnan(i[col]):
            return True
    return False

for index in range(max(num_rainfalls, num_levels), len(csv_data) - 1):
    is_valid = True
    # Check for current level, past rainfalls and past levels
    if not math.isnan(csv_data[index][2]) and \
            not has_nan(csv_data[index - num_rainfalls:index], 1) and \
            not has_nan(csv_data[index - num_levels:index], 2):
        # Build an array to send/save
        output['y_vals'].append(csv_data[index][2])

        rainfalls = [i[1] for i in csv_data[index - num_rainfalls:index]]
        output['x_rainfalls'].append(list(reversed(rainfalls)))

        levels = [i[2] for i in csv_data[index - num_levels:index]]
        output['x_levels'].append(list(reversed(levels)))

# pprint.pprint(output)
print(len(output['y_vals']))
# sio.savemat('nymbo_window_data.mat', output)
