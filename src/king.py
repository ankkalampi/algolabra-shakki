from utils import *

def get_attack_board(square, attack_tables):
    return attack_tables.king_attack_tables[square]