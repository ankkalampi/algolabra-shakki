from utils import *

white_pawn_double_mask = 0xFF << 8
black_pawn_double_mask = 0xFF >> 48
white_pawn_single_mask = 0xFF ^ 0xFFFFFFFFFFFFFFFF
black_pawn_single_mask = (0xFF >> 56) ^ 0xFFFFFFFFFFFFFFFF


class PawnSet:
    def __init__(self, attack_tables, all_pieces, friendly_pieces, is_white):
        self.is_white = is_white
        self.attack_tables = attack_tables
        self.all_pieces = all_pieces
        self.friendly_pieces = friendly_pieces
        if is_white:
            self.unmoved_pawns  = 0x000000000000FF00
            self.moved_pawns    = 0x0000000000000000
        else:
            self.unmoved_pawns  = 0x00FF000000000000
            self.moved_pawns    = 0x0000000000000000

        def get_double_move_board(self):
            attack_board = 0x0000000000000000
            unblocked_pawns = 0x0000000000000000
            if self.is_white:
                unblocked_pawns |= (self.unmoved_pawns << 8) & ((self.all_pieces ^ 0xFFFFFFFFFFFFFFFF) & white_pawn_double_mask)
                attack_board |= unblocked_pawns << 16
            else:
                unblocked_pawns |= (self.unmoved_pawns >> 8) & ((self.all_pieces ^ 0xFFFFFFFFFFFFFFFF) & black_pawn_double_mask)
                attack_board |= unblocked_pawns >> 16

            return attack_board

        def get_single_move_board(self):
            attack_board = 0x0000000000000000
            if self.is_white:
                attack_board |= ((self.moved_pawns | self.unmoved_pawns) & white_pawn_single_mask) << 8
            else:
                attack_board |= ((self.moved_pawns | self.unmoved_pawns) & black_pawn_single_mask) >> 8

            return attack_board

     
        # NOTE: this is called attack board for consistency, but it does inlude move-only moves
        def get_attack_board(self, location_board):

            attack_board = 0x0000000000000000

            while(location_board):
                location_square = bitscan(location_board)
                location_board &= location_board -1

                if self.is_white:
                    attack_board |= self.attack_tables.white_pawn_attack_tables[location_square]
                else:
                    attack_board |= self.attack_tables.black_pawn_attack_tables[location_square]

            attack_board |= get_single_move_board
            attack_board |= get_double_move_board

            return attack_board

        def generate_moves(self):
            moves = []
            
                