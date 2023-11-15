from math import *
import random
import copy

class Node:
    def __init__(self, move = None, parent = None, state = None):
        self.move = move
        self.parentNode = parent
        self.childNodes = []
        self.wins = 0
        self.visits = 0
        self.untriedMoves = state.getMoves()
        self.playerJustMoved = state.playerJustMoved

    def UCTSelectChild(self):
        s = sorted(self.childNodes, key = lambda c: c.wins/c.visits + sqrt(2 * log(self.visits) / c.visits)) #알고리즘을 통한 정렬
        return s[-1]  #마지막값(가장 큰 값) 리턴

    def AddChild(self, m ,s): #부모노드에 자식 노드 추가
        n = Node(move = m, parent = self, state = copy.deepcopy(s))
        self.untriedMoves.remove(m)
        self.childNodes.append(n)
        return n

    def Update(self, result): #게임 결과 입력
        self.visits += 1
        self.wins += result

    def __repr__(self): #훈련 결과값 출력
        return "player "+str(self.playerJustMoved) + "[M" + str(self.move) + " W/V " + str(self.wins) + "/" + str(self.visits) + " " + str(round((self.wins/self.visits)*100,2))+ " %" +" U" + str(self.untriedMoves) + "]"

    def ChildrenToString(self):
        s = ''
        for c in self.childNodes:
            s += str(c) + "\n"
        return s
