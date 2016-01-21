# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 16:05:38 2016

@author: tieqiangli
"""

import numpy as np
from sklearn.naive_bayes import GaussianNB

def bayseFilter(X,y):
    clf = GaussianNB()
    clf.fit(X,y)
    bayseX = clf.predict_proba(X)
    t = np.ones(bayseX.shape[0])    
    for i in range(0,bayseX.shape[1]):
        t = t*bayseX[:,i]
        
    bayseXfilter = t
    return bayseXfilter