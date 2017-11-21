#!/usr/bin/env python3
import random
import re
import signal
import time
import timeit
from wgAI import *
from wgUtil import *
from wgValidate import *
from wgScore import *
TIMEOUT = 10 # default 10 seconds timeout for keyboard input.
PENALTY = 20
NON_USED = 2
SLOW_PENALTY = 5
REJECT_OR_TMOUT = 10
HALT_NOW = 20
WINNING_SCORE = 50
MAX_ROUND = 50
RESPONSE_LIMIT = 40
SLOW_RESPONSE = 30
WORD_LIST_FILE = 'wordlist.txt'

# set up an internal storage for the players names and scores
players= { 0:{}, 1:{}}
players[0]['name']=''
players[0]['score']=0      
players[1]['name']=''
players[1]['score']=0

wordlist = []

# Here are the functions for user input with timeout options

def interrupted(signum, frame):
	# a signal triggered function,
	#it raises a ValueError once it is triggered.
	raise ValueError("interrupted")

def my_input(prompt,tm=TIMEOUT,defval=None):
#interrupt input if timeout 
	signal.signal(signal.SIGALRM, interrupted)
	signal.alarm(int(tm))
	try:
		name = input(prompt)
		signal.alarm(0)
		if name == '':
			name = defval
		return name
	except:
		# timeout
		return defval
## Here is a sample utility function that helps to return a formatted
## output to show the final scores
def get_final_scores():
	result = "\n\nThe final scores:\n"
	for i in range(0,2):
		result +=players[i]['name']+": "+str(players[i]['score'])+".\n"
	return result

# Chooses a random number and gets that line from the word list
def randomWord(wordlist):
	line = random.randrange(len(wordlist))
	return wordlist[line].strip()

## Here is the main game play function which control the game flow.
    
def playgame():
	GRN=BColors.GRN
	RED=BColors.RED
	BLU=BColors.BLU
	ENDC=BColors.ENDC
	round = 1

	print('''
	+-----------------------------------+
	| Welcome to the ST2411 Playground! |
	+-----------------------------------+
	''')
	cmd=""
	intel = 0
	while cmd != 's':
		cmd = my_input('''Type:
[s]tart to start,
[h]elp for help,
[o]verview for game objective,
[q]uit or
[a]i to play against AI
default [q] => ''',defval="q")
		if cmd in ['h','o']:
			WGMenus.showmenu(cmd)
		elif cmd == 'q':
			return
		elif cmd == 'a':
			difficulty = my_input('''
AI difficulty:
[e]asy
[h]ard
[i]mpossible
default [e] => ''',defval="e")
			if difficulty == 'e':
				print('You have chosen easy difficulty\n')
				intel = 1
			elif difficulty == 'h':
				print('You have chosen hard difficulty\n')
				intel = 2
			elif difficulty == 'i':
				print('You have chose impossible difficulty\n')
				intel = 3
			cmd='s'

	if intel == 0:
		pname0 = my_input("Player 1 name => ",defval="Anonymous 1")
		pname1 = my_input("Player 2 name => ",defval="Anonymous 2") 
		players[0]["name"]=pname0
		players[1]["name"]=pname1 # overwrite the default player name.
	else:
		pname0 = my_input("Player's name => ",defval="Anonymous")
		players[0]["name"]=pname0
		players[1]["name"]="AI" # overwrite the default player name.
	
	wordsUsed = []
	with open(WORD_LIST_FILE) as f:
		wordlist = f.readlines()
		f.close()
	curword = randomWord(wordlist)
	while True:
		wordsUsed.append(curword)
		print("\nAt Round "+str(round))
		pnum=(round + 1 )% 2
		for i in range(2):
			print("{0} scores: {1}   ".format(players[i]["name"],players[i]["score"]),end="")
		print()
		print("Current word: {0}{1}{2}".format(BLU,curword,ENDC))
		start_time = timeit.default_timer()
		if intel == 1 and pnum == 1:
			input = ai.easy(curword,wordsUsed,wordlist)
		elif intel == 2 and pnum == 1:
			input = ai.hard(curword,wordsUsed,wordlist)
		elif intel == 3 and pnum == 1:
			input = ai.impossible(curword,wordsUsed,wordlist)
		else:
			input = my_input(players[pnum]["name"]+"'s turn => ",tm=RESPONSE_LIMIT,defval=None)
		if input:
			input = input.strip()
		### Replace the following dummy sample section with you own
		##  program logic
		elapsed = timeit.default_timer() - start_time
		if int(elapsed) == RESPONSE_LIMIT:
			print("\n{0}Response time: {1:.2f}{2} s".format(GRN,elapsed,ENDC))
		else:
			print("{0}Response time: {1:.2f}{2} s".format(GRN,elapsed,ENDC))
		if input == None:
			players[pnum]["score"] = players[pnum]["score"] - REJECT_OR_TMOUT
			print ("{0}Input time out or no input given {1} points penalty. {2}".format(RED,REJECT_OR_TMOUT,ENDC))
		elif input == 'q':
		# special marks reduction for this.
			players[pnum]["score"] = players[pnum]["score"] - HALT_NOW
			print ("{0}Termination Request Accepted. {1} points penalty. {2}".format(RED,HALT_NOW,ENDC))
			break  # user wants to quit immediately.
		elif validate.validLength(input):
			players[pnum]["score"] = players[pnum]["score"] - REJECT_OR_TMOUT
			print ("{0}Length Not Valid. {1} points penalty. {2}".format(RED,REJECT_OR_TMOUT,ENDC))
		elif validate.lowerCase(input):
			players[pnum]["score"] = players[pnum]["score"] - REJECT_OR_TMOUT
			print ("{0}Characters are not all lowercase. {1} points penalty. {2}".format(RED,REJECT_OR_TMOUT,ENDC))
		elif validate.newLetters(curword,input):
			players[pnum]["score"] = players[pnum]["score"] - REJECT_OR_TMOUT
			print ("{0}More than 2 letters added. {1} points penalty. {2}".format(RED,REJECT_OR_TMOUT,ENDC))
		elif validate.noEndWithING(input):
			players[pnum]["score"] = players[pnum]["score"] - REJECT_OR_TMOUT
			print ("{0}Word ends with \'ing\' {1} points penalty. {2}".format(RED,REJECT_OR_TMOUT,ENDC))
		elif validate.noRepeats(input,wordsUsed):
			players[pnum]["score"] = players[pnum]["score"] - REJECT_OR_TMOUT
			print ("{0}Word has been used before. {1} points penalty. {2}".format(RED,REJECT_OR_TMOUT,ENDC))
		elif validate.inWordList(input,wordlist):
			players[pnum]["score"] = players[pnum]["score"] - REJECT_OR_TMOUT
			print ("{0}Invalid word used. {1} points penalty. {2}".format(RED,REJECT_OR_TMOUT,ENDC))
		else:
			string,points = score.sameLetters(curword,input)
			print(' + '.join(string),'=',points)
			players[pnum]["score"] += points
			add=points
			string,points = score.missingLetters(curword,input)
			if len(string):
				print(points,'points deduction for not using',string)
				players[pnum]["score"] -= points
			curword = input
			if elapsed > SLOW_RESPONSE:
				players[pnum]["score"] = players[pnum]["score"] - SLOW_PENALTY
				print ("{0}Response too slow. {1} points penalty. {2}".format(RED,SLOW_PENALTY,ENDC))
		
		### 
		####
		round = round + 1
		if round > MAX_ROUND:
			break                     # game ends at 50th round
		elif ((players[0]["score"] >= WINNING_SCORE ) or (players[1]["score"] >= WINNING_SCORE ))and (round+1)%2==0:
			break
	# end of while loop

	print("{0}{1}{2}".format(BLU,get_final_scores(),ENDC))
	if players[0]["score"] == players[1]["score"]:
		print("Wow, what a close fight, both of you are winners!")
	elif players[0]["score"] > players[1]["score"]:
		print ("Congratulation to "+players[0]["name"]+ ", you are the champion!")
	else:
		print ("Congratulation to "+players[1]["name"]+ ", you are the champion!")

def main():
	playgame()
	print ("\nSee you again Soon.")
#main program start here
#
if __name__ == '__main__':
	main()
