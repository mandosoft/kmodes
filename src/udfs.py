from sklearn.metrics.cluster import normalized_mutual_info_score as nmis
import pandas as pd

def sri(cluster):
    rii = 0
    max_rii = 0
    sr_mode = None
    cluster_mode = pd.Series() 
    for i in cluster: 
        for j in cluster:        
            if cluster[i].name != cluster[j].name:
                rii += nmis(cluster[i], cluster[j], average_method = 'arithmetic')
        if rii > max_rii:
            max_rii = rii
            cluster_mode = cluster[i]
    if cluster_mode.empty == True:
        del cluster_mode
    else:
        print('\n')
        print(cluster_mode)
    #cluster.insert(0, cluster_mode.name, cluster_mode) 
