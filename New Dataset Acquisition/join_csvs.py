from pathlib import Path
csv_folder = str(Path(__file__).parent.parent) + '/New Dataset/CSVs/'
import os
csv_list = os.listdir(csv_folder)

first = csv_folder + csv_list[0]


def process_csv(filename):
    import pandas
    # Load filename as string/ lines
    df = pandas.read_csv(filename, header=2)

    print(df.head(10))

process_csv(first)
