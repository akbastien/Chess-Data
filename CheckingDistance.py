"""
Created on Wednesday 28 @7:26, 2026

@Author: Sao Nguyen
"""
from BoardtoDistance import board, make_vector, VtoD

def verify_pieces_entries(board_vector):
  
piece_names = ["K", "Q", "R1", "R2", "B1", "B2", "Kn1", "Kn2", "P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8",
                "k", "q", "r1", "r2", "b1", "b2", "kn1", "kn2", "p1", "p2", "p3", "p4", "p5", "p6", "p7", "p8"]

print("Verifying Piece Entries")
for i, pos in enumerate(board_vector):
  if pos == [8, 8]:
    print(f"Index {i:2} | {piece_names[i]:15} | [8,8] (Captured / Not on Board)")
  else:
    print(f"Index {i:2} | {piece_names[i]:15} | {pos}")

#This here replace any non 1's with 0's
def binarize_matrix(matrix):
  binared = []
  for row in matrix:
    new_row  = [1 if val == 1 else 0 for val in row]
    binarized.append(new_row)
  return binarized

if name == "main":
  board_vec = make_vector(board) #Get the board vector
  verify_pieces_entries(board_vec) #This verify piece entries so double checking 1
  distance_matix = VtoD(board_vec) #Generate the distance matrix
  binary_matrix = binarize_matrix(distance_matrix) #Binarize the matrix so double checking 2
  print("\n Binarized Distance Matrix (1's and 0's)")
  for row in binary_matrix:
    print(row)
