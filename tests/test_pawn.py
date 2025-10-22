import pytest
from src.pawn import *
from src.attack_tables import get_attack_tables
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

#   1 0 1 1 1 0 1 0     BA
#   1 1 1 1 1 0 0 1     F9
#   0 0 1 0 1 0 1 0     2A
#   0 0 0 0 0 1 0 0     04
#   0 0 0 0 1 0 0 0     08
#   1 0 0 0 0 1 0 0     84
#   0 1 1 0 0 1 1 0     66
#   1 1 1 1 1 1 0 1     FD
ALL_PIECES_2  = 0xBAF92A04088466FD

#   0 0 0 0 0 0 0 0     00
#   0 0 0 1 0 0 0 1     11
#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 1 0 0 0     08
#   1 0 0 0 0 0 0 0     80
#   0 1 1 0 0 1 1 0     66
#   0 0 0 0 0 0 0 0     00
WHITE_PAWNS_2 = 0x0011000008806600

#   0 0 0 0 0 0 0 0     00
#   1 1 1 0 0 0 0 0     E0
#   0 0 0 0 1 0 1 0     0A
#   0 0 0 0 0 1 0 0     04
#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 0 0 0 0     00
BLACK_PAWNS_2 = 0x00E00A0400000000

BLACK_EXPECTED_MOVEMENT_MOVES = [
    #55->47 001 000
    0b110111101111001000,
    #55->39 001 000
    0b110111100111001000,
    #54->46 001 000
    0b110110101110001000,
    #54->38 001 000
    0b110110100110001000,
    #43->35 001 000
    0b101011100011001000,
    #34->26 001 000
    0b100010011010001000,
    #41->33 001 000
    0b101001100001001000
]

WHITE_EXPECTED_MOVEMENT_MOVES = [
    #23->31 001 000
    0b010111011111001000,
    #14->22 001 000
    0b001110010110001000,
    #14->30 001 000
    0b001110011110001000,
    #13->21 001 000
    0b001101010101001000,
    #13->29 001 000
    0b001101011101001000,
    #27->35 001 000
    0b011011100011001000,
    #9->17 001 000
    0b001001010001001000,
    #9->25 001 000
    0b001001011001001000,
]

WHITE_EXPECTED_CAPTURE_MOVES = [
    #14->23 001 000
    0b001110010111001000,
    #9->18 001 000
    0b001001010010001000,
    #27->34 001 000
    0b011011100010001000,

    #48->57 001 010
    0b110000111001001010,
    #48->57 001 011
    0b110000111001001011,
    #48->57 001 100
    0b110000111001001100,
    #48->57 001 101
    0b110000111001001101,

    #52->59 001 010
    0b110100111011001010,
    #52->59 001 011
    0b110100111011001011,
    #52->59 001 100
    0b110100111011001100,
    #52->59 001 101
    0b110100111011001101,

    #52->61 001 010
    0b110100111101001010,
    #52->61 001 011
    0b110100111101001011,
    #52->61 001 100
    0b110100111101001100,
    #52->61 001 101
    0b110100111101001101
]

BLACK_EXPECTED_CAPTURE_MOVES = [
    #54->45 001 000
    0b110110101101001000,
    #43->34 001 000
    0b101011100010001000,
    #41->34 001 000
    0b101001100010001000,
    #34->27 001 000
    0b100010011011001000
]

WHITE_EXPECTED_PROMOTION_MOVES = [
    #48->56 001 010
    0b110000111000001010,
    #48->56 001 011
    0b110000111000001011,
    #48->56 001 100
    0b110000111000001100,
    #48->56 001 101
    0b110000111000001101
]

BLACK_EXPECTED_PROMOTION_MOVES = []

WHITE_EXPECTED_ALL_MOVES =  WHITE_EXPECTED_MOVEMENT_MOVES \
                            + WHITE_EXPECTED_CAPTURE_MOVES \
                            + WHITE_EXPECTED_PROMOTION_MOVES

BLACK_EXPECTED_ALL_MOVES =  BLACK_EXPECTED_MOVEMENT_MOVES \
                            + BLACK_EXPECTED_CAPTURE_MOVES \
                            + BLACK_EXPECTED_PROMOTION_MOVES
test_cases = [
    pytest.param(
        generate_movement_moves_white,
        WHITE_PAWNS_2,
        ALL_PIECES_2,
        WHITE_EXPECTED_MOVEMENT_MOVES,
        id = "White pawn movement moves"
    ),

    pytest.param(
        generate_movement_moves_black,
        BLACK_PAWNS_2,
        ALL_PIECES_2,
        BLACK_EXPECTED_MOVEMENT_MOVES,
        id = "Black pawn movement moves"
    ),

    pytest.param(
        generate_capture_moves_white,
        WHITE_PAWNS_2,
        ALL_PIECES_2,
        WHITE_EXPECTED_CAPTURE_MOVES,
        id = "White pawn capture moves"
    ),

    pytest.param(
        generate_capture_moves_black,
        BLACK_PAWNS_2,
        ALL_PIECES_2,
        BLACK_EXPECTED_CAPTURE_MOVES,
        id = "Black pawn capture moves"
    ),

    pytest.param(
        generate_promotion_moves_white,
        WHITE_PAWNS_2,
        ALL_PIECES_2,
        WHITE_EXPECTED_PROMOTION_MOVES,
        id = "White pawn promotion moves"
    ),

    pytest.param(
        generate_promotion_moves_black,
        BLACK_PAWNS_2,
        ALL_PIECES_2,
        BLACK_EXPECTED_PROMOTION_MOVES,
        id = "Black pawn promotion moves"
    ),

    pytest.param(
        generate_moves_white,
        WHITE_PAWNS_2,
        ALL_PIECES_2,
        WHITE_EXPECTED_ALL_MOVES,
        id = "White pawn all moves"
    ),

    pytest.param(
        generate_moves_black,
        BLACK_PAWNS_2,
        ALL_PIECES_2,
        BLACK_EXPECTED_ALL_MOVES,
        id = "Black pawn all moves"
    ),
]




@pytest.mark.parametrize("function, location_board, all_pieces, expected", test_cases)
def test_move_generation(function, location_board, all_pieces, expected):
    result = function(location_board, all_pieces)




    assert sorted(result) == sorted(expected), (
        f"Failed test\n"
        f"  Expected:   \n{print_move_set(expected)}\n"
        f"  Got:        \n{print_move_set(result)}"
    )
