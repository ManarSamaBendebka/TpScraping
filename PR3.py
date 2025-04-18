import pandas as pd

df = pd.read_csv('jumia.zip', compression='zip')

print(df.head())
print(df.info())
print(df.describe(include='all'))