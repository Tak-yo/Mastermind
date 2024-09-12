import itertools, random
import numpy as np

colors = ["red", "yellow", "orange", "blue", "green","purple"]
guessables =[]
playerGuess = []
score = []
minimax = []
code = random.sample(colors,4)
turns = 0 

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

def compareCode(guess,code):
    red = 0
    white = 0
    for x,y in zip(guess,code):
        if x==y:
            red += 1
    #white pegs
    whitePegs = [x for x in code if x in guess]
    white = len(whitePegs) - red
    return red,white 

def scoreDist(code):
    global answers
    #create matrix of scores, red by white
    distr = np.full((5, 5), 0)
    #For a given code in guessables, check the possibility of getting an outcome from answers, then create a pdf of all outcomes
    for ans in answers:
        score = compareCode(code, ans)
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

def maxInfo():
    global guessables,answers
    bestGuess = ''
    bestGuessValue = 0
    for guess in guessables:
        if (expectedInfo(guess)>bestGuessValue):
            bestGuess = guess
            bestGuessValue = expectedInfo(guess)
    return bestGuess

def minScore(code):
    distr = scoreDist(code)
    maxVal = 0
    for row in distr:
        for score in row:
            if (score>maxVal):
                maxVal = score
    return code, maxVal

def minimax():
    global guessables,answers
    bestGuess = ''
    bestGuessValue = np.inf
    for guess in guessables:
        if (minScore(guess)[1]<bestGuessValue):
            bestGuess = minScore(guess)[0]
            bestGuessValue = minScore(guess)[1]
            
    return bestGuess   
    
def playTurn(guess):
    global guessables, answers, playerGuess, turns

    #set the playerGuess
    playerGuess = guess 
    score = compareCode(playerGuess,code)
    if not((score == (4,0) or turns>10)):
        print(playerGuess,score)
        
        #Remove that guess from guessables - no point guessing it anymore
        guessables = [x for x in guessables if x != playerGuess]

        #If not won, remove from the list of possible answers any code that would not give the same response if the current guess were the code
        for answer,index in zip(answers,range(len(answers))):
            if compareCode(playerGuess,answer) != score:
                answers.pop(index)  
        
        Uncertainty = round(np.log2(len(answers)),3)
        print("Remaining Uncertainty: " + str(Uncertainty))

        
        # Apply minimax technique to choose your next guess that would eliminate most possible solutions
        nextGuess = minimax()       
        turns += 1
        playTurn(nextGuess)
    elif (score == (4,0)):
        print('You win!')
        print("Turns: " + str(turns))
    else:
        print("You Lose!")
        print("Code was: " + str(code))
#initialise game

init()

#Play an initial guess of red, red, yellow, yellow

playTurn(playerGuess)