from src.utils import *
from src.globals import *

from src.attack_tables import get_attack_tables

white_pawn_double_mask = 0xFF << 8
black_pawn_double_mask = 0xFF >> 48
white_pawn_single_mask = 0xFF ^ 0xFFFFFFFFFFFFFFFF
black_pawn_single_mask = (0xFF >> 56) ^ 0xFFFFFFFFFFFFFFFF
white_pawn_nonpromotion_mask    = (0xFF >> 48) ^ 0xFFFFFFFFFFFFFFFF
black_pawn_nonpromotion_mask   = (0xFF << 8) ^ 0xFFFFFFFFFFFFFFFF
white_pawn_promotion_mask = black_pawn_double_mask
black_pawn_promotion_mask = white_pawn_double_mask



def get_double_move_board(location_board, all_pieces, is_white):
    """
    Compute and return an attack board (bitboard)
    for all single color pawn double moves

    Args:
    location_board: bitboard of all pawns of one color
    all_pieces: bitboard of all pieces in game situation
    is_white: True if it's white's turn

    Returns:
    bitboard: 64-bit bitboard representation of all single color double pawn moves
    """
    attack_board = EMPTY_BOARD
    
    
    if is_white:
        unmoved_pawns = location_board & WHITE_PAWNS_START
        
    else:
        unmoved_pawns = location_board & BLACK_PAWNS_START
        

    if is_white:
        single_move_blocked_bits = ((unmoved_pawns << 8) & -all_pieces) >> 8
        double_move_blocked_bits = ((unmoved_pawns << 16) & -all_pieces) >> 16

        attack_board |= (single_move_blocked_bits & double_move_blocked_bits) << 16
        
    else:
        single_move_blocked_bits = ((unmoved_pawns >> 8) & -all_pieces) << 8
        double_move_blocked_bits = ((unmoved_pawns >> 16) & -all_pieces) << 16

        attack_board |= (single_move_blocked_bits & double_move_blocked_bits) >> 16
        

    return attack_board

def get_single_move_board(location_board, all_pieces, is_white):
    """
    Compute and return an attack board (bitboard)
    for all single color pawn single moves

    Args:
    location_board: bitboard of all pawns of one color
    all_pieces: bitboard of all pieces in game situation
    is_white: True if it's white's turn

    Returns:
    bitboard: 64-bit bitboard representation of all single color single pawn moves
    """
    attack_board = EMPTY_BOARD
    unblocked_pawns = EMPTY_BOARD
    
    if is_white:
        unblocked_pawns |= ((location_board  << 8) & -all_pieces) >> 8
    else:
        unblocked_pawns |= ((location_board >> 8) & -all_pieces) << 8

    if is_white:
        attack_board |= unblocked_pawns << 8
    else:
        attack_board |= unblocked_pawns >> 8
    return attack_board


def get_capture_board(location_board, all_pieces, is_white):
    """
    Compute and return a capture board (bitboard)
    for all single color pawn capturing moves

    Args:
    location_board: bitboard of all pawns of one color
    all_pieces: bitboard of all pieces in game situation
    is_white: True if it's white's turn

    Returns:
    bitboard: 64-bit bitboard representation of all single color pawn capture moves
    """

    capture_board = EMPTY_BOARD
    attack_tables = get_attack_tables()
    
    while(location_board):
        location_square = bitscan(location_board)
        location_board &= location_board -1

        if is_white:
            capture_board |= attack_tables.white_pawn_attack_tables[location_square]
        else:
            capture_board |= attack_tables.black_pawn_attack_tables[location_square]

    
    return capture_board

    
# NOTE: this is called attack board for consistency, but it does inlude move-only moves
def get_attack_board(location_board, all_pieces, is_white):
    """
    Compute and return a bitboard
    combining all single, double and capture moves for
    pawns of a sigle color. Named attack board for consistency

    Args:
    location_board: bitboard of all pawns of one color
    all_pieces: bitboard of all pieces in game situation
    is_white: True if it's white's turn

    Returns:
    bitboard: 64-bit bitboard representation of all single color pawn moves
    """

    attack_board = EMPTY_BOARD

    attack_board |= get_single_move_board(location_board, all_pieces, is_white)
    attack_board |= get_double_move_board(location_board, all_pieces, is_white)
    attack_board |= get_capture_board(location_board, all_pieces, is_white)


    return attack_board




def generate_moves_white(location_board, all_pieces):
    moves = []
    attack_tables = get_attack_tables()

    unmoved_pawns = location_board & WHITE_PAWNS_START
    moved_pawns = location_board ^ WHITE_PAWNS_START

    location_board_no_promotion = (unmoved_pawns | moved_pawns) & white_pawn_nonpromotion_mask
    location_board_promotion = (unmoved_pawns | moved_pawns) & white_pawn_promotion_mask

    attack_board = get_attack_board(location_board, all_pieces, True)

    # normal moves
    while(location_board_no_promotion):
        location_square = bitscan(location_board_no_promotion)
        location_board_no_promotion &= location_board_no_promotion -1

        
        return_board = EMPTY_BOARD
        return_board |= (attack_tables.white_pawn_move_tables[location_square] & attack_board)
        
        
        while(return_board):
            move_square = bitscan(return_board)
            return_board &= return_board -1

            moves.append(generate_move(location_square, move_square, 0b001, 0b001))

    # promotion moves
    while(location_board_promotion):
        location_square = bitscan(location_board_promotion)
        location_board_no_promotion &= location_board_promotion -1

        
        return_board = EMPTY_BOARD
        return_board |= (attack_tables.white_pawn_move_tables[location_square] & attack_board)
        
        
        while(return_board):
            move_square = bitscan(return_board)
            return_board &= return_board -1

            moves.append(generate_move(location_square, move_square, 0b001, 0b010)) # knight
            moves.append(generate_move(location_square, move_square, 0b001, 0b011)) # bishop
            moves.append(generate_move(location_square, move_square, 0b001, 0b100)) # rook
            moves.append(generate_move(location_square, move_square, 0b001, 0b101)) # queen

    return moves


def generate_moves_black(location_board, all_pieces):
    moves = []
    attack_tables = get_attack_tables()

    unmoved_pawns = location_board & BLACK_PAWNS_START
    moved_pawns = location_board ^ BLACK_PAWNS_START
    
    location_board_no_promotion = (unmoved_pawns | moved_pawns) & black_pawn_nonpromotion_mask
    location_board_promotion = (unmoved_pawns | moved_pawns) & black_pawn_promotion_mask

    attack_board = get_attack_board(location_board, all_pieces, False)

    # normal moves
    while(location_board_no_promotion):
        location_square = bitscan(location_board_no_promotion)
        location_board_no_promotion &= location_board_no_promotion -1

        
        return_board = EMPTY_BOARD
        return_board |= (attack_tables.black_pawn_move_tables[location_square] & attack_board)
        
        
        while(return_board):
            move_square = bitscan(return_board)
            return_board &= return_board -1

            moves.append(generate_move(location_square, move_square, 0b001, 0b001))

    # promotion moves
    while(location_board_promotion):
        location_square = bitscan(location_board_promotion)
        location_board_no_promotion &= location_board_promotion -1

        
        return_board = EMPTY_BOARD
        return_board |= (attack_tables.black_pawn_move_tables[location_square] & attack_board)
        
        
        while(return_board):
            move_square = bitscan(return_board)
            return_board &= return_board -1

            moves.append(generate_move(location_square, move_square, 0b001, 0b010)) # knight
            moves.append(generate_move(location_square, move_square, 0b001, 0b011)) # bishop
            moves.append(generate_move(location_square, move_square, 0b001, 0b100)) # rook
            moves.append(generate_move(location_square, move_square, 0b001, 0b101)) # queen

    return moves

 

def get_moves(location_board, all_pieces, is_white):
    moves = []

    if is_white:
        moves.extend(generate_moves_white(location_board, all_pieces))
    else:
        moves.extend(generate_moves_black(location_board, all_pieces))

    return moves

                    

                