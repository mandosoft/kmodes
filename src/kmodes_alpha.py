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

while (k > 2): 
    k -= 1
    k_clusters = [pd.DataFrame() for _ in range(k)]
    k_random_samples = df.sample(k, axis = 1)
    df_remaining = df[df.columns.difference(k_random_samples.columns, False)]

    for i in k_random_samples:
        for j in df_remaining:
            max_rii = 0 
            rii = nmis(k_random_samples[i], df_remaining[j], average_method='arithmetic')
            if rii > max_rii: 
                max_rii = rii
                current_max = df_remaining[j]
        df_remaining = df_remaining[df_remaining.columns.difference(current_max)]

outf.close()
spinner.stop()
print('Took', time.perf_counter() - start_time, 'seconds')

