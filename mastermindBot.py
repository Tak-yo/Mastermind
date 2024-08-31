import Mastermind as mm
import itertools, time

colors = ["red", "yellow", "orange", "blue", "green","purple"]
guessables =[]
playerGuess = ""
score = []

mm.initGame()
print("game running")



def perm(num):
    guesses = []
    for p in itertools.product(range(num),repeat = 4):
        guesses.append(''.join(map(str, p))) 
    return guesses

def playGuess():
    print("playing guess")
    global playerGuess
    for pin in playerGuess:
        mm.setColor(colors[int(pin)])
        mm.moveCursor("right")
        

#create a set that represents all possible codes

answers = guessables = perm(len(colors)) 

#Play an initial guess of 0011

playerGuess = "0011"

#Remove that guess from guessables - no point guessing it anymore
guessables = [x for x in guessables if x != playerGuess]

playGuess()
time.sleep(1)
score = mm.check()
time.sleep(1)

#If not won, remove from the list of possible answers any code that would not give the same response if the current guess were the code

for code,index in zip(guessables,range(len(guessables))):
   if mm.compareCode(playerGuess,code) != score:
       del answers[index]  

# Apply minimax technique to pick the one that would eliminate most possible solutions

