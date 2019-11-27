from sklearn.metrics.cluster import normalized_mutual_info_score as nmis
import pandas as pd

def sri(cluster):
    sum_rii = 0
    max_sum = 0
    sr_mode = None
    cluster_mode = pd.Series() 
    for location, i in enumerate(cluster): 
        for j in cluster:        
            if (cluster[i].name != cluster[j].name):
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
    
    return cluster

  
