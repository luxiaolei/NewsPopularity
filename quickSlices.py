# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 07:13:58 2016

@author: tieqiangli
"""

import math
import pandas as pd

def csvDiv(f, s):
    
    df = pd.read_csv(f)
    k = df.shape[0]
    n = math.floor(k/s)
    
    for i in range(1,int(n)):
        dfTemp = df.ix[s*(i-1):s*i-1,:]
        fTemp = 'rawdata/input/'
        fp = fTemp + 'OnlineNewsPopularity_' + str(int(i)) + '.csv' 
        dfTemp.to_csv(fp,index=False,header=True)
        
if __name__=='__main__':
    
    f = 'rawdata/OnlineNewsPopularity_GOOD.csv'
    size = 500
    csvDiv(f,size)