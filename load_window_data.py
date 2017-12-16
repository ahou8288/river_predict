# imports
import csv
import math

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

num_levels = 3
num_rainfalls = 5

output = []


def has_nan(arr, col):
    for i in arr:
        if math.isnan(i[col]):
            return True
    return False

for index in range(max(num_rainfalls, num_levels), len(csv_data) - 1):
    # Is there a current level
    is_valid = True
    if not math.isnan(csv_data[index][2]) and \
            not has_nan(csv_data[index - num_rainfalls:index], 1) and \
            not has_nan(csv_data[index - num_levels:index], 2):
        print(str(index) + ' is valid ' +
              str(csv_data[index - 5:index]) + ' cur ' + str(csv_data[index]))
    else:
        print(str(index) + ' is invalid ' +
              str(csv_data[index - 5:index]) + ' cur ' + str(csv_data[index]))
