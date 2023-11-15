import numpy as np

BLACK = 1
WHITE = -1
BANNED = -99
EMPTY = 0
symbols = {BLACK: '●', WHITE: '○', EMPTY: '.', BANNED: 'X'}

def first_move(state):
    x = state.bd // 2
    return (x, x), 1

def second_move(state):
    x_axis, y_axis = state.last_mv
    size = state.bd

    i = x_axis <= size // 2 and 1 or -1
    j = y_axis <= size // 2 and 1 or -1

    return (x_axis + i, y_axis + j), 2

def calculate_score(continued, blocks, current, empty_space = False):
    if blocks == 2 and continued < 6:
        return 0
    if continued >= 6 :
        if empty_space:
            return 18000
        return 65000
    
    continued_score = [100, 200, 400, 8000, 18000, 65000]
    block_score = [0.5, 0.6, 0.01, 0.25, 0.25]
    not_current_score = [1, 1, 0.2, 0.15, 0.10]
    empty_score = [1, 1.2, 0.9, 0.4, 0.2]

    continued_idx = continued - 1
    value = continued_score[continued_idx]

    if blocks == 1 :
        value *= block_score[continued_idx]
    if not current:
        value *= not_current_score[continued_idx]
    if empty_space:
        value *= empty_score[continued_idx]

    return int(value)

def evaluate_line(line, color, current):
    evaluation = 0
    size = len(line)

    continued = 0
    blocks = 2
    empty = False

    for i in range (size):
        value = line[i]

        if value == color:
            continued += 1
        elif value == EMPTY and continued > 0:
            if not empty and i < size-1 and line[i+1] == color:
                empty = True
            else :
                evaluation += calculate_score(continued, blocks, current, empty)
                continued = 0
                blocks = 1
                empty = False
        elif value == EMPTY:
            blocks = 1
        elif continued > 0 :
            evaluation += calculate_score(continued, blocks, current)
            continued = 0
            blocks = 2
        else :
            blocks = 2
    if continued > 0 :
        evaluation += calculate_score(continued, blocks, current)
    
    return evaluation

def evaluate_color(state, color, current_color):
    values = state.state
    size = state.bd
    current = color == current_color
    evaluation = 0

    for i in range (size):
        evaluation += evaluate_line(values[i, :], color, current)
        evaluation += evaluate_line(values[:, i], color, current)

    for i in range(-size + 6, size - 5):
        evaluation += evaluate_line(np.diag(values, k = i), color, current)
        evaluation += evaluate_line(np.diag(np.fliplr(values), k = i), color, current)
    return evaluation * color

def evaluation_state (state, current_color):
    return evaluate_color(state, BLACK, current_color) + evaluate_color(state, WHITE, current_color)

def minMax(state, alpha, beta, depth, is_max_state):
    if depth == 0 or state.checkState():
        return evaluation_state(state, -state.color)
    
    if is_max_state:
        value = float('-inf')
        for move in state.get_Move():
            value = max(value, minMax(state.doMove(move), alpha, beta, depth-1, False))
            alpha = max(value, alpha)

            if alpha >= beta:
                break
        return value
    else :
        value = float('inf')
        for move in state.get_Move():
            value = min(value,minMax(state.doMove(move), alpha, beta, depth-1, True))
            beta = min(value, beta)

            if alpha >= beta :
                break
        return value

def get_best_moves(state, n, is_max_state):
    color = state.color
    top_moves = []

    for move in state.legal_moves():
        evaluation = evaluation_state(state.doMove(move), color)
        top_moves.append((move, evaluation))
    return sorted(top_moves, key=lambda x: x[1], reverse=is_max_state)[:n]

def selectMove(state, depth, is_max_state):
    values = state.state
    best_value = is_max_state and float('-inf'), float('inf')
    best_move = [-1, -1]
    total_turn = len(values[values != EMPTY])

    if not total_turn :
        return first_move(state)
    if total_turn == 1 :
        return second_move(state)
    
    best_moves = get_best_moves(state, 10, is_max_state)

    for moves in best_moves:
        move = moves[0]
        value = minMax(state.doMove(move), float('-inf'), float('inf'), depth - 1, not is_max_state)
        if ((is_max_state and value > best_value) or (not is_max_state and value < best_value)) :
            best_value, best_move = value, move

    if best_move[0] == -1 and best_move[1] == -1 :
        return best_moves[0]
    
    return best_move, best_value