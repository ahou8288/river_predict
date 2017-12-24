from zipfile import ZipFile
import os
import csv

river_num = 204001
all_files = [i for i in os.listdir() if '.zip' in i and str(river_num) in i]

for zip_filename in all_files:
    zipped_file = ZipFile(zip_filename,'r')
    csv_filename = str(river_num) + '.csv'
    csv_text = zipped_file.read(csv_filename).decode().splitlines()

    array_data = []

    for i in csv_text[4:]:
        items = [item.strip() for item in i.split(',')[:5]]
        array_data.append(items)
    print(array_data[:4])
