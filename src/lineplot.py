import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('output.csv', header=None)
df[0] = df[0].str.replace('[', '(')
df[0] = df[0].str.replace(']', ')')
df.columns = ['Cluster', 'Sr(Mode)']
# df.sort_values(by=['Sr(Mode)'], inplace=True, ascending=False)
print(df.head())
df.plot.scatter(x='Sr(Mode)', y='Cluster', c='DarkBlue')
plt.savefig('line_plot.pdf')
