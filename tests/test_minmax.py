import pytest, math
from src.minmax import minmax
from src.situation import Situation

#   0 0 0 0 0 0 0 0
#   0 0 0 0 0 0 k 0 
#   0 0 0 0 0 0 0 0
#   0 0 0 0 0 Q 0 0
#   0 0 0 0 0 0 0 R
#   0 0 0 0 0 0 0 0 
#   0 0 0 0 0 0 0 0
#   0 0 0 0 0 0 0 0
ABOUT_TO_CHECK = Situation()
ABOUT_TO_CHECK.black_bishops = 0
ABOUT_TO_CHECK.black_knights = 0
ABOUT_TO_CHECK.black_queens = 0
ABOUT_TO_CHECK.black_pawns = 0
ABOUT_TO_CHECK.black_rooks = 0
ABOUT_TO_CHECK.black_king = 0x0002000000000000
ABOUT_TO_CHECK.white_bishops = 0
ABOUT_TO_CHECK.white_knights = 0
ABOUT_TO_CHECK.white_queens =   0x0000000400000000
ABOUT_TO_CHECK.white_pawns = 0
ABOUT_TO_CHECK.white_rooks =    0x0000000001000000
ABOUT_TO_CHECK.white_king =     0x0000000000000001

ABOUT_TO_CHECK_EXPECTED = 0b011000011001100000


def test_correct_move_minmax_in_about_to_check():
    points, result = minmax(ABOUT_TO_CHECK, 4, -math.inf, math.inf, True)
    assert result == ABOUT_TO_CHECK_EXPECTED
   

def test_correct_move_value_minmax_in_about_to_check():
    points, result = minmax(ABOUT_TO_CHECK, 4, -math.inf, math.inf, True)
    assert points == 10000