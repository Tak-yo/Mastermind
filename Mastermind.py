import pygame, random, time, easygui, threading
# define the variables

orange = [255, 127, 0]
red = [255, 0, 0]
yellow = [255, 255, 0]
green = [0,255,0]
purple =[100,0,127]
blue = [0, 0, 255]
bgColor = [0, 130, 255]
black = [0,0,0]
blank = [255,255,255]

colors = ["red", "yellow", "orange", "blue", "green","purple"]
playerCode = ["blank","blank","blank","blank"]

y = 960
x = 323
yrect = 924
y_cir = 960
xrect = 288
left = 70
right = 70
playerPosition = 0
screen = ""
code = []

#Initialise game
def initGame():
    global code
    global screen
    y = 960
    x = 323
    pygame.init()
    screen = pygame.display.set_mode([747,994])
    screen.fill([0,130 ,255])
    #Draws player"s circles
    for i2 in range(4):
        for i1 in range(10):
            pygame.draw.circle(screen, [255,255,255], [x, y], 30, 0)
            y -= 100
        x += 100
        y = 960

    #Draws checking circles
    x = 50
    for i2 in range(10):
        for i1 in range(4):
            pygame.draw.circle(screen, blue, [x,y], 20, 0)
            x += 50
        x = 50
        y -= 100

    pygame.display.flip()

    isRepeat = easygui.buttonbox("Do you want to include the possibility of repeats?",
                            choices = ["Yes", "No"])

    if isRepeat == "Yes":
        code = random.choices(colors,k = 4)
    else:
        code = random.sample(colors,4)

    #Draws player cursor
    pygame.draw.rect(screen, [0,0,0], [xrect, yrect,left, right], 1)

#checks player"s code against answer

def check():
    global yrect
    global playerCode
    global colors
    global code
    global y_cir
    global xrect
    checkCursor = 3
    stats = []
    r_pegs = 0
    
    colors = []
    colors.extend(code)

    for i in range(4):
        if colors[checkCursor] == playerCode[checkCursor]:
            stats.append("True")
            r_pegs += 1
            del colors[checkCursor]
            del playerCode[checkCursor]
        else:
            stats.append("False")
        checkCursor -= 1
    w_pegs = 0
    index = len(playerCode)-1
    for i in range(4):
        if stats[index] == "False":
            if playerCode[index] in colors:
                w_pegs= w_pegs + 1
        index -= 1
    x_cir = 50

    
    if r_pegs == 0 and w_pegs == 0:
        pygame.draw.rect(screen, red, [25, y_cir- 3, 200, 5], 0)
    for i in range(r_pegs):
        pygame.draw.circle(screen, red, [x_cir, y_cir], 20, 0)
        x_cir = x_cir + 50
    for i in range(w_pegs):
        pygame.draw.circle(screen, [255,255,255], [x_cir, y_cir], 20, 0)
        x_cir = x_cir + 50
    
    pygame.display.flip()

# if player wins
    if r_pegs == 4:
        easygui.msgbox("You win!")
        pygame.quit()

#if player loses
    elif yrect == -76 and r_pegs != 4:
        joined_code = " ".join(code)
        easygui.msgbox("You Lose!")
        easygui.msgbox("The code was: ""+ joined_code  +"".")
        pygame.quit()

# reset player guess and code checking
    else:
        del stats[:]
        del playerCode[:]
        playerCode = ["blank","blank","blank","blank"]
    #move player to next guess
        pygame.draw.rect(screen, bgColor, [xrect, yrect, 70, 70],1)
        yrect = yrect - 100
        y_cir = y_cir - 100
        pygame.draw.rect(screen, black, [xrect, yrect, 70, 70],1)

#Set the color of selected pin
def setColor(color):
    global xrect
    pygame.draw.circle(screen, color, [xrect+35, yrect+36], 30, 0)
    playerCode[playerPosition] = str(color)
    pygame.display.flip()
    print(playerCode)

def moveCursor(direction):
    global xrect
    global playerPosition
    if (direction== "left" and xrect > 290):
        pygame.draw.rect(screen, bgColor, [xrect, yrect,left, right], 2)
        xrect -= 100
        playerPosition -= 1
        pygame.draw.rect(screen, black, [xrect, yrect,left, right], 1)
    elif (direction == "right" and xrect < 580):
        pygame.draw.rect(screen, bgColor, [xrect, yrect,left, right], 2)
        xrect += 100
        playerPosition += 1
        pygame.draw.rect(screen, black, [xrect, yrect,left, right], 1)
    pygame.display.flip()

#defines "game"
def runGame():
    global yrect
    global y_cir
    global xrect
    global playerPosition
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    moveCursor("left")
                elif event.key == pygame.K_RIGHT:
                    moveCursor("right")
                elif event.key == pygame.K_r:
                    setColor(red)
                elif event.key == pygame.K_o:
                    setColor(orange)
                elif event.key == pygame.K_y:
                    setColor(yellow)
                elif event.key == pygame.K_g:
                    setColor(green)
                elif event.key == pygame.K_p:
                    setColor(purple)
                elif event.key == pygame.K_b:
                    setColor(blue)
                elif event.key == pygame.K_SPACE:
                    setColor(blank)
                elif event.key == pygame.K_RETURN:
                    check()
                    
                pygame.display.flip()

