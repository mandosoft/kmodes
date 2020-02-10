import multiprocessing
from itertools import combinations
from tkinter import *
from tkinter import filedialog, simpledialog
import tk as tk
import cProfile, pstats, io
from multiprocessing import Pool
import numpy as np
from libconfig import *

# ------ GUI --------------------------
# Get variables file_path, label_number, and cut_off

window = Tk()
window.title('K Modes Alpha H')
window.geometry('560x650')

label1 = Label(window, text='Select a CSV file for upload:', anchor=CENTER, pady=30)
label2 = Label(window, text='Enter label number for\n first aligned attribute:', anchor=CENTER, pady=30)
label3 = Label(window, text='Set Sr(mode) cutoff value.\nRecommended value is .15:', anchor=CENTER, pady=30)

label1.grid(column=0, row=0)
label2.grid(column=0, row=3)
label3.grid(column=0, row=5)

label_number = IntVar()
label_number.set(1)
cut_off = DoubleVar()
cut_off.set(.15)
entry1 = Entry(width=30)
entry2 = Entry(width=3, textvariable=label_number)
entry3 = Entry(width=5, textvariable=cut_off)

entry1.grid(column=0, row=1, padx=15, pady=8)
entry2.grid(column=0, row=4)
entry3.grid(column=0, row=6)


def get_file_path():
    get_file_path.file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    entry1.delete(0, END)
    entry1.insert(0, get_file_path.file_path)


button1 = Button(text='Select File', fg='white', bg='purple', command=get_file_path)
button2 = Button(text='Submit and Run', fg='white', bg='purple', command=window.destroy)

button1.grid(column=0, row=2)
button2.grid(column=0, row=10, pady=30)

window.mainloop()

# -----------Pre-Processing--------------
# MSA Data Input
cut_off = cut_off.get()
file = open(get_file_path.file_path)
df = pd.read_csv(file, encoding='utf-8', header=None)
df = df.drop(df.columns[[0]], axis=1)
label_number = label_number.get() - 1
df = df.rename(columns=lambda x: x + label_number)

# Spinner. Helpful with large sequences
spinner = Halo(text='Running  ', spinner='simpleDots', color='green')
spinner.start()
start_time = time.perf_counter()

# Cluster Initialization
cluster_list = [pd.DataFrame(df[i]) for i in df]
cluster_list_clean = cluster_list.copy()
each_2nd_col = df[df.columns[::2]]

# Compare each second column to whole list. This finds pairwise associations quickly.
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

# not worth a list comp
r_list = []
for cluster in not_ranked_list:
    for i in unique_list:
        if (cluster.columns.values == i).all():
            r_list.append(cluster)

list1 = [i for cluster in r_list for i in cluster]

list2 = [j for cluster in cluster_list_clean for j in cluster]

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
csv_dict = multiprocessing.Manager().dict()


def sr_mode_calculator(x):
    max_sum = 0
    cc = len(list(combinations(x.columns, 2)))
    for i in x:
        sum_rii = 0
        for j in x:
            if x[i].name != x[j].name:
                sum_rii += nmis(x[i], x[j], average_method='arithmetic')
        if sum_rii > max_sum:
            max_sum = sum_rii
    sr_mode = max_sum / cc
    if sr_mode >= cut_off:
        csv_dict[tuple([tuple(sorted(x)), 'k = ' + str(k)])] = round(sr_mode, 3)


# Parallelize Sr(mode) computation
# pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
# pool.map_async(sr_mode_calculator, [i for i in cluster_list if len(i.columns) >= 2], chunksize=1)
# pool.close()

for cluster in cluster_list:
    if len(cluster.columns) >= 2:
        sr_mode_calculator(cluster)


# Main Loop
while k != 2:

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

    # Calculate new mode for best_cluster
    max_sum = 0
    cluster_mode = pd.Series()
    for location, i in enumerate(cluster_list[best_cluster]):
        sum_rii = 0
        for j in cluster_list[best_cluster]:
            if cluster_list[best_cluster][i].name != cluster_list[best_cluster][j].name:
                sum_rii += nmis(cluster_list[best_cluster][i], cluster_list[best_cluster][j], average_method='arithmetic')
        if sum_rii > max_sum:
            max_sum, cluster_mode, ix = sum_rii, cluster_list[best_cluster][i], location
    if cluster_mode.empty:
        print('Something went wrong')
    else:
        # Mode will always be leftmost column.
        # Drop designated mode, append to end of DataFrame, and reverse string ;)
        cluster_list[best_cluster] = cluster_list[best_cluster].drop(cluster_list[best_cluster].columns[ix], axis=1)
        cluster_list[best_cluster] = pd.concat([cluster_list[best_cluster], cluster_mode], axis=1)
        cols = cluster_list[best_cluster].columns.tolist()
        cols = cols[-1:] + cols[:-1]
        cluster_list[best_cluster] = cluster_list[best_cluster][cols]

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

    # Compute new mode for each cluster after breaking up and calculate Sr(Mode).
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

    for cluster in cluster_list:
        if len(cluster.columns) >= 2:
            sr_mode_calculator(cluster)

    # Parallelize Sr(mode) computation
    # pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    # pool.map_async(sr_mode_calculator, [i for i in cluster_list if len(i.columns) >= 2])
    # pool.close()

# pool.terminate()
spinner.stop()
print('Took', time.perf_counter() - start_time, 'seconds')