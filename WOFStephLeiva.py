from config import dictionaryloc
from config import wheeltextloc
from config import welcomeloc
from config import maxrounds
from config import vowelcost
from config import finalprize
from config import finalRoundTextLoc

import random

players={1:{"roundtotal":0,"gametotal":0,"name":""},
         2:{"roundtotal":0,"gametotal":0,"name":""},
         3:{"roundtotal":0,"gametotal":0,"name":""},
        }
roundNum = 1
dictionary = []
turntext = ""
wheelList = []
roundWord = ""
roundUnderscoreWord = ""
vowels = {"a", "e", "i", "o", "u"}
consonants = {'b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z'}
roundStatus = ""
finalRoundText = ''
welcomeMessage = ''

def readDictionaryFile():
    global dictionary
    opendict = open(dictionaryloc) 
    readdict = opendict.read().splitlines()
    dictionary = readdict
    opendict.close()

def readFinalRoundTxtFile():
    global finalRoundText  
    openfinalroundtxt = open(finalRoundTextLoc)
    readfinalroundtxt = openfinalroundtxt.read()
    finalRoundText = readfinalroundtxt
    print(finalRoundText)
    
def readWheelTxtFile():
    global wheelList
    openwheeltxt = open(wheeltextloc)
    readwheeltxt = openwheeltxt.read().splitlines()
    wheelList = readwheeltxt
    
def displayWelcomeMessage():
    global welcomeMessage
    openwelcome = open(welcomeloc)
    readwelcome = openwelcome.read()
    welcomeMessage = readwelcome
    print(welcomeMessage)

def getPlayerInfo():
    global players
    print('Now let\'s meet our contestants.')
    players[1]["name"] = input("Player 1, enter your name:  ")
    players[2]["name"] = input("Player 2, enter your name:  ")
    players[3]["name"] = input("Player 3, enter your name:  ")
    print(f'Welcome, {players[1]["name"]}, {players[2]["name"]} and {players[3]["name"]}.\n')    # read in player names from command prompt input
    
def getWord():
    global dictionary
    global roundWord
    global roundUnderscoreWord
    import random
    for i in range(len(dictionary)):
        roundWord = (f'{random.choice(dictionary)}')    #choose random word from dictionary
    roundUnderscoreWord = str('_'*len(roundWord))   #make a list of the word with underscores instead of letters.

def wofRoundSetup():
    global players
    global roundWord
    global roundUnderscoreWord
    global initPlayer
    print('The starting player will be chosen at random.')
    initPlayer = (random.choice(list(players.keys())))     # Return the starting player number (random)
    print(f'{players[initPlayer]["name"]}, you are up first for Round {roundNum}!')
    getWord()   # Use getWord function to retrieve the word and the underscore word (blankWord)
    wofTurn(initPlayer)

def nextPlayer(playerNum):    #there's likely a better way to do this but this works for now! not sustainable on larger scale.
    while True:
        if playerNum == 2:
            wofTurn(3)
            break
        elif playerNum == 3:
            wofTurn(1)
            break
        elif playerNum== 1:
            wofTurn(2)
            break

def wofTurn(playerNum):  
    global roundWord
    global roundUnderscoreWord
    global players

    stillinTurn = True
    while stillinTurn:
        choice = input(f'{players[playerNum]["name"]}, type \'S\' to spin the wheel, \'B\' to buy a vowel, or \'G\' to guess word:   ')           
        if(choice.strip().upper() == "S"):
            stillinTurn = spinWheel(playerNum)
        elif(choice.strip().upper() == "B"):
            stillinTurn = buyVowel(playerNum)
        elif(choice.upper() == "G"):
            stillinTurn = guessWord(playerNum)
        else:
            print("Not a correct option")        


def spinWheel(playerNum):
    global wheelList
    global players
    global vowels
    global spinOutcome

    print("You've chosen to spin the wheel.")
    wheelNum = random.randint(0,len(wheelList)-1)       # Get random wedge on wheellist
    spinOutcome = wheelList[wheelNum]
    stillinTurn = True
    if spinOutcome == 'LOSE TURN':      # Check for lose turn
        print("Oh no! You landed on LOSE TURN! You've lost this turn.")
        stillinTurn = False
        nextPlayer(playerNum)
    elif spinOutcome == 'BANKRUPT':     # Check for bankrupcy, and take action.
        print("Oh no! You landed on BANKRUPT! Your round total is now $0 and you've lost this turn.")
        players[playerNum]['roundtotal'] = 0
        stillinTurn = False
        nextPlayer(playerNum)
    else:
        print(f'Woohoo! You landed on ${spinOutcome}!')
        isitvowel = True
        while isitvowel is True:
            letter = input(f'Guess a consonant a chance to win ${spinOutcome} for every correct letter:    ')
            if letter in vowels:
                print("You entered a vowel. Please guess a consonant. You only spin and win for consonants.")
            elif letter in consonants:
                guessletter(letter,playerNum)    # Use guessletter function to see if guess is in word, and return count
                isitvowel = False
                continue
    return stillinTurn


def guessletter(letter, playerNum): 
    global players
    global roundUnderscoreWord

    goodGuess = False
    stillinTurn = True
    if letter not in roundWord :
        print('Oh no! The letter is not in the word.')
        nextPlayer(playerNum)
        goodGuess = False
        stillinTurn = False
    elif letter in roundUnderscoreWord:
        print(f'The letter {letter} has already been revealed.')
    else:
        index = [i for i, l in enumerate(roundWord) if l == letter]
        for i in index:
            roundUnderscoreWord = roundUnderscoreWord[:i] + letter + roundUnderscoreWord[i+1:]
        if roundUnderscoreWord == roundWord:
            fullword(playerNum)
        else:
            count = roundWord.count(letter)
            print(f'You have guessed correctly. The letter {letter} appears in the word {count} times.')    # return count of letters in word. 
            print(roundUnderscoreWord)
            players[playerNum]["roundtotal"]= players[playerNum]["roundtotal"]+(int(spinOutcome) * count)
            print(f'{players[playerNum]["name"]}\'s current round bank is ${players[playerNum]["roundtotal"]}. ')   # Change player round total if they guess right.     
            goodGuess = True    # return goodGuess= true if it was a correct guess
            stillinTurn = True
    return goodGuess, stillinTurn

def buyVowel(playerNum):
    global players
    global vowels
    global roundUnderscoreWord
    stillinTurn = True
    goodGuess = True
    if players[playerNum]["roundtotal"] < vowelcost:        # Ensure player has 250 for buying a vowelcost
        print("You do not have enough money to buy a vowel.")
        goodGuess = False
        stillinTurn = False
        wofTurn(playerNum)      #it is still their turn!
    else:
        isitconsonant = True
        while isitconsonant is True:
            vowelletter = input("What vowel do you want to buy for $250?:    ")
            if vowelletter in consonants:
                print("You entered a consonant. Please guess a vowel.")
            elif vowelletter in roundUnderscoreWord:
                print(f'The vowel {vowelletter} has already been revealed.')
            elif vowelletter in vowels: 
                players[playerNum]["roundtotal"] = players[playerNum]["roundtotal"] - (int(vowelcost)) 
                if vowelletter in vowels:
                    index = [i for i, l in enumerate(roundWord) if l == vowelletter]
                    for i in index:
                        roundUnderscoreWord = roundUnderscoreWord[:i] + vowelletter + roundUnderscoreWord[i+1:]
                    if roundUnderscoreWord == roundWord:
                        fullword(playerNum)
                    else:
                        count = roundWord.count(vowelletter)
                        print(f'You have guessed correctly. The vowel {vowelletter} appears in the word {count} time(s).')    # return count of letters in word. 
                        print(roundUnderscoreWord)
                        print(f'{players[playerNum]["name"]}\'s current round bank is ${players[playerNum]["roundtotal"]}.')   # Change player round total if they guess right.   
                        goodGuess = True
                        stillinTurn = True
                else:
                    print('Oh no! That vowel is not in the word. You still pay $250.')
                    print(roundUnderscoreWord)
                    print(f'{players[playerNum]["name"]}\'s current round bank is {players[playerNum]["roundtotal"]}.')
                    goodGuess = False  
                    stillinTurn = False
                    nextPlayer(playerNum)
                isitconsonant = False   
    return goodGuess, stillinTurn      
        
def guessWord(playerNum):
    global players
    global roundWord
    fullguess = input(f'Enter your full word guess:    ')
    if fullguess == roundWord:
        fullword(playerNum)
    else:
        print('Oh no! That is not correct! Good guess though.')
        nextPlayer(playerNum)    
    return False
    
def fullword(playerNum):
    global roundNum
    global maxrounds

    print(f'The word was {roundWord}.')
    print(f'Congratulations {players[playerNum]["name"]}, you have won this round!')
    players[playerNum]["gametotal"] += players[playerNum]["roundtotal"]
    players[1]["roundtotal"] *= 0
    players[2]["roundtotal"] *= 0
    players[3]["roundtotal"] *= 0
    print('Here is everyone\'s earnings.')
    print(players)
    print(f'End of Round {roundNum}.\n')
    roundNum +=1
    if roundNum == maxrounds:
        wofFinalRound()
    else:
        print(f'Now on to Round {roundNum}!')
        wofRoundSetup()


def rstlne():
    global roundUnderscoreWord   #can't figure out how to do it from a whole string/list of rstlne. If I were to come back to this with more time, I'd make this muuuuuch simpler
    letter = ('r')
    index = [i for i, l in enumerate(roundWord) if l in letter]
    for i in index:
        roundUnderscoreWord = roundUnderscoreWord[:i] + letter + roundUnderscoreWord[i+1:]
    letter = ('s')
    index = [i for i, l in enumerate(roundWord) if l in letter]
    for i in index:
        roundUnderscoreWord = roundUnderscoreWord[:i] + letter + roundUnderscoreWord[i+1:]
    letter = ('t')
    index = [i for i, l in enumerate(roundWord) if l in letter]
    for i in index:
        roundUnderscoreWord = roundUnderscoreWord[:i] + letter + roundUnderscoreWord[i+1:]
    letter = ('l')
    index = [i for i, l in enumerate(roundWord) if l in letter]
    for i in index:
        roundUnderscoreWord = roundUnderscoreWord[:i] + letter + roundUnderscoreWord[i+1:]
    letter = ('n')
    index = [i for i, l in enumerate(roundWord) if l in letter]
    for i in index:
        roundUnderscoreWord = roundUnderscoreWord[:i] + letter + roundUnderscoreWord[i+1:]
    letter = ('e')
    index = [i for i, l in enumerate(roundWord) if l in letter]
    for i in index:
        roundUnderscoreWord = roundUnderscoreWord[:i] + letter + roundUnderscoreWord[i+1:]

def wofFinalRound():
    global roundWord
    global roundUnderscoreWord
    global finalRoundText
    winplayer = 0
    amount = 0
    
    print('Welcome to the Final Round!\n')
    print('The player with the highest game total so far will be entering the final round. And that player is...')
    maxGame = max(players, key=lambda v: players[v]['gametotal'])   #don't know how this works but found on internet for max val in nested dict.
    print(f'{players[maxGame]["name"]}!')
    readFinalRoundTxtFile()
    getWord()
    rstlne()
    print('Here is final word.')
    print(roundUnderscoreWord)
    isitvowel = True
    while isitvowel is True:
        consonantguess1 = input('Enter consonant #1:    ')      #there's likely a better way to do this. but this works for now. not feasible on larger scale.
        if consonantguess1 in vowels:
            print("Please start with entering consonants")
            isitvowel = True
        elif consonantguess1 in consonants:
            index = [i for i, l in enumerate(roundWord) if l in consonantguess1]
            for i in index:
                roundUnderscoreWord = roundUnderscoreWord[:i] + consonantguess1 + roundUnderscoreWord[i+1:]
            isitvowel = False
            continue
    isitvowel = True
    while isitvowel is True:
        consonantguess2 = input('Enter consonant #2:    ')
        if consonantguess2 in vowels:
            print("Please start with entering consonants")
            isitvowel = True
        elif consonantguess2 in consonants:
            index = [i for i, l in enumerate(roundWord) if l in consonantguess2]
            for i in index:
                roundUnderscoreWord = roundUnderscoreWord[:i] + consonantguess2 + roundUnderscoreWord[i+1:]
            isitvowel = False
            continue
    isitvowel = True
    while isitvowel is True:
        consonantguess3 = input('Enter consonant #3:    ')
        if consonantguess3 in vowels:
            print("Please start with entering consonants.")
            isitvowel = True
        elif consonantguess3 in consonants:
            index = [i for i, l in enumerate(roundWord) if l in consonantguess3]
            for i in index:
                roundUnderscoreWord = roundUnderscoreWord[:i] + consonantguess3 + roundUnderscoreWord[i+1:]
            isitvowel = False
            continue
    isitconsonant = True
    while isitconsonant is True:
        vowelguess = input('Enter one vowel:    ')
        isitconsonant = True
        if vowelguess in consonants:
            print("Please enter a vowel.")
        elif vowelguess in vowels:
            index = [i for i, l in enumerate(roundWord) if l == vowelguess]
            for i in index:
                roundUnderscoreWord = roundUnderscoreWord[:i] + vowelguess + roundUnderscoreWord[i+1:]
            isitconsonant = False
    print(f'With your new letters, the final word is now: {roundUnderscoreWord}.')
    print('You have five seconds to answer!')

    from threading import Timer

    timeout = 5
    t = Timer(timeout, print, [f'Oooh unforuntalely, you ran out of time.The final word was {roundWord}.'])
    t.start()
    finalguess = input('Enter your final full word guess:    ')
    t.cancel()

    if finalguess != roundWord:
        print(f'Oooh unfortunately, that is incorrect. The final word was {roundWord}.')
    elif finalguess == roundWord:
        print('That is a good guess...great guess even...')
        print(f'...because you are absolutely correct! The final word was {roundWord}!')
        print(f'{players[maxGame]["name"]}, you have just won ${finalprize}!!')
    print(f'Thank you for playing\nWHEEL\nOF\nFORTUNE')
    print('*iconic outro music*')
    exit()

def main():
    displayWelcomeMessage()
    getPlayerInfo()
    readDictionaryFile()
    readWheelTxtFile()
    wofRoundSetup()

if __name__ == "__main__":
     main()
