#!/usr/bin/env python
import numpy
from lshash import LSHash
lsh = LSHash(6, 8)

dimension = 8

for index in range(300):
    v = numpy.random.randn(dimension)
    lsh.index(v)
v = numpy.random.randn(dimension)
result = lsh.query(v, num_results=10)
print result

