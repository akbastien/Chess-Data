# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 12:03:44 2026

@author: akbas
"""

import chess
import chess.pgn
import pandas as pd
import os


#Turns FEN board into vector
def toVector(board):
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


#Turns PGN game into FEN
def PGNtoFEN(game, n):
    # Go through each move in the game until
    # we reach the required move number
    board = chess.Board()
    
    for number, move in enumerate(game.mainline_moves()):
    
        # It copies the move played by each 
        # player on the virtual board
        board.push(move)
    
        # Remember that number starts from 0
        if number == n:  
            break

        fen = board.fen()
    
    return fen

def outcome(game):
    result = game.headers["Result"]
    
    if result == "1-0":
        return 1
    elif result == "0-1":
        return 0
    else:
        return 0.5



#Reads in games and creates dataset
def DataToDataset(directory): #make sure to put an r before listing the directory
    
    gameNumber = 0
    data = []
    gameNumber = 0
    for file in os.scandir(directory):
        if file.is_file():
            with open(file.path, "r") as f:
                
                gameNumber+= 1
                
                pgn = open(f)  # opening the file in python
                game = chess.pgn.read_game(pgn)  # reading the game present in file
                ply = 0  #total half moves (up to current point)
                totalPlies = sum(1 for _ in game.mainline_moves()) #total half moves in game
                winner = outcome(game)
                
                
                for move in game.mainline_moves():
                    ply += 1
                    board = PGNtoFEN(game, ply)
                    vector = toVector(board)
                    
                    results = dict([("Game No", gameNumber), ("Position No", ply), ("Total Positions", totalPlies) ("Board Vector", vector), ("Winner", winner)])
                    #records Game number (so we can keep track of which board is from which game),
                    # position, total positions, the board position vector, and the winner
                    data.append(results)
                    
                    
    
    df = pd.DataFrame(data)
    
    
    return df




chessData = DataToDataset("Placeholder Directory Here")

chessData.to_csv('/path/to/your/directory/your_file_name.csv', index=False)
                    
                    
