import sys
from pathlib import Path

# Lisää projektin juuri Pythonin polulle
project_root = str(Path(__file__).resolve().parents[1])
if project_root not in sys.path:
    sys.path.append(project_root)




import random
import time
from src.chess_board import ChessBoard
from src.utils import *
from src.attack_tables import get_attack_tables

from src.precomputation import *








def set_board(board: ChessBoard, board_position:str):
    print(f"Set board to {board_position}!")
    board.set_fen(board_position)

def make_move(board: ChessBoard):
    legal_moves = [get_uci(move) for move in list(board.legal_moves)]
    print(f"I found {len(legal_moves)} legal moves: {', '.join(legal_moves)}")
    
    choice = random.choice(legal_moves)
    board.execute_uci(choice)
    

    return choice


    




# TODO: King get_attack_board location_square is None DEBUG NEEDED





def main():

    board = ChessBoard()

    
    

    

    while True:
        opponent_move = input()
        time.sleep(random.randrange(1,10)/100)
        if opponent_move.startswith("BOARD:"):
            board.reset()
            #set_board(board, opponent_move.removeprefix("BOARD:"))
        elif opponent_move.startswith("RESET:"):
            board.reset()
            print("Board reset!")
        elif opponent_move.startswith("PLAY:"):
            choice = make_move(board)
            # example about logs
            print(f"I chose {choice}!")
            # example about posting a move
            print(f"MOVE:{choice}")
            
        elif opponent_move.startswith("MOVE:"):
            move = opponent_move.removeprefix("MOVE:")
            board.execute_uci(move)
            print(f"Received move: {move}")
        else:
            print(f"Unknown tag: {opponent_move}")
            break

if __name__ == "__main__":
    main()
