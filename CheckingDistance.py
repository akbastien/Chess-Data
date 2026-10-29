"""
Created on Wednesday 28 @7:26, 2026

@Author: Sao Nguyen
"""
from BoardtoDistance import board, make_vector, VtoD

def verify_pieces_entries(board_vector):
  
pieces_names = ["WKing", "WQ", "WR1", "WR2", "WB1", "WB2", "WKn1", "WKn2", "WP1", "WP2", "WP3", "WP4", "WP5", "WP6", "WP7", "WP8",
                "BKing", "BQ", "BR1", "BR2", "BB1", "BB2", "BKn1", "BKn2", "BP1", "BP2", "BP3", "BP4", "WP5", "WP6", "WP7", "WP8"]

print("Verifying Piece Entries")
for i, poos in enumerate(board_vector):
  if pos == [8,8]:
    print(f"Index {i:2} | {piece_names[i]:15} | [8,8] (Captured / Not on Board)")
  else:
    print(f"Index {i:2} | {piece_names[i]:15} | {pos}")

"""This here replace any non 1's with 0's"""
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
