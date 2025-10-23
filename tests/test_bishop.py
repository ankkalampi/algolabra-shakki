import pytest
from src.bishop import get_attack_board, get_moves, get_block_value
from src.utils import print_bitboard, print_move_set

#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 0 1 0 0     04
#   0 0 0 0 0 0 0 0     00
#   0 0 1 0 0 0 0 0     20
#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 0 0 0 0     00
BISHOPS = 0x0000040020000000

#   1 0 0 1 1 0 1 1     9B  
#   0 0 0 0 0 0 0 1     01
#   1 1 1 1 1 B 1 0     FE
#   0 0 0 0 0 0 0 0     00
#   0 1 B 0 1 0 0 0     68
#   1 0 1 1 0 1 1 1     B7
#   0 1 0 0 1 0 0 0     48
#   1 1 0 1 1 1 0 1     DD
ALL_PIECES = 0x9B01FE0068B748DD

# 2, 1, 0, 2
EXPECTED_BLOCK_VALUE_29 = 0b010001000010

# 2, 0, 3, 2
EXPECTED_BLOCK_VALUE_42 = 0b010000011010

test_cases = [
    pytest.param(
        29,
        ALL_PIECES,
        EXPECTED_BLOCK_VALUE_29,
        id = "Test bishop block value in square 29"
    ),

    pytest.param(
        42,
        ALL_PIECES,
        EXPECTED_BLOCK_VALUE_42,
        id = "Test bishop block value in square 42"
    )
]


@pytest.mark.parametrize("square, all_pieces, expected", test_cases)
def test_block_value(square, all_pieces, expected):
    result = get_block_value(square, all_pieces)


    assert result == expected, (
        f"Failed test\n"
        f"  Expected:   \n{(expected)}\n"
        f"  Got:        \n{(result)}"
    )


EXPECTED_MOVES = [
    #011000
    #29->36
    0b011101100100011000,
    #29->43
    0b011101101011011000,
    #29->20
    0b011101010100011000,
    #29->22
    0b011101010110011000,
    #29->15
    0b011101001111011000,
    #29->38
    0b011101100110011000,
    #29->47
    0b011101101111011000,
    #42->49
    0b101010110001011000,
    #42->56
    0b101010111000011000,
    #42->33
    0b101010100001011000,
    #42->24
    0b101010011000011000,
    #42->35
    0b101010100011011000,
    #42->28
    0b101010011100011000,
    #42->21
    0b101010010101011000,
    #42->51
    0b101010110011011000,
    #42->60
    0b101010111100011000
] 

test_cases = [
    pytest.param(
        BISHOPS,
        ALL_PIECES,
        EXPECTED_MOVES,
        id = "Get all bishop moves"
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



#   0 0 0 1 0 0 0 1     11
#   0 0 0 0 1 0 1 0     0A
#   1 0 0 0 1 0 0 0     88
#   0 1 0 1 1 0 1 0     5A
#   0 0 0 1 0 0 0 1     11
#   0 1 1 1 0 0 0 0     70
#   1 0 0 0 0 0 0 0     80
#   0 0 0 0 0 0 0 0     00
EXPECTED_ATTACK_BOARD = 0x110A885A11708000


test_cases = [
    pytest.param(
        BISHOPS,
        ALL_PIECES,
        EXPECTED_ATTACK_BOARD,
        id = "Get attack board for all bishops"
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