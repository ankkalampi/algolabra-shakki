from utils import *
from globals import *

from attack_tables import get_attack_tables
import bishop
import rook


def get_attack_board(location_board, all_pieces):
    
    attack_board = EMPTY_BOARD

    attack_tables = get_attack_tables()

    while(location_board):
        location_square = bitscan(location_board)
        location_board &= location_board -1

        block_value = bishop.get_block_value(location_square, all_pieces)
        attack_board |= attack_tables.bishop_blocking_attack_tables[block_value]

        block_value = rook.get_block_value(location_square, all_pieces)
        attack_board |= attack_tables.rook_blocking_attack_tables[block_value]

    return attack_board

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
