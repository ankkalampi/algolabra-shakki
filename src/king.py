from src.utils import *
from src.globals import *

from src.attack_tables import get_attack_tables


def get_attack_board(location_board, all_pieces):
    """
    Get bitboard for all king attacks for a specific color

    Args:
    location_board: bitboard of the king of a specific color
    all_pieces: bitboard of all pieces in game situation

    Returns:
    bitboard: 64-bit bitboard 
    """
    attack_tables = get_attack_tables()
    location_square = bitscan(location_board)

    
    return attack_tables.king_attack_tables[location_square]

def get_moves(location_board, all_pieces):
    """
    Get all moves for the king for a specific color

    Args:
    location_board: bitboard of the king of a specific color
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
        return_board |= (get_attack_board(location_square_bitboard, all_pieces))
        
        
        while(return_board):
            move_square = bitscan(return_board)
            return_board &= return_board -1

            moves.append(generate_move(location_square, move_square, 0b110))

    return moves

