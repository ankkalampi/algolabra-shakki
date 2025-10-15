
from attack_tables import AttackTables

import rook
import bishop
import queen
import knight
import king
from pawn import PawnSet
from king import KingSet

###  TO THIS CLASS: generating moves by checking if they are legal

class PieceSet:
    def __init__(self):
        self.pieces = 0x0000000000000000

class PieceSetXX:
    def __init__(self):

        self.attack_tables = AttackTables()
        self.all_pieces = PieceSet()
        self.white_pieces = PieceSet()
        self.black_pieces = PieceSet()


        self.white_pawns = PawnSet(self.attack_tables, self.all_pieces, self.white_pieces, True)

        self.white_king = KingSet(self.attack_tables, True)
        

        self.white_pawns        = 0x000000000000FF00
        self.white_knights      = 0x0000000000000042
        self.white_bishops      = 0x0000000000000024
        self.white_rooks        = 0x0000000000000081
        self.white_queens       = 0x0000000000000008
        self.white_king         = 0x0000000000000010

        self.white_pieces       = self.get_white_pieces()

        
        self.black_pawns        = 0x00FF000000000000
        self.black_knights      = 0x4200000000000000
        self.black_bishops      = 0x2400000000000000
        self.black_rooks        = 0x8100000000000000
        self.black_queens       = 0x0800000000000000
        self.black_king         = 0x1000000000000000

        self.black_pieces       = self.get_black_pieces()

        self.all_pieces = self.white_pieces | self.black_pieces


    def get_white_attack_board(self):
        attack_board = 0x0000000000000000

        attack_board |= knight.get_attack_board(self.white_knights, self.attack_tables, self.all_pieces)
        attack_board |= rook.get_attack_board(self.white_rooks, self.attack_tables, self.all_pieces)
        attack_board |= bishop.get_attack_board(self.white_bishops, self.attack_tables, self.all_pieces)


        attack_board |= queen.get_attack_board(self.white_queens, self.attack_tables, self.all_pieces)
        attack_board |= king.get_attack_board(self.white_king, self.attack_tables)



        return attack_board


    def get_black_attack_board(self):
        attack_board = 0x0000000000000000

        attack_board |= knight.get_attack_board(self.black_knights, self.attack_tables, self.all_pieces)
        attack_board |= rook.get_attack_board(self.black_rooks, self.attack_tables, self.all_pieces)
        attack_board |= bishop.get_attack_board(self.black_bishops, self.attack_tables, self.all_pieces)

        attack_board |= queen.get_attack_board(self.black_queens, self.attack_tables, self.all_pieces)
        attack_board |= king.get_attack_board(self.black_king, self.attack_tables)

        return attack_board
        
        


    def get_white_pieces(self):
        return ( self.black_pawns | self.black_knights | self.black_bishops |
                                    self.black_rooks | self.black_queens | self.black_king)

    def get_black_pieces(self):
        return ( self.black_pawns | self.black_knights | self.black_bishops |
                                    self.black_rooks | self.black_queens | self.black_king)

    def get_all_pieces(self):
        return self.white_pieces | self.black_pieces

    def reset(self):
        
        self.white_pawns        = 0x000000000000FF00
        self.white_knights      = 0x0000000000000042
        self.white_bishops      = 0x0000000000000024
        self.white_rooks        = 0x0000000000000081
        self.white_queens       = 0x0000000000000008
        self.white_king         = 0x0000000000000010

        self.white_pieces       = self.get_white_pieces()

        
        self.black_pawns        = 0x00FF000000000000
        self.black_knights      = 0x4200000000000000
        self.black_bishops      = 0x2400000000000000
        self.black_rooks        = 0x8100000000000000
        self.black_queens       = 0x0800000000000000
        self.black_king         = 0x1000000000000000

        self.black_pieces       = self.get_black_pieces()

        self.all_pieces = self.white_pieces | self.black_pieces


    

    
