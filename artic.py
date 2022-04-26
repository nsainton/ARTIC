#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 01:07:18 2022

@author: noahsaintonge
"""

#import glob
import pandas as pd
import Rapports as rp
#from scipy import stats
"""
path = 'Rapports'
files = glob.glob(path + '/*.xlsx')
print(files)

dfs = {}

for f in files:
    temp_df = pd.read_excel(f)
    total = list(temp_df)[len(list(temp_df))-1]
    temp_df.rename(columns = {total : 'TOTAL', 'SERVICE 1' : 'SERVICE'}, \
             inplace = True)
    SERVICE = temp_df['SERVICE'].dropna(axis = 0)
    values = np.unique(SERVICE, return_counts = False)
    print(values)
    dfs[f] = temp_df
    #print(f'Successfully created dataframe for {f} with shape \
    #      {temp_df.shape}')

"""
#Analysis of a medical dataFrame with a few data in it to try and do the
#maximum with the data we got
#First step: dataFrame preparation and implementation of functions that
#will allow us to do the proper analysis

#We are going to analyse the dataFrame following the following plan
#First, we are going to represent therapist by therapist how much patients
#they got and how frequently they came back after coming for the first time
#in the therapist office

#Second, we are going to represent year by year the evolution of attendance
#of the differents activities offered by the association

#thirdly, we are going to represent some more general statistics about the
#whole inpact of the prendre soin activities on the patients and physicians

#Finally, we are going to analyse which service prescripts more consultations
#for the prendre soin activities

dict_of_df = pd.read_excel('PPS4.xlsx', sheet_name = None)
dict_of_df = {k:rp.formate(v) for (k,v) in dict_of_df.items() if '2020' in k}

df = dict_of_df['Sylvie-2020']

#rp.main(df,dict_of_df)
def multi_therapies(dict_of_df):
    year = pd.concat(dict_of_df.values())
    print(year)
    duplicates = year[year.duplicated(subset = ['PATIENT'])]
    #function duplicated only remove one duplicate if there are more than one
    print(duplicates['PATIENT'])
    duplicate = {}
    for i in duplicates['PATIENT']:
        duplicate[str(i)] = []
    for k,v in dict_of_df.items():
        for ke in duplicate.keys():
            if v[v.isin([ke])].size > 0 : duplicate[ke].append(k)
    return (duplicate, duplicates)

def print_dic(dic):
    for i,j in dic.items():
        print('clef : ',i,' valeur : \n',j)
    return None

"""
if __name__ == "__main__":
    import sys
    main(sys.argv[1])
"""