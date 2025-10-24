import pytest
from src.situation import Situation, is_attempting_to_capture_friendly_piece, is_friendly_king_in_check, generate_situation
from src.utils import print_bitboard, print_move
@pytest.fixture
def mock_situation():
    sit = Situation()
    sit.white_pawns =       0x0000000040279800
    sit.white_knights =     0x0000000000000042
    sit.white_bishops =     0x0000000000800004
    sit.white_rooks =       0x0000000000000180
    sit.white_queens =      0x0000000000000400
    sit.white_king =        0x0000000000000010

    sit.black_pawns =       0x0000619A04000000
    sit.black_knights =     0x0000840000000000
    sit.black_bishops =     0x0000100400000000
    sit.black_rooks =       0x8100000000000000
    sit.black_queens =      0x0000000100000000
    sit.black_king =        0x1000000000000000

    sit.white_turn = True

    return sit

# TEST MOVES
WHITE_CAPTURES_FRIENDLY =   0b001011010010001000
WHITE_CAPTURES_HOSTILE =    0b001010101110101000
WHITE_ONLY_MOVES =          0b000010001001011000

BLACK_CAPTURES_FRIENDLY =   0b111111101111100000
BLACK_CAPTURES_HOSTILE =    0b011010010001001000
BLACK_ONLY_MOVES =          0b101111100101010000




test_cases = [
    pytest.param(
        WHITE_CAPTURES_FRIENDLY,
        True,
        True,
        id="White is attempting to capture friendly piece"
        ),

    pytest.param(
        WHITE_CAPTURES_HOSTILE,
        True,
        False,
        id="White is attempting to capture hostile piece"
        ),

    pytest.param(
        WHITE_ONLY_MOVES,
        True,
        False,
        id="White moves but doesn't capture"
        ),

    
    pytest.param(
        BLACK_CAPTURES_FRIENDLY,
        False,
        True,
        id="Black is attempting to capture friendly piece"
        ),

    pytest.param(
        BLACK_CAPTURES_HOSTILE,
        False,
        False,
        id="Black is attempting to capture hostile piece"
        ),

    pytest.param(
        BLACK_ONLY_MOVES,
        False,
        False,
        id="Black moves but doesn't capture"
        ),
]



@pytest.mark.parametrize("move, white_turn, expected", test_cases)
def test_is_attempting_to_capture_friendly_piece(move, white_turn, expected, mock_situation):
    mock_situation.white_turn = white_turn
    result = is_attempting_to_capture_friendly_piece(move, mock_situation)


    assert result == expected, (
        f"Failed test\n"
        f"  Expected:   {expected}\n"
        f"  Got:        {result}"
    )


def mock_situation_in_white_check(situation):
    sit = situation
    sit.black_queens = 0x0000000000400000
    sit.white_bishops = 0x0000000000900000
    return sit


def mock_situation_in_black_check(situation):
    sit = situation
    sit.white_bishops = 0x0048000000000000
    sit.white_turn = False
    return sit


def mock_situation_not_in_white_check(situation):
    sit = situation
    sit.black_queens =  0x0000000000400000
    sit.white_pawns =   0x000000004007B800
    sit.black_bishops = 0x0000000400004000
    return sit


def mock_situation_not_in_black_check(situation):
    sit = situation
    sit.white_queens = 0x0001000000000000
    sit.white_turn = False
    return sit


# TEST MOVES
WHITE_ESCAPE_CHECK_SUCCESS =    0b000100000011110000
WHITE_ESCAPE_CHECK_FAIL =       0b000100001101110000
WHITE_MOVE_INTO_CHECK =         0b000100000101110000
WHITE_BLOCK_CHECK =             0b010100001101011000
WHITE_MOVE_WITHOUT_CHECK =      0b001011010011001000
WHITE_DISCOVER_CHECK =          0b001101010101001000

BLACK_ESCAPE_CHECK_SUCCESS =    0b111100110100110000
BLACK_ESCAPE_CHECK_FAIL =       0b111000111001100000
BLACK_MOVE_INTO_CHECK =         0b111100110011110000

BLACK_MOVE_WITHOUT_CHECK =      0b111100111101110000


test_cases = [
    pytest.param(
        mock_situation_in_white_check,
        WHITE_ESCAPE_CHECK_SUCCESS,
        False,
        id="White is in check but escapes"
        ),
    pytest.param(
        mock_situation_in_white_check,
        WHITE_ESCAPE_CHECK_FAIL,
        True,
        id="White is in check and fails to escape"
        ),
    pytest.param(
        mock_situation_in_white_check,
        WHITE_BLOCK_CHECK,
        False,
        id="White is in check but blocks it"
        ),
    pytest.param(
        mock_situation_not_in_white_check,
        WHITE_MOVE_INTO_CHECK,
        True,
        id="White wasn't in check, moves into check"
        ),
    pytest.param(
        mock_situation_not_in_white_check,
        WHITE_MOVE_WITHOUT_CHECK,
        False,
        id="White wasn't in check, and still isn't"
        ),

    pytest.param(
        mock_situation_in_black_check,
        BLACK_ESCAPE_CHECK_SUCCESS,
        False,
        id="Black is in check but escapes"
        ),
    pytest.param(
        mock_situation_in_black_check,
        BLACK_ESCAPE_CHECK_FAIL,
        True,
        id="Black is in check and fails to escape"
        ),
    
    pytest.param(
        mock_situation_not_in_black_check,
        BLACK_MOVE_INTO_CHECK,
        True,
        id="Black wasn't in check, moves into check"
        ),
    pytest.param(
        mock_situation_not_in_black_check,
        BLACK_MOVE_WITHOUT_CHECK,
        False,
        id="Black wasn't in check, and still isn't"
        ),
    ]

@pytest.mark.parametrize("function, move, expected", test_cases)
def test_is_friendly_king_in_check(function, move, expected, mock_situation):
    situation = function(mock_situation)
    situation = generate_situation(move, situation)
    result = is_friendly_king_in_check(situation)

    assert result == expected, (
        f"Failed test\n"
        f"  Expected:\n"
        f"{expected}\n"
        f"  Got:\n"
        f"{result}"
    )

#   0 0 0 0 0 0 0 0     00     
#   0 0 0 0 1 0 0 0     08
#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 0 0 0 0     00
#   0 0 0 0 0 0 0 0     00
BLACK_KING_NEW_POSITION = 0x0008000000000000






test_cases = [
    pytest.param(
        mock_situation_not_in_black_check,
        BLACK_MOVE_INTO_CHECK,
        BLACK_KING_NEW_POSITION,
        id="Moving black king"
        )
    ]



@pytest.mark.parametrize("function, move, expected", test_cases)
def test_generate_situation(function, move, expected, mock_situation):
    situation = function(mock_situation)
    
    situation = generate_situation(move, situation)
    print_move(move)
    print(print_bitboard(situation.black_king))
    result = situation.black_king
    

    assert result == expected, (
        f"Failed test\n"
        f"  Expected:\n"
        f"{print_bitboard(expected)}\n"
        f"  Got:\n"
        f"{print_bitboard(result)}"
    )