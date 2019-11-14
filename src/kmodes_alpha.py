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

outf.writelines('Multiple Sequence Alignment\n' + df.to_string(index = False))

while (k > 2): 
    k -= 1
    k_random_samples = df.sample(k, axis = 1)
    clusters = [pd.DataFrame(k_random_samples[i]) for i in k_random_samples]
    remaining_attr = df[df.columns.difference(k_random_samples.columns, False)]
    outf.writelines('\nIteration: ' + str(k) + '\n' + str(clusters))

'''
    for i in remaining_attr: 
        for j in k_random_samples:
            max_rii = 0 
            rii = nmis(remaining_attr[i], k_random_samples[j], average_method='arithmetic')
            if rii > max_rii: 
                max_rii = rii
                current_max = k_random_samples[j]
        cluster = pd.DataFrame(current_max)
        cluster = cluster.join(remaining_attr[i])
        outf.writelines('\n' + 'Cluster:' + str(k) + '\n' + cluster.to_string(header = True, index = False) + '\n'*2)
'''

outf.close()
spinner.stop()
print('Took', time.perf_counter() - start_time, 'seconds')

