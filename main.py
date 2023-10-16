import NmokRule
import MCTS
import random
import copy

tbd = NmokRule.bd
test = [1,2] #1 is player play, 2 is computer play
p1Inter = 1000
p2Inter = 20000


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


def UCTPlayGame():
    state = NmokRule.Nmok()
    while state.getMoves() != []:
        print (str(state))
        if state.playerJustMoved == 1:
            if test[0] == 1 :
            # if want play player to player(test code)
                while True :
                    m = input("Player " + str(state.playerJustMoved) + " which Do you want? : ")
                    m = m.split()
                    m[0] = int(m[0])
                    m[1] = int(m[1])

                    if m[1] >= 0 and m[1] < tbd and m[0] >= 0 and m[0] < tbd and state.state[m[1]][m[0]] == 0 :
                        break
            if test[0] == 2 :
                print("Player 1")
                rootstate = copy.deepcopy(state)
                m = UCT(rootstate, itermax = p1Inter)
                print ("Best Move : " ,end = ' ')
                print(m)
                print()

        else:
            if test[1] == 1 :
                while True :
                    m = input("Player " + str(state.playerJustMoved) + " which Do you want? : ")
                    m = m.split()
                    m[0] = int(m[0])
                    m[1] = int(m[1])

                    if m[1] >= 0 and m[1] < tbd and m[0] >= 0 and m[0] < tbd and state.state[m[1]][m[0]] == 0 :
                        break

            if test[1] == 2 :
                print("Player 2")
                rootstate = copy.deepcopy(state)
                m = UCT(rootstate, itermax = p2Inter)
                print ("Best Move : " ,end = ' ')
                print(m)
                print()
        state.doMoves(m)

    print(str(state))

    if state.getResult(state.playerJustMoved) == 1.0:
        print ("Player " + str(state.playerJustMoved) + " Wins!!")

    elif state.getResult(state.playerJustMoved) == 0.0:
        print ("Payer " + str(3 - state.playerJustMoved) + " Wins!!")

    else: print ("Draw!!") # 무승부


if __name__ == "__main__":
    UCTPlayGame() #메인 함수 실행.
