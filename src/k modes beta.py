#import pdb; pdb.set_trace()
import numpy as np
from sklearn.metrics.cluster import normalized_mutual_info_score as nmis
from sklearn.metrics.cluster import adjusted_mutual_info_score as amis
from collections import defaultdict 
import tkinter as tk
from tkinter import filedialog

# Python program for implementation of MergeSort 
def mergeSort(arr): 
    if len(arr) >1: 
        mid = len(arr)//2 #Finding the mid of the array 
        L = arr[:mid] # Dividing the array elements  
        R = arr[mid:] # into 2 halves 
  
        mergeSort(L) # Sorting the first half 
        mergeSort(R) # Sorting the second half 
  
        i = j = k = 0
          
        # Copy data to temp arrays L[] and R[] 
        while i < len(L) and j < len(R): 
            if L[i].col_num < R[j].col_num: 
                arr[k] = L[i] 
                i+=1
            else: 
                arr[k] = R[j] 
                j+=1
            k+=1
          
        # Checking if any element was left 
        while i < len(L): 
            arr[k] = L[i] 
            i+=1
            k+=1
          
        while j < len(R): 
            arr[k] = R[j] 
            j+=1
            k+=1

class Atr:
    def __init__(self, col_num, amino_acids):
        self.col_num = col_num
        self.amino_acids = amino_acids
        self.clustered = [self]
    
def cluster(attributes, a, b):

    #checks if two clusters that are larger than one are clustering together
    if len(a.clustered) > 2 and len(b.clustered) > 2:
        for i in range(len(b.clustered)):
            max_R = 0
            if b.clustered[i] != b:
                rii = 0
                for j in range(len(attributes)):
                    if attributes[j] != b and attributes[j] != b.clustered[i]:
                        rii = nmis(b.clustered[i].amino_acids, attributes[j].amino_acids)
                        if rii > max_R:
                            max_R = rii
                            cluster_attribute = attributes[j]
                #print(cluster_attribute.col_num, b.clustered[i].col_num)
                if b.clustered[i] not in cluster_attribute.clustered:
                    b.clustered[i].clustered = [b.clustered[i]]
                    cluster_attribute.clustered.append(b.clustered[i])
        b.clustered = [b]
        a.clustered.append(b)
    
    else:
        for i in range(len(b.clustered)):
            if b.clustered[i] not in a.clustered:
                a.clustered.append(b.clustered[i])
        b.clustered = [b]
        if b in attributes:
            attributes.remove(b)

def mode(attributes, a):
    max_R = 0
    sr_mode = None
    for i in range(len(a.clustered)):
        rii = 0
        for j in range(len(a.clustered)):
            if a.clustered[i] != a.clustered[j]:
                #print(a.clustered[i].col_num, a.clustered[j].col_num)
                rii += nmis(a.clustered[i].amino_acids, a.clustered[j].amino_acids)
        rii = rii / len(a.clustered)
        #print(a.clustered[i].col_num, rii)
        if rii > max_R:
            max_R = rii
            sr_mode = a.clustered[i]
    if sr_mode != None:
        sr_mode.clustered = a.clustered   
        mergeSort(sr_mode.clustered)
        attributes.append(sr_mode)
        attributes.remove(a)
    elif sr_mode == None:
        attributes.remove(a)
        mergeSort(a.clustered)
        attributes.append(a)

#searches the past cluster list
def search(li, a, b):
    for i in range(len(li)):
        if li[i] == (a, b):
            return False
    return True

#lists
data = []
sample_names = []
attributes = []
#prompts to select a file to use
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()
file = open(file_path) 
samples = file.readlines() 
#formats file so that the code can analyze properly
for i in range(len(samples)):
        samples[i] = samples[i].replace("\n", "")
        li = list(samples[i].split(","))
        sample_names.append(li[0])
        li.pop(0)
        data.append(li)

data = np.array(data)
print(data)
num_attributes = len(data[0])
max_R = 0
rii = 0
k = num_attributes

for i in range(num_attributes):
    new_atr = Atr(i, data[:, i])
    attributes.append(new_atr)
    print(attributes[i].col_num, attributes[i].amino_acids)

testfile = open("testfile.txt", 'w')
past_clusters = []

limiter = 2
checker = True

#main function starts here 
#loops until x clusters remain
while len(attributes) > 3:
    print(len(attributes))
    max_R = 0
    lim_checker = True
    #makes sure that two large clusters do not cluster together until later in the loop
    while lim_checker:
        lim_checker = False
        cluster_attribute1 = attributes[np.random.randint(0, len(attributes))]
        #random attribute chosen and compared
        for i in range(len(attributes)):
            if cluster_attribute1 != attributes[i] and attributes[i] not in past_clusters:
                rii = nmis(cluster_attribute1.amino_acids, attributes[i].amino_acids)
                if rii > max_R:
                    max_R = rii
                    cluster_attribute2 = attributes[i]
        #attribute paired with random compared 
        for i in range(len(attributes)):
            if cluster_attribute2 != attributes[i] and attributes[i] not in past_clusters:
                rii = nmis(cluster_attribute2.amino_acids, attributes[i].amino_acids)
                if rii > max_R:
                    max_R = rii
                    cluster_attribute1 = attributes[i]
                if checker:
                    if len(cluster_attribute1.clustered) >= 2 and len(cluster_attribute2.clustered) >= 2:
                        past_clusters.append(cluster_attribute1)
                        lim_checker = True
    
    past_clusters.clear()

    #writes the data to a file 

    testfile.write("k:")
    testfile.write(str(len(attributes) - 1))
    testfile.write("\n")
    #outputs the clusters and attributes pertaining to it into a text file
    testfile.write("Cluster: (")
    testfile.write(str(cluster_attribute1.col_num + 6))
    #testfile.write(str(cluster_attribute1))
    testfile.write(',')
    testfile.write(str(cluster_attribute2.col_num + 6))
    #testfile.write(str(cluster_attribute2))
    testfile.write(')')
    testfile.write("\n")
    testfile.write("Rii:")
    testfile.write(str(round(max_R, 3)))
    testfile.write("\n")

    #clusters the two attributes together 
    cluster(attributes, cluster_attribute1, cluster_attribute2)
    
    first_orders = 0
    for i in range(len(attributes)):
        mode(attributes, attributes[0])
        if len(attributes[0].clustered) < 2:
            first_orders += 1
        if len(attributes[0].clustered) > 1:
            testfile.write('(')
            for j in range(len(attributes[0].clustered)):
                testfile.write(str(attributes[0].clustered[j].col_num + 6))
                testfile.write(' ')       
            testfile.write(')')
            testfile.write("\n")
    if len(attributes) <= k * .5:
        checker = False
    
    testfile.write("\n")
    
        