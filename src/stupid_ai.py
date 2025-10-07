import random
import time

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

        self.black_en_passant   = 0x0000000000000000
        self.black_pawns        = 0x00FF000000000000
        self.black_knights      = 0x4200000000000000
        self.black_bishops      = 0x2400000000000000
        self.black_rooks        = 0x8100000000000000
        self.black_queens       = 0x0800000000000000
        self.black_king         = 0x1000000000000000

        self.white_to_move = True
        self.available_moves = []

        # bitmasks for checking that pieces won't move outside the board
        # for pawns the masks check if opening double move is available
        self.white_pawn_double_mask = 0xFF << 8
        self.black_pawn_double_mask = 0xFF >> 48


    # resets the board to opening situation
    def reset_board(self):
        self.white_en_passant   = 0x0000000000000000
        self.white_pawns        = 0x000000000000FF00
        self.white_knights      = 0x0000000000000042
        self.white_bishops      = 0x0000000000000024
        self.white_rooks        = 0x0000000000000081
        self.white_queens       = 0x0000000000000008
        self.white_king         = 0x0000000000000010

        self.black_en_passant   = 0x0000000000000000
        self.black_pawns        = 0x00FF000000000000
        self.black_knights      = 0x4200000000000000
        self.black_bishops      = 0x2400000000000000
        self.black_rooks        = 0x8100000000000000
        self.black_queens       = 0x0800000000000000
        self.black_king         = 0x1000000000000000

        self.white_to_move = True
        self.available_moves = []
        self.empty_squares = 0x0000000000000000

        

    # find all legal moves based on whose turn it is
    def generate_available_moves(self):

        # calculate empty squares (complement of all squares with pieces)
        self.empty_squares = ~(self.white_pawns | self.white_knights | self.white_bishops |
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
    def move_to_notation(origin, destination, promotion=""):
        origin_file = origin % 8
        origin_rank = (origin // 8) + 1 # +1 is due to chess notation starting form 1 not 0

        destination_file = destination % 8
        destination_rank = (destination // 8) +1

        # files are converted to characters. in ASCII, a=97

        return f"{chr(97+origin_file)}{origin_rank}{chr(97+destination_file)}{destination_rank}{promotion}"
        

    # filters out moves that put the movng party's king in check, as well as illegal castling
    def filter_illegal_moves(self):
        pass

    # generates en passant moves based on the en passant bitboard
    # NOTE: en passant table must be always updated when a move is commited!
    def generate_en_passant_moves(self):
        pass




    # generates pawn moves, does not yet check if a move is illegal for checking the king
    def generate_pawn_moves(self):
        
        
        # generate bitboards for legal moves

        # WHITE
        if (self.white_to_move):
            # calculate single square pawn moves (shifting bits 8 positions left, so up one rank)
            # also checks that moves don't take pawns outside of the board using bitmask (0xFF)
            pawn_moves = (self.white_pawns << 8) & empty_squares & ~(0xFF << 8)

            # calculate double square moves 
            # (moving piece must be in starting position, destination square must be empty,
            # and the square in between has to be empty as well)
            double_moves = ((self.white_pawns & self.white_pawn_double_mask) << 16) & empty_squares & (empty_squares << 8)

        # BLACK
        else:
            # calculate single square pawn moves (shifting bits 8 positions right, so down one rank)
            pawn_moves = (self.black_pawns >> 8) & empty_squares

            # calculate double square moves 
            # (moving piece must be in starting position, destination square must be empty,
            # and the square in between has to be empty as well)
            double_moves = ((self.black_pawns & self.black_pawn_double_mask) >> 16) & empty_squares & (empty_squares >> 8)


        

    # generates knight moves, does not yet check if a move is illegal for checking the king
    def generate_knight_moves(self):
        pass

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



def set_board(board: chess.Board, board_position:str):
    print(f"Set board to {board_position}!")
    board.set_fen(board_position)

def make_move(board: chess.Board):
    legal_moves = [move.uci() for move in list(board.legal_moves)]
    print(f"I found {len(legal_moves)} legal moves: {', '.join(legal_moves)}")
    choice = random.choice(legal_moves)
    board.push_uci(choice)

    return choice






def main():

    #board = chess.Board()

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
