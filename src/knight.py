from utils import bitscan

def get_attack_board(location_board, attack_tables, all_pieces):

    attack_board = 0x0000000000000000

    while(location_board):
        location_square = bitscan(location_board)
        location_board &= location_board -1

        
        attack_board |= attack_tables.knight_attack_tables[location_square]
        

    return attack_board