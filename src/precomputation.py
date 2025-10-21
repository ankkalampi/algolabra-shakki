
from src.globals import EMPTY_BOARD
from src.utils import *

# bitmasks for checking that pieces won't move outside the board
# for pawns the masks check if opening double move is available
white_pawn_double_mask = 0xFF << 8
black_pawn_double_mask = 0xFF >> 48
white_pawn_promote_mask = black_pawn_double_mask
black_pawn_promote_mask = white_pawn_double_mask

pawn_right_edge_mask    = 0xFEFEFEFEFEFEFEFE
pawn_left_edge_mask     = 0x7F7F7F7F7F7F7F7F
pawn_top_mask           = 0xFFFFFFFFFFFFFFFF
pawn_bottom_mask        = 0xFFFFFFFFFFFFFFFF
pawn_mask               = 0xFFFFFFFFFFFFFFFF

knight_plus6_mask      = 0x3F3F3F3F3F3F3F3F
knight_plus10_mask     = 0xFCFCFCFCFCFCFCFC
knight_plus15_mask     = 0x7F7F7F7F7F7F7F7F
knight_plus17_mask     = 0xFEFEFEFEFEFEFEFE
knight_minus6_mask     = 0xFCFCFCFCFCFCFCFC
knight_minus10_mask    = 0x3F3F3F3F3F3F3F3F
knight_minus15_mask    = 0xFEFEFEFEFEFEFEFE
knight_minus17_mask    = 0x7F7F7F7F7F7F7F7F

king_north_mask        = 0xFFFFFFFFFFFFFFFF  
king_northeast_mask    = 0x7F7F7F7F7F7F7F7F
king_east_mask         = 0x7F7F7F7F7F7F7F7F
king_southeast_mask    = 0xFEFEFEFEFEFEFEFE
king_south_mask        = 0xFFFFFFFFFFFFFFFF
king_southwest_mask    = 0x7F7F7F7F7F7F7F7F
king_west_mask         = 0xFEFEFEFEFEFEFEFE
king_northwest_mask    = 0xFEFEFEFEFEFEFEFE


def precompute_single_rook_attack_table(square):
    """
    Compute and return an attack table (bitboard)
    for rook in a specific square

    Args:
    square: the square index (integer, in range (0,64))

    Returns:
    bitboard: 64-bit bitboard representation of attack board/table
    """
    bitboard = 0

    # get rank and file of the square
    rank = square // 8
    file = square % 8

    space_right = file      # number of squares to the right 
    space_left = 7 - file   # number of squares to the left
    space_down = rank       # number of squares below
    space_up = 7 - rank     # number of squares above

    # lengths of directions
    # order: up, right, down, left
    direction_lengths = [space_up,
                            space_right,
                            space_down,
                            space_left]

    # scalars for directional bit shifts
    # order: up, right, down, left
    direction_scalars = [8, -1, -8, 1]

    for direction in range(0,4):
        for move in range(1, direction_lengths[direction] +1):
            temp_bitboard = 0
            temp_bitboard |= (1 << square)
            if direction_scalars[direction] < 0:
                move_bitboard = (temp_bitboard >> (move * abs(direction_scalars[direction]))) & 0xFFFFFFFFFFFFFFFF # masking makes sure no extra bits are added
            else:
                move_bitboard = (temp_bitboard << (move * direction_scalars[direction])) & 0xFFFFFFFFFFFFFFFF # masking makes sure no extra bits are added
            bitboard |= move_bitboard



    return bitboard

# calculate attack table for queen
# attack table for queen is just bishop attack table + rook attack table
def precompute_single_queen_attack_table(square):
    bitboard = precompute_single_bishop_attack_table(square)
    bitboard |= precompute_single_rook_attack_table(square)

    return bitboard


def precompute_single_bishop_attack_table(square):
    """
    Compute and return an attack table (bitboard)
    for biashop in a specific square

    Args:
    square: the square index (integer, in range (0,64))

    Returns:
    bitboard: 64-bit bitboard representation of attack board/table
    """
    bitboard = 0

    # get rank and file of the square
    rank = square // 8
    file = square % 8

    space_right = file      # number of squares to the right 
    space_left = 7 - file   # number of squares to the left
    space_down = rank       # number of squares below
    space_up = 7 - rank     # number of squares above

    # diagonal lengths
    # order: northeast, southeast, southwest, northwest
    diagonal_lengths = [min(space_right, space_up),
                        min(space_right, space_down),
                        min(space_down, space_left),
                        min(space_left, space_up)]

    # scalars for diagonal bit shifts
    # order: northeast, southeast, southwest, northwest
    diagonal_scalars = [7, -9, -7, 9]

    # add diagonals to bitboard
    for diagonal in range (0,4):
        move_bitboard = 0
        for move in range(1, diagonal_lengths[diagonal]+1 ):
            # create temporary bitboard for a single move, and combine that bitboard with the main bitboard
            
            temp_bitboard = 0
            temp_bitboard |= (1 << square)
            if diagonal_scalars[diagonal] < 0:
                move_bitboard = (temp_bitboard >> (move * abs(diagonal_scalars[diagonal]))) & 0xFFFFFFFFFFFFFFFF # masking makes sure no extra bits are added
            else:
                move_bitboard = (temp_bitboard << (move * diagonal_scalars[diagonal])) & 0xFFFFFFFFFFFFFFFF # masking makes sure no extra bits are added
            bitboard |= move_bitboard

    return bitboard


    # generate all tables for a piece type using precompute function of that piece
# param func: piece specific precomputation function
def precompute_attack_tables(func):
    bitboards = []

    for x in range(0, 64):
        
        bitboard = func(x)
        bitboards.append(bitboard)
    
    return bitboards


# precomputes blocking attack tables for a specific square
def precompute_rook_blocking_attack_tables(square):
    attack_tables = []

    for block_value in range(0, 4096):
        attack_tables.append(create_rook_blocking_attack_board(square, block_value))

    return attack_tables

# precomputes blocking attack tables for a specific square
def precompute_bishop_blocking_attack_tables(square):
    attack_tables = []

    for block_value in range(0, 4096):
        attack_tables.append(create_bishop_blocking_attack_board(square, block_value))

    return attack_tables

# precomputes blocking attack tables for a specific square
def precompute_queen_blocking_attack_tables(square):
    attack_tables = []

    for block_value in range(0, 4096):
        bitboard = 0
        bitboard |= create_bishop_blocking_attack_board(square, block_value)
        bitboard |= create_rook_blocking_attack_board(square, block_value)

        attack_tables.append(bitboard)

    return attack_tables



def precompute_single_king_attack_table(square):
    """
    Compute and return an attack table (bitboard)
    for king in a specific square

    Args:
    square: the square index (integer, in range (0,64))

    Returns:
    bitboard: 64-bit bitboard representation of attack board/table
    """
    bitboard = EMPTY_BOARD

    square_bitboard = get_bitboard_of_square(square)

    # add move north
    bitboard |= (square_bitboard << 8) & king_north_mask

    # add move northeast
    bitboard |= (square_bitboard << 7) & king_northeast_mask

    # add move east
    bitboard |= (square_bitboard >> 1) & king_east_mask

    # add move southeast
    bitboard |= (square_bitboard >> 7) & king_southeast_mask

    # add move south
    bitboard |= (square_bitboard >> 8) & king_south_mask

    # add move southwest
    bitboard |= (square_bitboard >> 9) & king_southwest_mask

    # add move west
    bitboard |= (square_bitboard << 1) & king_west_mask

    # add move northwest
    bitboard |= (square_bitboard << 9) & king_northwest_mask

    return bitboard

# TODO: This function shares a lot in common with similar functions. could refactor to simplify code
# creates a blocked attack bitboard for a rook in a specific square
# this attack bitboard is based on 12-bit blocking info
def create_rook_blocking_attack_board(square, block_value):
    """
    Compute and return attack table (bitboard)
    for rook in a specific square based on blocking value.
    Blocking value describes distance to nearest blocking piece
    per direction. Blocking value is a 12bit number
    with 3 bits for each direction 

    Args:
    square: the square index (integer, in range (0,64))
    block_value: 12bit blocking value

    Returns:
    bitboard: 64-bit bitboard representation of attack board/table
    """
    bitboard = 0

    # get rank and file of the square
    rank = square // 8
    file = square % 8

    # note: edge squares won't block, that's why they don't have to be considered
    space_right = file -1 if file > 0 else 0      # number of squares to the right 
    space_left = 7 - file -1 if file < 8 else 0   # number of squares to the left
    space_down = rank -1 if rank > 0 else 0      # number of squares below
    space_up = 7 - rank -1 if rank < 8 else 0     # number of squares above

    # lengths of directions
    # order: up, right, down, left
    direction_lengths = [space_up,
                            space_right,
                            space_down,
                            space_left]

    # scalars for directional bit shifts
    # order: up, right, down, left
    direction_scalars = [8, -1, -8, 1]

    # bit representations of first blocking square of each direction
    blocking_bits = [
                    (block_value >> 9) & 0b111,
                    (block_value >> 6) & 0b111,
                    (block_value >> 3) & 0b111,
                    block_value & 0b111,
                    ]

    for direction in range(0,4):
        # if there is no blocking, attack squares are calculated from direction length
        if blocking_bits[direction] == 0:
            loop_length = direction_lengths[direction] +1
        else:
            loop_length = blocking_bits[direction]
            
        for move in range(1, loop_length +1):
            temp_bitboard = 0
            temp_bitboard |= (1 << square)
            if direction_scalars[direction] < 0:
                move_bitboard = (temp_bitboard >> (move * abs(direction_scalars[direction]))) & 0xFFFFFFFFFFFFFFFF # masking makes sure no extra bits are added
            else:
                move_bitboard = (temp_bitboard << (move * direction_scalars[direction])) & 0xFFFFFFFFFFFFFFFF # masking makes sure no extra bits are added
            bitboard |= move_bitboard

    return bitboard


def create_bishop_blocking_attack_board(square, block_value):
    """
    Compute and return attack table (bitboard)
    for bishop in a specific square based on blocking value.
    Blocking value describes distance to nearest blocking piece
    per direction. Blocking value is a 12bit number
    with 3 bits for each direction 

    Args:
    square: the square index (integer, in range (0,64))
    block_value: 12bit blocking value

    Returns:
    bitboard: 64-bit bitboard representation of attack board/table
    """
    bitboard = 0

    # get rank and file of the square
    rank = square // 8
    file = square % 8

    space_right = file      # number of squares to the right 
    space_left = 7 - file   # number of squares to the left
    space_down = rank       # number of squares below
    space_up = 7 - rank     # number of squares above

    # diagonal lengths
    # order: northeast, southeast, southwest, northwest
    # note: edge squares won't block, that's why they don't have to be considered
    northeast = min(space_right, space_up)
    if northeast > 0:
        northeast -= 1
    southeast = min(space_right, space_down)
    if southeast > 0:
        southeast -= 1
    southwest = min(space_down, space_left)
    if southwest > 0:
        southwest -= 1
    northwest = min(space_left, space_up)
    if northwest > 0:
        northwest -= 1

    diagonal_lengths = [northeast,
                        southeast,
                        southwest,
                        northwest]

    # scalars for diagonal bit shifts
    # order: northeast, southeast, southwest, northwest
    diagonal_scalars = [7, -9, -7, 9]

    # bit representations of first blocking square of each direction
    blocking_bits = [
                    (block_value >> 9) & 0b111,
                    (block_value >> 6) & 0b111,
                    (block_value >> 3) & 0b111,
                    block_value & 0b111
                    ]

    # add diagonals to bitboard
    for direction in range(0,4):
        # if there is no blocking, attack squares are calculated from direction length
        if blocking_bits[direction] == 0:
            loop_length = diagonal_lengths[direction] +1
        else:
            loop_length = blocking_bits[direction]
            
        for move in range(1, loop_length +1):
            temp_bitboard = 0
            temp_bitboard |= (1 << square)
            if diagonal_scalars[direction] < 0:
                move_bitboard = (temp_bitboard >> (move * abs(diagonal_scalars[direction]))) & 0xFFFFFFFFFFFFFFFF # masking makes sure no extra bits are added
            else:
                move_bitboard = (temp_bitboard << (move * diagonal_scalars[direction])) & 0xFFFFFFFFFFFFFFFF # masking makes sure no extra bits are added
            
            
            bitboard |= move_bitboard

    return bitboard



def precompute_single_knight_attack_table(square):
    """
    Compute and return an attack table (bitboard)
    for knight in a specific square

    Args:
    square: the square index (integer, in range (0,64))

    Returns:
    bitboard: 64-bit bitboard representation of attack board/table
    """

    square_bitboard = get_bitboard_of_square(square)

    # a knight has eight moves, whick on a bitboard are +6,+10,+15,+17,-6,-10,-15,-17
    # if a knight is too close to a border of the board, the moves that would land outside of the board
    # would appear on the other side of the board. That's why bitmasks are used to filter out these incorrect moves
    plus6_moves     = (square_bitboard << 6)     & knight_plus6_mask
    plus10_moves    = (square_bitboard << 10)    & knight_plus10_mask
    plus15_moves    = (square_bitboard << 15)    & knight_plus15_mask
    plus17_moves    = (square_bitboard << 17)    & knight_plus17_mask
    minus6_moves    = (square_bitboard >> 6)     & knight_minus6_mask
    minus10_moves   = (square_bitboard >> 10)    & knight_minus10_mask
    minus15_moves   = (square_bitboard >> 15)    & knight_minus15_mask
    minus17_moves   = (square_bitboard >> 17)    & knight_minus17_mask

    # returns a bitboard with pseudo-legal knight moves
    return (plus6_moves | plus10_moves | plus15_moves | plus17_moves |
                minus6_moves | minus10_moves | minus15_moves | minus17_moves)

def precompute_single_white_pawn_attack_table(square):
    """
    Compute and return an capture table (bitboard)
    for white pawn in a specific square

    Args:
    square: the square index (integer, in range (0,64))

    Returns:
    bitboard: 64-bit bitboard representation of attack board/table
    """
    square_bitboard = get_bitboard_of_square(square)
    plus9_move = (square_bitboard << 9) & pawn_right_edge_mask & pawn_top_mask
    plus7_move = (square_bitboard << 7) & pawn_left_edge_mask & pawn_top_mask

    return plus9_move | plus7_move

def precompute_single_black_pawn_attack_table(square):
    square_bitboard = get_bitboard_of_square(square)

    minus9_move = (square_bitboard >> 9) & pawn_left_edge_mask & pawn_bottom_mask
    minus7_move = (square_bitboard >> 7) & pawn_right_edge_mask & pawn_bottom_mask

    return minus9_move | minus7_move

def precompute_single_white_pawn_move_table(square):
    """
    Compute and return a movement table (bitboard)
    for white pawn in a specific square 

    Args:
    square: the square index (integer, in range (0,64))

    Returns:
    bitboard: 64-bit bitboard representation of attack board/table
    """
    square_bitboard = get_bitboard_of_square(square)
    single_move = pawn_mask & (square_bitboard <<8)
    double_move = (square_bitboard & white_pawn_double_mask) << 16

    return single_move | double_move


def precompute_single_black_pawn_move_table(square):
    square_bitboard = get_bitboard_of_square(square)
    single_move = pawn_mask & (square_bitboard >> 8)
    double_move = (square_bitboard & black_pawn_double_mask) >> 16

    return single_move | double_move

create_bishop_blocking_attack_board(27, 0b000001010011 )
