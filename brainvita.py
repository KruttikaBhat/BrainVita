"""
Brain Vita (Solo Noble)

Authors:
CED16I010 - Kruttika Bhat
CED16I030 - Shruti Raghavan
CED16I045 - Madhumita Murali

Instructions:

The  board  consists  of  holes  (positions)  that  can
hold marbles. All  positions  except  one  have marbles
placed  in  them  at  the  beginning   of the  game.  A
valid  move  for  a  marble   is   moving  it  from its
position to  an empty position (which is  two positions
away, horizontally, or  vertically)  by  jumping over a
non-empty position. The  marble in  the jumped position
is removed from  the board. The game ends when there is
no valid move.

The objective is  to  move marbles such that at the end
of  the game, there are  as  few marbles as possible. A
single  marble  is  a  perfect  result.

The score is displayed  on  the top right corner.

The  following  code  implements  Brain  Vita in python
using  the  pygame  library.
It  uses the concept of  threads to implement the score,
layout  and  move  methods  parallely.
Green Circle: Position filled with marble.
White Circle: Empty position.
Blue Circle: Selected marble. 
"""
import pygame
from pygame.locals import *
import time
import threading
#Colors
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)
BLUE= (0,0,255)
YELLOW=(255,255,0)
#Constants
x_i=100
y_i=100
rad=24
inc=50
s=7
score=0
#The dynamically updated base array
B = [[0 for x in range(s)] for y in range(s)]
c=4
display_width = 1100
display_height = 4000
size = [display_width, display_height]
pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption("BrainVita")
clock = pygame.time.Clock()
def layout():
    """
    This method prepares the board on the screen.
    It is run by a thread of its own.
    """
    screen.fill(BLACK)
    for i in range(s):
        for j in range(s):
            B[i][j]=1
    for i in (0,1,5,6):
        for j in (0,1,5,6):
            B[i][j]=0
    B[3][3]=-1
    x=x_i
    y=y_i
    for i in range(0,7):
        for j in range(0,7):
            if B[i][j]!=0:
                if B[i][j]==-1:
                    pygame.draw.circle(screen,WHITE,[x,y],rad)
                else:
                    pygame.draw.circle(screen,GREEN,[x,y],rad)
            x=x+inc
        y=y+inc
        x=x_i
    score_display()
    pygame.display.flip()
def score_display():
    """
    This method displays the score.
    It is run by a thread of its own.
    """
    global score
    myfont = pygame.font.SysFont("monospace", 15)
    label = myfont.render("Score: %d" % (score), 1, YELLOW)
    screen.fill(BLACK, rect=label.get_rect(topleft=(500,100)))
    screen.blit(label, (500, 100))
    pygame.display.update()
def message_display(display):
    """
    This method displays messages
    It is run by a thread of its own.
    """
    font = pygame.font.Font(None, 50)
    text = font.render(display, True, WHITE)
    text_rect = text.get_rect()
    text_x = screen.get_width() / 2 - text_rect.width / 2
    text_y = screen.get_height() / 2 - text_rect.height / 2
    screen.blit(text, [500, 350])
    pygame.display.update()
    time.sleep(1)
    pygame.draw.rect(screen,BLACK,[500,350,text_rect.width,text_rect.height])
    pygame.display.update()
def moves():
    """
    This method checks is there's at least 1 valid move left.
    It is run by a thread of its own.
    """
    global c
    c=0
    for i in range(0,7):
        if (c==0):
            for j in range(0,7):
                if c==0:
                    if ((i<5) and (B[i+1][j]==1) and (B[i+2][j]==1)):
                        c=1
                    elif (i>1) and (B[i-1][j]==1) and (B[i-2][j]==1):
                        c=1
                    elif (j<5) and (B[i][j+1]==1) and (B[i][j+2]==1):
                        c=1
                    elif (j>1) and (B[i][j-1]==1) and (B[i][j-2]==1):
                        c=1
def updateScore():
    """
    This method updates the score as the player plays.
    It is run by a thread of its own.
    """
    global score
    score=score+1
    print("\nScore: ",score)
def play():
    """
    This is the main play method.
    """
    mousex = 0
    mousey = 0
    done = False
    X=x_i-inc/2
    Y=y_i-inc/2
    fclick=0
    global c
    global score
    t1 = threading.Thread(target=layout)
    t1.start()
    while c>0:
        clock.tick(10)
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                c=-1 # Flag that we are done so we exit this loop
            elif event.type == MOUSEBUTTONDOWN: #mouse button is clicked
                mousex, mousey = event.pos
                i=int((mousex-X)//inc)
                j=int((mousey-Y)//inc)
                x=x_i+inc*i
                y=y_i+inc*j
                print(i,'\t',j)
                print('\n',fclick,'\t')
                #checks if mouse is over a marble
                if fclick==0 and (j>=0) and (j<7) and (i>=0) and \
                   (i<7) and ((mousex-x)<=(2*rad)) and \
                   ((mousey-y)<=(2*rad)) and (B[i][j]==1):
                   x_1=x
                   y_1=y
                   I_1=i
                   J_1=j
                   (cx,cy)=(x_i+i*inc,y_i+j*inc)
                   pygame.draw.circle(screen,BLUE,[cx,cy],rad)
                   pygame.display.flip()
                   fclick=1
                   clock.tick(10)
                #For the second click to remove a marble
                elif fclick==1:
                    mx=x_i+inc*(i+I_1)/2
                    my=y_i+inc*(j+J_1)/2
                    mi=int((I_1+i)/2)
                    mj=int((J_1+j)/2)
                    if (j>=0) and (j<7) and (i>=0) and (i<7) and \
                       ((mousex-x)<=(2*rad)) and ((mousey-y)<=(2*rad)) and \
                       (((abs(i-I_1)==2) and (abs(j-J_1)==0)) or \
                       ((abs(i-I_1)==0) and (abs(j-J_1)==2))) and \
                       (B[i][j]==-1) and (B[mi][mj]==1):
                         #Fills the position to which the selected marble is moved
                         (cnewx,cnewy)=(x_i+i*inc,y_i+j*inc)
                         pygame.draw.circle(screen,GREEN,[cnewx,cnewy],rad)
                         pygame.display.flip()
                         B[i][j]=1
                         #Empties the position that was selected first
                         pygame.draw.circle(screen,WHITE,[cx,cy],rad)
                         pygame.display.flip()
                         B[I_1][J_1]=-1
                         #Empties the middle positon
                         cx=x_i+mi*inc
                         cy=y_i+mj*inc
                         pygame.draw.circle(screen,WHITE,[cx,cy],rad)
                         pygame.display.flip()
                         B[mi][mj]=-1
                         fclick=0
                         print("\ninside if ",fclick)
                         clock.tick(50)
                         t2 = threading.Thread(target=moves,)
                         t3 = threading.Thread(target=updateScore,)
                         t4 = threading.Thread(target=score_display,)
                         t2.start()
                         t3.start()
                         t4.start()
                         t2.join()
                         t3.join()
                         t4.join()
                         print("\nc: ",c)
                    else:
                        print("\nIllegal move!")
                        t5 = threading.Thread(target=message_display,args=("ILLEGAL MOVE",))
                        t5.start()
                        fclick=0
                        clock.tick(50)
                        pygame.draw.circle(screen,GREEN,[cx,cy],rad)
                        pygame.display.flip()

            if score==31:
                time.sleep(1)
                screen.fill(BLACK)
                pygame.display.update()
                t6 = threading.Thread(target=message_display,args=("YOU WIN!!!",))
                t6.start()
                time.sleep(2)
                c=-1
            if c==0:
                time.sleep(1)
                screen.fill(BLACK)
                pygame.display.update()
                t7 = threading.Thread(target=message_display,args=("GAME OVER",))
                t7.start()
                time.sleep(2)
    pygame.display.flip()
def main():
    """
    This is the driver method that invokes the play method.
    """
    play()
    #closes the pygame application
    pygame.quit()
main()
