# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 10:44:38 2020

@author: stam
"""

import os, pickle
import numpy as np
import pandas as pd


def bring_new_y():
    
    os.chdir(r'D:\BioASQ\evaluate_py')
    test_file = "pure_zero_shot_test_set_top100.txt"
    
    y = []
    file = open(test_file)
    for line in file:
    	y.append(line[2:-2].split("labels: #")[1])
    print(len(y))
    
    file = open("top_100_labels.txt")
    labels=list()
    for line in file:
    	labels.append(line[:-1])
        
    new_y = []
    known_y = []
    for label_y in y:
    	string = ""
    	flag = "false"
    	string_known=""
    	for label in label_y.split("#"):
    		if label in labels:
    			flag = "true"
    			string = string + label + "#"
    		else:
    			string_known=string_known+label+"#"
    	if (flag == "false"):
    		string = "None#"
    	new_y.append(string[:-1].split('#'))
    	known_y.append(string_known[:-1].split('#'))
     
    return new_y


def coverage_custom(y_test, y_pred):
    ''' Input:
            y_test: vector of ground truth
            y_pred: vector of predictions
        
        Return:
            Coverage score per instance'''
            
    k = []
    for y in range(0, len(y_test)):
        
        kk = []
        for i in range(0, len(y_test[y])):
            
            kk.append( list(y_pred[y]).index(y_test[y][i]) )
        
        k.append(max(kk))
        
    return k

#%%  if you want to load the summarization files

os.chdir(r'D:\NN_bioBERT_summary')
files = os.listdir(os.getcwd())
print(files)

which = files[2] #[0] or [2]
with open(which, "rb") as f:
    full_decisions, full_best_3_scores = pickle.load(f)
f.close()


which = 'torch_NN_bioBERT_test_set_decisions_scores_official' 
NN_bioBERT_44k_decisions = full_decisions[:] 


#%%

y_test = bring_new_y()[:]

k = coverage_custom(y_test, NN_bioBERT_44k_decisions)
print(np.round(np.mean(k),3) , len(k))
pd.DataFrame(k).hist(bins = 50)

bin_range = np.array([0,1,3,10,30,50,100])
out, bins  = pd.cut(k, bins=bin_range, include_lowest=True, right=False, retbins=True)
out.value_counts()
pd.DataFrame(out.value_counts()).to_csv(which + '_bins.csv')


#%%
    
os.chdir(r'D:\BioASQ\evaluate_py')
print(os.getcwd())
#zz = 'label_dependence_max_NN_bioBERT_44k_decisions_scores_official.pickle'
zz = 'label_dependence_sum_weighted_NN_bioBERT_44k_decisions_scores_shuffled_70percent_plus_noise_official.pickle'

with open(zz, "rb") as f:
    				label_dependence = pickle.load(f)
f.close()

which = zz
NN_bioBERT_44k_decisions = label_dependence

#%%

os.chdir(r'D:\BioASQ\evaluate_py')

print(os.getcwd())
zz = 'occurence_label_dependence_sum_weighted_NN_bioBERT_44k_decisions_scores_official.pickle'
#zz = 'occurence_label_dependence_max_weighted_NN_bioBERT_44k_decisions_scores_shuffled_70percent_official.pickle'
#zz = 'occurence_label_dependence_max_weighted_NN_bioBERT_44k_decisions_scores_shuffled_70percent_plus_noise_official.pickle'
with open(zz, "rb") as f:
    				label_dependence = pickle.load(f)
f.close()

which = zz
NN_bioBERT_44k_decisions = label_dependence

y_test = bring_new_y()[:]

k = coverage_custom(y_test, NN_bioBERT_44k_decisions)
print(np.round(np.mean(k),3) , len(k))
pd.DataFrame(k).hist(bins = 50)

bin_range = np.array([0,1,3,10,30,50,100])
out, bins  = pd.cut(k, bins=bin_range, include_lowest=True, right=False, retbins=True)
out.value_counts()
pd.DataFrame(out.value_counts()).to_csv(which + '_bins.csv')