import math

bd = 3
class Nmok :
    def __init__(self, state = [[0 for rows in range(bd)]for cols in range(bd)]) :
        self.lownums = 3
        self.movetime = 1
        self.permove = 0
        self.state = state
        self.playerJustMoved = 1
        self.lastmove = [math.floor(bd/2),math.floor(bd/2)]

    def clone(self) :
        state = Nmok()
        state.state = self.state[:][:]
        state.lownums = self.lownums
        return state

    def getResult(self, playerjm) :
        result = self.checkState()
        assert result != 0
        if result == -1 :
            return 0.5
        elif result == playerjm :
            return 1.0
        else :
            return 0.0

    def getMoves(self) :
        if self.checkState() != 0 :
            return []
        else :
            moving = []
            for i in range (bd) :
                for j in range (bd) :
                    if self.state[i][j] == 0 :
                        moving.append((j,i))
        return moving

    def doMoves(self,move) :
        moveX = move[0]
        moveY = move[1]

        assert moveX >= 0 and moveX <=bd-1 and moveY >= 0 and moveY <= bd-1
        assert self.state[moveY][moveX] == 0

        self.permove += 1

        self.state[moveY][moveX] = self.playerJustMoved

        if self.permove == self.movetime :
            self.permove = 0
            self.playerJustMoved = 3 - self.playerJustMoved
            self.lastmove = [moveX,moveY]

    def checkState(self):
        lastx = self.lastmove[0]
        lasty = self.lastmove[1]

        result = 0

        lownum = self.lownums - 1
        pmv = self.state[lasty][lastx]
        isStone = 0

        for i in range(0, self.lownums) :
            if lastx - i >= 0 and lastx - i + lownum < bd :
                for j in range (0, self.lownums) :
                    if self.state[lasty][lastx-i+j] != 0 :
                        isStone += self.state[lasty][lastx-i+j]
                    else :
                        isStone = 0
                        break
                if isStone == self.lownums and pmv == 1 :
                    return 1
                elif isStone == self.lownums*2 and pmv == 2 :
                    return 2
                else :
                    isStone = 0

        for i in range(0, self.lownums) :
            if lasty - i >= 0 and lasty - i + lownum < bd :
                for j in range (0, self.lownums) :
                    if self.state[lasty-i+j][lastx] != 0 :
                        isStone += self.state[lasty-i+j][lastx]
                    else :
                        isStone = 0
                        break
                if isStone == self.lownums and pmv == 1 :
                    return 1
                elif isStone == self.lownums*2 and pmv == 2 :
                    return 2
                else :
                    isStone = 0

        for i in range (0, self.lownums) :
            if lastx - i >= 0 and lastx - i + lownum < bd and lasty - i >= 0 and lasty - i + lownum < bd :
                for j in range (0, self.lownums) :
                    if self.state[lasty-i+j][lastx-i+j] != 0 :
                        isStone += self.state[lasty-i+j][lastx-i+j]
                    else :
                        isStone = 0
                        break
                if isStone == self.lownums and pmv == 1 :
                    return 1
                elif isStone == self.lownums*2 and pmv == 2 :
                    return 2
                else :
                    isStone = 0

        for i in range (0, self.lownums) :
            if lastx - i >= 0 and lastx - i + lownum < bd and lasty + i < bd and lasty + i - lownum >= 0 :
                for j in range (0, self.lownums) :
                    if self.state[lasty+i-j][lastx-i+j] != 0 :
                        isStone += self.state[lasty+i-j][lastx-i+j]
                    else :
                        isStone = 0
                        break
                if isStone == self.lownums and pmv == 1 :
                    return 1
                elif isStone == self.lownums*2 and pmv == 2 :
                    return 2
                else :
                    isStone = 0

        bkpoint = -1

        for i in range (bd) :
            for j in range (bd) :
                if self.state[j][i] == 0 :
                    bkpoint = 0
        return bkpoint

    def __repr__(self): #시템이 해당 객체를 이해할 수 있는 형식으로 전환해줌.
        s = "  | "
        for i in range (bd) :
            s += str(i%10)
            s += " | "
        s += "\n"

        for i in range(bd):
            s += "---"
            for j in range (bd) :
                s += "----"
            s += "\n"
            s += str(i%10)
            s += " | "
            for k in range (bd) :
                s += str(self.state[i][k])
                s += " | "
            s += "\n"

        return s
