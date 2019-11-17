from libconfig import * 

#prompts "Choose File" window to select a file to read as input
tk.Tk().withdraw()
file_path = filedialog.askopenfilename()
file = open(file_path) 

#Spinner. Helpful with large sequences
spinner = Halo(text='Running  ', spinner='simpleDots', color='green')
spinner.start()

start_time = time.perf_counter()
 
#Data input stream
df = pd.read_csv(file, encoding='utf-8', header=None)
df = df.drop(df.columns[[0]], axis=1)
df.index+=1

#Outfile testwrite 
outf = open('outfile.txt', 'w')

n = len(df.columns)
k = n

#outf.writelines('\nMultiple Sequence Alignment\n' + df.to_string(index = False) + '\n'*2)

while (k > 2): 
    k -= 1
    k_random_samples = df.sample(k, axis = 1)
    cluster_list = [pd.DataFrame(k_random_samples[i]) for i in k_random_samples]
    remaining_attr = df[df.columns.difference(k_random_samples.columns, False)]

    for i in remaining_attr:
        max_rii = 0 
        for location, cluster in enumerate(cluster_list):  
            for j in cluster:
                rii = nmis(remaining_attr[i], cluster[j], average_method='arithmetic')
            if rii > max_rii: 
                max_rii, best_cluster = rii, location         
        cluster_list[best_cluster] = cluster_list[best_cluster].join(remaining_attr[i])

    outf.writelines('\nValue of K:' + str(k) + '\n')
    for cluster in cluster_list:
         outf.writelines(str(cluster.columns.values).replace('[','(').replace(']',')'))
    outf.writelines('\n'*2)

outf.close()
spinner.stop()
print('Took', time.perf_counter() - start_time, 'seconds')
