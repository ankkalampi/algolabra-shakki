import pytest
from src.situation import Situation, is_attempting_to_capture_friendly_piece

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