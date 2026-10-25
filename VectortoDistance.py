import math
from collections import deque

#Function from Utkarsh Trivedi
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
#Code for Knight distance edited from Utkarsh Trivedi https://www.geeksforgeeks.org/dsa/minimum-steps-reach-target-knight/
  piecePosition2 = []
  pieceRow = []
  i = 0
  k = 0
  rel = 0
  
  while i < 32:
    pieceRow = []
    while k < 32:
      if piecePosition[k] == (8,8) or piecePosition[i] == (8,8):
        pieceRow.append(0)
      elif k == i:
        pieceRow.append(0)
      elif k != i:
        #King
        if i == 0:
          rel = abs((piecePosition[i][0] - piecePosition[k][0]))+abs((piecePosition[i][1] - piecePosition[k][1]))
          pieceRow.append(rel)
          rel = 0
        #Queen
        if i == 1:
          if piecePosition[i][0] == piecePosition[k][0] or piecePosition[i][1] == piecePosition[k][1]:
            rel = 1
          elif abs(piecePosition[i][0] - piecePosition[k][0]) == abs(piecePosition[i][1] - piecePosition[k][1]):
            rel = 1
          else:
            rel = 2
          pieceRow.append(rel)
          rel = 0
        #Rook1
        if i == 2:
          if piecePosition[i][0] == piecePosition[k][0] or piecePosition[i][1] == piecePosition[k][1]:
            rel = 1
          else:
            rel = 2
          pieceRow.append(rel)
          rel = 0
        #Rook2
        if i == 3:
          if piecePosition[i][0] == piecePosition[k][0] or piecePosition[i][1] == piecePosition[k][1]:
            rel = 1
          else:
            rel = 2
          pieceRow.append(rel)
          rel = 0
        #Bishop1
        if i == 4:
          if (math.remainder(piecePosition[i][0]+piecePosition[i][1],2)) != (math.remainder(piecePosition[k][0]+piecePosition[k][1],2)):
            rel = 0
          elif abs(piecePosition[i][0] - piecePosition[k][0]) == abs(piecePosition[i][1] - piecePosition[k][1]):
            rel = 1
          else:
            rel = 2
          pieceRow.append(rel)
          rel = 0
        #Bishop2
        if i == 5:
          if (math.remainder(piecePosition[i][0]+piecePosition[i][1],2)) != (math.remainder(piecePosition[k][0]+piecePosition[k][1],2)):
            rel = 0
          elif abs(piecePosition[i][0] - piecePosition[k][0]) == abs(piecePosition[i][1] - piecePosition[k][1]):
            rel = 1
          else:
            rel = 2
          pieceRow.append(rel)
          rel = 0
        #Knight1
        if i == 6:
          n = 8
          knightPos = (piecePosition[i][0] + 1, piecePosition[i][1] + 1)
          targetPos = (piecePosition[k][0] + 1, piecePosition[k][1] + 1)
          pieceRow.append(minStepToReachTarget(knightPos, targetPos, n))
        #Knight2
        if i == 7:
          n = 8
          knightPos = (piecePosition[i][0] + 1, piecePosition[i][1] + 1)
          targetPos = (piecePosition[k][0] + 1, piecePosition[k][1] + 1)
          pieceRow.append(minStepToReachTarget(knightPos, targetPos, n))
        #Pawn1
        if i == 8:
          if (piecePosition[i][0]-1) == piecePosition[k][0] or (piecePosition[i][0]+1) == piecePosition[k][0]:
            rel = abs(piecePosition[i][1] - piecePosition[k][1])
          else:
            rel = 0
          pieceRow.append(rel)
          rel = 0
        #Pawn2
        if i == 9:
          if (piecePosition[i][0]-1) == piecePosition[k][0] or (piecePosition[i][0]+1) == piecePosition[k][0]:
            rel = abs(piecePosition[i][1] - piecePosition[k][1])
          else:
            rel = 0
          pieceRow.append(rel)
          rel = 0
        #Pawn3
        if i == 10:
          if (piecePosition[i][0]-1) == piecePosition[k][0] or (piecePosition[i][0]+1) == piecePosition[k][0]:
            rel = abs(piecePosition[i][1] - piecePosition[k][1])
          else:
            rel = 0
          pieceRow.append(rel)
          rel = 0
        #Pawn4
        if i == 11:
          if (piecePosition[i][0]-1) == piecePosition[k][0] or (piecePosition[i][0]+1) == piecePosition[k][0]:
            rel = abs(piecePosition[i][1] - piecePosition[k][1])
          else:
            rel = 0
          pieceRow.append(rel)
          rel = 0
        #Pawn5
        if i == 12:
          if (piecePosition[i][0]-1) == piecePosition[k][0] or (piecePosition[i][0]+1) == piecePosition[k][0]:
            rel = abs(piecePosition[i][1] - piecePosition[k][1])
          else:
            rel = 0
          pieceRow.append(rel)
          rel = 0
        #Pawn6
        if i == 13:
          if (piecePosition[i][0]-1) == piecePosition[k][0] or (piecePosition[i][0]+1) == piecePosition[k][0]:
            rel = abs(piecePosition[i][1] - piecePosition[k][1])
          else:
            rel = 0
          pieceRow.append(rel)
          rel = 0
        #Pawn7
        if i == 14:
          if (piecePosition[i][0]-1) == piecePosition[k][0] or (piecePosition[i][0]+1) == piecePosition[k][0]:
            rel = abs(piecePosition[i][1] - piecePosition[k][1])
          else:
            rel = 0
          pieceRow.append(rel)
          rel = 0
        #Pawn8
        if i == 15:
          if (piecePosition[i][0]-1) == piecePosition[k][0] or (piecePosition[i][0]+1) == piecePosition[k][0]:
            rel = abs(piecePosition[i][1] - piecePosition[k][1])
          else:
            rel = 0
          pieceRow.append(rel)
          rel = 0
        #king
        if i == 16:
          rel = abs((piecePosition[i][0] - piecePosition[k][0]))+abs((piecePosition[i][1] - piecePosition[k][1]))
          pieceRow.append(rel)
          rel = 0
        #queen
        if i == 17:
          if piecePosition[i][0] == piecePosition[k][0] or piecePosition[i][1] == piecePosition[k][1]:
            rel = 1
          elif abs(piecePosition[i][0] - piecePosition[k][0]) == abs(piecePosition[i][1] - piecePosition[k][1]):
            rel = 1
          else:
            rel = 2
          pieceRow.append(rel)
          rel = 0
        #rook1
        if i == 18:
          if piecePosition[i][0] == piecePosition[k][0] or piecePosition[i][1] == piecePosition[k][1]:
            rel = 1
          else:
            rel = 2
          pieceRow.append(rel)
          rel = 0
        #rook2
        if i == 19:
          if piecePosition[i][0] == piecePosition[k][0] or piecePosition[i][1] == piecePosition[k][1]:
            rel = 1
          else:
            rel = 2
          pieceRow.append(rel)
          rel = 0
        #bishop1
        if i == 20:
          if (math.remainder(piecePosition[i][0]+piecePosition[i][1],2)) != (math.remainder(piecePosition[k][0]+piecePosition[k][1],2)):
            rel = 0
          elif abs(piecePosition[i][0] - piecePosition[k][0]) == abs(piecePosition[i][1] - piecePosition[k][1]):
            rel = 1
          else:
            rel = 2
          pieceRow.append(rel)
          rel = 0
        #bishop2
        if i == 21:
          if (math.remainder(piecePosition[i][0]+piecePosition[i][1],2)) != (math.remainder(piecePosition[k][0]+piecePosition[k][1],2)):
            rel = 0
          elif abs(piecePosition[i][0] - piecePosition[k][0]) == abs(piecePosition[i][1] - piecePosition[k][1]):
            rel = 1
          else:
            rel = 2
          pieceRow.append(rel)
          rel = 0
        #knight1
        if i == 22:
          n = 8
          knightPos = (piecePosition[i][0] + 1, piecePosition[i][1] + 1)
          targetPos = (piecePosition[k][0] + 1, piecePosition[k][1] + 1)
          pieceRow.append(minStepToReachTarget(knightPos, targetPos, n))
        #knight2
        if i == 23:
          n = 8
          knightPos = (piecePosition[i][0] + 1, piecePosition[i][1] + 1)
          targetPos = (piecePosition[k][0] + 1, piecePosition[k][1] + 1)
          pieceRow.append(minStepToReachTarget(knightPos, targetPos, n))
        #pawn1
        if i == 24:
          if (piecePosition[i][0]-1) == piecePosition[k][0] or (piecePosition[i][0]+1) == piecePosition[k][0]:
            rel = abs(piecePosition[i][1] - piecePosition[k][1])
          else:
            rel = 0
          pieceRow.append(rel)
          rel = 0
        #pawn2
        if i == 25:
          if (piecePosition[i][0]-1) == piecePosition[k][0] or (piecePosition[i][0]+1) == piecePosition[k][0]:
            rel = abs(piecePosition[i][1] - piecePosition[k][1])
          else:
            rel = 0
          pieceRow.append(rel)
          rel = 0
        #pawn3
        if i == 26:
          if (piecePosition[i][0]-1) == piecePosition[k][0] or (piecePosition[i][0]+1) == piecePosition[k][0]:
            rel = abs(piecePosition[i][1] - piecePosition[k][1])
          else:
            rel = 0
          pieceRow.append(rel)
          rel = 0
        #pawn4
        if i == 27:
          if (piecePosition[i][0]-1) == piecePosition[k][0] or (piecePosition[i][0]+1) == piecePosition[k][0]:
            rel = abs(piecePosition[i][1] - piecePosition[k][1])
          else:
            rel = 0
          pieceRow.append(rel)
          rel = 0
        #pawn5
        if i == 28:
          if (piecePosition[i][0]-1) == piecePosition[k][0] or (piecePosition[i][0]+1) == piecePosition[k][0]:
            rel = abs(piecePosition[i][1] - piecePosition[k][1])
          else:
            rel = 0
          pieceRow.append(rel)
          rel = 0
        #pawn6
        if i == 29:
          if (piecePosition[i][0]-1) == piecePosition[k][0] or (piecePosition[i][0]+1) == piecePosition[k][0]:
            rel = abs(piecePosition[i][1] - piecePosition[k][1])
          else:
            rel = 0
          pieceRow.append(rel)
          rel = 0
        #pawn7
        if i == 30:
          if (piecePosition[i][0]-1) == piecePosition[k][0] or (piecePosition[i][0]+1) == piecePosition[k][0]:
            rel = abs(piecePosition[i][1] - piecePosition[k][1])
          else:
            rel = 0
          pieceRow.append(rel)
          rel = 0
        #pawn8
        if i == 31:
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

VtoD(pieces)
