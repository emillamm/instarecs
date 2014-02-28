#!/usr/bin/env python

import numpy as np
from sklearn.neighbors import KDTree

X = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]])
kdt = KDTree(X, leaf_size=30, metric='euclidean')
result = kdt.query(X, k=2, return_distance=False) 

print result


