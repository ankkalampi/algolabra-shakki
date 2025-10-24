import math
from src.situation import Situation
from src.utils import *


PAWN_VALUE = 1
KNIGHT_VALUE = 3
BISHOP_VALUE = 3
ROOK_VALUE = 5
QUEEN_VALUE = 8

ENEMY_TERRITORY_BONUS = 3
CENTER_BONUS = 1
CHECK_BONUS = 5

ENDGAME_PIECE_AMOUNT = 14


def evaluate_situation(situation):
    """
    Returns numerical value to situation

    Args:
    situation: situation object

    Returns:
    integer value
    """
    points = 0
    white_pawns = situation.white_pawns
    white_knights = situation.white_knights
    white_bishops = situation.white_bishops
    white_rooks = situation.white_rooks
    white_queens = situation.white_queens
    white_king = situation.white_king

    black_pawns = situation.black_pawns
    black_knights = situation.black_knights
    black_bishops = situation.black_bishops
    black_rooks = situation.black_rooks
    black_queens = situation.black_queens
    black_king = situation.black_king

    points += calculate(white_pawns, PAWN_VALUE)
    points += calculate(white_knights, PAWN_VALUE)
    points += calculate(white_rooks, PAWN_VALUE)
    points += calculate(white_queens, PAWN_VALUE)
    

    points -= calculate(black_pawns, PAWN_VALUE)
    points -= calculate(black_pawns, PAWN_VALUE)
    points -= calculate(black_pawns, PAWN_VALUE)
    points -= calculate(black_pawns, PAWN_VALUE)

    return points
    



def calculate(pieces, value):
    points = 0
    while(pieces):
        piece = bitscan(pieces)
        pieces &= pieces -1

        points += value

        return points
        
