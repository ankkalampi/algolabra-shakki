import pytest
from src.pawn import *
from src.attack_tables import get_attack_tables
from tests.test_situation import mock_situation
from src.pawn import get_double_move_board
from src.utils import *


#   1 0 1 1 1 0 1 1     BB
#   1 1 1 1 1 0 0 1     F9
#   0 0 1 0 1 0 1 0     2A
#   0 0 0 0 0 1 0 0     04
#   0 0 0 1 1 0 0 0     18
#   1 0 0 0 0 1 0 0     84
#   0 1 1 0 0 1 1 1     67
#   1 1 1 1 1 1 0 1     FD
ALL_PIECES  = 0xBBF92A04188467FD


#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 0 0 0 0     00
#   0 0 0 1 1 0 0 0     18
#   1 0 0 0 0 0 0 0     80
#   0 1 1 0 0 1 1 1     67
#   0 0 0 0 0 0 0 0     00
WHITE_PAWNS = 0x0000000018806700


#   0 0 0 0 0 0 0 0     00
#   1 1 1 1 0 0 0 1     F1
#   0 0 0 0 1 0 1 0     0A
#   0 0 0 0 0 1 0 0     04
#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 0 0 0 0     00
BLACK_PAWNS = 0x00F10A0400000000


#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 0 0 0 0     00
#   0 1 1 0 0 0 1 1     63
#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 0 0 0 0     00
WHITE_EXPECTED_DOUBLE = 0x00000063000000


#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 0 0 0 0     00
#   1 1 0 1 0 0 0 1     D1
#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 0 0 0 0     00
BLACK_EXPECTED_DOUBLE = 0x000000D100000000


#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 0 0 0 0     00
#   0 0 0 1 1 0 0 0     18
#   1 0 0 0 0 0 0 0     80
#   0 1 1 0 0 0 1 1     63
#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 0 0 0 0     00
WHITE_EXPECTED_SINGLE = 0x0000001880630000


#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 0 0 0 0     00
#   1 1 0 1 0 0 0 1     D1
#   0 0 0 0 1 0 1 0     0A
#   0 0 0 0 0 1 0 0     04
#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 0 0 0 0     00
BLACK_EXPECTED_SINGLE = 0x0000D10A04000000


#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 0 0 0 0     00
#   0 0 1 1 1 1 0 0     3C
#   0 1 0 0 0 0 0 0     40
#   1 1 1 1 1 1 1 1     FF
#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 0 0 0 0     00
WHITE_EXPECTED_CAPTURE = 0x0000003C40FF0000


#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 0 0 0 0     00
#   1 1 1 1 1 0 1 0     FA
#   0 0 0 1 0 1 0 1     15
#   0 0 0 0 1 0 1 0     0A
#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 0 0 0 0     00
BLACK_EXPECTED_CAPTURE = 0x0000FA150A000000


test_cases = [
    pytest.param(
        get_single_move_board,
        WHITE_PAWNS,
        ALL_PIECES,
        True,
        WHITE_EXPECTED_SINGLE,
        id = "White single move board"
    ),
    pytest.param(
        get_double_move_board,
        WHITE_PAWNS,
        ALL_PIECES,
        True,
        WHITE_EXPECTED_DOUBLE,
        id = "White double move board"
    ),
    pytest.param(
        get_capture_board,
        WHITE_PAWNS,
        ALL_PIECES,
        True,
        WHITE_EXPECTED_CAPTURE,
        id = "White capture board"
    ),

    pytest.param(
        get_single_move_board,
        BLACK_PAWNS,
        ALL_PIECES,
        False,
        BLACK_EXPECTED_SINGLE,
        id = "Black single move board"
    ),
    pytest.param(
        get_double_move_board,
        BLACK_PAWNS,
        ALL_PIECES,
        False,
        BLACK_EXPECTED_DOUBLE,
        id = "Black double move board"
    ),
    pytest.param(
        get_capture_board,
        BLACK_PAWNS,
        ALL_PIECES,
        False,
        BLACK_EXPECTED_CAPTURE,
        id = "Black capture board"
    )
]







@pytest.mark.parametrize("function, location_board, all_pieces, is_white, expected", test_cases)
def test_get_pawn_move_and_attack_board(function, location_board, all_pieces, is_white, expected):
    result = function(location_board, all_pieces, is_white)


    assert result == expected, (
        f"Failed test\n"
        f"  Expected:   \n{print_bitboard(expected)}\n"
        f"  Got:        \n{print_bitboard(result)}"
    )
