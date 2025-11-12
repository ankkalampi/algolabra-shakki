import math
from src.situation import Situation
from src.utils import *
import src.bishop as bishop
import src.rook as rook
import src.queen as queen
from src.attack_tables import get_attack_tables
from src.situation import get_all_pieces



PAWN_VALUE = 1
KNIGHT_VALUE = 3
BISHOP_VALUE = 3
ROOK_VALUE = 5
QUEEN_VALUE = 8

ENEMY_TERRITORY_BONUS = 3
CENTER_BONUS = 1
CHECK_BONUS = 5

ENDGAME_PIECE_AMOUNT = 14


def evaluate_situation(situation):
    """
    Returns numerical value to situation

    Args:
    situation: situation object

    Returns:
    integer value
    """
    points = 0
    white_pawns = situation.white_pawns
    white_knights = situation.white_knights
    white_bishops = situation.white_bishops
    white_rooks = situation.white_rooks
    white_queens = situation.white_queens
    white_king = situation.white_king

    black_pawns = situation.black_pawns
    black_knights = situation.black_knights
    black_bishops = situation.black_bishops
    black_rooks = situation.black_rooks
    black_queens = situation.black_queens
    black_king = situation.black_king

    attack_tables = get_attack_tables()

    all_pieces = get_all_pieces(situation)

    points += calculate_white_pawns(white_pawns, PAWN_VALUE, attack_tables, black_king)
    print(f"VALUE AFTER WHITE PAWNS: {points}")
    points += calculate_knights(white_knights, KNIGHT_VALUE, attack_tables, black_king)
    print(f"VALUE AFTER WHITE KNIGHTS: {points}")
    points += calculate_bishops(white_bishops, BISHOP_VALUE, attack_tables, all_pieces, black_king)
    print(f"VALUE AFTER WHITE BISHOPS: {points}")
    points += calculate_rooks(white_rooks, ROOK_VALUE, attack_tables, all_pieces, black_king)
    print(f"VALUE AFTER WHITE ROOKS: {points}") 
    points += calculate_queens(white_queens, QUEEN_VALUE, attack_tables, all_pieces, black_king)
    print(f"VALUE AFTER WHITE QUEENS: {points}")
    
    print(f"POINTS: {points}")
    points -= calculate_black_pawns(black_pawns, PAWN_VALUE, attack_tables, white_king)
    points -= calculate_knights(black_knights, KNIGHT_VALUE, attack_tables, white_king)
    points -= calculate_bishops(black_bishops, BISHOP_VALUE, attack_tables, all_pieces, white_king)
    points -= calculate_rooks(black_rooks, ROOK_VALUE, attack_tables, all_pieces, white_king)
    points -= calculate_queens(black_queens, QUEEN_VALUE, attack_tables, all_pieces, white_king)
    print(f"POINTS: {points}")

    return points
    



def calculate(pieces, value, attack_table, enemy_king):
    points = 0

    # going through white pieces
    

    while(pieces):
        piece = bitscan(pieces)
        pieces &= pieces -1
        points += value
          

    return points

def calculate_white_pawns(pieces, value, attack_tables, enemy_king):

    points = 0
    if pieces == 0: return 0
    runs = 0

    while(pieces):
        runs += 1
        piece = bitscan(pieces)
        pieces &= pieces -1
        points += value

        if (enemy_king & attack_tables.white_pawn_attack_tables[piece] != 0):
            points += CHECK_BONUS
          

    return points

def calculate_black_pawns(pieces, value, attack_tables, enemy_king):

    points = 0
    if pieces == 0: return 0

    while(pieces):
        piece = bitscan(pieces)
        pieces &= pieces -1
        points += value

        if (enemy_king & attack_tables.black_pawn_attack_tables[piece] != 0):
            points += CHECK_BONUS
          

    return points

def calculate_knights(pieces, value, attack_tables, enemy_king):
    points = 0
    if pieces == 0: return 0

    while(pieces):
        piece = bitscan(pieces)
        pieces &= pieces -1
        points += value

        if (enemy_king & attack_tables.knight_attack_tables[piece] != 0):
            points += CHECK_BONUS
          

    return points

def calculate_bishops(pieces, value, attack_tables, all_pieces, enemy_king):
    points = 0
    if pieces == 0: return 0

    while(pieces):
        piece = bitscan(pieces)
        pieces &= pieces -1
        points += value

        if (enemy_king & attack_tables.bishop_blocking_attack_tables[piece][bishop.get_block_value(piece, all_pieces)] != 0):
            points += CHECK_BONUS
          

    return points

def calculate_rooks(pieces, value, attack_tables, all_pieces, enemy_king):
    points = 0
    if pieces == 0: return 0

    while(pieces):
        piece = bitscan(pieces)
        pieces &= pieces -1
        points += value

        

        if (enemy_king & attack_tables.rook_blocking_attack_tables[piece][rook.get_block_value(piece, all_pieces)] != 0):
            points += CHECK_BONUS
          

    return points

def calculate_queens(pieces, value, attack_tables, all_pieces, enemy_king):
    points = 0
    if pieces == 0: return 0

    while(pieces):
        piece = bitscan(pieces)
        pieces &= pieces -1
        points += value

        attack_board = 0

        block_value = bishop.get_block_value(piece, all_pieces)
        attack_board |= attack_tables.bishop_blocking_attack_tables[piece][block_value]

        block_value = rook.get_block_value(piece, all_pieces)
        attack_board |= attack_tables.rook_blocking_attack_tables[piece][block_value]
    

        if (enemy_king & attack_board != 0):
            points += CHECK_BONUS
          

    return points
        
