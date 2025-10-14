from utils import *

# creates 12-bit block value for bishop to be used to index bihop blocking attack tables
def get_block_value(square, attack_tables, all_pieces):
    # bitboard that has the locations of pieces intersecting the attack diagonals
    block_board = attack_tables.bishop_attack_tables[square] & all_pieces

    # get rank and file of the square
    rank = square // 8
    file = square % 8

    space_right = file      # number of squares to the right 
    space_left = 7 - file   # number of squares to the left
    space_down = rank       # number of squares below
    space_up = 7 - rank     # number of squares above

    # diagonal lengths
    # order: northeast, southeast, southwest, northwest
    diagonal_lengths = [min(space_right, space_up),
                        min(space_right, space_down),
                        min(space_down, space_left),
                        min(space_left, space_up)]

    # scalars for diagonal bit shifts
    # order: northeast, southeast, southwest, northwest
    diagonal_scalars = [7, -7, -9, 9]

    # block value component array for easier assignment
    block_value_components = [  0b000,
                                0b000,
                                0b000,
                                0b000]

    

    for diagonal in range(0, 4):
        for sq in range(0, diagonal_lengths):
            temp_bitboard = 0
            temp_bitboard |= (1 << square)
            if diagonal_scalars[diagonal] < 0:
                move_bitboard = (temp_bitboard >> (sq * abs(diagonal_scalars[diagonal]))) & 0xFFFFFFFFFFFFFFFF # masking makes sure no extra bits are added
            else:
                move_bitboard = (temp_bitboard << (sq * diagonal_scalars[diagonal])) & 0xFFFFFFFFFFFFFFFF # masking makes sure no extra bits are added
            
            if move_bitboard & block_board != 0:
                block_value_components[diagonal] |= sq & 0b000
                break

    # construct block value from block values that correspond to individual diagonals
    block_value = 0b000000000000
    block_value |= block_value_components[0]
    block_value |= (block_value_components[1] << 3)
    block_value |= (block_value_components[2] << 6)
    block_value |= (block_value_components[3] << 9)


    return block_value


def get_attack_board(location_board, attack_tables, all_pieces):

    attack_board = 0x0000000000000000

    while(location_board):
        location_square = bitscan(location_board)
        location_board &= location_board -1

        block_value = get_block_value(location_square, attack_tables, all_pieces)
        attack_board |= attack_tables.bishop_blocking_attack_tables[block_value]

    return attack_board