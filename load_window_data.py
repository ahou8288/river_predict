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
for i in csv_data:
    print(i)

num_levels = 3
num_rainfall = 5

output = []

for index in range(max(num_rainfall,num_levels),len(csv_data)-1):
    # Is there a current level
    if math.isnan(csv_data[index+1][2]):
        is_valid=True
        # Is there past rainfall data
        for i in range(num_rainfall):
            if math.isnan(csv_data[index-i][1]):
                is_valid=False
                break
        # Is there past level data
        for i in range(num_levels):
            if math.isnan(csv_data[index-i][2]):
                is_valid=False
                break
        if is_valid:
            print(str(index)+' is valid')
        else:
            print(str(index)+' is invalid')
    # break
