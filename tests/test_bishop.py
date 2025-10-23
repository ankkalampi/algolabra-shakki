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
EXPECTED_BLOCK_VALUE_29 = 0b010000001010

# 2, 0, 3, 2
EXPECTED_BLOCK_VALUE_42 = 0b010011000010

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
def test_bishop_block_value(square, all_pieces, expected):
    result = get_block_value(square, all_pieces)


    assert result == expected, (
        f"Failed test\n"
        f"  Expected:   \n{(expected)}\n"
        f"  Got:        \n{(result)}"
    )