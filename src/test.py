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
print(timeit.timeit(time2, number=100))
