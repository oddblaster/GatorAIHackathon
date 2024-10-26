import pandas as pd
from pandas import read_csv

filename = 'data/Hospitals.csv'
names = ['id', 'name', 'city', 'state', 'lon', 'lat']
df = read_csv(filename, names=names)

for x in df.index:
    if df.loc[x, "state"] != "FL":
        df.drop(x, inplace = True)
        
pd.set_option('display.max_rows', 307)

print(df)