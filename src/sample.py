import pandas as pd
example_data = {'a':[1,2],'b':[2,3],'c':[4,5]}
df = pd.DataFrame(example_data)
example_list = [[],[],[]]

for i in range(len(list(df))):
    example_list[i].append(list(df)[i])
print(example_list)
