

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
    uci = 0b00000000000000000
    uci |= (origin_square)
    uci |= (destination_square << 6)
    uci |= (piece << 12)
    uci |= (promotion << 15)

    return uci

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
        bitboard = 0x0000000000000000
        bitboard |= (1 << square)

        return bitboard

def get_destination_from_move(move):
    return (move >> 6) & 0b111111

def get_origin_from_move(move):
    return move & 0b111111

def get_piece_type_from_move(move):
    return (move >> 12) & 0b111

def get_promotion_from_move(move):
    return (move >> 15) & 0b111

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


