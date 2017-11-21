class BColors:
    # a utility class to provide the control sequence for
    # the color / attribute effects (gnome-terminal)
    HEADER = '\033[95m'
    BLU = '\033[94m'
    GRN = '\033[92m'
    RED = '\033[31m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
#end of class BColors
class WGMenus:
    # a utility class to provide the showmenu function
    # to display the help or overview menus  
    def showmenu(x):
        overview='''
Objective of the game:

This is a two players game. It will first prompt the players to enter their
names to start a new game session. A game session begins by showing a random
initial challenging word. Each player will then take turn to enter a new
word to response to the challenge according to the game rules and earn points.
Repeat the above process until the game session is over. 
The game session will be terminated when one of the players scores 50 or more
points.
The player in play can also stop the game session by entering
a letter 'q' (subject to a penalty, see below).
The program will display the final scores of the two players and declare the result.
'''
        helpmenu='''
Game Rules:

. The two players will take turn to enter the replacement word.
. The word must be entered within 40 seconds or the player will lose his turn.
. The player in play will lose the turn immediately upon entering an invalid word. 
. The player in play can enter a single letter 'q' to stop the game.
. The game will be ended automatically when one of the players scores more than or equal to 50 points.
. The game will also be terminated when it reaches the 50th round.
. The challenging word reminds the same until a valid replacement word is entered.

Acceptance Rules for a new word:

. The minimum length of the word is 6 letters.
. It is listed in the internal dictionary.
. It has not been used in the current play session.
. It is made up by the letters of the current challenging word and/or plus no more than 2 new letters.
. It cannot be ended with -ing- .

Scoring Rules:
For each accepted new word:
. +2 point for each letter taken from the challenging word.
. -1 point for each unique unused letter from the challenging word.
. -5 points if it takes more than 30 seconds to enter the replacement word.
. -10 points for entering an invalid word or no input within the time limit (40 seconds).
. -20 points for halting the game (by enter a single letter 'q'). 

        '''
        if x == 'h':
            print(helpmenu)
        elif x == 'o':
            print(overview)
          

