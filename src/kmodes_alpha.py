from libconfig import * 

#prompts "Choose File" window to select a file to read as input
tk.Tk().withdraw()
file_path = filedialog.askopenfilename()
file = open(file_path) 
 
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

#Syntax for nmis calcs 
#score = nmis(df[1], df[2])

#Step 1 Module 
# Eliminate global vars following completion 

k = len(df.columns)
k_clusters = [[] for i in range(k)]

while (k > 2):
    k_random_samples  = df.sample(k, axis = 1)
    outf.writelines(str(k) + ' random samples ' + '\n'*2 + k_random_samples.to_string(index=False) + '\n'*3)
    k -= 1  

#Write to clusters 
for i in range(len(k_clusters)): 
    for j in range(i + 1, len(k_clusters)):
        k_clusters[i].append((df.sample(1, axis=1)))
        if k_clusters[i] == k_clusters[j]:
            k_clusters[j].pop(0)
            k_clusters[j].append(df.sample(1, axis=1))
 
#Outfile testwrite
outf.writelines('Value of K: ' + str(k) + '\n'*3)
#outf.writelines('Clusters: ' + '\n'*2 + str(k_clusters) + '\n'*3)
#outf.writelines(str(k_random_samples))
outf.close()

