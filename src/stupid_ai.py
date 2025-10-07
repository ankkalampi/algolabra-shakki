import random
import time

class ChessBoard:
    def __init__(self):
        # init bitboards for each piece type
        self.white_pawns    = 0x000000000000FF00
        self.white_knights  = 0x0000000000000042
        self.white_bishops  = 0x0000000000000024
        self.white_rooks    = 0x0000000000000081
        self.white_queens   = 0x0000000000000008
        self.white_king     = 0x0000000000000010

        self.black_pawns    = 0x00FF000000000000
        self.black_knights  = 0x4200000000000000
        self.black_bishops  = 0x2400000000000000
        self.black_rooks    = 0x8100000000000000
        self.black_queens   = 0x0800000000000000
        self.black_king     = 0x1000000000000000

        self.white_to_move = True

    def generate_pawn_moves(self):
        moves = []

        # calculate empty squares (complement of all squares with pieces)
        empty_squares = ~(self.white_pawns | self.white_knights | self.white_bishops |
                            self.white_rooks | self.white_queens | self.white_king |
                            self.black_pawns | self.black_knights | self.black_bishops |
                            self.black_rooks | self.black_queens | self.black_king)
        
        # calculate legal moves for who is to move
        if (self.white_to_move):
            # calculate single square pawn moves (shifting bits per 8 moves up one rank)
            pawn_moves = (self.white_pawns << 8) & empty_squares

            # calculate double square moves 
            # (moving piece must be in starting position, destination square must be empty,
            # and the square in between has to be empty as well)
            double_moves = ((self.white_pawns & 0x000000000000FF00) << 16) & empty_squares & (empty_squares << 8)



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
