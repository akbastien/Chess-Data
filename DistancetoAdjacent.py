"""
Created on Thursday 29, @1:00, 2026

@Author: Sao Nguyen
"""
import chess
import math
from collections import deque

#This is setting up for board setup adn vector creation
board = chess.board("r1bqkb1r/pppp1Qpp/2n2n2/4p3/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 0 4")

def make_vector(board):
  searchVector = ["K", "Q", "R", "R", "B", "B", "N", "N", "P", "P", "P", "P", "P", "P", "P", "P", 
                  "k", "q", "r", "r", "b", "b", "n", "n", "p", "p", "p", "p", "p", "p", "p", "p"]
  boardVector = []
  grid = []

for row in board.board_fen().split("/"):
  cells = []
  for ch in row:
    if ch.isdigit():
      cells.extend(["x"] * int(ch))
    else:
      cells.append(ch)
  grid.append(cells)

for piece in searchVector:
  pos [8,8]
  for i, row in enumerate(grid):
    if piece in row:
      j = row.idex(piece)
      grid[i][j] = "x"
      pos = [j, 7-i]
      break
  boardVector.append(pos)

return boardVector

def minStepToReachTarget(knightPos, targetPos, n):
  x, y = knightPos[0], knightPos[1]
  tx, ty = targetPos[0], targetPos[1]
  dx = [2,2,-2,-2,1,1,-1,-1]
  dy = [1,-1,1,-1,2,-2,2,-2]
  
  q = deque()
  visited = [[False] * n for _ in range(n)]
  q.append((x,y,0)
  visited[x][y] = True

while q:
  x, y, steps = q.popleft()
  if x == tx and y == ty:
    return steps
    for i in range(8):
      nx = x + dx[i]
      ny = y + dy[i]
      if (nx >= 0 and nx < n and ny >= 0 and ny < n and not visited[nx][ny]):
        visited[nx][ny] = True
        q.append((nx, ny, steps + 1))
        
return -1

def VtoD(piecePosition):
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
      if i in [0,16]:
        rel = max(abs((piecePosition[i][0] - piecePosition[k][0])), abs((piecePosition[i][1] - piecePosition[i][1])))
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
      # Rooks
      if i in [2, 3, 18, 19]:
        if piecePosition[i][0] == piecePosition[k][0] or piecePosition[i][1] == piecePosition[k][1]:
          rel = 1
        else:
          rel = 2
        pieceRow.append(rel)
        rel = 0
      # Bishops
      if i in [4, 5, 20, 21]:
        if (math.remainder(piecePosition[i][0]+piecePosition[i][1],2)) != (math.remainder(piecePosition[k][0]+piecePosition[k][1],2)):
          rel = 0
        elif abs(piecePosition[i][0] - piecePosition[k][0]) == abs(piecePosition[i][1] - piecePosition[k][1]):
          rel = 1
        else:
          rel = 2
        pieceRow.append(rel)
        rel = 0
      # Knights
      if i in [6, 7, 22, 23]:
        n = 8
        knightPos = (piecePosition[i][0], piecePosition[i][1])
        targetPos = (piecePosition[k][0], piecePosition[k][1])
        pieceRow.append(minStepToReachTarget(knightPos, targetPos, n))
      # Pawns
      if i in [8, 9, 10, 11, 12, 13, 14, 15, 24, 25, 26, 27, 28, 29, 30, 31]:
        if i in [8, 9, 10, 11, 12, 13, 14, 15] and (piecePosition[i][1] <= piecePosition[k][1]):
          rel = 0
        elif i in [24, 25, 26, 27, 28, 29, 30, 31] and (piecePosition[i][1] >= piecePosition[k][1]):
          rel = 0
          if (piecePosition[i][0]-1) == piecePosition[k][0] or (piecePosition[i][0]+1) == piecePosition[k][0]:
            rel = abs(piecePosition[i][1] - piecePosition[k][1])
          else:
            rel = 0
         pieceRow.append(rel)
         rel = 0
        
   k = k + 1
  
i += 1
k = 0
piecePosition2.append(pieceRow)

return piecePosition2

def VtoA(piecePosition):
  distance_matrix = VtoD(piecePosition)
  adjacency_matrix = []

for row in distance_matrix: #Keep 1 if the distance is 1, otherwise place with 0
  new_row = [1 if val == 1 else 0 for val in row]
  adjacency_matrix.append(new_row)

return adjacency_matrix

if name == "main":
  board_vec = make_vector(board) #Get the board vector
  adj_matrix = VtoA(board_vec) #Generate adjacency matrix
  print(" Adjacency Matrix ")
for i, row in enumerate(adj_matrix):
  print(f"Row {i:2}: {row}")
