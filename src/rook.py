from src.utils import *
from src.globals import *



from src.attack_tables import get_attack_tables

# creates 12-bit block value for bishop to be used to index bihop blocking attack tables
def get_block_value(square, all_pieces):
    """
    Get block value for a rook in a specific square.
    Block value is 

    Args:
    square: square index
    all_pieces: bitboard of all pieces in game situation

    Returns:
    block_value: 12-bit block value
    """
    attack_tables = get_attack_tables()
    block_board = attack_tables.rook_attack_tables[square] & all_pieces

    # get rank and file of the square
    rank = square // 8
    file = square % 8

    space_right = file      # number of squares to the right 
    space_left = 7 - file   # number of squares to the left
    space_down = rank       # number of squares below
    space_up = 7 - rank     # number of squares above

    # lengths of directions
    # order: up, right, down, left
    direction_lengths = [space_up,
                            space_right,
                            space_down,
                            space_left]

    # scalars for directional bit shifts
    # order: up, right, down, left
    direction_scalars = [8, -1, -8, 1]

    # block value component array for easier assignment
    block_value_components = [  0b000,
                                0b000,
                                0b000,
                                0b000]

    

    for diagonal in range(0, 4):
        for sq in range(1, direction_lengths[diagonal]+1):
            temp_bitboard = EMPTY_BOARD
            temp_bitboard |= (1 << square)
            if direction_scalars[diagonal] < 0:
                move_bitboard = (temp_bitboard >> (sq * abs(direction_scalars[diagonal]))) & 0xFFFFFFFFFFFFFFFF # masking makes sure no extra bits are added
            else:
                move_bitboard = (temp_bitboard << (sq * direction_scalars[diagonal])) & 0xFFFFFFFFFFFFFFFF # masking makes sure no extra bits are added
            
            if move_bitboard & block_board != 0:
                block_value_components[diagonal] |= sq & 0b111
                break

    # construct block value from block values that correspond to individual diagonals
    block_value = 0b000000000000
    block_value |= block_value_components[3]
    block_value |= (block_value_components[2] << 3)
    block_value |= (block_value_components[1] << 6)
    block_value |= (block_value_components[0] << 9)


    return block_value

def get_attack_board(location_board, all_pieces):
    """
    Get bitboard for all rook attacks for a specific color

    Args:
    location_board: bitboard of all rooks of a specific color
    all_pieces: bitboard of all pieces in game situation

    Returns:
    bitboard: 64-bit bitboard 
    """

    attack_board = EMPTY_BOARD
    attack_tables = get_attack_tables()

    while(location_board):
        location_square = bitscan(location_board)
        location_board &= location_board -1

        block_value = get_block_value(location_square, all_pieces)
        attack_board |= attack_tables.rook_blocking_attack_tables[location_square][block_value]

    return attack_board

def get_moves(location_board, all_pieces):
    """
    Get all moves for rooks for a specific color

    Args:
    location_board: bitboard of all rooks of a specific color
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

            moves.append(generate_move(location_square, move_square, 0b100))

    return moves

