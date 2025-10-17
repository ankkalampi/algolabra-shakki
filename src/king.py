from utils import *
from globals import *

from attack_tables import get_attack_tables


def get_attack_board(location_board, all_pieces):
    attack_tables = get_attack_tables()
    return attack_tables.king_attack_tables[location_board]

def get_moves(location_board, all_pieces):
    moves = []


    while(location_board):
        location_square = bitscan(location_board)
        location_board &= location_board -1

        
        return_board = EMPTY_BOARD
        return_board |= (get_attack_board(location_board, all_pieces))
        
        
        while(return_board):
            move_square = bitscan(return_board)
            return_board &= return_board -1

            moves.append(generate_uci(location_square, move_square, 0b011))

    return moves

