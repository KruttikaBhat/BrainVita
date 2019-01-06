import pygame
from pygame.locals import *
import time
import threading

board=threading.Lock()
mutex=threading.Lock()
turn=1

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)
BLUE= (0,0,255)
YELLOW=(255,255,0)

rad=24
inc=50
s=7
mousex=0
mousey=0
wrong=0


display_width = 1400
display_height = 1000
size = [display_width, display_height]
pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption("BrainVita")
clock = pygame.time.Clock()

class player:
    def __init__(self,x,y,n):
        self.x_i= x
        self.y_i = y
        self.num=n
        self.B = [[0 for x in range(s)] for y in range(s)]
        self.score=0
        self.c=4
        self.fclick=0
        self.X=self.x_i-inc/2
        self.Y=self.y_i-inc/2
        self.x_1=0
        self.y_1=0
        self.I_1=0
        self.J_1=0
        self.cx=0
        self.cy=0

p1=player(100,100,1)
p2=player(800,100,2)

def text_format(message, textFont, textSize, textColor):
    newFont=pygame.font.Font(textFont, textSize)
    newText=newFont.render(message, 0, textColor)

    return newText



# Game Fonts
font = "gomarice_game_music_love.ttf"

def layout(p):

    for i in range(s):
        for j in range(s):
            p.B[i][j]=1
    for i in (0,1,5,6):
        for j in (0,1,5,6):
            p.B[i][j]=0
    p.B[3][3]=-1
    x=p.x_i
    y=p.y_i
    for i in range(0,7):
        for j in range(0,7):
            if p.B[i][j]!=0:
                if p.B[i][j]==-1:
                    pygame.draw.circle(screen,WHITE,[x,y],rad)
                else:
                    pygame.draw.circle(screen,GREEN,[x,y],rad)
            x=x+inc
        y=y+inc
        x=p.x_i
    score_display()
    pygame.display.flip()



def score_display():
    myfont = pygame.font.Font(None, 50)
    screen.blit(myfont.render("SCORE",1,YELLOW),(500,50))
    player1 = myfont.render("Player 1: %d  " % (p1.score), 1, YELLOW)
    player2 = myfont.render("Player 2: %d  " % (p2.score), 1, YELLOW)
    title1 = myfont.render("Player 1", 1, YELLOW)
    title2 = myfont.render("Player 2", 1, YELLOW)
    screen.fill(BLACK, rect=player1.get_rect(topleft=(500,100)))
    screen.fill(BLACK, rect=player2.get_rect(topleft=(500,140)))
    screen.blit(player1, (500, 100))
    screen.blit(player2, (500, 140))
    screen.blit(title1, (175, 500))
    screen.blit(title2, (875, 500))
    pygame.display.update()

def message_display(display):
    font = pygame.font.Font(None, 50)
    text = font.render(display, True, WHITE)
    text_rect = text.get_rect()
    screen.blit(text, [display_width/2 - (text_rect[2]/2), (display_height/2)+100])
    pygame.display.update()
    time.sleep(1)
    pygame.draw.rect(screen,BLACK,[display_width/2 - (text_rect[2]/2), (display_height/2)+100,text_rect.width,text_rect.height])
    pygame.display.update()


def moves(p):
    p.c=0
    for i in range(0,7):
        if (p.c==0):
            for j in range(0,7):
                if p.c==0:
                    if ((i<5) and (p.B[i+1][j]==1) and (p.B[i+2][j]==1)):
                        p.c=1
                    elif (i>1) and (p.B[i-1][j]==1) and (p.B[i-2][j]==1):
                        p.c=1
                    elif (j<5) and (p.B[i][j+1]==1) and (p.B[i][j+2]==1):
                        p.c=1
                    elif (j>1) and (p.B[i][j-1]==1) and (p.B[i][j-2]==1):
                        p.c=1

def updateScore(p):
    p.score=p.score+1
    print("\nScore of player ",p.num," is:",p.score)


def movemarble(p):
    global turn
    global mousex
    global mousey
    i=int((mousex-p.X)//inc)
    j=int((mousey-p.Y)//inc)
    x=p.x_i+inc*i
    y=p.y_i+inc*j
    #print(i,'\t',j)
    #print('\n',fclick,'\t')
    print("\n",p.fclick," ",j," ",i," ",mousex-x," ",p.B[i][j])


    if p.fclick==0 and (j>=0) and (j<7) and (i>=0) and \
       (i<7) and ((mousex-x)<=(2*rad)) and \
       ((mousey-y)<=(2*rad)) and (p.B[i][j]==1):

       p.x_1=x
       p.y_1=y
       p.I_1=i
       p.J_1=j
       (p.cx,p.cy)=(p.x_i+i*inc,p.y_i+j*inc)
       pygame.draw.circle(screen,BLUE,[p.cx,p.cy],rad)
       pygame.display.flip()
       print("\nBlue: ",p.cx,",",p.cy)
       p.fclick=1
       clock.tick(10)


    elif p.fclick==1:
        mx=p.x_i+inc*(i+p.I_1)/2
        my=p.y_i+inc*(j+p.J_1)/2
        mi=int((p.I_1+i)/2)
        mj=int((p.J_1+j)/2)
        if (j>=0) and (j<7) and (i>=0) and (i<7) and \
           ((mousex-x)<=(2*rad)) and ((mousey-y)<=(2*rad)) and \
           (((abs(i-p.I_1)==2) and (abs(j-p.J_1)==0)) or \
           ((abs(i-p.I_1)==0) and (abs(j-p.J_1)==2))) and \
           (p.B[i][j]==-1) and (p.B[mi][mj]==1):
             #Fills the position to which the selected marble is moved
             (cnewx,cnewy)=(p.x_i+i*inc,p.y_i+j*inc)
             pygame.draw.circle(screen,GREEN,[cnewx,cnewy],rad)
             pygame.display.flip()
             p.B[i][j]=1
             print("\n1. Green: ",cnewx,",",cnewy)
             #Empties the position that was selected first
             pygame.draw.circle(screen,WHITE,[p.cx,p.cy],rad)
             pygame.display.flip()
             p.B[p.I_1][p.J_1]=-1
             print("\n2. White: ",p.cx,",",p.cy)
             #Empties the middle positon
             cx=p.x_i+mi*inc
             cy=p.y_i+mj*inc

             pygame.draw.circle(screen,WHITE,[cx,cy],rad)
             pygame.display.flip()
             p.B[mi][mj]=-1
             print("\n3. white: ",cx,",",cy)
             p.fclick=0
             #print("\ninside if ",fclick)
             clock.tick(50)
             t2 = threading.Thread(target=moves,args=(p,))
             t3 = threading.Thread(target=updateScore,args=(p,))
             t4 = threading.Thread(target=score_display,)
             t2.start()
             t3.start()
             t4.start()
             t2.join()

             t3.join()
             t4.join()
             mutex.acquire()
             turn=turn%2
             print("\n",turn)
             turn=turn+1
             mutex.release()
             print("\nTurn after change: ",turn)
             board.release()
        else:
            print("\nIllegal move!")
            message_display("ILLEGAL MOVE")
            illegal=1
            p.fclick=0
            clock.tick(50)
            pygame.draw.circle(screen,GREEN,[p.cx,p.cy],rad)
            pygame.display.flip()
            board.release()



def play(p):
    done = False
    global turn
    global mousex
    global mousey
    global wrong
    while p.c>0:
        clock.tick(10)
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                p.c=-1 # Flag that we are done so we exit this loop
                #pygame.quit()
            elif event.type == MOUSEBUTTONDOWN:
                mousex, mousey = event.pos 
                print("\nturn: ",turn," player:",p.num," wrong:",wrong)

                print("\n",mousex," ",p.x_i," ",p.x_i+7*inc," ",mousey," ",p.y_i," ",p.x_i+7*inc)
                """
                if turn==p.num and mousex>p.x_i and mousex<p.x_i+7*inc and p.illegal==1:
                    p.illegal=0
                    board.acquire()
                    movemarble(p)
                """
                if turn==p.num and mousex>p.x_i and mousex<p.x_i+7*inc:
                    if p.fclick==0 and wrong!=1:
                        board.acquire()
                    elif p.fclick==0 and wrong==1:
                        wrong=0
                    print("\nPlayer ",p.num," Clicks: ",p.fclick)

                    movemarble(p)

                elif turn!=p.num and p.fclick==0 and not(mousex>p.x_i and \
                     mousex<p.x_i+7*inc):
                    print("\nWrong board")
                    #message_display("Wrong board!")
                    wrong=1
                    #board.acquire()

            if p1.c==0 and p2.c==0:
                mutex.release()

            if p.c==0:
                mutex.acquire()
                time.sleep(1)
                screen.fill(BLACK)
                pygame.display.update()
                if p1.score>p2.score:
                    winner=1
                else:
                    winner=2
                message_display("Player ",winner," WINS!!!")
                #message_display("GAME OVER")
                time.sleep(2)

    pygame.display.flip()


def main():
    screen.fill(BLACK)

    layout(p1)
    layout(p2)
    #board.acquire()
    t1=threading.Thread(target=play,args=(p1,))
    t2=threading.Thread(target=play,args=(p2,))
    t1.start()
    time.sleep(3)
    t2.start()
    t1.join()
    t2.join()


def main_menu():

    menu=True
    selected="start"

    while menu:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_UP:
                    selected="start"
                elif event.key==pygame.K_DOWN:
                    selected="quit"
                if event.key==pygame.K_RETURN:
                    if selected=="start":
                        main()
                    if selected=="quit":
                        pygame.quit()
                        quit()

        # Main Menu UI
        screen.fill(BLACK)
        title=text_format("BrainVita", font, 100, BLUE)
        if selected=="start":
            text_start=text_format("START", font, 75, GREEN)
        else:
            text_start = text_format("START", font, 75, RED)
        if selected=="quit":
            text_quit=text_format("QUIT", font, 75, GREEN)
        else:
            text_quit = text_format("QUIT", font, 75, RED)

        title_rect=title.get_rect()
        start_rect=text_start.get_rect()
        quit_rect=text_quit.get_rect()

        # Main Menu Text
        screen.blit(title, (display_width/2 - (title_rect[2]/2), 200))
        screen.blit(text_start, (display_width/2 - (start_rect[2]/2), 400))
        screen.blit(text_quit, (display_width/2 - (quit_rect[2]/2), 500))
        pygame.display.update()
        clock.tick(10)
        pygame.display.set_caption("Python - Pygame Simple Main Menu Selection")

#Initialize the Game
main_menu()
#pygame.quit()
#quit()
