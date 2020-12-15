#!/usr/bin/env python
# coding: utf-8

# In[9]:


def find_stop_codon(seq:str)->int:
    seq = seq.lower()
    # find codons and append to temp list
    temp= [seq.find('tag'), seq.find('tga'), seq.find('taa')]
    # filter list to only positive integers
    # if filtered list is empty assign [-1], which means there is no matches.
    temp = [i for i in temp if i >= 0] or [-1]
    # return minimum index
    return min(temp)


# In[10]:


dna_sequence = "gcatcacgttatgtcgactctgtgtgagcgtctgctggg"
stop_codon = find_stop_codon(dna_sequence)
print(f"Stop codon is {dna_sequence[stop_codon:stop_codon+3] or 'not found'}, {stop_codon} ")


# In[ ]:




