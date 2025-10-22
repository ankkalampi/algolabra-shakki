from src.utils import *
from src.globals import *


from src.attack_tables import get_attack_tables



def get_attack_board(location_board, all_pieces):
    """
    Get bitboard for all knight attacks for a specific color

    Args:
    location_board: bitboard of all knights of a specific color
    all_pieces: bitboard of all pieces in game situation

    Returns:
    bitboard: 64-bit bitboard 
    """

    attack_board = EMPTY_BOARD

    attack_tables = get_attack_tables()

    while(location_board):
        location_square = bitscan(location_board)
        location_board &= location_board -1

        
        attack_board |= attack_tables.knight_attack_tables[location_square]
        

    return attack_board

def get_moves(location_board, all_pieces):
    """
    Get all moves for knight for a specific color

    Args:
    location_board: bitboard of all knights of a specific color
    all_pieces: bitboard of all pieces in game situation

    Returns:
    moves: a list of moves in 18-bit format
    """
    moves = []

    attack_tables = get_attack_tables()


    while(location_board):
        location_square = bitscan(location_board)
        location_board &= location_board -1

        
        return_board = EMPTY_BOARD
        return_board |= attack_tables.knight_attack_tables[location_square]
        
        
        while(return_board):
            move_square = bitscan(return_board)
            return_board &= return_board -1

            moves.append(generate_move(location_square, move_square, 0b010))

    return moves
    