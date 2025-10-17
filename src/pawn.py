from utils import *
from globals import *

from attack_tables import get_attack_tables

white_pawn_double_mask = 0xFF << 8
black_pawn_double_mask = 0xFF >> 48
white_pawn_single_mask = 0xFF ^ 0xFFFFFFFFFFFFFFFF
black_pawn_single_mask = (0xFF >> 56) ^ 0xFFFFFFFFFFFFFFFF
white_pawn_nonpromotion_mask    = (0xFF >> 48) ^ 0xFFFFFFFFFFFFFFFF
black_pawn_nonpromotion_mask   = (0xFF << 8) ^ 0xFFFFFFFFFFFFFFFF
white_pawn_promotion_mask = black_pawn_double_mask
black_pawn_promotion_mask = white_pawn_double_mask



def get_double_move_board(location_board, all_pieces, is_white):
    attack_board = EMPTY_BOARD
    unblocked_pawns = EMPTY_BOARD
    
    if is_white:
        unmoved_pawns = location_board & WHITE_PAWNS_START
        
    else:
        unmoved_pawns = location_board & BLACK_PAWNS_START
        

    if is_white:
        unblocked_pawns |= (unmoved_pawns << 8) & ((all_pieces ^ 0xFFFFFFFFFFFFFFFF) & white_pawn_double_mask)
        attack_board |= unblocked_pawns << 16
    else:
        unblocked_pawns |= (unmoved_pawns >> 8) & ((all_pieces ^ 0xFFFFFFFFFFFFFFFF) & black_pawn_double_mask)
        attack_board |= unblocked_pawns >> 16

    return attack_board

def get_single_move_board(location_board, all_pieces, is_white):
    attack_board = EMPTY_BOARD
    
    if is_white:
        unmoved_pawns = location_board & WHITE_PAWNS_START
        moved_pawns = location_board ^ WHITE_PAWNS_START
    else:
        unmoved_pawns = location_board & BLACK_PAWNS_START
        moved_pawns = location_board ^ BLACK_PAWNS_START

    if is_white:
        attack_board |= ((moved_pawns | unmoved_pawns) & white_pawn_single_mask) << 8
    else:
        attack_board |= ((moved_pawns | unmoved_pawns) & black_pawn_single_mask) >> 8

    return attack_board

    
# NOTE: this is called attack board for consistency, but it does inlude move-only moves
def get_attack_board(location_board, all_pieces, is_white):

    attack_board = EMPTY_BOARD
    attack_tables = get_attack_tables()
    if is_white:
        unmoved_pawns = location_board & WHITE_PAWNS_START
    else:
        moved_pawns = location_board ^ WHITE_PAWNS_START

    

    while(location_board):
        location_square = bitscan(location_board)
        location_board &= location_board -1

        if is_white:
            attack_board |= attack_tables.white_pawn_attack_tables[location_square]
        else:
            attack_board |= attack_tables.black_pawn_attack_tables[location_square]

    if is_white:
        attack_board |= get_single_move_board(location_board, all_pieces, True)
        attack_board |= get_double_move_board(location_board, all_pieces, True)
    else:
        attack_board |= get_single_move_board(location_board, all_pieces, False)
        attack_board |= get_double_move_board(location_board, all_pieces, False)

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

            moves.append(generate_uci(location_square, move_square, 0b001, 0b001))

    # promotion moves
    while(location_board_promotion):
        location_square = bitscan(location_board_promotion)
        location_board_no_promotion &= location_board_promotion -1

        
        return_board = EMPTY_BOARD
        return_board |= (attack_tables.white_pawn_move_tables[location_square] & attack_board)
        
        
        while(return_board):
            move_square = bitscan(return_board)
            return_board &= return_board -1

            moves.append(generate_uci(location_square, move_square, 0b001, 0b010)) # knight
            moves.append(generate_uci(location_square, move_square, 0b001, 0b011)) # bishop
            moves.append(generate_uci(location_square, move_square, 0b001, 0b100)) # rook
            moves.append(generate_uci(location_square, move_square, 0b001, 0b101)) # queen

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

            moves.append(generate_uci(location_square, move_square, 0b001, 0b001))

    # promotion moves
    while(location_board_promotion):
        location_square = bitscan(location_board_promotion)
        location_board_no_promotion &= location_board_promotion -1

        
        return_board = EMPTY_BOARD
        return_board |= (attack_tables.black_pawn_move_tables[location_square] & attack_board)
        
        
        while(return_board):
            move_square = bitscan(return_board)
            return_board &= return_board -1

            moves.append(generate_uci(location_square, move_square, 0b001, 0b010)) # knight
            moves.append(generate_uci(location_square, move_square, 0b001, 0b011)) # bishop
            moves.append(generate_uci(location_square, move_square, 0b001, 0b100)) # rook
            moves.append(generate_uci(location_square, move_square, 0b001, 0b101)) # queen

    return moves

 

def get_moves(location_board, all_pieces, is_white):
    moves = []

    if is_white:
        moves.extend(generate_moves_white(location_board, all_pieces))
    else:
        moves.extend(generate_moves_black(location_board, all_pieces))

    return moves

                    

                