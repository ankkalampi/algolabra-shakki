from utils import *
from globals import *

class KingSet:
    def __init__(self, attack_tables, is_white):
        if is_white:
            self.king = WHITE_KING_START
        else:
            self.king = BLACK_KING_START
        
        self.attack_tables = attack_tables

    def get_pieces(self):
        return self.king


def get_attack_board(self):
    return self.attack_tables.king_attack_tables[self.king]

def generate_moves(self):
    moves = []
    attack_board = self.attack_tables.king_attack_tables[self.king]

    while(attack_board):
        move_square = bitscan(attack_board)
        attack_board &= attack_board -1

        moves.append(generate_uci(self.king, move_square, 0b110, 0b000))

    return moves

