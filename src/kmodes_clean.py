import operator
import tkinter as tk
from collections import defaultdict
from tkinter import filedialog

import numpy as np
from sklearn.metrics.cluster import adjusted_mutual_info_score as amis
from sklearn.metrics.cluster import normalized_mutual_info_score as nmis

#prompts "Choose File" window to select a file to read as input
tk.Tk().withdraw()
file_path = filedialog.askopenfilename()
file = open(file_path) 

#Data input stream
input_samples = file.readlines() 

#Data output stream
testfile = open("testfile.txt", 'w')

#Reformats the sequence data rows and returns a list of columnwise Attribute objects   
def transform_data():
    sample_names = []
    sequence_data = []
    attributes = []
    
    for i in range(len(input_samples)):
        input_samples[i] = input_samples[i].replace("\n", "")
        li = list(input_samples[i].split(","))
        sample_names.append(li[0])
        li.pop(0) 
        sequence_data.append(li)

    data = np.array(sequence_data)
    num_attributes = len(data[0])

    for i in range(num_attributes): 
        attributes.append(Atr(i, data[:, i]))

    return attributes

#Defines the Attribute object class
class Atr:
    def __init__(self, col_num, amino_acids):
        self.col_num = col_num
        self.amino_acids = amino_acids
        self.list = [self]
    def __repr__(self):
        return '{self.col_num}, {self.amino_acids}'.format(self=self)

def cluster(attributes, a, b):
    if len(a.list) > 2 and len(b.list) > 2:
        for i in range(len(b.list)):
            max_R = 0
            if b.list[i] != b:
                rii = 0
                for j in range(len(attributes)):
                    if attributes[j] != b and attributes[j] != b.list[i]:
                        rii = nmis(b.list[i].amino_acids, attributes[j].amino_acids)
                        if rii > max_R:
                            max_R = rii
                            cluster_attribute = attributes[j]
                if b.list[i] not in cluster_attribute.list:
                    b.list[i].list = [b.list[i]]
                    cluster_attribute.list.append(b.list[i])
        b.list = [b]
        a.list.append(b)
    
    else:
        for i in range(len(b.list)):
            if b.list[i] not in a.list:
                a.list.append(b.list[i])
        b.list = [b] #potentially remove
        if b in attributes:
            attributes.remove(b)

def mode(attributes, a):
    max_R = 0
    sr_mode = None
    for i in range(len(a.list)):
        rii = 0
        for j in range(len(a.list)):
            if a.list[i] != a.list[j]:
                rii += nmis(a.list[i].amino_acids, a.list[j].amino_acids)
        rii = rii / len(a.list)
        if rii > max_R:
            max_R = rii
            sr_mode = a.list[i]
    if sr_mode != None:
        sr_mode.list = a.list   
        sorted(sr_mode.list, key=operator.attrgetter('col_num'))
        attributes.append(sr_mode)
        attributes.remove(a)
    elif sr_mode == None:
        attributes.remove(a)
        sorted(a.list, key=operator.attrgetter('col_num'))
        attributes.append(a)

def search(li, a, b):
    for i in range(len(li)):
        if li[i] == (a, b):
            return False
    return True

def write_to_file(attributes, cluster_attribute1, cluster_attribute2, max_R):
    k = len(attributes)
    testfile.write('k:' + str(k - 1) + '\n')
    testfile.write("Cluster: (" + str(cluster_attribute1.col_num) + 
    ',' + str(cluster_attribute2.col_num) + ')' + '\n')   
    testfile.write("Rii:" + str(round(max_R, 3)) + '\n')

    cluster(attributes, cluster_attribute1, cluster_attribute2)

    first_orders = 0
    for i in range(len(attributes)):
        mode(attributes, attributes[0])
        if len(attributes[0].list) < 2:
            first_orders += 1
        if len(attributes[0].list) > 1:
            testfile.write('(')
            for j in range(len(attributes[0].list)): #need to sort these here 
                testfile.write(str(attributes[0].list[j].col_num))
                testfile.write(' ')       
            testfile.write(')')
            testfile.write('\n')
    if len(attributes) <= k * .5:
        checker = False

    testfile.write('\n')

#Randomly select one attribute for each cluster to be the mode
#Calculate Rii between the selected mode and each remaining attribute 
#The attribute with the highest Rii to the mode is then compared to all remaining attributes
def main():
    attributes = transform_data()
    print(attributes)
    while len(attributes) > 3:
        max_R = 0 
        rii = 0 
        limiter = True
        checker = True
        past_clusters = []
        #makes sure that two large clusters do not cluster together until later in the loop
        while limiter:
            limiter = False
            cluster_attribute1 = attributes[np.random.randint(0, len(attributes))]
            print(cluster_attribute1)
            #random attribute chosen and compared
            for i in range(len(attributes)):
                if cluster_attribute1 != attributes[i] and attributes[i] not in past_clusters:
                    rii = nmis(cluster_attribute1.amino_acids, attributes[i].amino_acids)
                    print(rii)
                    if rii > max_R:
                        print(max_R)
                        max_R = rii
                        cluster_attribute2 = attributes[i]
                        print(cluster_attribute2)
            #attribute paired with random compared 
            for i in range(len(attributes)):
                if cluster_attribute2 != attributes[i] and attributes[i] not in past_clusters:
                    rii = nmis(cluster_attribute2.amino_acids, attributes[i].amino_acids)
                    print(rii)
                    if rii > max_R:
                        max_R = rii
                        cluster_attribute1 = attributes[i]
                        print(cluster_attribute1)
                    if checker:
                        if len(cluster_attribute1.list) >= 2 and len(cluster_attribute2.list) >= 2:
                            past_clusters.append(cluster_attribute1)
                            print(past_clusters)
                            limiter = True
        past_clusters.clear()
        write_to_file(attributes, cluster_attribute1, cluster_attribute2, max_R)
main()
