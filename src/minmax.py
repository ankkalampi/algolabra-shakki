from src.situation import generate_situation, get_moves
from src.heuristic import get_highest_value_move, get_lowest_value_move, evaluate_situation
import math

def minmax(situation, depth, alpha, beta, is_white):
    moves = get_moves(situation)
    if len(moves) == 0:
        if is_white:
            return (math.inf, None)
        else:
            return (-math.inf, None)

    if depth == 0:
        return (evaluate_situation(situation), None)

    best_move = None

    if is_white:
        max_value = -math.inf
        for move in moves:
            value, ignore = minmax(generate_situation(move, situation), depth -1, alpha, beta, False)
    
            if value > max_value:
                max_value = value
                best_move = move
            aplha = max(alpha, value)
            if beta <= aplha:
                break
        return (max_value, best_move)

    else:
        min_value = math.inf
        for move in moves:
            value, ignore = minmax(generate_situation(move, situation), depth -1, alpha, beta, True)
           
            if value < min_value:
                min_value = value
                best_move = move
            beta = min(beta, value)
            if beta <= alpha:
                break
        return (min_value, best_move)




    
        


