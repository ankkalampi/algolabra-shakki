from precomputation import *


class AttackTables:
    def __init__(self):

        print("Calculating attack tables...")
        self.knight_attack_tables = precompute_attack_tables(precompute_single_knight_attack_table)

        self.bishop_attack_tables = precompute_attack_tables(precompute_single_bishop_attack_table)
        self.bishop_blocking_attack_tables = precompute_attack_tables(precompute_bishop_blocking_attack_tables)

        self.rook_attack_tables = precompute_attack_tables(precompute_single_rook_attack_table)
        self.rook_blocking_attack_tables = precompute_attack_tables(precompute_rook_blocking_attack_tables)

        self.queen_attack_tables = precompute_attack_tables(precompute_single_queen_attack_table)
        self.queen_blocking_attack_tables = precompute_attack_tables(precompute_queen_blocking_attack_tables)
        print("Attack tables calculated!")