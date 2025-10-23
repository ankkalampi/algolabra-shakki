from src.utils import *
from src.globals import *

from src.attack_tables import get_attack_tables
import src.bishop as bishop
import src.rook as rook


def get_attack_board(location_board, all_pieces):
    """
    Get bitboard for all queen attacks for a specific color

    Args:
    location_board: bitboard of all queens of a specific color
    all_pieces: bitboard of all pieces in game situation

    Returns:
    bitboard: 64-bit bitboard 
    """
    
    attack_board = EMPTY_BOARD

    attack_tables = get_attack_tables()

    while(location_board):
        location_square = bitscan(location_board)
        location_board &= location_board -1

        block_value = bishop.get_block_value(location_square, all_pieces)
        attack_board |= attack_tables.bishop_blocking_attack_tables[location_square][block_value]

        block_value = rook.get_block_value(location_square, all_pieces)
        attack_board |= attack_tables.rook_blocking_attack_tables[location_square][block_value]

    return attack_board

def get_moves(location_board, all_pieces):
    """
    Get all moves for queens for a specific color

    Args:
    location_board: bitboard of all queens of a specific color
    all_pieces: bitboard of all pieces in game situation

    Returns:
    moves: a list of moves in 18-bit format
    """
    moves = []


    while(location_board):
        location_square = bitscan(location_board)
        location_board &= location_board -1

        
        location_square_bitboard = get_bitboard_of_square(location_square)
        
        
        return_board = EMPTY_BOARD
        return_board |= get_attack_board(location_square_bitboard, all_pieces)
        
        
        while(return_board):
            move_square = bitscan(return_board)
            return_board &= return_board -1

            moves.append(generate_move(location_square, move_square, 0b101))

    return moves
