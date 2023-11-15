import numpy as np

BLACK = 1
WHITE = -1
BANNED = -99
EMPTY = 0
symbols = {BLACK: '●', WHITE: '○', EMPTY: '.', BANNED: 'X'}

def is_valid_position(bd, position) :
        return position[0] >= 0 and position[0] < bd and position[1] >= 0 and position[1] < bd

def expend_area(bd, idx):
    area_idx = np.copy(idx)
    for i in range(bd):
        for j in range (bd):
            if idx[i, j]:
                for direct in [[1, 0], [0, 1], [1, 1], [1, -1]]:
                    x_axis, y_axis = direct
                    for side in (1, -1) :
                        xs, ys = i + x_axis * side, j + y_axis * side
                        if is_valid_position(bd, [xs, ys]):
                            area_idx[xs, ys] = True

def nested_list(lst, sublst):
    sbj_size = len(lst)
    obj_size = len(sublst)

    for i in range(sbj_size - obj_size):
        result = lst[i:min(i + obj_size, sbj_size-1)]
        if (result == sublst).all():
            return True
    return False

class SixMok:
    def __init__(self, bd, state = None, color=BLACK):
        if np.all(state != None) :
            self.state = np.copy(state)
        else :
            self.state = np.full((bd, bd), EMPTY)
    
        self.bd = bd
        self.color = color
        self.last_mv = None
        self.winner = 0
    
    def get_Move(self):
        prev_move_idx = self.state != EMPTY
        area_idx = expend_area(self.bd, prev_move_idx)
        return np.column_stack(np.where(area_idx == True))

    def doMove(self, position):
        next_state = SixMok(bd = self.bd, state = self.state, color = -self.color)
        next_state[position] = next_state.color
        next_state.last_mv = list(position)
        return next_state

    def is_valid_position(self, position):
        return (is_valid_position(self.bd, position) and self.state[position]==EMPTY)
    
    def check_pattern(self, pattern):
        count = 0
        for line in self.check_Result():
            if nested_list(line, pattern):
                count += 1
        return count

    def get_Result(self):
        pattern = np.full((6, ), 1)

        if self.check_pattern(pattern * BLACK):
            self.winner = BLACK
            return True, BLACK
        if self.check_pattern(pattern * WHITE):
            self.winner = WHITE
            return True, WHITE
        return False, EMPTY

    def is_full(self) :
        return not np.any(self.state == EMPTY)

    def check_State(self):
        is_win, color = self.getResult()
        if self.is_full(): return True
        return is_win
    
    def check_Result(self):
        lines = list()

        for i in range (self.bd):
            lines.append(self.state[i, :])
            lines.append(self.state[:, i])

        for i in range (self.bd + 6, self.bd-5):
            lines.append(np.diag(self.state, k = i))
            lines.append(np.diag(np.fliplr(self.state), k = i))

        for line in lines :
            yield line
    
    def __getitem__(self, position):
        i, j = position
        return self.state[i, j]

    def __setitem__(self, position, value):
        i, j = position
        self.state[i, j] = value

    def __str__(self):
        out = ' ' * 3
        out += '{}\n'.format(''.join(
            '{}{}'.format((i + 1) % 10, i < 10 and ' ' or "'")
            for i in range(self.size)
        ))

        for i in range(self.size):
            out += '{}{} '.format(i + 1 < 10 and ' ' or '', i + 1)
            for j in range(self.size):
                out += symbols[self[i, j]]
                if self.last_move and (i, j) == tuple(self.last_move):
                    out += '*'
                else:
                    out += ' '
            if i == self.size - 1:
                out += ''
            else:
                out += '\n'
        return out

    def __repr__(self):
        return self.__str__()