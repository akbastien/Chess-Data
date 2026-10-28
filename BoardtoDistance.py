# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 10:37:29 2026

@author: akbas
"""
import chess

board = chess.Board("r1bqkb1r/pppp1Qpp/2n2n2/4p3/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 0 4")

def make_vector(board): #type(board) == chess.Board()
    searchVector = ["K", "Q", "R", "R", "B", "B", "N", "N", "P", "P", "P", "P", "P", "P", "P", "P", 
                    "k", "q", "r", "r", "b", "b", "n", "n", "p", "p", "p", "p", "p", "p", "p", "p"];
    boardVector = []  #Final board
    grid = []
    
    #Board Matrix
    for row in board.board_fen().split("/"):
        cells = []
        for ch in row:
            if ch.isdigit():
                cells.extend(["x"] * int(ch))
            else:
                cells.append(ch)
        grid.append(cells)

    #Board Vector
    for piece in searchVector:
        pos = [8, 8]                      # default: piece not on board
        for i, row in enumerate(grid):
            if piece in row:
                j = row.index(piece)
                grid[i][j] = "x"          # mark as used (lists are mutable)
                pos = [j, 7-i]          # [rank, file], 0-indexed
                break
        boardVector.append(pos)

    return boardVector


print(make_vector(board))


"""
Created on Sun Oct 25 4:23 2026

@author: Finch Gerwe
"""
import math
from collections import deque

#Function written by Utkarsh Trivedi https://www.geeksforgeeks.org/dsa/minimum-steps-reach-target-knight/
def minStepToReachTarget(knightPos, targetPos, n):

    # Convert 1-based indexing to 0-based indexing
    x = knightPos[0]
    y = knightPos[1]
    tx = targetPos[0]
    ty = targetPos[1]

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
          if (math.remainder(piecePosition[i][0]+piecePosition[i][1],2)) != (math.remainder(piecePosition[k][0]+piecePosition[k][1],2)):
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
          knightPos = (piecePosition[i][0], piecePosition[i][1])
          targetPos = (piecePosition[k][0], piecePosition[k][1])
          pieceRow.append(minStepToReachTarget(knightPos, targetPos, n))
        #Pawns
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
    k= 0
    piecePosition2.append(pieceRow)

  print(piecePosition2)
  return piecePosition2

#pieces = ["K","Q","R","R","B","B","N","N","P","P","P","P","P","P","P","P","k","q","r","r","b","b","n","n","p","p","p","p","p","p","p","p"]

pieces = [(4,0),(3,0),(0,0),(7,0),(2,0),(5,0),(1,0),(6,0),(0,1),(1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(7,1),(4,7),(3,7),(0,7),(7,7),(2,7),(5,7),(1,7),(6,7),(0,6),(1,6),(2,6),(3,6),(4,6),(5,6),(6,6),(7,6)]

VtoD(make_vector(board))
