#CREATE DATASET TO USE IN FINAL MODEL


import math
from collections import deque
import numpy as np
import pandas as pd
import ast
import networkx as nx
from sklearn.model_selection import GroupShuffleSplit


#creates an ordered list of magnitudes of eigenvalues
def getEigenvalues(matrix):
    
    values1 = np.linalg.eigvals(matrix)
    values = []
    for num in values1:
        num1 = float(abs(num))
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


#APPEND DISTANCE MATRIX EIGENVALUES

def eig_features(vec):
    M = np.array(VtoD(vec))
    out = {}
    name = "Distance"
    out = {
        f"{name}Eigs":   getEigenvalues(M),
        f"{name}EigsWW": getEigenvalues(WWsubmatrix(M)),
        f"{name}EigsWB": getEigenvalues(WBsubmatrix(M)),
        f"{name}EigsBB": getEigenvalues(BBsubmatrix(M)),
        f"{name}EigsBW": getEigenvalues(BWsubmatrix(M)),
    }
    return pd.Series(out)   # so apply() expands into columns

#Eigenvalue summary data

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

#Make chess graph
def makeGraph (vec):
    i=0
    j=0
    D = np.array(VtoD(vec))
    A = np.array(DistancetoAdjacency(D))
    G = nx.DiGraph()
    G.add_nodes_from([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31])
    while i < 32:
        while j < 32:
            if A[i,j]!=0:
                G.add_edge(i,j)
                
            j = j + 1
            
        i = i + 1
        j = 0
    
    return G



##########################SET DIRECTORY#############################################################################
df = pd.read_csv(r"C:\Users\akbas\Desktop\MATH 495\Chess Analysis\Dataframes\ChessData.csv")



df["Board Vector"] = df["Board Vector"].apply(ast.literal_eval)

df = df.join(df["Board Vector"].apply(eig_features))

df["NumPieces"] = df["Board Vector"].apply(onBoard)

eig_cols = ["DistanceEigs", "DistanceEigsWW", "DistanceEigsWB",
            "DistanceEigsBB", "DistanceEigsBW"]
for col in eig_cols:
    stats = pd.DataFrame(
        df[col].apply(eigAnalysis).tolist(),
        index=df.index,
        columns=[f"{col}_zeros", f"{col}_minNonzero", f"{col}_max"],
    )
    df = pd.concat([df, stats], axis=1)
    df = df.drop(columns=col)


#APPEND CENTRALITY LIST

graphs = df["Board Vector"].apply(makeGraph)

centrality_dicts = graphs.apply(nx.degree_centrality)

centrality_df = pd.DataFrame(centrality_dicts.tolist(), index=df.index)
df = df.join(centrality_df)




###########################################SET DIRECTORY##########################################################

df.to_csv(r'C:\Users\akbas\Desktop\MATH 495\Chess Analysis\Dataframes\FinalModelDF.csv', index=False)






#DATA SPLITTING


gss = GroupShuffleSplit(n_splits=1, test_size=0.25, random_state=42)
train_idx, test_idx = next(gss.split(df, groups=df["Game No"]))

train_df = df.iloc[train_idx]
test_df = df.iloc[test_idx]

# sanity check: no game appears in both sets
assert set(train_df["Game No"]).isdisjoint(test_df["Game No"])


##################################SET DIRECTORY################################################################

train_df.to_csv(r"C:\Users\akbas\Desktop\MATH 495\Chess Analysis\Dataframes\FinalModelTrain.csv", index=False)
test_df.to_csv(r"C:\Users\akbas\Desktop\MATH 495\Chess Analysis\Dataframes\FinalModelTest.csv", index=False)

