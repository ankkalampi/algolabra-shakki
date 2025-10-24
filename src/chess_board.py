import random
import time
from src.utils import * 







from src.situation import Situation, generate_situation, get_moves, try_move







class ChessBoard:
    def __init__(self):
        
        self.situation = Situation()
        
       

    def get_legal_moves(self):
        return get_moves(self.situation)

    def execute_uci(self, uci):
        print(f"MOVE FROM UCI: {show_move(get_move_from_uci(uci, self.situation))}")
        if try_move(get_move_from_uci(uci, self.situation), self.situation):
            self.situation = generate_situation(get_move_from_uci(uci, self.situation), self.situation)
        else:
            print("MOVE NOT LEGAL   ")

        
        print("black_pawns: ")
        print(print_bitboard(self.situation.black_pawns))
        print("white_pawns: ")
        print(print_bitboard(self.situation.white_pawns))

    def reset(self):
        self.situation = Situation()
        

     

            
        
          




