from src.situation import generate_situation, get_moves
from src.heuristic import get_highest_value_move, get_lowest_value_move, evaluate_situation
import math
from src.heuristic import sort_moves

from src.utils import show_move
def minmax(situation, depth, alpha, beta, is_white):
    """
    Use minmax algorithm to deduce best move in a given situation

    Args:
    situation: situation object of the given situation
    depth: depth to which the algorithm calculates
    aplha: used for recursive calls, must be -inf for initial call
    beta: used for recursive calls, must be inf for initial call
    is_white: true, if the current player is white

    Returns:
    tuple: (best_score, best_move)
    """

    #print(f"Minmax call started! alpha: {alpha}  beta: {beta} white turn: {is_white}")
    moves = get_moves(situation)
    if len(moves) == 0:
        if is_white:
            return (-10000, None)
        else:
            return (10000, None)

    if depth == 0:
        return (evaluate_situation(situation), None)

    best_move = None



    if is_white:
        max_value = -math.inf
        for move in moves:
            #print(f"Starting recursive call of minmax! depth: {depth-1}")
            value, ignore = minmax(generate_situation(move, situation), depth -1, alpha, beta, False)
    
            if value > max_value:
                max_value = value
                best_move = move
            alpha = max(alpha, value)
            if beta <= alpha:
                #print(f"PRUNED!!!! beta: {beta}  alpha: {alpha} depth: {depth}")
                break
        #print(f"Returning from minmax! depth: {depth} max_value: {max_value} best_move: {show_move(best_move)}")
        return (max_value, best_move)

    else:
        min_value = math.inf
        for move in moves:
            #print(f"Starting recursive call of minmax! depth: {depth-1}")
            value, ignore = minmax(generate_situation(move, situation), depth -1, alpha, beta, True)
           
            if value < min_value:
                min_value = value
                best_move = move
            beta = min(beta, value)
            if beta <= alpha:
                #print(f"PRUNED!!!! beta: {beta}  alpha: {alpha} depth: {depth}")
                break
        #print(f"Returning from minmax! depth: {depth} min_value: {min_value} best_move: {show_move(best_move)}")
        return (min_value, best_move)









    
        


