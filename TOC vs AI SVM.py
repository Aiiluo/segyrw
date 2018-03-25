# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 13:58:18 2018

@author: proc1
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVR
from sklearn import metrics

# #############################################################################
# Generate sample data X=Acoustic impedance Y=TOC
well_data = np.loadtxt('all well.txt')
X = well_data[:, 0:1]
y = well_data[:, 1:2]

# #############################################################################
# Fit regression model
svr_rbf = SVR(kernel='rbf', C=1e2, gamma=1)
#svr_rbf = SVR(kernel='linear', C=1e2)
#svr_rbf = SVR(kernel='poly', C=1e3, degree=2)
func = svr_rbf.fit(X, y)
y_pred = func.predict(X)

# #############################################################################
# Look at the results
lw = 2
plt.figure(figsize=(10,7))
plt.scatter(X, y, color='darkorange', label='TOC')
plt.scatter(X, y_pred, marker=".", color='grey', lw=lw, label='TOC Prediction')
#plt.errorbar(X_train, y_train, yerr=y_train_err, fmt='.k')
plt.xlabel('Acoustic impedance')
plt.ylabel('TOC')
plt.title('Relationship between Acoustic impedance and TOC')
plt.legend()
plt.savefig("Relationship between Acoustic impedance and TOC", dpi=150)

plt.legend()
plt.show()

# #############################################################################
# Get function parameters
print(func.dual_coef_)

# #############################################################################
# Function Ecaluation,from sklearn get Root Mean Squared Error, RMSE
# 用scikit-learn计算MSE
print("MSE:", metrics.mean_squared_error(y, y_pred))
# 用scikit-learn计算RMSE
print("RMSE:", np.sqrt(metrics.mean_squared_error(y, y_pred)))