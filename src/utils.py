
from src.globals import *
# finds the index of the least significant bit in a bitboard
    # used for getting indices of piece locations
def bitscan(bitboard):
    if bitboard == 0:
        return None
    
    return (bitboard & -bitboard).bit_length() -1

# generate 18-bit representation for uci
# this is actually not proper uci, as this has also information about the piece moving
# values:
# pawn:     0b001
# knight:   0b010
# bishop:   0b011
# rook:     0b100
# queen:    0b101
# king:     0b110
def generate_move(origin_square, destination_square, piece, promotion = 0b000):

    origin_bin = square_index_to_6_bits(origin_square)
    destination_bin = square_index_to_6_bits(destination_square)
    uci = 0b00000000000000000
    uci |= (promotion)
    uci |= (piece << 3)
    uci |= (destination_bin << 6)
    uci |= (origin_bin << 12)
    

    return uci

def square_index_to_6_bits(square):
    return square & 0b111111

# returns uci notation. uci notation is a string of 4 characters, with the exception that 
# a pawn promotion takes place, adding fifth character to the string. 
# promotion character is empty on default
def get_uci(move):

    origin_bitboard = get_origin_from_move(move)
    destination_bitboard = get_destination_from_move(move)

    promotion_bits = get_promotion_from_move(move)

    if promotion_bits == 0b010:
        promotion = "k"
    elif promotion_bits == 0b011:
        promotion = "b"
    elif promotion_bits == 0b100:
        promotion = "r"
    elif promotion_bits == 0b101:
        promotion = "q"
    else:
        promotion = ""

    # get square numbers from bitboard representations
    origin = (origin_bitboard).bit_length() - 1
    destination = (destination_bitboard).bit_length() - 1

    origin_file = origin % 8
    origin_rank = (origin // 8) + 1 # +1 is due to chess notation starting form 1 not 0

    destination_file = destination % 8
    destination_rank = (destination // 8) +1

    # files are converted to characters. in ASCII, a=97

    return f"{chr(97+origin_file)}{origin_rank}{chr(97+destination_file)}{destination_rank}{promotion}"

def get_bitboard_of_square(square):
        bitboard = EMPTY_BOARD
        bitboard |= (1 << square)

        return bitboard



def get_destination_from_move(move):
    return (move >> 6) & 0b111111

def get_origin_from_move(move):
    return (move >> 12) & 0b111111

def get_piece_type_from_move(move):
    return (move >> 3) & 0b111

def get_promotion_from_move(move):
    return move & 0b111

def get_square_from_string(string):
    file_char = string[0:1]
    rank_char = string[1:2]

    if file_char == "a":
        file = 0
    elif file_char == "b":
        file = 1
    elif file_char == "c":
        file = 2
    elif file_char == "d":
        file = 3
    elif file_char == "e":
        file = 4
    elif file_char == "f":
        file = 5
    elif file_char == "g":
        file = 6
    elif file_char == "h":
        file = 7
    else:
        file = None

    rank = int(rank_char)

    return (rank * 8) + file

def print_bitboard(bitboard):
    indices = set()
    
    while(bitboard):
        index = bitscan(bitboard)
        bitboard &= bitboard -1
        indices.add(index)
    
    bitboard_string = ""

    for index in range(63,-1,-1):
        if (index % 8) == 7 and index != 63:
            bitboard_string += "\n"

        if index in indices:
            bitboard_string += "1 "
        else:
            bitboard_string += "0 "

    return bitboard_string

def print_move(move):
    origin = get_origin_from_move(move)
    destination = get_destination_from_move(move)
    piece = get_piece_type_from_move(move)
    promotion = get_promotion_from_move(move)

    move_string = ""

    move_string += str(origin)
    move_string += " -> "
    move_string += str(destination)
    
    if piece == 1:
        move_string += " pawn "
    elif piece == 2:
        move_string += " knight "
    elif piece == 3:
        move_string += " bishop "
    elif piece == 4:
        move_string += " rook "
    elif piece == 5:
        move_string += " queen "
    elif piece == 6:
        move_string += " king "
    else:
        move_string += " ERROR "

    if promotion == 0:
        move_string += " no promotion "
    elif promotion == 2:
        move_string += " promotion: knight "
    elif promotion == 3:
        move_string += " promotion: bishop "
    elif promotion == 4:
        move_string += " promotion: rook "
    elif promotion == 5:
        move_string += " promotion: queen "
    else:
        move_string += " ERROR "

    print(move_string)

def print_move_set(moves):
    print("MOVESET:")
    for move in moves:
        print_move(move)

def show_block_value(block_value):
    block_string = ""
    first = (block_value >> 9) & 0b111
    second = (block_value >> 6) & 0b111
    third = (block_value >> 3) & 0b111
    fourth = (block_value) & 0b111

    block_string += str(first)
    block_string += " "
    block_string += str(second)
    block_string += " "
    block_string += str(third)
    block_string += " "
    block_string += str(fourth)
    block_string += " "

    return block_string

def get_move_bits(origin, destination, piece, promotion =0b000):
    origin = origin & 0b111111
    destination = destination & 0b111111
    piece = piece & 0b111
    promotion = promotion & 0b111

    bits = 0b000000000000000000

    bits  |= (origin << 12)
    bits  |= (destination << 6)
    bits  |= (piece << 3)
    bits  |= (promotion)

    return bits & 0b111111111111111111


def get_move_from_uci(uci, situation):

    origin_string = uci[:2]
    destination_string = uci[2:4]

    origin_square = get_square_from_string(origin_string)
    destination_square = get_square_from_string(destination_string)

    if len(uci) == 5:
        promotion_string = uci[4:5]
        return generate_move(origin_square, destination_square, 0b001, promotion_string)

    piece = 0
    
    if situation.white_turn:
        if (situation.white_pawns & origin_square != 0) | (situation.black_pawns & origin_square != 0):
            piece = 0b001
        elif (situation.white_knights & origin_square != 0) | (situation.black_knights & origin_square != 0):
            piece = 0b010
        elif (situation.white_bishops & origin_square != 0) | (situation.black_bishops & origin_square != 0):
            piece = 0b011
        elif (situation.white_rooks & origin_square != 0) | (situation.black_rooks & origin_square != 0):
            piece = 0b100
        elif (situation.white_queens & origin_square != 0) | (situation.black_queens & origin_square != 0):
            piece = 0b101
        elif (situation.white_knights & origin_square != 0) | (situation.black_knights & origin_square != 0):
            piece = 0b110
        else:
            piece = 0b000

    return generate_move(origin_square, destination_square, piece)





