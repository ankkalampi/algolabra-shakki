import pytest
from src.king import get_attack_board, get_moves
from src.utils import print_bitboard, print_move_set, get_move_bits

#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 0 0 0 0     00
#   0 0 0 1 0 0 0 0     10
KING = 0x0000000000000010

#   0 0 0 0 0 1 1 0     06
#   0 0 0 0 0 0 0 0     00
#   1 0 1 0 1 0 1 0     AA
#   1 0 0 0 1 0 0 0     88
#   0 1 0 0 0 0 0 0     40
#   0 1 0 0 1 0 0 0     48
#   0 0 1 0 0 1 0 0     24
#   0 1 0 1 0 0 0 0     50
ALL_PIECES = 0x0600AA8840482450





EXPECTED_MOVES = [
   get_move_bits(4,5,6),
   get_move_bits(4,3,6),
   get_move_bits(4,13,6),
   get_move_bits(4,12,6),
   get_move_bits(4,11,6),
]

test_cases = [
    pytest.param(
        KING,
        ALL_PIECES,
        EXPECTED_MOVES,
        id = "Get all king moves"
    )
]

@pytest.mark.parametrize("location_board, all_pieces, expected", test_cases)
def test_get_moves(location_board, all_pieces, expected):
    result = get_moves(location_board, all_pieces)


    assert sorted(result) == sorted(expected), (
        f"Failed test\n"
        f"  Expected:   \n{print_move_set(expected)}\n"
        f"  Got:        \n{print_move_set(result)}"
    )



#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 0 0 0 0     00
#   0 0 1 1 1 0 0 0     38
#   0 0 1 0 1 0 0 0     28
EXPECTED_ATTACK_BOARD = 0x0000000000003828


test_cases = [
    pytest.param(
        KING,
        ALL_PIECES,
        EXPECTED_ATTACK_BOARD,
        id = "Get attack board for the king"
    )
]

@pytest.mark.parametrize("location_board, all_pieces, expected", test_cases)
def test_get_attack_board(location_board, all_pieces, expected):
    result = get_attack_board(location_board, all_pieces)


    assert result == expected, (
        f"Failed test\n"
        f"  Expected:   \n{print_bitboard(expected)}\n"
        f"  Got:        \n{print_bitboard(result)}"
    )