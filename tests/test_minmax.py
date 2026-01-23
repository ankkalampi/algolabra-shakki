import pytest, math
from src.minmax import minmax
from src.situation import Situation




CHECK_IN_THREE = Situation()
CHECK_IN_THREE.black_bishops = 0
CHECK_IN_THREE.black_knights = 0x4040000000000000
CHECK_IN_THREE.black_queens = 0
CHECK_IN_THREE.black_pawns = 0x0000000000000000
CHECK_IN_THREE.black_rooks = 0x0000000000004000
CHECK_IN_THREE.black_king = 0x0002000000000000
CHECK_IN_THREE.white_bishops = 0
CHECK_IN_THREE.white_knights = 0
CHECK_IN_THREE.white_queens =   0x0000000000080000
CHECK_IN_THREE.white_pawns = 0
CHECK_IN_THREE.white_rooks =    0x0000000004000000
CHECK_IN_THREE.white_king =     0x0000000000000001

CHECK_IN_FIVE = Situation()
CHECK_IN_FIVE.black_bishops = 0
CHECK_IN_FIVE.black_knights = 0x4040000000000000
CHECK_IN_FIVE.black_queens = 0
CHECK_IN_FIVE.black_pawns = 0x0000000000000000
CHECK_IN_FIVE.black_rooks = 0x0000000000004000
CHECK_IN_FIVE.black_king = 0x0400000000000000
CHECK_IN_FIVE.white_bishops = 0
CHECK_IN_FIVE.white_knights = 0
CHECK_IN_FIVE.white_queens =   0x0000000000080000
CHECK_IN_FIVE.white_pawns = 0
CHECK_IN_FIVE.white_rooks =    0x0000000010000000
CHECK_IN_FIVE.white_king =     0x0000000000000001

CHECK_IN_ONE = Situation()
CHECK_IN_ONE.black_bishops = 0
CHECK_IN_ONE.black_knights = 0x4040000000000000
CHECK_IN_ONE.black_queens = 0
CHECK_IN_ONE.black_pawns = 0x0000000000000000
CHECK_IN_ONE.black_rooks = 0x0000000000004000
CHECK_IN_ONE.black_king = 0x0000010000000000
CHECK_IN_ONE.white_bishops = 0
CHECK_IN_ONE.white_knights = 0
CHECK_IN_ONE.white_queens =   0x0000000000020000
CHECK_IN_ONE.white_pawns = 0
CHECK_IN_ONE.white_rooks =    0x0000000004000000
CHECK_IN_ONE.white_king =     0x0000000000000001

CHECK_IN_FIVE_EXPECTED = 0b011100011010100000 # 28-> 26 rook no promotion
CHECK_IN_THREE_EXPECTED = 0b010011010001101000 # 19-> 17 queen no promotion
CHECK_IN_ONE_EXPECTED = 0b011010011000100000 # 26-> 24 rook no promotion

CHECKMATE_VALUE = 10000




def test_correct_move_and_correct_value_minmax_in_check_in_three():
    points, result = minmax(CHECK_IN_THREE, 3, -math.inf, math.inf, True)
    assert result == CHECK_IN_THREE_EXPECTED
    assert points == CHECKMATE_VALUE

def test_correct_move_and_correct_value_minmax_in_check_in_one():
    points, result = minmax(CHECK_IN_ONE, 3, -math.inf, math.inf, True)
    assert result == CHECK_IN_ONE_EXPECTED
    assert points == CHECKMATE_VALUE

"""
def test_correct_move_minmax_in_check_in_five():
    points, result = minmax(CHECK_IN_FIVE, 3, -math.inf, math.inf, True)
    assert result == CHECK_IN_FIVE_EXPECTED
"""




