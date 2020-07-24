# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 10:22:48 2020

@author: stam
"""


import os, pickle
os.chdir(r'D:\BioASQ\evaluate_py')
import pandas as pd
import numpy as np
z = 'predictions_occ_only'

with open(z + ".pickle", "rb") as f:
    			y	 = pickle.load(f)
f.close()

y_occ = []
for i in y:
	y_occ.append(i.split('#'))


#here we load the vector with predictions
#import copy
#yy = copy.deepcopy(NN_bioBERT_44k_decisions)

where = []
c = -1
for i in y_occ:
    c +=1
    if i == ['None']:
        where.append(c)
        
print(len(where))
#%%

os.chdir(r'D:\BioASQ\evaluate_py')
print(os.getcwd())
zz = 'label_dependence_max_weighted_NN_bioBERT_44k_decisions_scores_official.pickle'
#zz = 'label_dependence_max_weighted_NN_bioBERT_44k_decisions_scores_shuffled_70percent_official.pickle'
#zz = 'label_dependence_max_weighted_NN_bioBERT_44k_decisions_scores_shuffled_70percent_plus_noise_official.pickle'

with open(zz, "rb") as f:
    				label_dependence = pickle.load(f)
f.close()

which = zz
yy = label_dependence


for i in range(0, len(y_occ)):
    if i in where:
        continue
    
    else:
        pos, labels = [], []
        for j in y_occ[i]:
            yy[i] = list(yy[i])
            pos.append(yy[i].index(j))
            labels.append(j)
        
        how = sorted(range(len(pos)), key=lambda k: pos[k], reverse = True)
        #c = -1
        for _ in how:
            #c += 1       
            yy[i].remove(labels[_])
            yy[i].insert(0, labels[_])
    
          
print(os.getcwd())

with open('occurence_' + zz, 'wb') as handle:
     pickle.dump(yy, handle)                
handle.close()

#%%

# print(os.getcwd())
# with open('label_dependence_max_weighted_with_occurence_NN_bioBERT_44k_decisions_scores_shuffled_70percent_plus_noise.pickle', 'wb') as handle:
#      pickle.dump(yy, handle)                
# handle.close()