import pytest
from src.queen import get_attack_board, get_moves
from src.utils import print_bitboard, print_move_set, get_move_bits, show_block_value

#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 1 0 0 0     08
#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 0 0 0 0     00
#   0 1 0 0 0 0 0 0     40
#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 0 0 0 0     00
QUEENS = 0x0000080000400000

#   0 0 0 0 0 1 1 0     06
#   0 0 0 0 0 0 0 0     00
#   1 0 1 0 Q 0 1 0     AA
#   1 0 0 0 1 0 0 0     88
#   0 1 0 0 0 0 0 0     40
#   0 Q 0 0 1 0 0 0     48
#   0 0 1 0 0 1 0 0     24
#   0 1 0 0 0 0 0 0     40
ALL_PIECES = 0x0600AA8840482440





EXPECTED_MOVES = [
   get_move_bits(22,31,5),
   get_move_bits(22,30,5),
   get_move_bits(22,29,5),
   get_move_bits(22,36,5),
   get_move_bits(22,43,5),
   get_move_bits(22,23,5),
   get_move_bits(22,21,5),
   get_move_bits(22,20,5),
   get_move_bits(22,19,5),
   get_move_bits(22,15,5),
   get_move_bits(22,14,5),
   get_move_bits(22,13,5),
   get_move_bits(22,6,5),

   

   get_move_bits(43,59,5),
   get_move_bits(43,51,5),
   get_move_bits(43,57,5),
   get_move_bits(43,50,5),
   get_move_bits(43,42,5),
   get_move_bits(43,41,5),
   get_move_bits(43,34,5),
   get_move_bits(43,25,5),
   get_move_bits(43,16,5),
   get_move_bits(43,35,5),
   get_move_bits(43,36,5),
   get_move_bits(43,29,5),
   get_move_bits(43,22,5),
   get_move_bits(43,44,5),
   get_move_bits(43,45,5),
   get_move_bits(43,52,5),
   get_move_bits(43,61,5)
]

test_cases = [
    pytest.param(
        QUEENS,
        ALL_PIECES,
        EXPECTED_MOVES,
        id = "Get all queen moves"
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



#   0 0 1 0 1 0 1 0     2A
#   0 0 0 1 1 1 0 0     1C
#   0 0 1 1 1 1 1 0     3E
#   0 0 0 1 1 1 0 0     1C
#   1 1 1 0 0 0 1 0     E2
#   1 1 1 1 1 0 0 1     F9
#   1 1 1 0 0 0 0 0     E0
#   0 1 0 0 0 0 0 0     40
EXPECTED_ATTACK_BOARD = 0x2A1C3E1CE2F9E040


test_cases = [
    pytest.param(
        QUEENS,
        ALL_PIECES,
        EXPECTED_ATTACK_BOARD,
        id = "Get attack board for all queens"
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