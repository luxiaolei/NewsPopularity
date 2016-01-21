# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 16:02:55 2016

@author: tieqiangli
"""

from __future__ import print_function
print(__doc__)

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from sklearn import cross_validation, linear_model

f = '/Users/tieqiangli/mapperinput/cases/NewsPopularity/rawdata/input/OnlineNewsPopularity_3.csv'

df = pd.read_csv(f)

X = df.ix[:,0:df.shape[1]-1]
y = df.ix[:,df.shape[1]-1]

def plot_lasso_cv(X,y):

    lasso = linear_model.Lasso()
    alphas = np.logspace(-4, -.5, 30)
    
    scores = list()
    scores_std = list()
    
    for alpha in alphas:
        lasso.alpha = alpha
        this_scores = -cross_validation.cross_val_score(lasso, X, y, cv=10, scoring='mean_absolute_error')
        scores.append(np.mean(this_scores))
        scores_std.append(np.std(this_scores))
    
    plt.figure(figsize=(4, 3))
    plt.semilogx(alphas, scores)
    # plot error lines showing +/- std. errors of the scores
    plt.semilogx(alphas, np.array(scores) + np.array(scores_std) / np.sqrt(len(X)),
                 'b--')
    plt.semilogx(alphas, np.array(scores) - np.array(scores_std) / np.sqrt(len(X)),
                 'b--')
    plt.ylabel('CV score')
    plt.xlabel('alpha')
    plt.axhline(np.max(scores), linestyle='--', color='.5')
    
    ##############################################################################
    # Bonus: how much can you trust the selection of alpha?
    
    # To answer this question we use the LassoCV object that sets its alpha
    # parameter automatically from the data by internal cross-validation (i.e. it
    # performs cross-validation on the training data it receives).
    # We use external cross-validation to see how much the automatically obtained
    # alphas differ across different cross-validation folds.
#    lasso_cv = linear_model.LassoCV(alphas=alphas)
#    k_fold = cross_validation.KFold(len(X), 3)
#    
#    print("Answer to the bonus question:",
#          "how much can you trust the selection of alpha?")
#    print()
#    print("Alpha parameters maximising the generalization score on different")
#    print("subsets of the data:")
#    for k, (train, test) in enumerate(k_fold):
#        lasso_cv.fit(X[train], y[train])
#        print("[fold {0}] alpha: {1:.5f}, score: {2:.5f}".
#              format(k, lasso_cv.alpha_, lasso_cv.score(X[test], y[test])))
#    print()
#    print("Answer: Not very much since we obtained different alphas for different")
#    print("subsets of the data and moreover, the scores for these alphas differ")
#    print("quite substantially.")
    
    plt.show()

