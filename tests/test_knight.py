import pytest
from src.knight import get_attack_board, get_moves
from src.utils import print_bitboard, print_move_set

#   1 0 0 1 1 0 0 1     99
#   0 1 0 1 0 1 1 0     56
#   1 0 1 1 1 1 0 1     BD
#   0 1 1 0 1 0 1 0     6A
#   0 0 0 1 1 0 0 0     18
#   0 1 0 1 0 1 0 0     54
#   1 0 1 0 0 0 1 1     A2
#   1 0 1 1 1 0 0 1     B9
ALL_PIECES = 0x9956BD6A1854A2B9

#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 0 0 0 0     00
#   0 1 0 0 1 0 0 0     48
#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 0 0 0 0     00
WHITE_KNIGHTS = 0x0000004800000000

#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 0 0 0 0     00
#   0 0 1 0 0 1 0 0     24
#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 0 0 0 0     00
BLACK_KNIGHTS = 0x0000240000000000


#   0 0 0 0 0 0 0 0     00
#   1 0 1 1 0 1 0 0     B4
#   0 0 1 1 0 0 1 0     32
#   0 0 0 0 0 0 0 0     00
#   0 0 1 1 0 0 1 0     32
#   1 0 1 1 0 1 0 0     B4
#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 0 0 0 0     00
WHITE_EXPECTED_ATTACK_BOARD = 0x00B4320032B40000


#   0 1 0 1 1 0 1 0     5A
#   1 0 0 1 1 0 0 1     99
#   0 0 0 0 0 0 0 0     00
#   1 0 0 1 1 0 0 1     99
#   0 1 0 1 1 0 1 0     5A
#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 0 0 0 0     00
BLACK_EXPECTED_ATTACK_BOARD = 0x5A9900995A000000


test_cases = [
    pytest.param(
        WHITE_KNIGHTS,
        ALL_PIECES,
        WHITE_EXPECTED_ATTACK_BOARD,
        id = "Knight attack board for white"
    ),

    pytest.param(
        BLACK_KNIGHTS,
        ALL_PIECES,
        BLACK_EXPECTED_ATTACK_BOARD,
        id = "Knight attack board for black"
    ),


]

@pytest.mark.parametrize("location_board, all_pieces, expected", test_cases)
def test_get_knight_attack_board(location_board, all_pieces, expected):
    result = get_attack_board(location_board, all_pieces)


    assert result == expected, (
        f"Failed test\n"
        f"  Expected:   \n{print_bitboard(expected)}\n"
        f"  Got:        \n{print_bitboard(result)}"
    )

WHITE_EXPECTED_MOVES = [
    #35->50
    0b100011110010010000,
    #35->41
    0b100011101001010000,
    #35->25
    0b100011011001010000,
    #35->18
    0b100011010010010000,
    #35->20
    0b100011010100010000,
    #35->29
    0b100011011101010000,
    #35->45
    0b100011101101010000,
    #35->52
    0b100011110100010000,
    #38->53
    0b100110110101010000,
    #38->44
    0b100110101100010000,
    #38->28
    0b100110011100010000,
    #38->21
    0b100110010101010000,
    #38->23
    0b100110010111010000,
    #38->55
    0b100110110111010000
]

test_cases = [
    pytest.param(
        WHITE_KNIGHTS,
        ALL_PIECES,
        WHITE_EXPECTED_MOVES,
        id = "Get knight moves"
    )

]



@pytest.mark.parametrize("location_board, all_pieces, expected", test_cases)
def test_get_knight_moves(location_board, all_pieces, expected):
    result = get_moves(location_board, all_pieces)


    assert sorted(result) == sorted(expected), (
        f"Failed test\n"
        f"  Expected:   \n{print_move_set(expected)}\n"
        f"  Got:        \n{print_move_set(result)}"
    )