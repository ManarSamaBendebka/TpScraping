import dask.dataframe as dd

df = dd.read_csv('jumia_data_tp.csv')
print(df.head())
print(df.describe().compute())











