from libconfig import * 

#prompts "Choose File" window to select a file to read as input
tk.Tk().withdraw()
file_path = filedialog.askopenfilename()
file = open(file_path) 

#Spinner. Helpful with large sequences
spinner = Halo(text='Running', spinner='simpleDots', color='green')
spinner.start()
 
#Data input stream
#NEEDTOFIX C parser was throwing UnicodeDecodeErrors. Switching engines does not fix the problem. 
#Not related to pandas as the built-in readLines() also did not work 
#Note that chunksize returns a TextFileObject rather than a Traditional DataFrame

df = pd.read_csv(file, encoding='utf-8', header=None)
df = df.drop(df.columns[[0]], axis=1)
df.index+=1

#Outfile testwrite 
outf = open('outfile.txt', 'w')
outf.writelines('Multiple Sequence Alignment: ' + '\n'*2 + df.to_string(index=False)+ '\n'*3)

#Step 1 Module 
# Eliminate global vars following completion 
# Do not use df.columns.values as this gives write access to underlying data in each column 

k = len(df.columns)
#k_clusters = [[] for i in range(k)]
 
while (k > 2):
    k_random_samples  = df.sample(k-1, axis = 1)
    outf.writelines('\n'*2 + str(k-1) + ' random samples' + '\n')
    outf.writelines('(')
    for i in k_random_samples:
        outf.writelines(str(k_random_samples[i].name) + ' ')
    outf.writelines(')')
    outf.writelines('\n'*2)
   
    for i in k_random_samples:
        for j in df:
            max_rii = 0
            if k_random_samples[i].name !=  df[j].name: 
                rii = nmis(k_random_samples[i], df[j], average_method='arithmetic')
                outf.writelines(str(k_random_samples[i].name) + '->' + str(df[j].name) + ': '  +  str(rii)+ '\n')
                if rii > max_rii: 
                    max_rii = rii
    k -= 1
   
    #outf.writelines('\n' + str(max_rii))


#Outfile testwrite
outf.writelines('\n'*2 + 'End Value of K: ' + str(k) + '\n'*3)
#outf.writelines('Max Rii: ' + str(rii))
#outf.writelines(str(k_random_samples)) 
outf.close()
spinner.stop()
