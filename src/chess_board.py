import random
import time
from utils import * 
from precomputation import *


from globals import *

import attack_tables



import pawn
import knight
import bishop
import rook
import queen
import king

class Situation:
    def __init(self):
        self.white_pawns = WHITE_PAWNS_START
        self.white_knights = WHITE_KNIGHTS_START
        self.white_bishops = WHITE_BISHOPS_START
        self.white_rooks = WHITE_ROOKS_START
        self.white_queens = WHITE_QUEENS_START
        self.white_king = WHITE_KING_START

        self.black_pawns = BLACK_PAWNS_START
        self.black_knights = BLACK_KNIGHTS_START
        self.black_bishops = BLACK_BISHOPS_START
        self.black_rooks = BLACK_ROOKS_START
        self.black_queens = BLACK_QUEENS_START
        self.black_king = BLACK_KING_START

        self.white_turn = True


def get_all_pieces(situation):
    all_pieces = 0

    all_pieces |= situation.white_pawns
    all_pieces |= situation.white_knights
    all_pieces |= situation.white_bishops
    all_pieces |= situation.white_rooks
    all_pieces |= situation.white_queens
    all_pieces |= situation.white_king

    all_pieces |= situation.black_pawns
    all_pieces |= situation.black_knights
    all_pieces |= situation.black_bishops
    all_pieces |= situation.black_rooks
    all_pieces |= situation.black_queens
    all_pieces |= situation.black_king

    return all_pieces

def get_moves(situation):
    moves = []

    all_pieces = get_all_pieces(situation)

    if situation.white_turn:
        moves.extend(pawn.get_moves(situation.white_pawns, all_pieces, True))
        moves.extend(knight.get_moves(situation.white_knights, all_pieces))
        moves.extend(bishop.get_moves(situation.white_bishops, all_pieces))
        moves.extend(rook.get_moves(situation.white_rooks, all_pieces))
        moves.extend(queen.get_moves(situation.white_queens, all_pieces))
        moves.extend(king.get_moves(situation.white_king, all_pieces))
    else:
        moves.extend(pawn.get_moves(situation.black_pawns, all_pieces, False))
        moves.extend(knight.get_moves(situation.black_knights, all_pieces))
        moves.extend(bishop.get_moves(situation.black_bishops, all_pieces))
        moves.extend(rook.get_moves(situation.black_rooks, all_pieces))
        moves.extend(queen.get_moves(situation.black_queens, all_pieces))
        moves.extend(king.get_moves(situation.black_king, all_pieces))

    legal_moves = []

    for move in moves:
        if test_move(move, situation):
            legal_moves.append(move)


    return legal_moves



class ChessBoard:
    def __init__(self):
        
        self.situation = Situation()
        self.moves = []

    def execute_move(self, move):
        self.situation = generate_situation(move, self.situation)
        self.moves = get_moves(self.situation)


def test_move(move, situation):
    if is_attempting_to_capture_friendly_piece(move, situation):
        return False
    new_situation = generate_situation(move, situation)
    return is_friendly_king_in_check(new_situation)


def is_friendly_king_in_check(situation):
    pass

def is_attempting_to_capture_friendly_piece(move, situation):
    pass

# using this function assumes that the move is not trying to capture a friendly piece
def generate_situation(move, situation):
    new_situation = situation
    new_situation.white_turn = not situation.white_turn
    # TODO: content of function
    origin = get_origin_from_move(move)
    destination = get_destination_from_move(move)
    piece_type = get_piece_type_from_move(move)
    
    if piece_type == 0b001:
        promotion = get_promotion_from_move(move)

        if 


    return new_situation



        