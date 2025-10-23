import math
from src.situation import Situation


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
    pass
