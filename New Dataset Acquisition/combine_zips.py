import os
river_num = 204001
all_files = [i for i in os.listdir() if '.zip' in i and str(river_num) in i]
print(all_files)
