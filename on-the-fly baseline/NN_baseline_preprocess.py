# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 01:58:05 2020

@author: stam

Create the appropriate dictionaries per pickle: keys -> instanceX, value: dictionary structure (dictX)
dictX: keys -> investigated labels, value: i) the abs distance from the bioBERT embedding of each instance's sentence' or ii) the corresponding cosine similarity
"""

import os, pickle
import numpy as np
import torch

path = r'D:\BioASQ\evaluate_py'
os.chdir(path)

# load embeddings of the investigated labels (pre-compued process)
z = 'top_100_labels_embeddings'
with open(z + '.pickle', "rb") as f:
            label_embeddings = pickle.load(f)
f.close()

# select between the the manner that distances are takein into consideration between embedding vectors:
choice = input('Press your choice: \n1. Nearest-Neighbors using absolute distance \n2. Nearest-Neighbor using cosine similarity \n... ')

    
# provide the path with pre-computed sentence embeddings per sentence
name = r'D:\44k pickles\pure_Zeroshot_test_set_'

for i in range(0,5): # we have 5 separate pickles, having split them to batches of 10,000 instances

    
    with open(name + str(i)+".pickle", "rb") as f:
      sentence_embeddings = pickle.load(f)
    f.close()
    
    
    d = {}
    for j in range(0, len(sentence_embeddings)):
        
        if j % 500 == 0:
            print(j)
        d['instance' + str(j)] = {}
        
        #Initialize empy lists per label for every examined instance
        for label in label_embeddings.keys():
            d['instance' + str(j)][label] = []
            
        for k in range(0, len(sentence_embeddings.iloc[j])): # number of sentences
            
            if len(sentence_embeddings.iloc[j][k]) == 0:
                continue
            
            for label in label_embeddings.keys():
                
                q = label_embeddings[label]
                
                if choice == '1':
                    
                    d['instance' + str(j)][label].append(np.sum(np.abs(q - sentence_embeddings.iloc[j][k].cpu().numpy())))
                    prefix = 'NN_bioBERT_44k_batch'
                elif choice == '2':
                
                    d['instance' + str(j)][label].append( torch.cosine_similarity( torch.from_numpy(q), sentence_embeddings.iloc[j][k].cpu(), dim=0).cpu().numpy())
                    prefix = 'torch_NN_bioBERT_44k_batch'
                
    # for every input batch, another one output batch is computed, holding the appropriate distances into them                
    with open(prefix + str(i) + '.pickle', 'wb') as handle:
        pickle.dump(d, handle)                
    handle.close()
    
print('**Preprocess has been completed***')