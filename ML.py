# -*- coding: utf-8 -*-
"""
Created on Sun Jan 30 16:41:51 2022

@author: Firos
"""


import numpy as np
import pandas as pd
import random
import math


df = pd.read_csv('A-1_data.csv')
df = df.dropna()
df = df.sample(frac=1).reset_index(drop=True)
x = df.iloc[:,0:19]
y = df.iloc[:,19]

df_training = df.iloc[:len(df)-15,:].copy(deep=True)
df_test = df.tail(15).copy(deep=True)
df_condensed = pd.DataFrame()



rnd_index = random.randint(0,50)
df_element1 = df.loc[rnd_index]
df_condensed = df_condensed.append(df_element1)
df_training = df_training.drop(rnd_index)




while(True): 
    change = 0
    nearest_neighbour = 9999
    for ind1 in df_training.index:
        min_dist = 99999
        for ind2 in df_condensed.index:
            if(ind1==ind2):
                continue
            else:
                dist = math.dist(x.loc[ind1],x.loc[ind2])
                if(dist<min_dist):
                    nearest_neighbour = ind2
                    min_dist = dist
        if(y[ind1]==y[nearest_neighbour]):
            continue
        else:
            df_condensed = df_condensed.append(df.loc[ind1])
            df_training = df_training.drop(ind1)
            change += 1;
    
    if(change==0):
        break            

dictionar = {}
dictionar[1] = 'A'
dictionar[0] = 'B'


for ind1 in df_test.index:
    nearest = {}
    min_dist = 9999
    zeros = 0
    ones = 0
    for ind2 in df_condensed.index:
        dist = math.dist(x.loc[ind1],x.loc[ind2])
        nearest[dist] = y[ind2]
    for i in sorted(nearest.keys())[0:5]:
        if(nearest[i]==1):
            ones += 1
        if(nearest[i]==0):
            zeros += 1
    
    if(zeros>ones):
        df_test.loc[ind1,'estimated_ca_cervix_condensed'] = 0
    else:
        df_test.loc[ind1,'estimated_ca_cervix_condensed'] = 1


df_training = df.iloc[:len(df)-15,:].copy(deep=True)


for ind1 in df_test.index:
    nearest = {}
    min_dist = 9999
    zeros = 0
    ones = 0
    for ind2 in df_training.index:
        dist = math.dist(x.loc[ind1],x.loc[ind2])
        nearest[dist] = y[ind2]
    for i in sorted(nearest.keys())[0:5]:
        if(nearest[i]==1):
            ones += 1
        else:
            zeros += 1
        
    if(zeros>ones):
        df_test.loc[ind1,'estimated_normal'] = 0
    else:
        df_test.loc[ind1,'estimated_normal'] = 1


misclassification_condensed = 0
misclassification_normal = 0
for i in df_test.index:
    if(df_test.loc[i,'ca_cervix'] != df_test.loc[i,'estimated_ca_cervix_condensed']):
        misclassification_condensed += 1
    if(df_test.loc[i,'ca_cervix'] != df_test.loc[i,'estimated_normal']):
        misclassification_normal += 1
 
accuracy_condensed = 1-(misclassification_condensed/len(df_test))
accuracy_normal = 1-(misclassification_normal/len(df_test))