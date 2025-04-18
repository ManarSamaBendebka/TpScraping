import pandas as pd

chunksize = 1000
filename = 'jumia_data_tp.csv'

for chunk in pd.read_csv(filename, chunksize=chunksize):

    print(len(chunk))
