import random
import time
from src.utils import * 







from src.situation import Situation, generate_situation, get_moves







class ChessBoard:
    def __init__(self):
        
        self.situation = Situation()
        
        self.legal_moves = []

    def get_legal_moves(self):
        return get_moves(self.situation)

    def execute_uci(self, uci):





        self.situation = generate_situation(get_move_from_uci(uci, self.situation), self.situation)
        self.legal_moves = get_moves(self.situation)

    def reset(self):
        self.situation = Situation()
        self.legal_moves = []

     

            
        
          




