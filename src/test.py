import pandas as pd

df_list = [pd.DataFrame({"a": [1,2,3], "b": [4,5,6], "c": [7,8,9]}) for _ in range(3)]

df_to_compare = df_list[1]

locations = [i for i, df in enumerate(df_list) if df_to_compare.equals(df)]

print(locations)
