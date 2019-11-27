from libconfig import * 
from udfs import *

#prompts "Choose File" window to select a file to read as input
#tk.Tk().withdraw()
#file_path = filedialog.askopenfilename()
#file = open(file_path) 

#Spinner. Helpful with large sequences
spinner = Halo(text='Running  ', spinner='simpleDots', color='green')
spinner.start()

start_time = time.perf_counter()
 
#Data input stream use file in arg
df = pd.read_csv('K modes test sequence revised-3.csv', encoding='utf-8', header=None)
df = df.drop(df.columns[[0]], axis=1)
df.index+=1

#File MSA Output 
outf = open('outfile.txt', 'w')
#outf.writelines('\nMultiple Sequence Alignment\n' + df.to_string(index = False) + '\n'*2)

n = len(df.columns)
k = n

#Initialization 
k -= 1
k_random_samples = df.sample(k, axis = 1)
cluster_list = [pd.DataFrame(k_random_samples[i]) for i in k_random_samples]
remaining_attr = df[df.columns.difference(k_random_samples.columns, False)]
max_rii = 0 
rii = 0

#Initial pairwise clustering on random values
for location, cluster in enumerate(cluster_list):
    cluster_mode = cluster[cluster.columns[0]] 
    rii = nmis(remaining_attr[remaining_attr.columns[0]], cluster_mode, average_method='arithmetic')
    if (rii > max_rii): 
        max_rii, best_cluster = rii, location       
cluster_list[best_cluster] = pd.concat([cluster_list[best_cluster], remaining_attr], axis=1)

#Write out initial pairwise clustering
outf.writelines('First Pairwise Association at K = ' + str(k) + '\n')
for cluster in cluster_list:
    outf.writelines(str(cluster.columns.values).replace('[','(').replace(']',')'))
outf.writelines('\n'*2)


#Subsequent iterative steps
while (k  > 2):
    
    k -= 1
    
    #Select a random  mode
    enumerated_list = list(enumerate(cluster_list))
    outf.writelines('\nEnumerated List: ' + str(enumerated_list) + '\n'*2)
    
    random_df_il, random_df = random.choice(enumerated_list)
    outf.writelines('\nIndex Location: ' + str(random_df_il) + '  ' 'Random DataFrame: \n' + random_df.to_string(index=False)) 
    
    new_mode = random_df[random_df.columns[0]] 
    
    outf.writelines('\nNew Mode: \n ' + new_mode.to_string(index=False)) 
    
    rii = 0
    max_rii = 0
    #Add random mode to best cluster 
    for location, cluster in enumerated_list:
        cluster_mode = cluster[cluster.columns[0]]
        if (location != random_df_il):
            outf.writelines('\nLocation: ' + str(location) + '\nCluster Mode: ' + cluster_mode.to_string(index=False))
            rii = nmis(new_mode, cluster_mode, average_method='arithmetic')
            if (rii > max_rii):
                max_rii, best_cluster = rii, location
    outf.writelines('\nrandom index ' + str(random_df_il) + ' chose cluster index ' + str(best_cluster) + '\n')
    
    cluster_list[random_df_il] = cluster_list[random_df_il].drop(cluster_list[random_df_il].columns[0], axis=1) 
    cluster_list[best_cluster] = pd.concat([cluster_list[best_cluster], new_mode], axis=1)
     
    #Handles the cluster where mode has been removed 
    if cluster_list[random_df_il].empty == True:
        del cluster_list[random_df_il]

    '''
    elif cluster_list[random_df_il].empty == False: 
        for i in cluster_list[random_df_il]:
            remaining_attr = cluster_list[random_df_il][i]
            for location, cluster in enumerate(cluster_list):
                cluster_mode = cluster[cluster.columns[0]]
                if (remaining_attr.name != cluster_mode.name):
                    rii = nmis(remaining_attr, cluster_mode, average_method='arithmetic')
                    if (rii > max_rii):
                        max_rii, best_cluster = rii, location
            cluster_list[best_cluster] = pd.concat([cluster_list[best_cluster], remaining_attr], axis=1)
        del cluster_list[random_df_il]

    else:
        print('\nThere was a problem breaking up a cluster.\n')
    
    #Compute new mode for each cluster
    for location, cluster in enumerate(cluster_list): 
        cluster_list[location] = sri(cluster)
    '''

    #Write out clustering at each iteration k 
    outf.writelines('\n'*2 + 'Clusters at Iteration K = ' + str(k) + '\n')
    outf.writelines('\nUnsorted: \n')
    for cluster in cluster_list:
        outf.writelines(str(cluster.columns.values).replace('[','(').replace(']',')'))
    outf.writelines('\n'*3)

#    outf.writelines('\nSorted: \n')
#    for cluster in cluster_list:
#        cluster = cluster.reindex(sorted(cluster.columns), axis=1)
#        outf.writelines(str(cluster.columns.values).replace('[','(').replace(']',')'))
#    outf.writelines('\n'*3)
outf.close()
spinner.stop()
print('Took', time.perf_counter() - start_time, 'seconds')
