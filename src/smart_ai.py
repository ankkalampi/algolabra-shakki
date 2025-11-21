import sys
from pathlib import Path

import math

project_root = str(Path(__file__).resolve().parents[1])
if project_root not in sys.path:
    sys.path.append(project_root)






import random
import time
from src.chess_board import ChessBoard
from src.utils import *
from src.attack_tables import get_attack_tables

from src.precomputation import *
from src.heuristic import get_highest_value_move, evaluate_move, get_lowest_value_move
from src.minmax import minmax
import src.timing


DEPTH = 3









def set_board(board: ChessBoard, board_position:str):
    print(f"Set board to {board_position}!")
    #board.set_fen(board_position)

def make_move(board: ChessBoard):
    start = time.perf_counter()
    #print(f"NUMBER OF LEGAL MOVES: {len(board.get_legal_moves())}")
    legal_moves = [get_uci(move) for move in list(board.get_legal_moves())]
    #print(f"I found {len(legal_moves)} legal moves for AI: {', '.join(legal_moves)}")
    
    if len(legal_moves) != 0:
        minmax_start = time.perf_counter()
        best_score, best_move = minmax(board.situation, DEPTH, -math.inf, math.inf, False)
        minmax_end = time.perf_counter()
        minmax_time = minmax_end - minmax_start
        uci = get_uci(best_move)
        board.execute_uci(uci)

        end = time.perf_counter()
        turn_time = end - start
        minmax_percentage = minmax_time / turn_time * 100
        sorting_percentage = src.timing.SORTING_TIME / turn_time * 100
        situation_generation_percentage = src.timing.SITUATION_GENERATION_TIME / turn_time * 100

       
        src.timing.SORTING_TIME = 0.0
        src.timing.SITUATION_GENERATION_TIME = 0.0



        print(f"TURN TIME: {turn_time}")
        print(f"IN MINMAX: {minmax_percentage}%")
        print(f"IN SORT: {sorting_percentage}%")
        print(f"IN SITUATION_GENERATION: {situation_generation_percentage}%")
        return uci
    

    return None


    




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
            #print(f"NUMBER OF LEGAL MOVES: {len(board.get_legal_moves())}")
            legal_moves = [get_uci(move) for move in list(board.get_legal_moves())]
            #print(f"I found {len(legal_moves)} legal moves for Player: {', '.join(legal_moves)}")
            if not choice:
                print("RESET:")
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
