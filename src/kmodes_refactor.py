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


#score = nmis(df[1], df[2])

#Step 1 Module 
# Eliminate global vars following completion 

k = len(df.columns)
k_clusters = [[] for i in range(k)]


#for i in range(len(k_clusters)):
 #   k_clusters[i].append(df.columns(df.sample(1, axis=1)))


#TypeError: 'Int64Index' object is not callable

 
#Outfile testwrite
outf.writelines('Value of K: ' + str(k) + '\n'*3)
outf.writelines('Clusters: ' + '\n'*2 + str(''))
outf.writelines(str(df.info))
outf.close()

