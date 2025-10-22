from src.utils import *
from src.globals import *

from src.attack_tables import get_attack_tables



WHITE_PAWN_NONPROMOTION_MASK    = 0x0000FFFFFFFFFFFF
BLACK_PAWN_NONPROMOTION_MASK   = 0xFFFFFFFFFFFF0000
WHITE_PAWN_PROMOTION_MASK = 0x00FF000000000000
BLACK_PAWN_PROMOTION_MASK = 0x000000000000FF00
WHITE_PROMOTION_ZONE = 0xFF00000000000000
BLACK_PROMOTION_ZONE = 0x00000000000000FF



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

def generate_movement_moves_white(location_board, all_pieces):
    """
    Generate white pawn non-promotion movement moves in a specific situation

    Args:
    location_board: bitboard of all white pawns
    all_pieces: bitboard of all pieces in game situation

    Returns:
    moves: list of moves in 18bit format
    """

    moves = []
    location_board_no_promotion = location_board & WHITE_PAWN_NONPROMOTION_MASK
    movement_board = get_single_move_board(location_board_no_promotion, all_pieces, True)
    movement_board |= get_double_move_board(location_board_no_promotion, all_pieces, True)
    attack_tables = get_attack_tables()

    while(location_board_no_promotion):
        location_square = bitscan(location_board_no_promotion)
        location_board_no_promotion &= location_board_no_promotion -1

        
        return_board = EMPTY_BOARD
        return_board |= (attack_tables.white_pawn_move_tables[location_square] & movement_board)
        
        
        while(return_board):
            move_square = bitscan(return_board)
            return_board &= return_board -1

            moves.append(generate_move(location_square, move_square, 0b001, 0b000))

    return moves

def generate_movement_moves_black(location_board, all_pieces):
    """
    Generate black pawn non-promotion movement moves in a specific situation

    Args:
    location_board: bitboard of all black pawns
    all_pieces: bitboard of all pieces in game situation

    Returns:
    moves: list of moves in 18bit format
    """

    moves = []
    location_board_no_promotion = location_board & BLACK_PAWN_NONPROMOTION_MASK
    movement_board = get_single_move_board(location_board, all_pieces, False)
    movement_board |= get_double_move_board(location_board, all_pieces, False)
    attack_tables = get_attack_tables()

    while(location_board_no_promotion):
        location_square = bitscan(location_board_no_promotion)
        location_board_no_promotion &= location_board_no_promotion -1

        
        return_board = EMPTY_BOARD
        return_board |= (attack_tables.black_pawn_move_tables[location_square] & movement_board)
        
        
        while(return_board):
            move_square = bitscan(return_board)
            return_board &= return_board -1

            moves.append(generate_move(location_square, move_square, 0b001, 0b000))

    return moves

def generate_capture_moves_white(location_board, all_pieces):
    """
    Generate white pawn capturing moves in a specific situation.
    Also generates promotion moves if capturing results in promotion

    Args:
    location_board: bitboard of all white pawns
    all_pieces: bitboard of all pieces in game situation

    Returns:
    moves: list of moves in 18bit format
    """

    moves = []
    
    attack_board = get_capture_board(location_board, all_pieces, True) & all_pieces
    attack_tables = get_attack_tables()
    

    while(location_board):
        
        location_square = bitscan(location_board)
        location_board &= location_board -1

        
        return_board = EMPTY_BOARD
        
        return_board |= (attack_tables.white_pawn_attack_tables[location_square] & attack_board)
        
        
        while(return_board):
            move_square = bitscan(return_board)
            return_board &= return_board -1

            # add promotion moves if pawn ends up in promotion zone
            if get_bitboard_of_square(move_square) & WHITE_PROMOTION_ZONE != 0:
                moves.append(generate_move(location_square, move_square, 0b001, 0b010))
                moves.append(generate_move(location_square, move_square, 0b001, 0b011))
                moves.append(generate_move(location_square, move_square, 0b001, 0b100))
                moves.append(generate_move(location_square, move_square, 0b001, 0b101))
            else:
                moves.append(generate_move(location_square, move_square, 0b001, 0b000))

    return moves

def generate_capture_moves_black(location_board, all_pieces):
    """
    Generate black pawn capturing moves in a specific situation
    Also generates promotion moves if capturing results in promotion

    Args:
    location_board: bitboard of all black pawns
    all_pieces: bitboard of all pieces in game situation

    Returns:
    moves: list of moves in 18bit format
    """

    moves = []
    
    attack_board = get_capture_board(location_board, all_pieces, False) & all_pieces
    attack_tables = get_attack_tables()
    

    while(location_board):
        
        location_square = bitscan(location_board)
        location_board &= location_board -1

        
        return_board = EMPTY_BOARD
        
        return_board |= (attack_tables.black_pawn_attack_tables[location_square] & attack_board)
        
        
        while(return_board):
            move_square = bitscan(return_board)
            return_board &= return_board -1

            # add promotion moves if pawn ends up in promotion zone
            if get_bitboard_of_square(move_square) & BLACK_PROMOTION_ZONE != 0:
                moves.append(generate_move(location_square, move_square, 0b001, 0b010))
                moves.append(generate_move(location_square, move_square, 0b001, 0b011))
                moves.append(generate_move(location_square, move_square, 0b001, 0b100))
                moves.append(generate_move(location_square, move_square, 0b001, 0b101))
            else:
                moves.append(generate_move(location_square, move_square, 0b001, 0b000))

    return moves


def generate_promotion_moves_white(location_board, all_pieces):
    """
    Generate white pawn promotion moves in a specific situation

    Args:
    location_board: bitboard of all white pawns
    all_pieces: bitboard of all pieces in game situation

    Returns:
    moves: list of moves in 18bit format
    """
    moves = []
    location_board_promotion = location_board & WHITE_PAWN_PROMOTION_MASK
    attack_board = get_attack_board(location_board, all_pieces, True)
    attack_tables = get_attack_tables()

    while(location_board_promotion):
        location_square = bitscan(location_board_promotion)
        location_board_promotion &= location_board_promotion -1

        
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


def generate_promotion_moves_black(location_board, all_pieces):
    """
    Generate black pawn promotion moves in a specific situation

    Args:
    location_board: bitboard of all black pawns
    all_pieces: bitboard of all pieces in game situation

    Returns:
    moves: list of moves in 18bit format
    """
    moves = []
    location_board_promotion = location_board & BLACK_PAWN_PROMOTION_MASK
    attack_board = get_attack_board(location_board, all_pieces, False)
    attack_tables = get_attack_tables()

    while(location_board_promotion):
        location_square = bitscan(location_board_promotion)
        location_board_promotion &= location_board_promotion -1

        
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


def generate_moves_white(location_board, all_pieces):
    """
    Generate all white pawn moves in a specific situation

    Args:
    location_board: bitboard of all white pawns
    all_pieces: bitboard of all pieces in game situation

    Returns:
    moves: list of moves in 18bit format
    """
    moves = []
    moves.extend(generate_movement_moves_white(location_board, all_pieces))
    moves.extend(generate_capture_moves_white(location_board, all_pieces))
    moves.extend(generate_promotion_moves_white(location_board, all_pieces))
    return moves


def generate_moves_black(location_board, all_pieces):
    """
    Generate all black pawn moves in a specific situation

    Args:
    location_board: bitboard of all white pawns
    all_pieces: bitboard of all pieces in game situation

    Returns:
    moves: list of moves in 18bit format
    """
    moves = []
    moves.extend(generate_movement_moves_black(location_board, all_pieces))
    moves.extend(generate_capture_moves_black(location_board, all_pieces))
    moves.extend(generate_promotion_moves_black(location_board, all_pieces))
    return moves

 

def get_moves(location_board, all_pieces, is_white):
    """
    Returns all pawn moves of a specific color in a specific situation

    Args:
    location_board: bitboard of all white pawns
    all_pieces: bitboard of all pieces in game situation
    is_white: True if white

    Returns:
    moves: list of moves in 18bit format
    """
    moves = []

    if is_white:
        moves.extend(generate_moves_white(location_board, all_pieces))
    else:
        moves.extend(generate_moves_black(location_board, all_pieces))

    return moves

                    

