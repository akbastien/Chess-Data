# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 12:09:53 2026

@author: akbas
"""


#input ordered eigenvalue list, output number of zeros, smallest nonzero, largest eigenvalue
def eigAnalysis(eigs, tol=1e-10):
    
    n = len(eigs)
    
    
    zeros = 0
    for i in range(n):
        if abs(eigs[i]) < tol:
            zeros += 1
    
    minNonzero = None
    for e in eigs:
        if abs(e) >= tol:
            minNonzero = e
            break
    
    maxEig = eigs[n-1]
    
    return [zeros, minNonzero, maxEig]


#input position vector, output number of pieces on board
def onBoard(positions):
    
    n = len(positions)
    
    offBoard = 0
    for p in positions:
        if p == [8,8]:
           offBoard += 1
           
    return n-offBoard

