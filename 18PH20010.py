# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 18:32:19 2022

@author: Firos
"""

import requests
import pandas as pd
import numpy as np

author = input()
url = 'https://poetrydb.org/author/'+author
token = requests.get(url).json()

if(isinstance(token, list)):
    df = pd.DataFrame(token)
    
    total_lines = 0
    min_lines = 100000000
    titles = []
    
    for i in df.index:
        line_count = int(df.loc[i,'linecount'])
        total_lines += line_count
        if(line_count<min_lines):
            titles.clear()
            titles.append(df.loc[i,'title'])
            min_lines = line_count
        elif(line_count==min_lines):
            titles.append(df.loc[i,'title'])
        else:
            continue
    
    print(total_lines)
    for i in titles:
        print(i)

else:
    print('0')
    print('-')