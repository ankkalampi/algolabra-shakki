from utils import *
from globals import *


class KnightSet:
    def __init__(self, attack_tables, is_white):
        self.attack_tables = attack_tables
        if is_white:
            self.pieces = WHITE_KNIGHTS_START
        else:
            self.pieces =  BLACK_KNIGHTS_START


    def get_pieces(self):
        return self.pieces

def get_attack_board(location_board, attack_tables, all_pieces):

    attack_board = 0x0000000000000000

    while(location_board):
        location_square = bitscan(location_board)
        location_board &= location_board -1

        
        attack_board |= attack_tables.knight_attack_tables[location_square]
        

    return attack_board