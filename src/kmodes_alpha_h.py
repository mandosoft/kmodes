from itertools import combinations

from libconfig import *

# Prompts "Choose File" window to select a file to read as input
tk.Tk().withdraw()
file_path = filedialog.askopenfilename()
file = open(file_path)

# Spinner. Helpful with large sequences
spinner = Halo(text='Running  ', spinner='simpleDots', color='green')
spinner.start()

start_time = time.perf_counter()
 
# Data input stream use file in arg
df = pd.read_csv(file, encoding='utf-8', header=None)
df = df.drop(df.columns[[0]], axis=1)
df = df.rename(columns=lambda x: x+5)

# File write out
outf = open('outfile.txt', 'w')

# Optional:
# outf.writelines('\nMultiple Sequence Alignment\n' + df.to_string(index=False) + '\n'*2)

n = len(df.columns)
k = n

# Initialization
cluster_list = [pd.DataFrame(df[i]) for i in df]
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

not_ranked_list = [cluster for cluster in cluster_list if len(cluster.columns) == 2]
ranked_dict = {}

outf.writelines('Not Ranked List: \n')
for cluster in not_ranked_list:
    outf.writelines(str(cluster.columns.values).replace('[', '(').replace(']', ')'))
outf.writelines('\n' * 2)

# SR(Mode) Calculation
for cluster in not_ranked_list:
    max_sum = 0
    cc = len(list(combinations(cluster.columns, 2)))
    for i in cluster:
        sum_rii = 0
        for j in cluster:
            if cluster[i].name != cluster[j].name:
                sum_rii += nmis(cluster[i], cluster[j], average_method='arithmetic')
        if sum_rii > max_sum:
            max_sum = sum_rii
    sr_mode = max_sum/cc
    ranked_dict[sr_mode] = cluster.columns.values

dict_list = list(ranked_dict.items())
dict_list.sort(reverse=True)
new_dict = dict(dict_list)
f = open("sr_mode_dict.txt", "w")
f.write(str(dict_list))
f.close()

'''
cluster_list = [pd.DataFrame(k_random_samples[i]) for i in k_random_samples]
remaining_attr = df[df.columns.difference(k_random_samples.columns, False)]
max_rii = 0 
rii = 0

# Initial pairwise clustering on random values
for location, cluster in enumerate(cluster_list):
    cluster_mode = cluster[cluster.columns[0]] 
    rii = nmis(remaining_attr[remaining_attr.columns[0]], cluster_mode, average_method='arithmetic')
    if rii > max_rii:
        max_rii, best_cluster = rii, location       
cluster_list[best_cluster] = pd.concat([cluster_list[best_cluster], remaining_attr], axis=1)

# Write out initial pairwise clustering
outf.writelines('First Pairwise Association at K = ' + str(k) + '\n')
for cluster in cluster_list:
    if len(cluster.columns) > 1:
        outf.writelines(str(cluster.columns.values).replace('[', '(').replace(']', ')'))
outf.writelines('\n'*2)

# Subsequent iterative steps
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

    # Sort and write out clustering at each iteration k.
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
    outf.writelines('\n'*2)
'''
outf.close()
spinner.stop()
print('Took', time.perf_counter() - start_time, 'seconds')
