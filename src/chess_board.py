import random
import time
from utils import * 







from situation import Situation, generate_situation, get_moves







class ChessBoard:
    def __init__(self):
        
        self.situation = Situation()
        print("TESTING!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(self.situation.white_turn)
        print("TESTING!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        self.legal_moves = []

    def execute_uci(self, uci):





        self.situation = generate_situation(self.get_move_from_uci(uci), self.situation)
        self.legal_moves = get_moves(self.situation)

    def reset(self):
        self.situation = Situation()
        self.legal_moves = []

    def get_move_from_uci(self, uci):

        origin_string = uci[:2]
        destination_string = uci[2:4]

        origin_square = get_square_from_string(origin_string)
        destination_square = get_square_from_string(destination_string)

        if len(uci) == 5:
            promotion_string = uci[4:5]
            return generate_move(origin_square, destination_square, 0b001, promotion_string)

        piece = 0
        
        if self.situation.white_turn:
            if (self.situation.white_pawns & origin_square != 0) | (self.situation.black_pawns & origin_square != 0):
                piece = 0b001
            elif (self.situation.white_knights & origin_square != 0) | (self.situation.black_knights & origin_square != 0):
                piece = 0b010
            elif (self.situation.white_bishops & origin_square != 0) | (self.situation.black_bishops & origin_square != 0):
                piece = 0b011
            elif (self.situation.white_rooks & origin_square != 0) | (self.situation.black_rooks & origin_square != 0):
                piece = 0b100
            elif (self.situation.white_queens & origin_square != 0) | (self.situation.black_queens & origin_square != 0):
                piece = 0b101
            elif (self.situation.white_knights & origin_square != 0) | (self.situation.black_knights & origin_square != 0):
                piece = 0b110
            else:
                piece = 0b000

        return generate_move(origin_square, destination_square, piece) 

            
        
          




