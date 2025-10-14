import random
import time
import chess_board as chess


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








def set_board(board: chess.ChessBoard, board_position:str):
    print(f"Set board to {board_position}!")
    board.set_fen(board_position)

def make_move(board: chess.ChessBoard):
    legal_moves = [move.uci() for move in list(board.legal_moves)]
    print(f"I found {len(legal_moves)} legal moves: {', '.join(legal_moves)}")
    choice = random.choice(legal_moves)
    board.push_uci(choice)

    return choice


    










def main():

    board = chess.ChessBoard()

    origin = 0b1000000000000
    destination = 0b100000000000000000000

    print(board.get_uci(origin, destination))

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
