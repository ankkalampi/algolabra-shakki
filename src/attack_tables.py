from precomputation import *

_attack_tables = None

def get_attack_tables():
    global _attack_tables
    if _attack_tables is None:
        _attack_tables = _generate_tables()
    return _attack_tables

def _generate_tables():
    return AttackTables()

class AttackTables:
    def __init__(self):

        print("Calculating attack tables...")
        self.white_pawn_attack_tables = precompute_attack_tables(precompute_single_white_pawn_attack_table)
        self.black_pawn_attack_tables = precompute_attack_tables(precompute_single_black_pawn_attack_table)
        self.white_pawn_move_tables = precompute_attack_tables(precompute_single_white_pawn_move_table)
        self.black_pawn_move_tables = precompute_attack_tables(precompute_single_black_pawn_move_table)
        self.knight_attack_tables = precompute_attack_tables(precompute_single_knight_attack_table)

        self.bishop_attack_tables = precompute_attack_tables(precompute_single_bishop_attack_table)
        self.bishop_blocking_attack_tables = precompute_attack_tables(precompute_bishop_blocking_attack_tables)

        self.rook_attack_tables = precompute_attack_tables(precompute_single_rook_attack_table)
        self.rook_blocking_attack_tables = precompute_attack_tables(precompute_rook_blocking_attack_tables)

        self.queen_attack_tables = precompute_attack_tables(precompute_single_queen_attack_table)
        self.queen_blocking_attack_tables = precompute_attack_tables(precompute_queen_blocking_attack_tables)
        self.king_attack_tables = precompute_attack_tables(precompute_single_king_attack_table)
        print("Attack tables calculated!")