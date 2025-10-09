import random
import time

# TODO: generate bitboards for pawn moves (partially complete) 
# TODO: generate bitboards for knight moves
# TODO: generate bitboards for bishop moves
# TODO: generate bitboards for rook moves
# TODO: generate bitboards for queen moves
# TODO: generate bitboards for king moves (incl. castling)
# TODO: generate bitboards for en passant

# TODO: add logic for in_check situation to these functions

# TODO: create function for generating attack bitboard (to check where the opponent can attack in a certain situation)
# TODO: create function for generating attack bitboard (to check where the current player can attack in a certain situation) 

# TODO: create logic for testing a move (recalculate attack bitboards)
# TODO: create logic for removing illegal moves
# TODO: create logic for commiting a move (update data such as in_check, white_to_move, etc)

# TODO: create simple heuristics

# TODO: implement minmax algorithm

# TODO: create testing

# TODO: fine tune heuristics



class ChessBoard:
    def __init__(self):
        # init bitboards for each piece type

        self.white_en_passant   = 0x0000000000000000
        self.white_pawns        = 0x000000000000FF00
        self.white_knights      = 0x0000000000000042
        self.white_bishops      = 0x0000000000000024
        self.white_rooks        = 0x0000000000000081
        self.white_queens       = 0x0000000000000008
        self.white_king         = 0x0000000000000010

        self.white_pieces       = ( self.white_pawns | self.white_knights | self.white_bishops |
                                    self.white_rooks | self.white_queens | self.white_king)

        self.black_en_passant   = 0x0000000000000000
        self.black_pawns        = 0x00FF000000000000
        self.black_knights      = 0x4200000000000000
        self.black_bishops      = 0x2400000000000000
        self.black_rooks        = 0x8100000000000000
        self.black_queens       = 0x0800000000000000
        self.black_king         = 0x1000000000000000

        self.black_pieces       = ( self.black_pawns | self.black_knights | self.black_bishops |
                                    self.black_rooks | self.black_queens | self.black_king)

        self.white_to_move = True
        self.available_moves = []
        self.empty_squares = 0x0000000000000000
        self.in_check = False

        # bitmasks for checking that pieces won't move outside the board
        # for pawns the masks check if opening double move is available
        self.white_pawn_double_mask = 0xFF << 8
        self.black_pawn_double_mask = 0xFF >> 48

        self.knight_plus6_mask      = 0x3F3F3F3F3F3F3F3F
        self.knight_plus10_mask     = 0x3F3F3F3F3F3F3F3F
        self.knight_plus15_mask     = 0x7F7F7F7F7F7F7F7F
        self.knight_plus17_mask     = 0x7F7F7F7F7F7F7F7F
        self.knight_minus6_mask     = 0xFEFEFEFEFEFEFEFE
        self.knight_minus10_mask    = 0xFCFCFCFCFCFCFCFC
        self.knight_minus15_mask    = 0xF8F8F8F8F8F8F8F8
        self.knight_minus17_mask    = 0xF0F0F0F0F0F0F0F0


    # resets the board to opening situation
    def reset(self):
        self.white_en_passant   = 0x0000000000000000
        self.white_pawns        = 0x000000000000FF00
        self.white_knights      = 0x0000000000000042
        self.white_bishops      = 0x0000000000000024
        self.white_rooks        = 0x0000000000000081
        self.white_queens       = 0x0000000000000008
        self.white_king         = 0x0000000000000010

        self.white_pieces       = self.get_white_pieces()

        self.black_en_passant   = 0x0000000000000000
        self.black_pawns        = 0x00FF000000000000
        self.black_knights      = 0x4200000000000000
        self.black_bishops      = 0x2400000000000000
        self.black_rooks        = 0x8100000000000000
        self.black_queens       = 0x0800000000000000
        self.black_king         = 0x1000000000000000

        self.black_pieces       = self.get_black_pieces()

        self.white_to_move = True
        self.available_moves = []
        self.empty_squares = 0x0000000000000000
        self.in_check = False


    def get_white_pieces(self):
        return ( self.black_pawns | self.black_knights | self.black_bishops |
                                    self.black_rooks | self.black_queens | self.black_king)

    def get_black_pieces(self):
        return ( self.black_pawns | self.black_knights | self.black_bishops |
                                    self.black_rooks | self.black_queens | self.black_king)

        

    # find all legal moves based on whose turn it is
    def generate_available_moves(self):

        # calculate empty squares (complement of all squares with pieces)
        self.empty_squares = ~( self.white_pawns | self.white_knights | self.white_bishops |
                                self.white_rooks | self.white_queens | self.white_king |
                                self.black_pawns | self.black_knights | self.black_bishops |
                                self.black_rooks | self.black_queens | self.black_king)


        

        

        self.generate_pawn_moves()
        self.generate_en_passant_moves()
        self.generate_knight_moves()
        self.generate_bishop_moves()
        self.generate_rook_moves()
        self.generate_queen_moves()
        self.generate_king_moves()
        self.filter_illegal_moves()
        



    # returns uci notation. uci notation is a string of 4 characters, with the exception that 
    # a pawn promotion takes place, adding fifth character to the string. 
    # promotion character is empty on default
    def push_uci(self, origin_bitboard, destination_bitboard, promotion=""):

        # get square numbers from bitboard representations
        origin = (origin_bitboard).bit_length() - 1
        destination = (destination_bitboard).bit_length() - 1

        origin_file = origin % 8
        origin_rank = (origin // 8) + 1 # +1 is due to chess notation starting form 1 not 0

        destination_file = destination % 8
        destination_rank = (destination // 8) +1

        # files are converted to characters. in ASCII, a=97

        return f"{chr(97+origin_file)}{origin_rank}{chr(97+destination_file)}{destination_rank}{promotion}"
        

    # filters out moves that put the moving party's king in check, as well as illegal castling
    def filter_illegal_moves(self):
        pass

    # generates en passant moves based on the en passant bitboard
    # NOTE: en passant table must be always updated when a move is commited!
    def generate_en_passant_moves(self):
        pass

    # generate bitboard for showing attack squares for white
    def generate_white_attack_board(self):
        pass

    # generate bitboard for showing attack squares for black
    def generate_black_attack_board(self):
        pass

        








    # generates pawn moves, does not yet check if a move is illegal for checking the king
    def generate_pawn_moves(self):
        
        
        # generate bitboards for legal moves

        # WHITE
        if (self.white_to_move):
            # calculate single square pawn moves (shifting bits 8 positions left, so up one rank)
            single_moves = (self.white_pawns << 8) & self.empty_squares 


            unmoved_pawns = self.white_pawns & self.white_pawn_double_mask
            unblocked_pawns = (self.white_pawns << 8) & self.empty_squares  

            # calculate double square moves 
            # (moving piece must be in starting position, destination square must be empty,
            # and the square in between has to be empty as well)
            double_moves = (unmoved_pawns << 16) & (unblocked_pawns << 8) & self.empty_squares 

            

        # BLACK
        else:
            # calculate single square pawn moves (shifting bits 8 positions right, so down one rank)
            single_moves = (self.black_pawns >> 8) & self.empty_squares

            unmoved_pawns = self.black_pawns & self.black_pawn_double_mask
            unblocked_pawns = (self.black_pawns << 8) & self.empty_squares

            # calculate double square moves 
            # (moving piece must be in starting position, destination square must be empty,
            # and the square in between has to be empty as well)
            double_moves = (unmoved_pawns >> 16) & (unblocked_pawns >> 8) & self.empty_squares 

        
        return single_moves | double_moves
        


        

    # generates knight moves, does not yet check if a move is illegal for checking the king
    def generate_knight_moves(self):
        
        # a knight has eight moves, whick on a bitboard are +6,+10,+15,+17,-6,-10,-15,-17
        # if a knight is too close to a border of the board, the moves that would land outside of the board
        # would appear on the other side of the board. That's why bitmasks are used to filter out these incorrect moves

        # WHITE
        if(white_to_move):
            plus6_moves     = (self.white_knights << 6)     & self.knight_plus6_mask
            plus10_moves    = (self.white_knights << 10)    & self.knight_plus10_mask
            plus15_moves    = (self.white_knights << 15)    & self.knight_plus15_mask
            plus17_moves    = (self.white_knights << 17)    & self.knight_plus17_mask
            minus6_moves    = (self.white_knights >> 6)     & self.knight_minus6_mask
            minus10_moves   = (self.white_knights >> 10)    & self.knight_minus10_mask
            minus15_moves   = (self.white_knights >> 15)    & self.knight_minus15_mask
            minus17_moves   = (self.white_knights >> 17)    & self.knight_minus17_mask

        # BLACK
        else:
            plus6_moves     = (self.black_knights << 6)     & self.knight_plus6_mask
            plus10_moves    = (self.black_knights << 10)    & self.knight_plus10_mask
            plus15_moves    = (self.black_knights << 15)    & self.knight_plus15_mask
            plus17_moves    = (self.black_knights << 17)    & self.knight_plus17_mask
            minus6_moves    = (self.black_knights >> 6)     & self.knight_minus6_mask
            minus10_moves   = (self.black_knights >> 10)    & self.knight_minus10_mask
            minus15_moves   = (self.black_knights >> 15)    & self.knight_minus15_mask
            minus17_moves   = (self.black_knights >> 17)    & self.knight_minus17_mask


        return (plus6_moves | plus10_moves | plus15_moves | plus17_moves |
                minus6_moves | minus10_moves | minus15_moves | minus17_moves) & empty_squares
    

    

    # generates bishop moves, does not yet check if a move is illegal for checking the king
    def generate_bishop_moves(self):
        pass

    # generates rook moves, does not yet check if a move is illegal for checking the king
    def generate_rook_moves(self):
        pass

    # generates queen moves, does not yet check if a move is illegal for checking the king
    def generate_queen_moves(self):
        pass

    # generates king moves, including castling
    def generate_king_moves(self):
        pass




def set_board(board: ChessBoard, board_position:str):
    print(f"Set board to {board_position}!")
    board.set_fen(board_position)

def make_move(board: ChessBoard):
    legal_moves = [move.uci() for move in list(board.legal_moves)]
    print(f"I found {len(legal_moves)} legal moves: {', '.join(legal_moves)}")
    choice = random.choice(legal_moves)
    board.push_uci(choice)

    return choice


    










def main():

    board = ChessBoard()

    origin = 0b1000000000000
    destination = 0b100000000000000000000

    print(board.push_uci(origin, destination))

    while True:
        opponent_move = input()
        time.sleep(random.randrange(1,10)/100)
        if opponent_move.startswith("BOARD:"):
            set_board(board, opponent_move.removeprefix("BOARD:"))
        elif opponent_move.startswith("RESET:"):
            board.reset()
            print("Board reset!")
        elif opponent_move.startswith("PLAY:"):
            choice = make_move(board)
            # example about logs
            print(f"I chose {choice}!")
            # example about posting a move
            print(f"MOVE:{choice}")
        elif opponent_move.startswith("MOVE:"):
            move = opponent_move.removeprefix("MOVE:")
            board.push_uci(move)
            print(f"Received move: {move}")
        else:
            print(f"Unknown tag: {opponent_move}")
            break

if __name__ == "__main__":
    main()
