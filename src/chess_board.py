import random
import time
from utils import * 
from precomputation import *


from globals import *

import attack_tables

from situation import Situation, generate_situation, get_moves







class ChessBoard:
    def __init__(self):
        
        self.situation = Situation()
        self.moves = []

    def execute_move(self, move):
        self.situation = generate_situation(move, self.situation)
        self.moves = get_moves(self.situation)

    def reset(self):
        self.situation = Situation()
        self.moves = []


