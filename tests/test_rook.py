import pytest
from src.rook import get_attack_board, get_moves, get_block_value
from src.utils import print_bitboard, print_move_set, get_move_bits, show_block_value

#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 1 0 0 0     08
#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 0 0 0 0     00
#   0 1 0 0 0 0 0 0     40
#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 0 0 0 0     00
ROOKS = 0x0000080000400000

#   0 0 0 0 0 1 1 0     06
#   0 0 0 0 0 0 0 0     00
#   1 0 1 0 B 0 1 0     AA
#   1 0 0 0 1 0 0 0     88
#   0 1 0 0 0 0 0 0     40
#   0 B 0 0 1 0 0 0     48
#   0 0 1 0 0 1 0 0     24
#   0 1 0 0 0 0 0 0     40
ALL_PIECES = 0x0600AA8840482440

# 1,3,2,0
EXPECTED_BLOCK_VALUE_22 = 0b001011010000

# 0,2,1,2
EXPECTED_BLOCK_VALUE_43 = 0b000010001010

test_cases = [
    pytest.param(
        22,
        ALL_PIECES,
        EXPECTED_BLOCK_VALUE_22,
        id = "Test rook block value in square 22"
    ),

    pytest.param(
        43,
        ALL_PIECES,
        EXPECTED_BLOCK_VALUE_43,
        id = "Test rook block value in square 43"
    )
]


@pytest.mark.parametrize("square, all_pieces, expected", test_cases)
def test_block_value(square, all_pieces, expected):
    result = get_block_value(square, all_pieces)


    assert result == expected, (
        f"Failed test\n"
        f"  Expected:   \n{(show_block_value(expected))}\n"
        f"  Got:        \n{(show_block_value(result))}"
    )


EXPECTED_MOVES = [
   get_move_bits(22,21,4),
   get_move_bits(22,20,4),
   get_move_bits(22,19,4),
   get_move_bits(22,14,4),
   get_move_bits(22,6,4),
   get_move_bits(22,23,4),
   get_move_bits(22,30,4),

   get_move_bits(43,42,4),
   get_move_bits(43,41,4),
   get_move_bits(43,35,4),
   get_move_bits(43,44,4),
   get_move_bits(43,45,4),
   get_move_bits(43,51,4),
   get_move_bits(43,59,4),
   
   
] 

test_cases = [
    pytest.param(
        ROOKS,
        ALL_PIECES,
        EXPECTED_MOVES,
        id = "Get all rook moves"
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



#   0 0 0 0 1 0 0 0     08
#   0 0 0 0 1 0 0 0     08
#   0 0 1 1 0 1 1 0     36
#   0 0 0 0 1 0 0 0     08
#   0 1 0 0 0 0 0 0     40
#   1 0 1 1 1 0 0 0     B8
#   0 1 0 0 0 0 0 0     40
#   0 1 0 0 0 0 0 0     40
EXPECTED_ATTACK_BOARD = 0x0808360840B84040


test_cases = [
    pytest.param(
        ROOKS,
        ALL_PIECES,
        EXPECTED_ATTACK_BOARD,
        id = "Get attack board for all rooks"
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