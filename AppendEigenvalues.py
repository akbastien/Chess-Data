# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 12:05:45 2026

@author: akbas
"""

import math
from collections import deque
import numpy as np
import pandas as pd
import ast


#creates an ordered list of magnitudes of eigenvalues
def getEigenvalues(matrix):
    values1 = np.linalg.eigvals(matrix)
    values = []
    for num in values1:
        num1 = abs(num)
        values.append(num1)
    values.sort()
    
    return values


def minStepToReachTarget(knightPos, targetPos, n):

    # Convert 1-based indexing to 0-based indexing
    x = knightPos[0] - 1
    y = knightPos[1] - 1
    tx = targetPos[0] - 1
    ty = targetPos[1] - 1

    # All 8 possible Knight moves
    dx = [2, 2, -2, -2, 1, 1, -1, -1]
    dy = [1, -1, 1, -1, 2, -2, 2, -2]

    # Queue stores position and number of steps
    q = deque()

    # Mark visited cells
    visited = [[False] * n for _ in range(n)]

    # Start BFS from the initial position
    q.append((x, y, 0))
    visited[x][y] = True

    while q:
        x, y, steps = q.popleft()

        # If target is reached
        if x == tx and y == ty:
            return steps

        # Try all 8 possible Knight moves
        for i in range(8):
            nx = x + dx[i]
            ny = y + dy[i]

            # Check if the new position is valid and unvisited
            if (nx >= 0 and nx < n and ny >= 0 and ny < n
                    and not visited[nx][ny]):

                visited[nx][ny] = True

                # Add the new position with updated steps
                q.append((nx, ny, steps + 1))

    return -1

def VtoD(piecePosition):
#Code for Knight distance edited from Utkarsh Trivedi
  piecePosition2 = []
  pieceRow = []
  i = 0
  k = 0
  rel = 0
  
  while i < 32:
    pieceRow = []
    while k < 32:
      if piecePosition[k] == [8,8] or piecePosition[i] == [8,8]:
        pieceRow.append(0)
      elif k == i:
        pieceRow.append(0)
      elif k != i:
        #Kings
        if i in [0, 16]:
          rel = max(abs((piecePosition[i][0] - piecePosition[k][0])),abs((piecePosition[i][1] - piecePosition[k][1])))
          pieceRow.append(rel)
          rel = 0
        #Queens
        if i in [1, 17]:
          if piecePosition[i][0] == piecePosition[k][0] or piecePosition[i][1] == piecePosition[k][1]:
            rel = 1
          elif abs(piecePosition[i][0] - piecePosition[k][0]) == abs(piecePosition[i][1] - piecePosition[k][1]):
            rel = 1
          else:
            rel = 2
          pieceRow.append(rel)
          rel = 0
        #Rooks
        if i in [2, 3, 18, 19]:
          if piecePosition[i][0] == piecePosition[k][0] or piecePosition[i][1] == piecePosition[k][1]:
            rel = 1
          else:
            rel = 2
          pieceRow.append(rel)
          rel = 0
        #Bishops
        if i in [4, 5, 20, 21]:
          if ((piecePosition[i][0]+piecePosition[i][1])%2 != (piecePosition[k][0]+piecePosition[k][1])%2):
            rel = 0
          elif abs(piecePosition[i][0] - piecePosition[k][0]) == abs(piecePosition[i][1] - piecePosition[k][1]):
            rel = 1
          else:
            rel = 2
          pieceRow.append(rel)
          rel = 0
        #Knight1
        if i in [6, 7, 22, 23]:
          n = 8
          knightPos = (piecePosition[i][0] + 1, piecePosition[i][1] + 1)
          targetPos = (piecePosition[k][0] + 1, piecePosition[k][1] + 1)
          pieceRow.append(minStepToReachTarget(knightPos, targetPos, n))
        #White Pawns
        if i in [8, 9, 10, 11, 12, 13, 14, 15]:
          if (piecePosition[i][1] > piecePosition[k][1])  :
              rel = 0
          elif (piecePosition[i][0]-1) == piecePosition[k][0] or (piecePosition[i][0]+1) == piecePosition[k][0]:
            rel = abs(piecePosition[i][1] - piecePosition[k][1])
          else:
            rel = 0
          pieceRow.append(rel)
          rel = 0
        #Black Pawns
        if i in [24, 25, 26, 27, 28, 29, 30, 31]:
            if (piecePosition[i][1] < piecePosition[k][1])  :
                rel = 0
            elif (piecePosition[i][0]-1) == piecePosition[k][0] or (piecePosition[i][0]+1) == piecePosition[k][0]:
              rel = abs(piecePosition[i][1] - piecePosition[k][1])
            else:
              rel = 0
            pieceRow.append(rel)
            rel = 0
            
            
      k = k + 1
  
    i += 1
    k= 0
    piecePosition2.append(pieceRow)

  return piecePosition2


# ADJACENCY MATRIX GENERATION
def DistancetoAdjacency(distance_matrix):
    adjacency_matrix = []
    
    for row in distance_matrix:
        new_row = [1 if val == 1 else 0 for val in row]
        adjacency_matrix.append(new_row)
        
    return adjacency_matrix

#LAPLACIAN MATRIX GENERATION
def AdjacencyToLaplacian(adjacency_matrix):
    
    #This converts an Adjacency Matrix into a Laplacian Matrix using L = D - A.
    size = len(adjacency_matrix)
    
    # Initialize Degree Matrix (D) with 0s
    degree_matrix = [[0 for _ in range(size)] for _ in range(size)]
    
    # Calculate the degree (row sum) for each node and place it on the diagonal
    for i in range(size):
        degree = sum(adjacency_matrix[i])
        degree_matrix[i][i] = degree
        
    # Initialize Laplacian Matrix (L)
    laplacian_matrix = [[0 for _ in range(size)] for _ in range(size)]
    
    # Calculate L = D - A
    for i in range(size):
        for j in range(size):
            laplacian_matrix[i][j] = degree_matrix[i][j] - adjacency_matrix[i][j]
            
    return laplacian_matrix

#white to white submatrix [0-15]x[0-15]
def WWsubmatrix(matrix):
    rows = list(range(0,16))
    cols = list(range(0,16))
    index_constructor = np.ix_(rows, cols)
    submatrix = matrix[index_constructor]
    
    return submatrix
    
#white to black submatrix [0-15]x[16-31]
def WBsubmatrix(matrix):
    rows = list(range(0,16))
    cols = list(range(16,32))
    index_constructor = np.ix_(rows, cols)
    submatrix = matrix[index_constructor]
    
    return submatrix
    
#black to black submatrix [16-31]x[16-31]
def BBsubmatrix(matrix):
    rows = list(range(16,32))
    cols = list(range(16,32))
    index_constructor = np.ix_(rows, cols)
    submatrix = matrix[index_constructor]
    
    return submatrix
    
#black to white submatrix [16-31]x[0-15]
def BWsubmatrix(matrix):
    rows = list(range(16,32))
    cols = list(range(0,16))
    index_constructor = np.ix_(rows, cols)
    submatrix = matrix[index_constructor]
    
    return submatrix



df = pd.read_csv(r"C:\Users\akbas\Desktop\MATH 495\Chess Analysis\ChessData.csv")

df["Board Vector"] = df["Board Vector"].apply(ast.literal_eval)

def eig_features(vec):
    D = np.array(VtoD(vec))
    A = np.array(DistancetoAdjacency(D))
    L = np.array(AdjacencyToLaplacian(A))
    out = {}
    for name, M in [("Distance", D), ("Adjacency", A), ("Laplacian", L)]:
        out[f"{name}Eigs"]   = getEigenvalues(M)
        out[f"{name}EigsWW"] = getEigenvalues(WWsubmatrix(M))
        out[f"{name}EigsWB"] = getEigenvalues(WBsubmatrix(M))
        out[f"{name}EigsBB"] = getEigenvalues(BBsubmatrix(M))
        out[f"{name}EigsBW"] = getEigenvalues(BWsubmatrix(M))
    return pd.Series(out)


df = df.join(df["Board Vector"].apply(eig_features))


df.to_csv(r'C:\Users\akbas\Desktop\MATH 495\Chess Analysis\EigenvalueDF.csv', index=False)    