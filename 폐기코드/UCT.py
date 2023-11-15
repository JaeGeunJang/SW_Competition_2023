import MCTS
import random
import copy

def UCT(rootstate, itermax):
    rootnode = MCTS.Node(state = rootstate)
    for i in range(itermax):
        if i%100 == 0 :
            print("Itermax" + str(i))
        node = rootnode #tictactoe
        state = copy.deepcopy(rootstate)

        #selection #적절한 자식노드 선택
        while node.untriedMoves == [] and node.childNodes != []:
            node = node.UCTSelectChild()
            state.doMoves(node.move)

        #Expansion #탐험, 선택되지 않은 자식노드 추가
        if node.untriedMoves != []:
            m = random.choice(node.untriedMoves)
            curState = state.playerJustMoved
            state.doMoves(m)
            state.playerJustMoved = curState
            node = node.AddChild(m, state)
            state.playerJustMoved = node.playerJustMoved

        #simulation #선태된 노드에 대해서 랜덤하게 게임 진행
        while state.getMoves() != []:
            state.doMoves(random.choice(state.getMoves()))

        #BackPropagation 결과값에따른 노드 업데이트, 승률(가중치) 입력.
        while node != None:
            node.Update(state.getResult(node.playerJustMoved))
            node = node.parentNode

    print (rootnode.ChildrenToString())
    #승률에 따라서 자식 노드들 정렬
    s = sorted(rootnode.childNodes, key = lambda c: c.wins/c.visits)
    return sorted(s, key = lambda c: c.visits)[-1].move #가장 승률이 높은 값 결정.