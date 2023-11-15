import pygame as pg
import math

bsize = 19
board = [[0 for i in range (bsize)] for j in range (bsize)] #board, input like [yaxis, xaxis]
turn = 1

def print_board() :
    for i in range(bsize) :
        for j in range(bsize) :
            print(board[i][j], end = " ")
        print('\n')
    print('\n')

pg.init()

def printBoard(board, turn) :
    BLACK= ( 0,  0,  0)
    WHITE= (255,255,255)
    RED  = (255,  0,  0)
    BCOL = (219, 178, 92)
    CLCE = (45,45,45)

    size  = [900,1200]

    screen= pg.display.set_mode(size)

    done = False

    clock = pg.time.Clock()

    #print board setting
    lblk = 20 #interval between board and edge of screen
    lnum = bsize - 1 #number of board line

    ublk = size[1]-size[0]+lblk #interval between up of board and up edge of screen
    lwid = math.ceil((size[0]-2*lblk)/(lnum+2)) #interval each line
    lwid += lwid%2
    hwid = lwid/2 #range of axis
    csiz = math.floor(lwid/3)

    bblk = (((lwid//2)//5)+2)*5 #interval between edge of board and first line

    bwid = size[0]-2*lblk-2*bblk #size of playing board (first line to end line)

    #fixing error value (to make int point)
    llft = math.trunc((bwid-lnum*lwid)/2) 
    lrgt = round((bwid-lnum*lwid)/2)

    #line start point
    xstart = bblk+lblk+llft
    ystart = ublk+bblk+llft
    xyends = bblk+lblk+lrgt

    #define type of font
    numfont = pg.font.SysFont('arial', bblk-6)

    #save last move and orders
    lastmove = [-1, -1]
    orders = 0

    #drawing total
    while not done :
        if orders%2 == 0 :
            member = "BLACK"
        else :
            member = "WHITE"

        pg.display.set_caption("AI SIX-MOK. Turn = " + member + ", order = " + str(orders))

        #game exit
        for event in pg.event.get() :
            if event.type == pg.QUIT :
                done = True

        #fill background
        screen.fill(BLACK)

        #make board
        pg.draw.rect(screen, BCOL, [lblk, ublk, size[0]-2*lblk, size[0]-2*lblk])

        #make line 
        for i in range (bsize) :
            text_num = numfont.render(str(i%10),True, CLCE)

            #horision line
            pg.draw.line(screen, BLACK, [xstart, ystart+(lwid*i)], [size[0]-xyends, ystart+(lwid*i)],3)
            screen.blit(text_num,(xstart+lwid*i-6,ystart-bblk-6))

            #vertical line
            pg.draw.line(screen, BLACK, [xstart+(lwid*i), ystart], [xstart+(lwid*i), size[1]-xyends],3)
            screen.blit(text_num,(xstart-bblk,ystart+lwid*i-bblk/2))

        #display the stone already put.
        for i in range(bsize) :
            for j in range (bsize) :
                if board[i][j] != 0 :
                    if board[i][j] == 1 :
                        pg.draw.circle(screen, BLACK, [xstart+lwid*j, ystart+lwid*i], lwid*0.4)
                    elif board[i][j] == 2 :
                        pg.draw.circle(screen, WHITE, [xstart+lwid*j, ystart+lwid*i], lwid*0.4)
        
        #display the last move
        if lastmove != [-1, -1] :
            pg.draw.circle(screen, RED, [xstart+lwid*lastmove[0], ystart+lwid*lastmove[1]], csiz/2)
        
        #get mouse position
        mx,my = pg.mouse.get_pos()
        
        #if mouse on the board, set xais and yaxis
        if mx > xstart-hwid and mx < size[0]-xyends+hwid and my > ystart-hwid and my < size[1]-xyends+hwid :
            xaxis = int((mx-xstart+lwid/2)//lwid)
            yaxis = int((my-ystart+lwid/2)//lwid)
            
            #display the present position
            if turn == 1 :
                pg.draw.circle(screen, BLACK, [xstart+lwid*xaxis, ystart+lwid*yaxis], csiz, 2)
            elif turn == 2 :
                pg.draw.circle(screen, WHITE, [xstart+lwid*xaxis, ystart+lwid*yaxis], csiz, 2)
            
            #put the stome
            for event in pg.event.get() :
                if event.type == pg.MOUSEBUTTONDOWN and board[yaxis][xaxis] == 0:
                    board[yaxis][xaxis] = turn
                    lastmove = [xaxis, yaxis]
                    turn = 3-turn
                    orders += 1

                    #print_board()
            
        pg.display.flip()

    pg.quit()

printBoard(board, turn)