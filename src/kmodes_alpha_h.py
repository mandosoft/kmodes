#!/bin/env python3

import warnings
import random
from itertools import combinations
from sklearn.metrics.cluster import normalized_mutual_info_score as nmis
from src.gui import *

warnings.simplefilter(action='ignore', category=FutureWarning)
sys.stdout.write("\nLooking for strong pairwise associations...")

df = submit_and_run.df
cluster_list = [pd.DataFrame(df[i]) for i in df]
cluster_list_clean = cluster_list.copy()
each_2nd_col = df[df.columns[::2]]

"""Compare each second column to whole list. This finds pairwise associations quickly."""
for i in each_2nd_col:
    max_rii = 0
    rii = 0
    for location, cluster in enumerate(cluster_list):
        cluster_mode = cluster[cluster.columns[0]]
        if each_2nd_col[i].name != cluster_mode.name:
            rii = nmis(each_2nd_col[i], cluster_mode, average_method='arithmetic')
            if rii > max_rii:
                max_rii, best_cluster = rii, location
    # noinspection PyUnboundLocalVariable
    cluster_list[best_cluster] = pd.concat([cluster_list[best_cluster], each_2nd_col[i]], axis=1)


"""All list processing below prevents shared attributes between pairwise associations"""
pairwise = 2
pairwise_list = [cluster for cluster in cluster_list if len(cluster.columns) == pairwise]
pairwise_cluster_labels = [list(cluster.columns.values) for cluster in pairwise_list]
del_list = [x for each in pairwise_cluster_labels for x in each]

unique_list = list()
for each in pairwise_cluster_labels:
    if set(each).issubset(set(del_list)):
        del_list = list(filter((each[0]).__ne__, del_list))
        del_list = list(filter((each[1]).__ne__, del_list))
        unique_list.append(each)

unique_pairwise_clusters = list()
for cluster in pairwise_list:
    for i in unique_list:
        if (cluster.columns.values == i).all():
            unique_pairwise_clusters.append(cluster)

"""Get remaining data as single attributes"""
series_from_upc = [i for cluster in unique_pairwise_clusters for i in cluster]
series_clean_list = [j for cluster in cluster_list_clean for j in cluster]
final_set = [item for item in series_clean_list if item not in series_from_upc]

difference_set = list()
for i in cluster_list_clean:
    for j in final_set:
        if j == i.columns.values:
            difference_set.append(pd.DataFrame(i))

unique_pairwise_clusters.extend(difference_set)

"""Main vars for K Modes Iterations"""
cluster_list = unique_pairwise_clusters.copy()
k = len(cluster_list)
max_rii = 0
rii = 0
csv_dict = dict()


def calculate_sr_mode(c: pd.DataFrame) -> pd.DataFrame:

    if len(c.columns) >= 2:
        max_sum = 0
        cc = len(list(combinations(c.columns, 2)))
        for i in c:
            sum_rii = 0
            for j in c:
                if c[i].name != c[j].name:
                    sum_rii += nmis(c[i], c[j], average_method='arithmetic')
            if sum_rii > max_sum:
                max_sum = sum_rii
        sr_mode = max_sum / cc
        csv_dict[tuple([tuple(sorted(c)), 'k = ' + str(k)])] = round(sr_mode, 3)

    return c


def calculate_new_mode(c: pd.DataFrame) -> pd.DataFrame:

    max_sum = 0
    # TODO specify dtype explicitly
    cluster_mode = pd.Series()
    for location, i in enumerate(c):
        sum_rii = 0
        for j in c:
            if c[i].name != c[j].name:
                sum_rii += nmis(c[i], c[j], average_method='arithmetic')
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


"""--------------- K Modes Algorithm --------------------"""
cluster_list = [calculate_sr_mode(cluster) for cluster in cluster_list]

while k != 2:

    k -= 1
    sys.stdout.write("\n--> Running K modes at iteration #:" + str(k))

    """Begin by selecting a random mode from list"""
    enumerated_list = list(enumerate(cluster_list))
    random_df_il, random_df = random.choice(enumerated_list)
    new_mode = random_df[random_df.columns[0]]

    """Add random mode to best cluster"""
    rii = 0
    max_rii = 0
    for location, cluster in enumerated_list:
        cluster_mode = cluster[cluster.columns[0]]
        if location != random_df_il:
            rii = nmis(new_mode, cluster_mode, average_method='arithmetic')
            if rii > max_rii:
                max_rii, best_cluster = rii, location
    cluster_list[random_df_il] = cluster_list[random_df_il].drop(cluster_list[random_df_il].columns[0], axis=1)
    cluster_list[best_cluster] = pd.concat([cluster_list[best_cluster], new_mode], axis=1)

    """Calculate the new mode for the best cluster"""
    cluster_list[best_cluster] = calculate_new_mode(cluster_list[best_cluster])

    """Go back to the cluster the random mode came from and auction off remaining attributes"""
    if cluster_list[random_df_il].empty:
        del cluster_list[random_df_il]

    elif not cluster_list[random_df_il].empty:
        for i in cluster_list[random_df_il]:
            rii = 0
            max_rii = 0
            remaining_attr = cluster_list[random_df_il][i]
            for location, cluster in enumerated_list:
                cluster_mode = cluster[cluster.columns[0]]
                if location != random_df_il:
                    rii = nmis(remaining_attr, cluster_mode, average_method='arithmetic')
                    if rii > max_rii:
                        max_rii, best_cluster = rii, location
            cluster_list[best_cluster] = pd.concat([cluster_list[best_cluster], remaining_attr], axis=1)
        del cluster_list[random_df_il]

    else:
        sys.stderr.write('\nThere was a problem breaking up a cluster.')

    """Compute new mode and sr mode for each cluster in the cluster list"""
    cluster_list = [calculate_new_mode(cluster) for cluster in cluster_list]
    cluster_list = [calculate_sr_mode(cluster) for cluster in cluster_list]

sys.stdout.write('\nRun Complete!')
