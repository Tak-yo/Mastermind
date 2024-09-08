import Mastermind as mm
import itertools, time
import numpy as np

colors = ["red", "yellow", "orange", "blue", "green","purple"]
guessables =[]
playerGuess = []
score = []
minimax = []

mm.initGame()
print("game running")

def perm():
    guesses = []
    for p in itertools.product(colors,repeat = 4):
        guesses.append(list(p)) 
    return guesses

def init():
    global answers, guessables, minimax, playerGuess
    #initialise a list of posible answers and possible guesses
    answers = guessables = perm()   
    playerGuess = ['red','red','yellow','yellow']

def playGuess():
    print("playing guess")
    global playerGuess
    for pin in playerGuess:
        mm.setColor(pin)
        mm.moveCursor("right")

def scoreDist(code):
    global answers
    #create matrix of scores, red by white
    distr = np.full((5, 5), 0)
    #For a given code in guessables, check the possibility of getting an outcome from answers, then create a pdf of all outcomes
    for ans in answers:
        score = mm.compareCode(code, ans)
        #add score count to distribution
        distr[score[0]][score[1]] += 1
    return distr

def info(px):
    information = px*(np.log2(1/px))
    return information

def expectedInfo(code):
    total = len(answers)
    sdf = scoreDist(code)
    Ex = 0
    for row in sdf:
        for score in row:
            probability = float(score/total)
            if (probability>0):
                Ex += info(probability)   
    return Ex

def minimax():
    global guessables,answers
    bestGuess = ''
    bestGuessValue = 0
    for guess in guessables:
        if (expectedInfo(guess)>bestGuessValue and guess in answers):
            bestGuess = guess
            bestGuessValue = expectedInfo(guess)
    return bestGuess

def playTurn(guess):
    global guessables, answers, playerGuess

    #set the playerGuess
    playerGuess = guess 
    print(playerGuess)
    #play your guess
    playGuess()
    time.sleep(1)
    score = mm.check()
    time.sleep(1)
    
    #Remove that guess from guessables - no point guessing it anymore
    guessables = [x for x in guessables if x != playerGuess]

    #If not won, remove from the list of possible answers any code that would not give the same response if the current guess were the code
    for answer,index in zip(answers,range(len(answers))):
        if mm.compareCode(playerGuess,answer) != score:
            answers.pop(index)  
    
    print(len(answers))
    
    # Apply minimax technique to choose your next guess that would eliminate most possible solutions
    
    nextGuess = minimax()
    print (nextGuess)
    playTurn(nextGuess)
    
#initialise game

init()

#Play an initial guess of red, red, yellow, yellow

playTurn(playerGuess)

