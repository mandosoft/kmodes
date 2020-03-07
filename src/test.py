import pandas as pd
from sklearn.metrics.cluster import normalized_mutual_info_score as nmis
import timeit


def time():

    def calculate_new_mode(x):

        max_sum = 0
        cluster_mode = pd.Series()
        for location, i in enumerate(x):
            sum_rii = 0
            for j in x:
                if x[i].name != x[j].name:
                    sum_rii += nmis(x[i], x[j], average_method='arithmetic')
            if sum_rii > max_sum:
                max_sum, cluster_mode, ix = sum_rii, x[i], location

        # these are already pandas pattern
        if cluster_mode.empty:
            del cluster_mode
        else:
            x = x.drop(x.columns[ix], axis=1)
            x = pd.concat([x, cluster_mode], axis=1)
            cols = x.columns.tolist()
            cols = cols[-1:] + cols[:-1]
            x = x[cols]

        return x

    df = pd.read_csv('testsequence.csv', encoding='utf-8', header=None)
    calculate_new_mode(df)


def time2():

    def calculate_new_mode(x):

        max_sum = 0
        for location, i in x.iteritems():
            print(next(location))
            # name is type int, i is type series
            sum_rii = 0
            # sum_rii += nmis(i, next(i), average_method='arithmetic')

        return x

    df = pd.read_csv('testsequence.csv', encoding='utf-8', header=None)
    calculate_new_mode(df)

# print(timeit.timeit(time, number=100))
# print(timeit.timeit(time2, number=100))


# ---------- Get labelling schema from first row ----------------------

df = pd.read_csv('~/Desktop/kmodes/testfiles/TOPRIM pfam Yeast Top2.csv', encoding='utf-8', header=None)
df = df.rename(columns={df.columns[0]: 'SEQUENCE_ID'})
df = df.set_index('SEQUENCE_ID', drop=True)
df = df.rename(columns=lambda x: x - 1)
first_row_ix = df.index[0]
ix_label = first_row_ix.rsplit('/', 1)
ix_label = ix_label[1]
ix_label = ix_label.rsplit('-', 1)
df_label = int(ix_label[0])
column_lab_dict = dict()
stored = [df[i].iloc[0] for i in df]

for i in df:
    if df[i].iloc[0] != '-':
        column_lab_dict[df.columns[i]] = df_label
        df_label += 1
    else:
        column_lab_dict[df.columns[i]] = ''
df = df.rename(columns=column_lab_dict)

df.to_csv('testfile_out.csv', index=True, header=True)
