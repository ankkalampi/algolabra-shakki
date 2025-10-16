import random
import time
from utils import * 
from precomputation import *
from piece_set import PieceSet

from attack_tables import AttackTables

from pawn import PawnSet
from bishop import BishopSet
from knight import KnightSet
from rook import RookSet
from queen import QueenSet
from king import KingSet




class ChessBoard:
    def __init__(self):
        
        self.attack_tables = AttackTables()


        self.white_pawns = PawnSet(self.attack_tables, True)
        self.white_knights = KnightSet(self.attack_tables, True)
        self.white_bishops = BishopSet(self.attack_tables, True)
        self.white_rooks = RookSet(self.attack_tables, True)
        self.white_queens = QueenSet(self.attack_tables, True)
        self.white_king = KingSet(self.attack_tables, True)
        
        self.black_pawns = PawnSet(self.attack_tables, False)
        self.black_knights = KnightSet(self.attack_tables, False)
        self.black_bishops = BishopSet(self.attack_tables, False)
        self.black_rooks = RookSet(self.attack_tables, False)
        self.black_queens = QueenSet(self.attack_tables, False)
        self.black_king = KingSet(self.attack_tables, False)

        self.white_turn = True
        self.friendly_pieces

    def get_moves(self):
        all_pieces = 0
        white_pieces = 0
        black_pieces = 0

        white_pieces = (self.white_pawns.get_pieces() |
                        self.white_knights.get_pieces() |
                        self.white_bishops.get_pieces() |
                        self.white_rooks.get_pieces() |
                        self.white_queens.get_pieces() |
                        self.white_king.get_pieces())

        black_pieces = (self.black_pawns.get_pieces() |
                        self.black_knights.get_pieces() |
                        self.black_bishops.get_pieces() |
                        self.black_rooks.get_pieces() |
                        self.black_queens.get_pieces() |
                        self.black_king.get_pieces()) 

        all_pieces = white_pieces | black_pieces

        if white_turn:
            self.friendly_pieces = white_pieces
        else:
            self.friendly_pieces = black_pieces

        moves = []

        if self.white_turn:
            moves.extend(self.white_pawns.get_moves(all_pieces))
            moves.extend(self.white_knights.get_moves(all_pieces))
            moves.extend(self.white_bishops.get_moves(all_pieces))
            moves.extend(self.white_rooks.get_moves(all_pieces))
            moves.extend(self.white_queens.get_moves(all_pieces))
            moves.extend(self.white_king.get_moves(all_pieces))

        
        else:
            moves.extend(self.black_pawns.get_moves(all_pieces))
            moves.extend(self.black_knights.get_moves(all_pieces))
            moves.extend(self.black_bishops.get_moves(all_pieces))
            moves.extend(self.black_rooks.get_moves(all_pieces))
            moves.extend(self.black_queens.get_moves(all_pieces))
            moves.extend(self.black_king.get_moves(all_pieces))

        white_attack_board = self.get_white_attack_board(all_pieces)
        black_attack_board = self.get_black_attack_board(all_pieces)

        moves = self.filter_illegal_moves(moves)

        return moves

    def get_white_attack_board(self, all_pieces):
        return (self.white_pawns.get_attack_board(all_pieces) |
                self.white_bishops.get_attack_board(all_pieces) |
                self.white_knights.get_attack_board(all_pieces) |
                self.white_rooks.get_attack_board(all_pieces) |
                self.white_queens.get_attack_board(all_pieces) |
                self.white_king.get_attack_board(all_pieces))

    def get_black_attack_board(self, all_pieces):
        return (self.black_pawns.get_attack_board(all_pieces) |
                self.black_bishops.get_attack_board(all_pieces) |
                self.black_knights.get_attack_board(all_pieces) |
                self.black_rooks.get_attack_board(all_pieces) |
                self.black_queens.get_attack_board(all_pieces) |
                self.black_king.get_attack_board(all_pieces))


    def filter_illegal_moves(self, moves):
        legal_moves = []

        for move in moves:
            
            if self.check_move(move):
                legal_moves.append(move)
        
        return legal_moves


    def check_move(self, move):
        is_legal = True

        

        if self.check_if_trying_to_capture_friendly_piece(move):
            is_legal = False
        else: 
            if self.check_if_friendly_king_in_check(move):
                is_legal = False

        return is_legal

    def check_if_friendly_king_in_check(self, move):
        pass

    def check_if_trying_to_capture_friendly_piece(self, move):
        destination = get_destination_from_move(move)

        return ((destination & self.friendly_pieces) != 0)


    def attempt_move(self, move):
        pass



        




