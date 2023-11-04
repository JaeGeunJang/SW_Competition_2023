import time

def alphabeta(node, depth, alpha, beta, maximizingPlayer):
    if depth == 0 or game_over(node):
        return static_evaluation(node)

    if maximizingPlayer:
        maxEval = float('-inf')
        for child in get_all_moves(node):
            eval = alphabeta(child, depth - 1, alpha, beta, False)
            maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return maxEval
    else:
        minEval = float('inf')
        for child in get_all_moves(node):
            eval = alphabeta(child, depth - 1, alpha, beta, True)
            minEval = min(minEval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return minEval
    
def game_over(board):
    # board는 2차원 리스트로, 0은 빈 칸, 1은 플레이어1의 돌, 2는 플레이어2의 돌을 나타냄
    for x in range(len(board)):
        for y in range(len(board[0])):
            if board[x][y] != 0 and check_five_in_a_row(board, x, y):
                return True
    return False

def check_five_in_a_row(board, x, y):
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)] # 가로, 세로, 대각선, 반대 대각선
    for dx, dy in directions:
        count = 1
        for i in range(1, 5):
            nx, ny = x + i*dx, y + i*dy
            if nx < 0 or ny < 0 or nx >= len(board) or ny >= len(board[0]) or board[nx][ny] != board[x][y]:
                break
            count += 1
        if count == 5:
            return True
    return False

def static_evaluation(board, player):
    score = 0
    for x in range(len(board)):
        for y in range(len(board[0])):
            if board[x][y] == player:
                score += evaluate_position(board, x, y, player)
    return score

def evaluate_position(board, x, y, player):
    patterns = {
        'open_four': 100000,  
        'four': 50000,       
        'open_three': 10000,  
        'three': 5000,       
        'open_two': 1000,    
        'two': 500,          
    }
    
    position_score = 0
    
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            line = get_line(board, x, y, dx, dy)
            position_score += score_line(line, patterns, player)
    
    return position_score

def get_line(board, x, y, dx, dy):
    line = []
    for i in range(-4, 5): 
        nx, ny = x + i*dx, y + i*dy
        if 0 <= nx < len(board) and 0 <= ny < len(board[0]):
            line.append(board[nx][ny])
        else:
            line.append(None)  
    return line

def score_line(line, patterns, player):
    line_score = 0
    # Simplified pattern recognition logic
    if line[4] == player:
        if line[3:5] == [player, player] and line[2] == line[5] == 0:
            line_score += patterns['open_two']
        if line[2:6] == [player]*4 and (line[1] == 0 or line[6] == 0):
            line_score += patterns['open_four']
        if line[1:7] == [0] + [player]*4 + [0]:
            line_score += patterns['four']
    return line_score


def get_all_moves(board, player):
    moves = []
    for x in range(len(board)):
        for y in range(len(board[0])):
            if board[x][y] == 0:  # 빈 공간을 찾음
                # 수를 둘 때마다 새 보드 상태를 만들어야 함
                new_board = [row[:] for row in board]  # 보드 복사
                new_board[x][y] = player  # 새로운 돌을 놓음
                moves.append(new_board)
    return moves

def main():
    board = [[0 for _ in range(15)] for _ in range(15)]
    player_turn = 1
    game_running = True

    while game_running:
        print_board(board)  # 현재 게임 보드 출력 함수 (구현 필요)
        if player_turn == 1:
            x, y = get_player_move()  # 플레이어의 움직임을 받는 함수 (구현 필요)
        else:
            x, y = ai_move(board, player_turn)  # AI의 움직임을 결정하는 함수 (구현 필요)

        board[x][y] = player_turn
        if game_over(board):
            print(f"Player {player_turn} wins!")
            game_running = False
        
        player_turn = 3 - player_turn  # 플레이어 번호를 1과 2 사이에서 전환

def timed_alphabeta(node, depth, alpha, beta, maximizingPlayer, end_time, player):
    if time.time() > end_time:
        return static_evaluation(node, player)
    
    if depth == 0 or game_over(node):
        return static_evaluation(node, player)

    if maximizingPlayer:
        maxEval = float('-inf')
        for child in get_all_moves(node, player):
            eval = timed_alphabeta(child, depth - 1, alpha, beta, False, end_time, player)
            maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return maxEval
    else:
        minEval = float('inf')
        for child in get_all_moves(node, player):
            eval = timed_alphabeta(child, depth - 1, alpha, beta, True, end_time, player)
            minEval = min(minEval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return minEval

def iterative_deepening_alphabeta(node, max_time, player):
    end_time = time.time() + max_time
    depth = 1
    best_move = None
    while time.time() < end_time:
        best_eval = float('-inf')
        for move in get_all_moves(node, player):
            if time.time() >= end_time:
                break
            eval = timed_alphabeta(move, depth, float('-inf'), float('inf'), False, end_time, player)
            if eval > best_eval:
                best_eval = eval
                best_move = move
        depth += 1
    return best_move

def ai_move(board, player):
    # 여기서는 임시로 최대 5초 동안 가장 좋은 수를 찾는다고 가정합니다.
    best_move = iterative_deepening_alphabeta(board, 5, player)
    # 여기서 best_move는 새로운 보드 상태입니다. 움직임의 좌표를 찾아야 합니다.
    for x in range(len(board)):
        for y in range(len(board[0])):
            if board[x][y] != best_move[x][y]:
                return x, y

def get_player_move():
    # 플레이어에게 입력을 받아서 반환하는 함수
    x = int(input("Enter the X coordinate: "))
    y = int(input("Enter the Y coordinate: "))
    return x, y

def print_board(board):
    # 게임 보드를 출력하는 함수
    for row in board:
        print(' '.join(str(cell) for cell in row))
    print()

if __name__ == "__main__":
    main()
