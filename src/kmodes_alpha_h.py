from itertools import combinations
from tkinter import filedialog

import tk as tk
import numpy as np
from libconfig import *

# Prompts "Choose File" window to select a file to read as input
tk.Tk().withdraw()
file_path = filedialog.askopenfilename()
file = open(file_path)

# Spinner. Helpful with large sequences
spinner = Halo(text='Running  ', spinner='simpleDots', color='green')
spinner.start()
start_time = time.perf_counter()

# MSA Data Input
df = pd.read_csv(file, encoding='utf-8', header=None)
df = df.drop(df.columns[[0]], axis=1)
df = df.rename(columns=lambda x: x + 5)

# File write out
outf = open('outfile.txt', 'w')

# Initialization
cluster_list = [pd.DataFrame(df[i]) for i in df]
cluster_list_clean = cluster_list.copy()
each_2nd_col = df[df.columns[::2]]

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

# Pre-processing for input into k-modes algorithm
not_ranked_list = [cluster for cluster in cluster_list if len(cluster.columns) == 2]
temp_list = [list(cluster.columns.values) for cluster in not_ranked_list]
seen = set()
unique_list = [x for x in temp_list if frozenset(x) not in seen and not seen.add(frozenset(x))]

r_list = []
for cluster in not_ranked_list:
    for i in unique_list:
        if (cluster.columns.values == i).all():
            r_list.append(cluster)

list1 = []
for cluster in r_list:
    for i in cluster:
        list1.append(i)
list2 = []
for cluster in cluster_list_clean:
    for j in cluster:
        list2.append(j)

final_set = [item for item in list2 if item not in list1]

diff_df_set = []
for i in cluster_list_clean:
    for j in final_set:
        if j == i.columns.values:
            diff_df_set.append(pd.DataFrame(i))
r_list.extend(diff_df_set)
cluster_list = r_list.copy()

# Main globals. Use wisely.
k = len(cluster_list)
max_rii = 0
rii = 0
csv_dict = dict()

# Main loop
while k > 2:

    k -= 1

    # Newly enumerate the list and select a random mode
    enumerated_list = list(enumerate(cluster_list))
    random_df_il, random_df = random.choice(enumerated_list)
    new_mode = random_df[random_df.columns[0]]

    # Add chosen mode to best cluster
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

    # Handles the cluster where mode has been removed
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
        print('\nThere was a problem breaking up a cluster.\n')

    # Compute new mode for each cluster.
    for cluster in cluster_list:
        max_sum = 0
        cluster_mode = pd.Series()
        for location, i in enumerate(cluster):
            sum_rii = 0
            for j in cluster:
                if cluster[i].name != cluster[j].name:
                    sum_rii += nmis(cluster[i], cluster[j], average_method='arithmetic')
            if sum_rii > max_sum:
                max_sum, cluster_mode, ix = sum_rii, cluster[i], location
        if cluster_mode.empty:
            del cluster_mode
        else:
            # Mode will always be leftmost column.
            # Drop designated mode, append to end of DataFrame, and reverse string.
            cluster = cluster.drop(cluster.columns[ix], axis=1)
            cluster = pd.concat([cluster, cluster_mode], axis=1)
            cols = cluster.columns.tolist()
            cols = cols[-1:] + cols[:-1]
            cluster = cluster[cols]

    # SR(Mode) Calculation
    for cluster in cluster_list:
        if len(cluster.columns) == 1:
            break
        else:
            max_sum = 0
            cc = len(list(combinations(cluster.columns, 2)))
            for i in cluster:
                sum_rii = 0
                for j in cluster:
                    if cluster[i].name != cluster[j].name:
                        sum_rii += nmis(cluster[i], cluster[j], average_method='arithmetic')
                if sum_rii > max_sum:
                    max_sum = sum_rii
            sr_mode = max_sum / cc
            csv_dict[tuple(cluster)] = sr_mode
'''
    # Text File Writer
    outf.writelines('\nClusters at Iteration K = ' + str(k) + '\n')
    sorted_list = []
    cluster_list_cpy = cluster_list
    for cluster in cluster_list_cpy:
        cluster = cluster.reindex(sorted(cluster.columns), axis=1)
        sorted_list.append(cluster)
    sorted_list = sorted(sorted_list, key=lambda x: x.columns[0])
    for cluster in sorted_list:
        if len(cluster.columns) > 1:
            outf.writelines(str(cluster.columns.values).replace('[', '(').replace(']', ')'))
    outf.writelines('\n' * 2)
'''
# CSV Writer Output
w = csv.writer(open("output.csv", "w"))
for key, val in csv_dict.items():
    w.writerow([sorted(key), round(val, 3)])

outf.close()
spinner.stop()
print('Took', time.perf_counter() - start_time, 'seconds')
