import pandas as pd

df_parquet = pd.read_parquet('test_output.parquet')

print(df_parquet.dtypes)
a = df_parquet.loc[0]['amount']
print(type(df_parquet.loc[0]['amount']))
print((df_parquet.loc[1]['amount']))