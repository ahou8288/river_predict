from pathlib import Path
parent = str(Path(__file__).parent.parent) + '/'
zip_folder = parent + 'New Dataset/ZIPs/'
csv_folder = parent + 'New Dataset/CSVs/'

import zipfile
import os

# Loop over each zip file
for i in os.listdir(zip_folder):
    # Open the zip file
    with zipfile.ZipFile(zip_folder + i, "r") as zip_ref:
        # Find the file inside the zip. (if it exists)
        if len(zip_ref.namelist())>0:
            zipped_csv_filename = zip_ref.namelist()[0]

            # Name the new csv the same as the zip but with the .csv extension.
            csv_name = i[:len(i) - 4] + '.csv'
            csv_name = csv_folder + csv_name

            # Extract the file to the csv folder (with it's original name)
            zip_ref.extract(zipped_csv_filename, csv_folder)
            # Change file to have new csv name.
            # eg. 204001.csv -> river_204001_1980_1985.csv
            os.rename(csv_folder+zipped_csv_filename,csv_name)
