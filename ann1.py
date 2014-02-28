#!/usr/bin/env python

from nearpy import Engine
from nearpy.hashes import RandomBinaryProjections
from nearpy.filters import NearestFilter, UniqueFilter, DistanceThresholdFilter
import numpy

# Dimension of our vector space
dimension = 2

# Create a random binary hash with 10 bits
rbp1 = RandomBinaryProjections('rbp1', 10)
rbp2 = RandomBinaryProjections('rbp2', 10)
rbp3 = RandomBinaryProjections('rbp3', 10)
rbp4 = RandomBinaryProjections('rbp4', 10)
rbp5 = RandomBinaryProjections('rbp5', 10)

# We are looking for the ten closest neighbours
nearest = NearestFilter(20)
# We want unique candidates
unique = UniqueFilter()
dist = DistanceThresholdFilter(10)

# Create engine with pipeline configuration
engine = Engine(dimension, lshashes=[rbp1, rbp2, rbp3, rbp4, rbp5], vector_filters = [unique, nearest, dist])

# Index 1000000 random vectors (set their data to a unique string)
for index in range(300):
    v = numpy.random.randn(dimension)
    engine.store_vector(v, 'data_%d' % index)

# Create random query vector
query = numpy.random.randn(dimension)

# Get nearest neighbours
N = engine.neighbours(query)
print N
