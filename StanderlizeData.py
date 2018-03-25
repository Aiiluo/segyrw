import numpy as np
from sklearn.preprocessing import StandardScaler


def Standerlize(in_file):
    # #############################################################################
    # Generate sample data
    in_data = np.loadtxt(in_file)
    X = in_data[:, 0:1]
    y = in_data[:, 1:2]
    # Stadardize X
    scx = StandardScaler()
    scx.fit(X)
    X_std = scx.transform(X)
    # Stadardize Y
    scy = StandardScaler()
    scx.fit(y)
    y_std = scx.transform(y)



