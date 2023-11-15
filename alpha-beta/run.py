import numpy as np
from NmokRule import SixMok
from alpha_beta import selectMove

BLACK = 1
WHITE = -1
BANNED = -99
EMPTY = 0
symbols = {BLACK: 'O', WHITE: 'X', EMPTY: '+', BANNED: '.'}

class PlayGame:
    def __init__(self, size = 19, depth = 2):
        self.size = size
        self.depth = depth
        self.gg = False
        self.restart()
    
    def restart(self, player_idx = -1):
        self.is_max_state = True if player_idx == -1 else False
        self.state = SixMok(self.size)
        self.ai_color = -player_idx

    def play(self, x_axis, y_axis):
        position = (x_axis, y_axis)
        if self.state.color != self.ai_color:
            return False
        if not self.state.is_valid_position(position):
            return False
        self.state = self.state.doMove(position)
        self.gg = self.state.check_State()
        print(self.gg)
        return True
    
    def ai_play(self):
        if self.state.color == self.ai_color:
            return False, (0, 0)
        move, value = selectMove(self.state, self.depth, self.is_max_state)
        self.state = self.state.doMove(move)
        print(f"AI : [{move}], [{value}]")
        self.gg = self.state.check_State()

        return True, move
    
    def get_status(self):
        board = self.state.state

        return {
            'board': board.tolist(),
            'doMove': -self.state.color,
            'gg': self.gg,
            'winner': self.state.winner
        }
def print_board(board):
    # 상단에 열 번호 표시
    top_row = '   ' + ' '.join('{:2}'.format(i%10) for i in range(1, len(board) + 1))
    print(top_row)

    # 각 행과 그 행의 번호 표시
    for idx, row in enumerate(board, 1):
        row_str = '{:2}  '.format(idx%10) + ' '.join('{:2}'.format(symbols[cell]) for cell in row)
        print(row_str)



def main():
    size = 19
    depth = 2
    game = PlayGame(size, depth)

    while not game.gg:
        print_board(game.get_status()['board'])
        try:
            x, y = map(int, input("Enter your move(x y): ").split())
            x, y = y-1, x-1
            success = game.play(x, y)
        except:
            continue

        if not success:
            print("Invalid move. Try again.")
            continue

        ai_moved, ai_move = game.ai_play()
        if ai_moved:
            print(f"AI moved at {ai_move}")

        # 게임 결과 확인
        if game.gg:
            winner = "Player" if game.state.winner != game.ai_color else "AI"
            print_board(game.get_status()['board'])
            print(f"Game Over. {winner} wins.")
            break

if __name__ == "__main__":
    main()