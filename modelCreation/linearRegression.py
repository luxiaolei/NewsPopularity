# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 17:30:21 2015

@author: tieqiangli
"""

from sklearn import datasets
from sklearn import cross_validation
from sklearn.cross_validation import cross_val_predict
from sklearn import linear_model
import matplotlib.pyplot as plt

boston = datasets.load_boston()
X = boston.data
y = boston.target
# cross_val_predict returns an array of the same size as `y` where each entry
# is a prediction obtained by cross validated:
#predicted = cross_val_predict(lr, boston.data, boston.target, cv=10)

''' linear least square regression '''
lr = linear_model.LinearRegression()

scores = cross_validation.cross_val_score(lr, X, y, cv=100, scoring='mean_absolute_error')

print("Accuracy: %0.2f (+/- %0.2f)" % (-scores.mean(), scores.std() * 2))


''' lasso '''
lasso = linear_model.Lasso()

scores_lasso = cross_validation.cross_val_score(lasso, X, y, cv=100, scoring='mean_absolute_error')

print("Accuracy: %0.2f (+/- %0.2f)" % (-scores_lasso.mean(), scores_lasso.std() * 2))

''' Lars '''
lars = linear_model.Lars()

scores_lars = cross_validation.cross_val_score(lars, X, y, cv=100, scoring='mean_absolute_error')

print("Accuracy: %0.2f (+/- %0.2f)" % (-scores_lars.mean(), scores_lars.std() * 2))

#fig, ax = plt.subplots()
#ax.scatter(y, predicted)
#ax.plot([y.min(), y.max()], [y.min(), y.max()], 'k--', lw=4)
#ax.set_xlabel('Measured')
#ax.set_ylabel('Predicted')
#plt.show()

