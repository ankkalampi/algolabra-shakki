import src.pawn as pawn
import src.knight as knight
import src.bishop as bishop
import src.rook as rook
import src.queen as queen
import src.king as king

from src.utils import *

from src.globals import * 

class Situation:
    def __init__(self):
        self.white_pawns = WHITE_PAWNS_START
        self.white_knights = WHITE_KNIGHTS_START
        self.white_bishops = WHITE_BISHOPS_START
        self.white_rooks = WHITE_ROOKS_START
        self.white_queens = WHITE_QUEENS_START
        self.white_king = WHITE_KING_START

        self.black_pawns = BLACK_PAWNS_START
        self.black_knights = BLACK_KNIGHTS_START
        self.black_bishops = BLACK_BISHOPS_START
        self.black_rooks = BLACK_ROOKS_START
        self.black_queens = BLACK_QUEENS_START
        self.black_king = BLACK_KING_START

        self.white_turn = True


def get_all_pieces(situation):
    all_pieces = 0

    all_pieces |= situation.white_pawns
    all_pieces |= situation.white_knights
    all_pieces |= situation.white_bishops
    all_pieces |= situation.white_rooks
    all_pieces |= situation.white_queens
    all_pieces |= situation.white_king

    all_pieces |= situation.black_pawns
    all_pieces |= situation.black_knights
    all_pieces |= situation.black_bishops
    all_pieces |= situation.black_rooks
    all_pieces |= situation.black_queens
    all_pieces |= situation.black_king

    return all_pieces

def get_all_friendly_pieces(situation):
    friendly_pieces = 0

    if situation.white_turn:
        friendly_pieces |= situation.white_pawns
        friendly_pieces |= situation.white_knights
        friendly_pieces |= situation.white_bishops
        friendly_pieces |= situation.white_rooks
        friendly_pieces |= situation.white_queens
        friendly_pieces |= situation.white_king
    else:
        friendly_pieces |= situation.black_pawns
        friendly_pieces |= situation.black_knights
        friendly_pieces |= situation.black_bishops
        friendly_pieces |= situation.black_rooks
        friendly_pieces |= situation.black_queens
        friendly_pieces |= situation.black_king

    return friendly_pieces

def get_moves(situation):
    moves = []

    all_pieces = get_all_pieces(situation)

    if situation.white_turn:
        moves.extend(pawn.get_moves(situation.white_pawns, all_pieces, True))
        moves.extend(knight.get_moves(situation.white_knights, all_pieces))
        moves.extend(bishop.get_moves(situation.white_bishops, all_pieces))
        moves.extend(rook.get_moves(situation.white_rooks, all_pieces))
        moves.extend(queen.get_moves(situation.white_queens, all_pieces))
        moves.extend(king.get_moves(situation.white_king, all_pieces))
    else:
        moves.extend(pawn.get_moves(situation.black_pawns, all_pieces, False))
        moves.extend(knight.get_moves(situation.black_knights, all_pieces))
        moves.extend(bishop.get_moves(situation.black_bishops, all_pieces))
        moves.extend(rook.get_moves(situation.black_rooks, all_pieces))
        moves.extend(queen.get_moves(situation.black_queens, all_pieces))
        moves.extend(king.get_moves(situation.black_king, all_pieces))

    legal_moves = []

    for move in moves:
        if test_move(move, situation):
            legal_moves.append(move)


    return legal_moves

def test_move(move, situation):
    #print("testing move")
    if is_attempting_to_capture_friendly_piece(move, situation):
        return False
    new_situation = generate_situation(move, situation)
    return is_friendly_king_in_check(new_situation)


def is_friendly_king_in_check(situation):
    all_pieces = get_all_pieces(situation)

    enemy_attack_board = 0

    if situation.white_turn:
        enemy_attack_board |= pawn.get_attack_board(situation.black_pawns, all_pieces, False)
        enemy_attack_board |= knight.get_attack_board(situation.black_knights, all_pieces)
        enemy_attack_board |= bishop.get_attack_board(situation.black_bishops, all_pieces)
        enemy_attack_board |= rook.get_attack_board(situation.black_rooks, all_pieces)
        enemy_attack_board |= queen.get_attack_board(situation.black_queens, all_pieces)
        enemy_attack_board |= king.get_attack_board(situation.black_king, all_pieces)

        return (enemy_attack_board & situation.white_king) != 0
    else:
        enemy_attack_board |= pawn.get_attack_board(situation.white_pawns, all_pieces, True)
        enemy_attack_board |= knight.get_attack_board(situation.white_knights, all_pieces)
        enemy_attack_board |= bishop.get_attack_board(situation.white_bishops, all_pieces)
        enemy_attack_board |= rook.get_attack_board(situation.white_rooks, all_pieces)
        enemy_attack_board |= queen.get_attack_board(situation.white_queens, all_pieces)
        enemy_attack_board |= king.get_attack_board(situation.white_king, all_pieces)

        return (enemy_attack_board & situation.black_king) != 0

    

def is_attempting_to_capture_friendly_piece(move, situation):
    
    destination = get_destination_from_move(move)

    return (get_all_friendly_pieces(situation) & destination) == 0



# using this function assumes that the move is not trying to capture a friendly piece
def generate_situation(move, situation):
    #print("generating new situation")
    new_situation = situation
    #print(f"Old white_turn: {situation.white_turn}")
    new_situation.white_turn =   not situation.white_turn
    #print(f"New white_turn: {new_situation.white_turn}")

    origin = get_origin_from_move(move)
    destination = get_destination_from_move(move)
    piece_type = get_piece_type_from_move(move)
    
    # piece type pawn
    if piece_type == 0b001:
        
        promotion = get_promotion_from_move(move)

        if promotion != 0:

            # promotion knight
            if promotion == 0b010:
                if situation.white_turn:
                    new_situation.white_pawns = situation.white_pawns ^ origin
                    new_situation.white_knights = situation.white_knights & destination
                else:
                    new_situation.black_pawns = situation.black_pawns ^ origin
                    new_situation.black_knights = situation.black_knights & destination

            # promotion bishop
            elif promotion == 0b011:
                if situation.white_turn:
                    new_situation.white_pawns = situation.white_pawns ^ origin
                    new_situation.white_bishops = situation.white_bishops & destination
                else:
                    new_situation.black_pawns = situation.black_pawns ^ origin
                    new_situation.black_knights = situation.black_bishops & destination

            # promotion rook
            elif promotion == 0b100:
                if situation.white_turn:
                    new_situation.white_pawns = situation.white_pawns ^ origin
                    new_situation.white_rooks = situation.white_rooks & destination
                else:
                    new_situation.black_pawns = situation.black_pawns ^ origin
                    new_situation.black_rooks = situation.black_rooks & destination

            # promotion queen
            elif promotion == 0b100:
                if situation.white_turn:
                    new_situation.white_pawns = situation.white_pawns ^ origin
                    new_situation.white_queens = situation.white_queens & destination
                else:
                    new_situation.black_pawns = situation.black_pawns ^ origin
                    new_situation.black_queens = situation.black_queens & destination

        else:
            if situation.white_turn:
                new_situation.white_pawns = situation.white_pawns ^ origin
                new_situation.white_pawns = situation.black_pawns & destination
            else:
                new_situation.black_pawns = situation.black_pawns ^ origin
                new_situation.black_pawns = situation.black_pawns & destination

    # piece type knight
    elif piece_type == 0b010:
        if situation.white_turn:
                new_situation.white_knights = situation.white_knights ^ origin
                new_situation.white_knights = situation.black_knights & destination
        else:
            new_situation.black_knights = situation.black_knights ^ origin
            new_situation.black_knights = situation.black_knights & destination

    # piece type bishop
    elif piece_type == 0b011:
        if situation.white_turn:
                new_situation.white_bishops = situation.white_bishops ^ origin
                new_situation.white_bishops = situation.black_bishops & destination
        else:
            new_situation.black_bishops = situation.black_bishops ^ origin
            new_situation.black_bishops = situation.black_bishops & destination

    # piece type rook
    elif piece_type == 0b100:
        if situation.white_turn:
                new_situation.white_rooks = situation.white_rooks ^ origin
                new_situation.white_rooks = situation.black_rooks & destination
        else:
            new_situation.black_rooks = situation.black_rooks ^ origin
            new_situation.black_rooks = situation.black_rooks & destination

    # piece type queen
    elif piece_type == 0b101:
        if situation.white_turn:
                new_situation.white_queens = situation.white_queens ^ origin
                new_situation.white_queens = situation.black_queens & destination
        else:
            new_situation.black_queens = situation.black_queens ^ origin
            new_situation.black_queens = situation.black_queens & destination

    # piece type king
    elif piece_type == 0b110:
        if situation.white_turn:
                new_situation.white_king = situation.white_king ^ origin
                new_situation.white_king = situation.black_king & destination
        else:
            new_situation.black_king = situation.black_king ^ origin
            new_situation.black_king = situation.black_king & destination

    return new_situation



        