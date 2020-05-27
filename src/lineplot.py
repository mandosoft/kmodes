import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('../outfiles/output.csv', header=None)
df[0] = df[0].str.replace('[', '(')
df[0] = df[0].str.replace(']', ')')
df.columns = ['Cluster', 'Sr(Mode)']
df.sort_values(by=['Sr(Mode)'], inplace=True, ascending=False)
print(df.head())
print(df.describe())
df.plot.barh(x='Cluster', y='Sr(Mode)', stacked=True, legend='True', use_index=False, grid=False)
plt.savefig('line_plot.pdf')

mean = df.mean()
df.plot.hist(bins=61, alpha=0.8, title='Sr Mode Values', density=True, figsize=(12,8), color='#86bf91', zorder=2, rwidth=0.9)
plt.xlabel('Sr(mode)')
plt.ylabel('Number of Clusters w/ Sr(Mode) Value')
plt.axvline(mean[0], color='w', linestyle='dashed', linewidth=2)
plt.savefig('hist.pdf')


plt.savefig('scatter.pdf')