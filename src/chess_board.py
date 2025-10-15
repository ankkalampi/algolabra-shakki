import random
import time
from utils import * 
from precomputation import *
from piece_set import PieceSet






# TODO: generate bitboards for en passant

# TODO: add logic for in_check situation to these functions

# TODO: create function for generating attack bitboard (to check where the opponent can attack in a certain situation)
# TODO: create function for generating attack bitboard (to check where the current player can attack in a certain situation) 

# TODO: create logic for testing a move (recalculate attack bitboards)
# TODO: create logic for removing illegal moves
# TODO: create logic for commiting a move (update data such as in_check, white_to_move, etc)

# TODO: create simple heuristics

# TODO: implement minmax algorithm

# TODO: create testing

# TODO: fine tune heuristics



class ChessBoard:
    def __init__(self):
        # init bitboards for each piece type


        self.white_en_passant   = 0x0000000000000000
        self.black_en_passant   = 0x0000000000000000
        

        self.white_to_move = True
        self.available_moves = []
        self.empty_squares = 0x0000000000000000
        self.in_check = False

        self.pieces = PieceSet()

        

        


    # resets the board to opening situation
    def reset(self):
        
        self.white_en_passant   = 0x0000000000000000
        self.black_en_passant   = 0x0000000000000000

        self.white_to_move = True
        self.available_moves = []
        self.empty_squares = 0x0000000000000000
        self.in_check = False

        


        

    # find all legal moves based on whose turn it is
    def generate_available_moves(self, white_to_move):

        # calculate empty squares (complement of all squares with pieces)
        self.empty_squares = ~( self.white_pawns | self.white_knights | self.white_bishops |
                                self.white_rooks | self.white_queens | self.white_king |
                                self.black_pawns | self.black_knights | self.black_bishops |
                                self.black_rooks | self.black_queens | self.black_king)

        moves = []

        if white_to_move:
            moves.extend(self.generate_bishop_moves(self.white_bishops, self.all_pieces))
            moves.extend(self.generate_rook_moves(self.white_rooks, self.all_pieces))
            moves.extend(self.generate_queen_moves(self.white_queens, self.all_pieces))
            moves.extend(self.generate_knight_moves(self.white_knights, self.all_pieces))
        else:
            moves.extend(self.generate_bishop_moves(self.black_bishops, self.all_pieces))
            moves.extend(self.generate_rook_moves(self.black_rooks, self.all_pieces))
            moves.extend(self.generate_queen_moves(self.black_queens, self.all_pieces))
            moves.extend(self.generate_knight_moves(self.black_knights, self.all_pieces))


        return moves

        

    

        



    

    def push_uci(self, uci):
        pass
        

    # filters out moves that put the moving party's king in check, as well as illegal castling
    def filter_illegal_moves(self):
        pass

    # generates en passant moves based on the en passant bitboard
    # NOTE: en passant table must be always updated when a move is commited!
    def generate_en_passant_moves(self):
        pass

    # generate bitboard for showing attack squares for white
    def generate_white_attack_board(self):
        pass

    # generate bitboard for showing attack squares for black
    def generate_black_attack_board(self):
        pass

        


    def generate_pawn_double_moves(self, pawn_board, empty_squares, white_to_move):

        # mask is for checking that the pawns are in starting location
        if white_to_move:
            mask = self.white_pawn_double_mask
        else:
            mask = self.black_pawn_double_mask

        unmoved_pawns = pawn_board & mask
        unblocked_pawns = ((pawn_board << 8) & empty_squares) >> 8

        double_unblocked_pawns = ((pawn_board << 16) & empty_squares) >> 16

        eligible_pawns = unmoved_pawns & unblocked_pawns & double_unblocked_pawns

        moves = []


        while(eligible_pawns):
            # find first square on location board and form move
            location_square = bitscan(eligible_pawns)
            eligible_pawns &= -eligible_pawns
            if white_to_move:
                moves.append(generate_uci(location_square, location_square << 16, 0b001))
            else:
                moves.append(generate_uci(location_square, location_square >> 16, 0b001))

        return moves

    def generate_pawn_single_moves(self, pawn_board, empty_squares, white_to_move):

        if white_to_move:
            mask = self.white_pawn_promote_mask
            eligible_pawns = pawn_board & ~mask & (((pawn_board << 8) & empty_squares) << 8)
        else:
            mask = self.black_pawn_promote_mask
            eligible_pawns = pawn_board & ~mask & (((pawn_board >> 8) & empty_squares) >> 8)

      

        moves = []

        while(eligible_pawns):

            location_square = bitscan(eligible_pawns)
            eligible_pawns &= -eligible_pawns
            if white_to_move:
                moves.append(generate_uci(location_square, location_square << 8,0b001))
            else:
                moves.append(generate_uci(location_square, location_square >> 8, 0b001))

        return moves

    def generate_pawn_en_passant_moves(self, pawn_board, en_passant_board, white_to_move):

        moves = []

        right_pawn = en_passant_board & (pawn_board << 1)
        left_pawn = en_passant_board & (pawn_board >> 1)

        if white_to_move:
            if right_pawn != 0:
                moves.append(generate_uci(right_pawn, (right_pawn >> 7), 0b001))
            if left_pawn != 0:
                moves.append(generate_uci(left_pawn, (left_pawn >> 9), 0b001))
        else: 
            if right_pawn != 0:
                moves.append(generate_uci(right_pawn, (right_pawn << 9), 0b001))
            if left_pawn != 0:
                moves.append(generate_uci(left_pawn, (left_pawn << 7), 0b001))

        return moves

    def generate_promotion_moves(self, pawn_board, empty_squares, white_to_move):
        moves = []

        if white_to_move:
            mask = self.white_pawn_promote_mask
            eligible_pawns = pawn_board & mask & (((pawn_board << 8) & empty_squares) << 8)
        else:
            mask = self.black_pawn_promote_mask
            eligible_pawns = pawn_board & mask & (((pawn_board >> 8) & empty_squares) >> 8)

        while(eligible_pawns):
            location_square = bitscan(eligible_pawns)
            eligible_pawns &= -eligible_pawns

            if white_to_move:
                moves.append(generate_uci(location_square, location_square << 8,0b001, 0b001))
                moves.append(generate_uci(location_square, location_square << 8,0b001, 0b010))
                moves.append(generate_uci(location_square, location_square << 8,0b001, 0b011))
                moves.append(generate_uci(location_square, location_square << 8,0b001, 0b100))
            else:
                moves.append(generate_uci(location_square, location_square >> 8, 0b001, 0b001))
                moves.append(generate_uci(location_square, location_square >> 8, 0b001, 0b010))
                moves.append(generate_uci(location_square, location_square >> 8, 0b001, 0b011))
                moves.append(generate_uci(location_square, location_square >> 8, 0b001, 0b100))

        return moves


        

                





    # generates pawn moves, does not yet check if a move is illegal for checking the king
    def generate_pawn_moves(self):      
        # generate bitboards for legal moves

        # WHITE
        if self.white_to_move:
            # calculate single square pawn moves (shifting bits 8 positions left, so up one rank)
            single_moves = (self.white_pawns << 8) & self.empty_squares 


            unmoved_pawns = self.white_pawns & self.white_pawn_double_mask
            unblocked_pawns = (self.white_pawns << 8) & self.empty_squares  

            # calculate double square moves
            # (moving piece must be in starting position, destination square must be empty,
            # and the square in between has to be empty as well)
            double_moves = (unmoved_pawns << 16) & (unblocked_pawns << 8) & self.empty_squares 

            

        # BLACK
        else:
            # calculate single square pawn moves (shifting bits 8 positions right, so down one rank)
            single_moves = (self.black_pawns >> 8) & self.empty_squares

            unmoved_pawns = self.black_pawns & self.black_pawn_double_mask
            unblocked_pawns = (self.black_pawns << 8) & self.empty_squares

            # calculate double square moves 
            # (moving piece must be in starting position, destination square must be empty,
            # and the square in between has to be empty as well)
            double_moves = (unmoved_pawns >> 16) & (unblocked_pawns >> 8) & self.empty_squares 

        # returns a bitboard with pseudo-legal pawn moves
        return single_moves | double_moves


    



    # generate pseudo legal knight moves based on location board, precalculated attack boards and empty_squares (friendly pieces)  
    def generate_knight_moves(self, location_board, friendly_pieces):
        """
        Args:
            location_board: a bitboard that has all knight locations
            friendly_pieces: a bitboard that has all friendly pieces

        """
        moves = []

        while(location_board):
            # find first square on location board and get attack table
            location_square = bitscan(location_board)
            attack_board = self.precomputed_knight_attack_table[location_square]

            # remove square from location board using bit magic
            location_board &= location_board -1

            # iterate through attack squares in the same way as location board is iterated
            while(attack_board):
                # find first square in attack board
                attack_square = bitscan(attack_board)

                # remove square form attack board
                attack_board &= attack_board -1

                # if the attack square is on a friendly piece, do nothing
                if attack_square & friendly_pieces == 0: continue

                # if the attack square is on a hostile piece or an empty square, form the move
                moves.append(generate_uci(location_square, attack_square, 0b010))

        return moves

    


    

    

    # TODO: This function shares a lot in common with similar functions. could refactor to simplify code
    

    # TODO: This function shares a lot in common with similar functions. could refactor to simplify code
    







    # generate pseudo legal knight moves based on location board, precalculated attack boards and empty_squares (all pieces)  
    def generate_bishop_moves(self, location_board, all_pieces):
        """
        Args:
            location_board: a bitboard that has all bishop locations
            friendly_pieces: a bitboard that has all pieces

        """
        moves = []

        while(location_board):
            # find first square on location board and get attack table
            location_square = bitscan(location_board)

            # remove square from location board using bit magic
            location_board &= location_board -1

            # get bishop blocking value and find correct attack board
            block_value = self.get_bishop_block_value(location_square)
            attack_board = self.precomputed_bishop_blocking_attack_tables[location_square][block_value]


            # iterate through attack squares in the same way as location board is iterated
            while(attack_board):
                # find first square in attack board
                attack_square = bitscan(attack_board)

                # remove square form attack board
                attack_board &= attack_board -1

                # if the attack square is on a friendly piece, do nothing
                if attack_square & all_pieces == 0: continue

                # if the attack square is on a hostile piece or an empty square, form the move
                moves.append(generate_uci(location_square, attack_square, 0b011))

        return moves


    # generate pseudo legal knight moves based on location board, precalculated attack boards and empty_squares (all pieces)  
    def generate_rook_moves(self, location_board, all_pieces):
        """
        Args:
            location_board: a bitboard that has all rook locations
            friendly_pieces: a bitboard that has all pieces

        """
        moves = []

        while(location_board):
            # find first square on location board and get attack table
            location_square = bitscan(location_board)

            # remove square from location board using bit magic
            location_board &= location_board -1

            # get bishop blocking value and find correct attack board
            block_value = self.get_rook_block_value(location_square)
            attack_board = self.precomputed_rook_blocking_attack_tables[location_square][block_value]


            # iterate through attack squares in the same way as location board is iterated
            while(attack_board):
                # find first square in attack board
                attack_square = bitscan(attack_board)

                # remove square form attack board
                attack_board &= attack_board -1

                # if the attack square is on a friendly piece, do nothing
                if attack_square & all_pieces == 0: continue

                # if the attack square is on a hostile piece or an empty square, form the move
                moves.append(generate_uci(location_square, attack_square, 0b100))

        return moves


    def generate_queen_moves(self, location_board, all_pieces):
        moves = []
        

        while(location_board):
            # find first square on location board and get attack table
            location_square = bitscan(location_board)

            # remove square from location board using bit magic
            location_board &= location_board -1

            # GET MOVES AS ROOK

            # get rook blocking value and find correct attack board
            block_value = self.get_rook_block_value(location_square)
            attack_board = self.precomputed_rook_blocking_attack_tables[location_square][block_value]

            # iterate through attack squares in the same way as location board is iterated
            while(attack_board):
                # find first square in attack board
                attack_square = bitscan(attack_board)

                # remove square form attack board
                attack_board &= attack_board -1

                # if the attack square is on a friendly piece, do nothing
                if attack_square & all_pieces == 0: continue

                # if the attack square is on a hostile piece or an empty square, form the move
                moves.append(generate_uci(location_square, attack_square, 0b101))

            # GET MOVES AS BISHOP


            # get bishop blocking value and find correct attack board
            block_value = self.get_bishop_block_value(location_square)
            attack_board = self.precomputed_bishop_blocking_attack_tables[location_square][block_value]

            # iterate through attack squares in the same way as location board is iterated
            while(attack_board):
                # find first square in attack board
                attack_square = bitscan(attack_board)

                # remove square form attack board
                attack_board &= attack_board -1

                # if the attack square is on a friendly piece, do nothing
                if attack_square & all_pieces == 0: continue

                # if the attack square is on a hostile piece or an empty square, form the move
                moves.append(generate_uci(location_square, attack_square, 0b101))


        return moves







