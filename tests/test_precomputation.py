import pytest
from src.precomputation import *

BOTTOM_RIGHT_CORNER = 0
TOP_RIGHT_CORNER = 56
BOTTOM_LEFT_CORNER = 7
TOP_LEFT_CORNER = 63
CENTER = 27


KNIGHT_BOTTOM_RIGHT_EXPECTED_BOARD = 0x0000000000020400
KNIGHT_BOTTOM_LEFT_EXPECTED_BOARD = 0x0000000000402000
KNIGHT_TOP_RIGHT_EXPECTED_BOARD = 0x0004020000000000
KNIGHT_TOP_LEFT_EXPECTED_BOARD = 0x0020400000000000
KNIGHT_CENTER_EXPECTED_BOARD = 0x0000142200221400

ROOK_BOTTOM_RIGHT_EXPECTED_BOARD = 0x01010101010101FE
ROOK_BOTTOM_LEFT_EXPECTED_BOARD = 0x808080808080807F
ROOK_TOP_RIGHT_EXPECTED_BOARD = 0xFE01010101010101
ROOK_TOP_LEFT_EXPECTED_BOARD = 0x7F80808080808080
ROOK_CENTER_EXPECTED_BOARD = 0x08080808F7080808

BISHOP_BOTTOM_RIGHT_EXPECTED_BOARD = 0x8040201008040200
BISHOP_BOTTOM_LEFT_EXPECTED_BOARD = 0x0102040810204000
BISHOP_TOP_RIGHT_EXPECTED_BOARD = 0x0002040810204080
BISHOP_TOP_LEFT_EXPECTED_BOARD = 0x0040201008040201
BISHOP_CENTER_EXPECTED_BOARD = 0x8041221400142241

QUEEN_BOTTOM_RIGHT_EXPECTED_BOARD = ROOK_BOTTOM_RIGHT_EXPECTED_BOARD | BISHOP_BOTTOM_RIGHT_EXPECTED_BOARD
QUEEN_BOTTOM_LEFT_EXPECTED_BOARD = ROOK_BOTTOM_LEFT_EXPECTED_BOARD | BISHOP_BOTTOM_LEFT_EXPECTED_BOARD
QUEEN_TOP_RIGHT_EXPECTED_BOARD = ROOK_TOP_RIGHT_EXPECTED_BOARD | BISHOP_TOP_RIGHT_EXPECTED_BOARD
QUEEN_TOP_LEFT_EXPECTED_BOARD = ROOK_TOP_LEFT_EXPECTED_BOARD | BISHOP_TOP_LEFT_EXPECTED_BOARD
QUEEN_CENTER_EXPECTED_BOARD = ROOK_CENTER_EXPECTED_BOARD | BISHOP_CENTER_EXPECTED_BOARD

KING_BOTTOM_RIGHT_EXPECTED_BOARD = 0x0000000000000302
KING_BOTTOM_LEFT_EXPECTED_BOARD = 0x000000000000C040
KING_TOP_RIGHT_EXPECTED_BOARD = 0x0203000000000000
KING_TOP_LEFT_EXPECTED_BOARD = 0x40C0000000000000
KING_CENTER_EXPECTED_BOARD = 0x0000001C141C0000


test_cases = [
    pytest.param(
        precompute_single_knight_attack_table,
        BOTTOM_RIGHT_CORNER,
        KNIGHT_BOTTOM_RIGHT_EXPECTED_BOARD,
        id="Knight attack table in bottom right corner"
    ),
    pytest.param(
        precompute_single_knight_attack_table,
        BOTTOM_LEFT_CORNER,
        KNIGHT_BOTTOM_LEFT_EXPECTED_BOARD,
        id="Knight attack table in bottom left corner"
    ),
    pytest.param(
        precompute_single_knight_attack_table,
        TOP_RIGHT_CORNER,
        KNIGHT_TOP_RIGHT_EXPECTED_BOARD,
        id="Knight attack table in top right corner"
    ),
    pytest.param(
        precompute_single_knight_attack_table,
        TOP_LEFT_CORNER,
        KNIGHT_TOP_LEFT_EXPECTED_BOARD,
        id="Knight attack table in top left corner"
    ),
    pytest.param(
        precompute_single_knight_attack_table,
        CENTER,
        KNIGHT_CENTER_EXPECTED_BOARD,
        id="Knight attack table in center square (index 27)"
    ),

    pytest.param(
        precompute_single_rook_attack_table,
        BOTTOM_RIGHT_CORNER,
        ROOK_BOTTOM_RIGHT_EXPECTED_BOARD,
        id="Rook attack table in bottom right corner"
    ),
    pytest.param(
        precompute_single_rook_attack_table,
        BOTTOM_LEFT_CORNER,
        ROOK_BOTTOM_LEFT_EXPECTED_BOARD,
        id="Rook attack table in bottom left corner"
    ),
    pytest.param(
        precompute_single_rook_attack_table,
        TOP_RIGHT_CORNER,
        ROOK_TOP_RIGHT_EXPECTED_BOARD,
        id="Rook attack table in top right corner"
    ),
    pytest.param(
        precompute_single_rook_attack_table,
        TOP_LEFT_CORNER,
        ROOK_TOP_LEFT_EXPECTED_BOARD,
        id="Rook attack table in top left corner"
    ),
    pytest.param(
        precompute_single_rook_attack_table,
        CENTER,
        ROOK_CENTER_EXPECTED_BOARD,
        id="Rook attack table in center square (index 27)"
    ),

    pytest.param(
        precompute_single_bishop_attack_table,
        BOTTOM_RIGHT_CORNER,
        BISHOP_BOTTOM_RIGHT_EXPECTED_BOARD,
        id="Bishop attack table in bottom right corner"
    ),
    pytest.param(
        precompute_single_bishop_attack_table,
        BOTTOM_LEFT_CORNER,
        BISHOP_BOTTOM_LEFT_EXPECTED_BOARD,
        id="Bishop attack table in bottom left corner"
    ),
    pytest.param(
        precompute_single_bishop_attack_table,
        TOP_RIGHT_CORNER,
        BISHOP_TOP_RIGHT_EXPECTED_BOARD,
        id="Bishop attack table in top right corner"
    ),
    pytest.param(
        precompute_single_bishop_attack_table,
        TOP_LEFT_CORNER,
        BISHOP_TOP_LEFT_EXPECTED_BOARD,
        id="Bishop attack table in top left corner"
    ),
    pytest.param(
        precompute_single_bishop_attack_table,
        CENTER,
        BISHOP_CENTER_EXPECTED_BOARD,
        id="Bishop attack table in center square (index 27)"
    ),

    pytest.param(
        precompute_single_queen_attack_table,
        BOTTOM_RIGHT_CORNER,
        QUEEN_BOTTOM_RIGHT_EXPECTED_BOARD,
        id="Queen attack table in bottom right corner"
    ),
    pytest.param(
        precompute_single_queen_attack_table,
        BOTTOM_LEFT_CORNER,
        QUEEN_BOTTOM_LEFT_EXPECTED_BOARD,
        id="Queen attack table in bottom left corner"
    ),
    pytest.param(
        precompute_single_queen_attack_table,
        TOP_RIGHT_CORNER,
        QUEEN_TOP_RIGHT_EXPECTED_BOARD,
        id="Queen attack table in top right corner"
    ),
    pytest.param(
        precompute_single_queen_attack_table,
        TOP_LEFT_CORNER,
        QUEEN_TOP_LEFT_EXPECTED_BOARD,
        id="Queen attack table in top left corner"
    ),
    pytest.param(
        precompute_single_queen_attack_table,
        CENTER,
        QUEEN_CENTER_EXPECTED_BOARD,
        id="Queen attack table in center square (index 27)"
    ),
]

@pytest.mark.parametrize("function, square_value, expected", test_cases)
def test_single_attack_bitboard_precomputations(function, square_value, expected):
    bitboard = function(square_value)

    assert bitboard == expected, (
        f"Failed with input square {square_value}:\n"
        f"  Expected:   {format_bitboard(expected)}\n"
        f"  Got:        {format_bitboard(bitboard)}"
    )

def format_bitboard(bitboard):
    return format(bitboard, '016x')

