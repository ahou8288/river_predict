from pathlib import Path
csv_folder = str(Path(__file__).parent.parent) + '/New Dataset/CSVs/'
import os
csv_list = os.listdir(csv_folder)

first = csv_folder + csv_list[0]


def process_csv(filename):
    import pandas
    # Load filename as string/ lines
    skip = [0, 1, 3]
    try:
        df = pandas.read_csv(filename, skiprows=skip, usecols=[
                             'Date', 'Level (Metres)', 'Discharge (ML/d)'])
    except ValueError:  # Data does not have discharge volume
        df = pandas.read_csv(filename, skiprows=skip, usecols=[
                             'Date', 'Level (Metres)'])

    print(df.head(5))
    print()

    print(df.describe())

process_csv(first)
