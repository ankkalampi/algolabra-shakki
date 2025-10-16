from utils import *
from globals import *

class QueenSet:
    def __init__(self, attack_tables, is_white):
        self.attack_tables = attack_tables
        if is_white:
            self.pieces = WHITE_QUEENS_START
        else:
            self.pieces = BLACK_QUEENS_START


    def get_pieces(self):
        return self.pieces


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