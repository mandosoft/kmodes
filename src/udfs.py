from sklearn.metrics.cluster import normalized_mutual_info_score as nmis
import pandas as pd

def sri(cluster):
    outd = open('outfile_udfs.txt', 'w')
    outd.writelines('Cluster Values' + str(cluster.columns.values))
    sum_rii = 0
    max_sum = 0
    sr_mode = None
    cluster_mode = pd.Series() 
    for location, i in enumerate(cluster): 
        for j in cluster:        
            if (cluster[i].name != cluster[j].name):
                outd.writelines('\nCluster Name 1: ' + str(cluster[i].name) + '\nCluster Name 2: ' + str(cluster[j].name) + '\n'*2)
                sum_rii += nmis(cluster[i], cluster[j], average_method = 'arithmetic')
                if (sum_rii > max_sum):
                    max_sum, cluster_mode, ix = sum_rii, cluster[i], location
    if cluster_mode.empty == True:
        del cluster_mode
    else:
        cluster = cluster.drop(cluster.columns[ix], axis = 1)
        cluster = pd.concat([cluster, cluster_mode], axis=1)
        cols = cluster.columns.tolist()
        cols = cols[-1:] + cols[:-1]
        cluster = cluster[cols] 
    outd.close()
    return cluster

  
