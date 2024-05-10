import pandas as pd

file_path = '/home/agung_msbu/personal/digitalSkola/spark/pyspark-intro/data/parquet/productAmount_00001.parquet'

df = pd.read_parquet(file_path)

print(df.head())
print(df.count())
