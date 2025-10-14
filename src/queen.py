from utils import bitscan
import bishop
import rook


def get_attack_board(location_board, attack_tables, all_pieces):
    
    attack_board = 0x0000000000000000

    while(location_board):
        location_square = bitscan(location_board)
        location_board &= location_board -1

        block_value = bishop.get_block_value(location_square, attack_tables, all_pieces)
        attack_board |= attack_tables.bishop_blocking_attack_tables[block_value]

        block_value = rook.get_block_value(location_square, attack_tables, all_pieces)
        attack_board |= attack_tables.rook_blocking_attack_tables[block_value]

    return attack_board