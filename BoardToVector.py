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



