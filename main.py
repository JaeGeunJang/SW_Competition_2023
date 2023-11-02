import NmokRule
import copy
import UCT

tbd = NmokRule.bd
test = [1,2] #1 is player play, 2 is computer play
p1Inter = 1000
p2Inter = 20000


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
