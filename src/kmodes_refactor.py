import operator
import tkinter as tk
from collections import defaultdict
from tkinter import filedialog

import pandas as pd
import numpy as np
from sklearn.metrics.cluster import adjusted_mutual_info_score as amis
from sklearn.metrics.cluster import normalized_mutual_info_score as nmis

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
outf.writelines(df.to_string(index=False))





#score = nmis(df[1], df[2])

