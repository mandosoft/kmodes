import pandas as pd
from sklearn.metrics.cluster import normalized_mutual_info_score as nmis
from itertools import combinations


def calculate_sr_mode(c: pd.DataFrame, csv_dict, k) -> pd.DataFrame:

    n_mis = nmis
    cc = len(list(combinations(c.columns, 2)))

    if len(c.columns) < 2:
        return c
    elif len(c.columns) == 2:
        max_sum = n_mis(c[c.columns[0]], c[c.columns[1]], average_method='geometric')
    else:
        max_sum = max([sum([n_mis(c[i], c[j], average_method='geometric')
                            for j in c if c[i].name != c[j].name]) for i in c])

    sr_mode = max_sum / cc
    csv_dict[tuple([tuple(sorted(c)), 'k = ' + str(k)])] = round(sr_mode, 3)

    return c


def calculate_new_mode(c: pd.DataFrame) -> pd.DataFrame:
    n_mis = nmis
    max_sum = 0
    cluster_mode = pd.Series(dtype=object)
    for location, i in enumerate(c):
        sum_rii = 0
        for j in c:
            if c[i].name != c[j].name:
                sum_rii += n_mis(c[i], c[j], average_method='geometric')
        if sum_rii > max_sum:
            max_sum, cluster_mode, ix = sum_rii, c[i], location

    if cluster_mode.empty:
        del cluster_mode
    else:
        c = c.drop(c.columns[ix], axis=1)
        c = pd.concat([c, cluster_mode], axis=1)
        cols = c.columns.tolist()
        cols = cols[-1:] + cols[:-1]
        c = c[cols]

    return c
