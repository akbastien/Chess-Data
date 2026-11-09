# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 12:09:08 2026

@author: akbas
"""

import pandas as pd
import ast

df = pd.read_csv(r"C:\Users\akbas\Desktop\MATH 495\Chess Analysis\Dataframes\TrainData.csv")
df = df.drop(['DistanceEigs', 'DistanceEigsWW', 'DistanceEigsWB', 'DistanceEigsBB', 'DistanceEigsBW',
              'AdjacencyEigs', 'AdjacencyEigsWW', 'AdjacencyEigsWB', 'AdjacencyEigsBB', 'AdjacencyEigsBW' ], axis=1)


eig_cols = ["LaplacianEigs", "LaplacianEigsWW", "LaplacianEigsWB",
            "LaplacianEigsBB", "LaplacianEigsBW"]

# Parse the string columns into real lists
for col in ["Board Vector"] + eig_cols:
    df[col] = df[col].apply(ast.literal_eval)



####FUNCTIONS

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






df["NumPieces"] = df["Board Vector"].apply(onBoard)


for col in eig_cols:
    stats = pd.DataFrame(
        df[col].apply(eigAnalysis).tolist(),
        index=df.index,
        columns=[f"{col}_zeros", f"{col}_minNonzero", f"{col}_max"],
    )
    df = pd.concat([df, stats], axis=1)
    

for col in eig_cols:
    expanded = pd.DataFrame(df[col].tolist(), index=df.index)
    expanded.columns = [f"{col}_{i}" for i in expanded.columns]
    
    df = pd.concat([df.drop(columns=col), expanded], axis=1)



df.to_csv(r"C:\Users\akbas\Desktop\MATH 495\Chess Analysis\Dataframes\LaplacianData.csv", index=False)
