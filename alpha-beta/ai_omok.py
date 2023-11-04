import numpy as np
import time

# 전역 변수 설정
BOARD_SIZE = 19
FORBIDDEN_POINTS = set()  # 착수 금지점을 저장할 집합
MAX_DEPTH = 3  # 탐색 깊이 초기 설정
TIME_LIMIT = 30  # 각 수에 대한 시간 제한
board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)

def alphabeta(node, depth, alpha, beta, maximizing_player, end_time):
    if time.time() >= end_time:
        return None  # 시간 초과로 인해 None 반환

    if depth == 0 or is_terminal(node):
        return static_evaluation(node)
    
    if maximizing_player:
        value = -float('inf')
        for child in get_children(node):
            child_value = alphabeta(child, depth-1, alpha, beta, False, end_time)
            if child_value is None:  # 시간 초과로 인해 None 반환된 경우
                return None
            value = max(value, child_value)
            alpha = max(alpha, value)
            if alpha >= beta:
                break  # 베타 컷오프
        return value
    else:
        value = float('inf')
        for child in get_children(node):
            child_value = alphabeta(child, depth-1, alpha, beta, True, end_time)
            if child_value is None:  # 시간 초과로 인해 None 반환된 경우
                return None
            value = min(value, child_value)
            beta = min(beta, value)
            if beta <= alpha:
                break  # 알파 컷오프
        return value

# 시간 제한을 설정하고 알파베타 가지치기를 시작하는 함수
def timed_alphabeta(root, depth, player):
    end_time = time.time() + TIME_LIMIT  # 종료 시간 설정
    best_move = None
    best_value = -float('inf')
    
    for child in get_children(root, player):
        value = alphabeta(child, depth-1, -float('inf'), float('inf'), False, end_time)
        if value is None:  # 시간 초과로 인해 None 반환된 경우
            break  # 루프를 빠져나와 결과 반환하지 않음
        if value > best_value:
            best_value = value
            best_move = child  # 또는 이동할 수 있는 좌표 등으로 대체해야 할 수 있음

    return best_move

def game_over(board):
    # 게임이 끝났는지 체크하는 로직: 6목이 만들어졌는지 체크
    # 단순화를 위해 수직, 수평, 대각선 체크만 구현함
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            if y + 5 < BOARD_SIZE and np.all(board[x, y:y+6] == board[x, y]) and board[x, y] != 0:
                return True
            if x + 5 < BOARD_SIZE and np.all(board[x:x+6, y] == board[x, y]) and board[x, y] != 0:
                return True
            if x + 5 < BOARD_SIZE and y + 5 < BOARD_SIZE and np.all([board[x+i, y+i] == board[x, y] for i in range(6)]) and board[x, y] != 0:
                return True
            if x + 5 < BOARD_SIZE and y - 5 >= 0 and np.all([board[x+i, y-i] == board[x, y] for i in range(6)]) and board[x, y] != 0:
                return True
    return False

def get_children(node, player):
    # 주어진 상태에 대해 가능한 모든 자식 노드(다음 이동)를 생성하는 함수
    children = []
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            if (x, y) not in FORBIDDEN_POINTS and node[x, y] == 0:
                child = np.copy(node)
                child[x, y] = player
                children.append(child)
    return children

def is_terminal(node):
    # 게임이 끝났는지 여부를 확인하는 함수
    return game_over(node)

def get_forbidden_moves():
    # 착수 금지점을 지정하는 로직, 간단화를 위해 임의로 설정
    global FORBIDDEN_POINTS
    FORBIDDEN_POINTS.update({(0, 0), (BOARD_SIZE - 1, BOARD_SIZE - 1)})

def make_move(board, x, y, player):
    # 착수 금지점이 아닌지 체크 후 수를 두는 로직
    if (x, y) not in FORBIDDEN_POINTS and board[x, y] == 0:
        board[x, y] = player
        return True
    return False

def play_game(board):
    # 게임 플레이를 위한 메인 루프
    current_player = 1  # 1이 흑, 2가 백
    game_running = True
    first_move_done = False
    moves_done = 0

    get_forbidden_moves()  # 착수 금지점을 지정하는 단계

    while game_running:
        print_board(board)  # 현재 보드 상태 출력

        if current_player == 1 and not first_move_done:
            # 흑의 첫 수는 정 중앙에 둔다는 규칙 구현
            make_move(board, BOARD_SIZE // 2, BOARD_SIZE // 2, current_player)
            first_move_done = True
        else:
            # 현재 플레이어에 대해 최선의 수를 계산
            best_move = timed_alphabeta(board, MAX_DEPTH, current_player)
            if best_move is not None:
                # 이동 수행
                board = best_move
            else:
                # 시간 초과 또는 더 이상 수행할 수 없을 때
                game_running = False

        moves_done += 1
        # 플레이어 교체
        if moves_done % 2 == 0:
            current_player = 3 - current_player
        
        # 게임 종료 조건 검사
        if is_terminal(board):
            game_running = False
            print("Game Over")
            break  # 게임 종료 시 루프 탈출


def timed_alphabeta(root, depth, player):
    end_time = time.time() + TIME_LIMIT  # 종료 시간 설정
    best_move = None
    best_value = -float('inf')
    
    for child in get_children(root, player):
        value = alphabeta(child, depth-1, -float('inf'), float('inf'), False, end_time)
        if value is None:  # 시간 초과로 인해 None 반환된 경우
            break  # 루프를 빠져나와 결과 반환하지 않음
        if value > best_value:
            best_value = value
            best_move = child  # 또는 이동할 수 있는 좌표 등으로 대체해야 할 수 있음

    return best_move

def print_board(board):
    for row in board:
        print(' '.join(str(cell) for cell in row))

if __name__ == "__main__":
    play_game(board)