import pytest, math
from src.minmax import minmax
from src.situation import Situation


#   0 0 0 0 0 0 0 0
#   0 0 0 0 0 0 k 0 
#   0 0 0 0 0 0 0 0
#   0 0 0 0 0 Q 0 0
#   0 0 0 0 0 0 0 R
#   0 0 0 0 0 0 0 0 
#   0 0 0 0 0 0 0 0
#   0 0 0 0 0 0 0 K
#ABOUT_TO_CHECK = Situation()
#ABOUT_TO_CHECK.black_bishops = 0
#ABOUT_TO_CHECK.black_knights = 0
#ABOUT_TO_CHECK.black_queens = 0
#ABOUT_TO_CHECK.black_pawns = 0
#ABOUT_TO_CHECK.black_rooks = 0
#ABOUT_TO_CHECK.black_king = 0x0002000000000000
#ABOUT_TO_CHECK.white_bishops = 0
#ABOUT_TO_CHECK.white_knights = 0
#ABOUT_TO_CHECK.white_queens =   0x0000000400000000
#ABOUT_TO_CHECK.white_pawns = 0
#ABOUT_TO_CHECK.white_rooks =    0x0000000001000000
#ABOUT_TO_CHECK.white_king =     0x0000000000000001
#
#ABOUT_TO_CHECK_EXPECTED = 0b011000011001100000


CHECK_IN_TWO = Situation()
CHECK_IN_TWO.black_bishops = 0
CHECK_IN_TWO.black_knights = 0x0020000000000000
CHECK_IN_TWO.black_queens = 0
CHECK_IN_TWO.black_pawns = 0x00C0000000000000
CHECK_IN_TWO.black_rooks = 0
CHECK_IN_TWO.black_king = 0x0200000000000000
CHECK_IN_TWO.white_bishops = 0
CHECK_IN_TWO.white_knights = 0
CHECK_IN_TWO.white_queens =   0x0000000000040000
CHECK_IN_TWO.white_pawns = 0
CHECK_IN_TWO.white_rooks =    0x0000000008000000
CHECK_IN_TWO.white_king =     0x0000000000000001

CHECK_IN_TWO_EXPECTED = 0b011011011001100000 # 27-> 25 rook no promotion




def test_correct_move_minmax_in_check_in_two():
    points, result = minmax(CHECK_IN_TWO, 4, -math.inf, math.inf, True)
    assert result == CHECK_IN_TWO_EXPECTED


from src.utils import *
from src.situation import generate_situation, get_moves, print_move_set

new_sit = generate_situation(CHECK_IN_TWO_EXPECTED, CHECK_IN_TWO)

print_move_set(get_moves(new_sit))


# kirjoita testi, jossa askentasyvyys kolme. eli viimeinen siirto on valkean siirto
# hahmottele pari kappaletta kolmen siirron voittotilannetta
# tilanne, jossa kahden siirron voitto, ei yhden siirron voittoa
# tilanne, että minmax antaa oikean siirron kolmessa siirrossa
# tilanne, jossa yhden siirron voitto, kutsu syvyydellä kolme
# -> nämä kaikki ikään kuin yhtenä jatkuvana tilanteena