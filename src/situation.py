import src.pawn as pawn
import src.knight as knight
import src.bishop as bishop
import src.rook as rook
import src.queen as queen
import src.king as king
import copy

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

    print(f"number of pseudolegal moves: {len(moves)}")

    for move in moves:
        print(f"TESTING MOVE: {show_move(move)}")
        if try_move(move, situation):
            print(f"LEGAL MOVE, uci: {get_uci(move)}")
            legal_moves.append(move)
        else:
            print("ILLEGAL MOVE")


    return legal_moves

def try_move(move, situation):
    if situation.white_turn:
        print("TESTING MOVE white turn")
    else:
        print("TESTING MOVE black turn")
    if is_attempting_to_capture_friendly_piece(move, situation):
        print("attempting to capture friendly piece")
        return False
    new_situation = generate_situation(move, situation)
    #if is_friendly_king_in_check(new_situation):
        #print("friendly king in check")
        #return False
    #else:


    return True


def is_friendly_king_in_check(situation):
    """
    Check if friendly king is in check in given situation

    Args:
    situation: situation object

    Returns:
    True if friendly king is in check in given situation
    """
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
    """
    Check if given move would result in capturing a friendly piece

    Args:
    move: move in 12bit format (not uci)
    situation: situation object

    Returns:
    True if move is attempting to capture friendly piece
    """
    
    destination_bitboard = get_bitboard_of_square(get_destination_from_move(move))

    return (get_all_friendly_pieces(situation) & destination_bitboard) != 0



# using this function assumes that the move is not trying to capture a friendly piece
def generate_situation(move, situation):
    #print("generating new situation")
    new_situation = copy.deepcopy(situation)
    #print(f"Old white_turn: {situation.white_turn}")
    new_situation.white_turn =   not situation.white_turn
    #print(f"New white_turn: {new_situation.white_turn}")

    origin = get_bitboard_of_square(get_origin_from_move(move))
    destination = get_bitboard_of_square(get_destination_from_move(move))
    piece_type = get_piece_type_from_move(move)
    
    # piece type pawn
    if piece_type == 0b001:
        
        promotion = get_promotion_from_move(move)

        if promotion != 0:

            promote_pawn(origin, destination, promotion, new_situation)

        else:
            if situation.white_turn:
                new_situation.white_pawns = move_piece(origin, destination, situation.white_pawns)
            else:
                new_situation.black_pawns = move_piece(origin, destination, situation.black_pawns)

    # piece type knight
    elif piece_type == 0b010:
        if situation.white_turn:
            new_situation.white_knights = move_piece(origin, destination, situation.white_knights)
        else:
            new_situation.black_knights = move_piece(origin, destination, situation.black_knights)

    # piece type bishop
    elif piece_type == 0b011:
        if situation.white_turn:
            new_situation.white_bishops = move_piece(origin, destination, situation.white_bishops)
        else:
            new_situation.black_bishops = move_piece(origin, destination, situation.black_bishops)

    # piece type rook
    elif piece_type == 0b100:
        if situation.white_turn:
            new_situation.white_rooks = move_piece(origin, destination, situation.white_rooks)
        else:
            new_situation.black_rooks = move_piece(origin, destination, situation.black_rooks)

    # piece type queen
    elif piece_type == 0b101:
        if situation.white_turn:
            new_situation.white_queens = move_piece(origin, destination, situation.white_queens)
        else:
            new_situation.black_queens = move_piece(origin, destination, situation.black_queens)

    # piece type king
    elif piece_type == 0b110:
        if situation.white_turn:
            new_situation.white_king = move_piece(origin, destination, situation.white_king)
        else:
            new_situation.black_king = move_piece(origin, destination, situation.black_king)
        
    
    #update_capture(destination, new_situation, situation.white_turn)

    return new_situation

def update_capture(destination, situation, white_turn):
    if white_turn:
        situation.black_pawns ^= destination
        situation.black_knights ^= destination
        situation.black_bishops ^= destination
        situation.black_rooks ^= destination
        situation.black_queens ^= destination
    else:
        situation.white_pawns ^= destination
        situation.white_knights ^= destination
        situation.white_bishops ^= destination
        situation.white_rooks ^= destination
        situation.white_queens ^= destination

def move_piece(origin, destination, pieces):
    #print("old bitboard:")
    #print(print_bitboard(pieces))
    pieces ^= origin
    pieces |= destination
    #print("new bitboard:")
    #print(print_bitboard(pieces))
    return pieces

def promote_pawn(origin, destination, promotion, situation):
    # promotion knight
    if promotion == 0b010:
        if situation.white_turn:
            situation.white_pawns ^= origin
            situation.white_knights |= destination
        else:
            situation.black_pawns ^= origin
            situation.black_knights |= destination

    # promotion bishop
    elif promotion == 0b011:
        if situation.white_turn:
            situation.white_pawns ^= origin
            situation.white_bishops |= destination
        else:
            situation.black_pawns ^= origin
            situation.black_knights |= destination

    # promotion rook
    elif promotion == 0b100:
        if situation.white_turn:
            situation.white_pawns ^= origin
            situation.white_rooks |= destination
        else:
            situation.black_pawns ^= origin
            situation.black_rooks |= destination

    # promotion queen
    elif promotion == 0b100:
        if situation.white_turn:
            situation.white_pawns ^= origin
            situation.white_queens |= destination
        else:
            situation.black_pawns ^= origin
            situation.black_queens |= destination

str = """
# TEST MOVES
WHITE_ESCAPE_CHECK_SUCCESS =    0b000100000011110000
WHITE_ESCAPE_CHECK_FAIL =       0b000100001101110000
WHITE_MOVE_INTO_CHECK =         0b000100000101110000
WHITE_BLOCK_CHECK =             0b010100001101011000
WHITE_MOVE_WITHOUT_CHECK =      0b001011010011001000
WHITE_DISCOVER_CHECK =          0b001101010101001000

BLACK_ESCAPE_CHECK_SUCCESS =    0b111100110100110000
BLACK_ESCAPE_CHECK_FAIL =       0b111000111001100000
BLACK_MOVE_INTO_CHECK =         0b111100110011110000

BLACK_MOVE_WITHOUT_CHECK =      0b111100111101110000

print_move(WHITE_ESCAPE_CHECK_SUCCESS)
print_move(WHITE_ESCAPE_CHECK_FAIL)
print_move(WHITE_MOVE_INTO_CHECK)
print_move(WHITE_BLOCK_CHECK)
print_move(WHITE_MOVE_WITHOUT_CHECK)
print_move(WHITE_DISCOVER_CHECK)

print_move(BLACK_ESCAPE_CHECK_SUCCESS)
print_move(BLACK_ESCAPE_CHECK_FAIL)
print_move(BLACK_MOVE_INTO_CHECK)

print_move(BLACK_MOVE_WITHOUT_CHECK)

sit = Situation()
sit.white_pawns =       0x0000000040279800
sit.white_knights =     0x0000000000000042
sit.white_bishops =     0x0000000000800004
sit.white_rooks =       0x0000000000000180
sit.white_queens =      0x0001000000000000
sit.white_king =        0x0000000000000010

sit.black_pawns =       0x0000619A04000000
sit.black_knights =     0x0000840000000000
sit.black_bishops =     0x0000100400000000
sit.black_rooks =       0x8100000000000000
sit.black_queens =      0x0000000100000000
sit.black_king =        0x1000000000000000

sit.white_turn = True
print("black king")
print(print_bitboard(sit.black_king))
sit = generate_situation(BLACK_MOVE_INTO_CHECK, sit)

all_pieces = get_all_pieces(sit)
enemy_attack_board = 0
enemy_attack_board |= pawn.get_attack_board(sit.white_pawns, all_pieces, False)
enemy_attack_board |= knight.get_attack_board(sit.white_knights, all_pieces)
enemy_attack_board |= bishop.get_attack_board(sit.white_bishops, all_pieces)
enemy_attack_board |= rook.get_attack_board(sit.white_rooks, all_pieces)
enemy_attack_board |= queen.get_attack_board(sit.white_queens, all_pieces)
enemy_attack_board |= king.get_attack_board(sit.white_king, all_pieces)


check_board = enemy_attack_board & sit.black_king


print("white attack board")
print(print_bitboard(enemy_attack_board))
print("black king")
print(print_bitboard(sit.black_king))
print("check board")
print(print_bitboard(check_board))

print("white pawns")
print(print_bitboard(sit.white_pawns))
print("white knights")
print(print_bitboard(sit.white_knights))
print("white bishops")
print(print_bitboard(sit.white_bishops))
print("white rooks")
print(print_bitboard(sit.white_rooks))
print("white queens")
print(print_bitboard(sit.white_queens))
print("white king")
print(print_bitboard(sit.white_king))

print("black pawns")
print(print_bitboard(sit.black_pawns))
print("black knights")
print(print_bitboard(sit.black_knights))
print("black bishops")
print(print_bitboard(sit.black_bishops))
print("black rooks")
print(print_bitboard(sit.black_rooks))
print("black queens")
print(print_bitboard(sit.black_queens))
print("black king")
print(print_bitboard(sit.black_king))
"""


        