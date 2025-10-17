from utils import *
from globals import *

white_pawn_double_mask = 0xFF << 8
black_pawn_double_mask = 0xFF >> 48
white_pawn_single_mask = 0xFF ^ 0xFFFFFFFFFFFFFFFF
black_pawn_single_mask = (0xFF >> 56) ^ 0xFFFFFFFFFFFFFFFF
white_pawn_nonpromotion_mask    = (0xFF >> 48) ^ 0xFFFFFFFFFFFFFFFF
black_pawn_nonpromotion_mask   = (0xFF << 8) ^ 0xFFFFFFFFFFFFFFFF
white_pawn_promotion_mask = black_pawn_double_mask
black_pawn_promotion_mask = white_pawn_double_mask


class PawnSet:
    def __init__(self, attack_tables, is_white):
        self.is_white = is_white
        self.attack_tables = attack_tables
       
        if is_white:
            self.unmoved_pawns  = WHITE_PAWNS_START
            self.moved_pawns    = EMPTY_BOARD
        else:
            self.unmoved_pawns  = BLACK_PAWNS_START
            self.moved_pawns    = EMPTY_BOARD

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
    def get_attack_board(self):

        attack_board = 0x0000000000000000
        location_board = self.unmoved_pawns | self.moved_pawns

        while(location_board):
            location_square = bitscan(location_board)
            location_board &= location_board -1

            if self.is_white:
                attack_board |= self.attack_tables.white_pawn_attack_tables[location_square]
            else:
                attack_board |= self.attack_tables.black_pawn_attack_tables[location_square]

        attack_board |= self.get_single_move_board()
        attack_board |= self.get_double_move_board()

        return attack_board

    def generate_moves_white(self):
        moves = []

        location_board_no_promotion = (self.unmoved_pawns | self.moved_pawns) & white_pawn_nonpromotion_mask
        location_board_promotion = (self.unmoved_pawns | self.moved_pawns) & white_pawn_promotion_mask

        attack_board = self.get_attack_board()

        # normal moves
        while(location_board_no_promotion):
            location_square = bitscan(location_board_no_promotion)
            location_board_no_promotion &= location_board_no_promotion -1

            
            return_board = 0x0000000000000000
            return_board |= (self.attack_tables.white_pawn_move_tables[location_square] & attack_board)
            
            
            while(return_board):
                move_square = bitscan(return_board)
                return_board &= return_board -1

                moves.append(generate_uci(location_square, move_square, 0b001, 0b001))

        # promotion moves
        while(location_board_promotion):
            location_square = bitscan(location_board_promotion)
            location_board_no_promotion &= location_board_promotion -1

            
            return_board = 0x0000000000000000
            return_board |= (self.attack_tables.white_pawn_move_tables[location_square] & attack_board)
            
            
            while(return_board):
                move_square = bitscan(return_board)
                return_board &= return_board -1

                moves.append(generate_uci(location_square, move_square, 0b001, 0b010)) # knight
                moves.append(generate_uci(location_square, move_square, 0b001, 0b011)) # bishop
                moves.append(generate_uci(location_square, move_square, 0b001, 0b100)) # rook
                moves.append(generate_uci(location_square, move_square, 0b001, 0b101)) # queen

        return moves


    def generate_moves_black(self):
        moves = []
        
        location_board_no_promotion = (self.unmoved_pawns | self.moved_pawns) & black_pawn_nonpromotion_mask
        location_board_promotion = (self.unmoved_pawns | self.moved_pawns) & black_pawn_promotion_mask

        attack_board = self.get_attack_board()

        # normal moves
        while(location_board_no_promotion):
            location_square = bitscan(location_board_no_promotion)
            location_board_no_promotion &= location_board_no_promotion -1

            
            return_board = 0x0000000000000000
            return_board |= (self.attack_tables.black_pawn_move_tables[location_square] & attack_board)
            
            
            while(return_board):
                move_square = bitscan(return_board)
                return_board &= return_board -1

                moves.append(generate_uci(location_square, move_square, 0b001, 0b001))

        # promotion moves
        while(location_board_promotion):
            location_square = bitscan(location_board_promotion)
            location_board_no_promotion &= location_board_promotion -1

            
            return_board = 0x0000000000000000
            return_board |= (self.attack_tables.black_pawn_move_tables[location_square] & attack_board)
            
            
            while(return_board):
                move_square = bitscan(return_board)
                return_board &= return_board -1

                moves.append(generate_uci(location_square, move_square, 0b001, 0b010)) # knight
                moves.append(generate_uci(location_square, move_square, 0b001, 0b011)) # bishop
                moves.append(generate_uci(location_square, move_square, 0b001, 0b100)) # rook
                moves.append(generate_uci(location_square, move_square, 0b001, 0b101)) # queen

        return moves

    def remove_piece(self, square):
        if (self.unmoved_pawns & square != 0):
            self.unmoved_pawns ^= square
        if (self.moved_pawns & square != 0):
            self.moved_pawns ^= square

    def generate_moves(self):
        if self.is_white:
            return self.generate_moves_white()
        else:
            return self.generate_moves_black()

    def get_pieces(self):
        return self.unmoved_pawns | self.moved_pawns

                    

                