#!/usr/bin/env python3
#Sample code to illustrate the usage of wgEngine2017 to facilitate a
#Player vs Machine wordgame.
#Program skeleton was provided by Mr Karl Kwan
#Author:
#Daryl Lim (1625608) DISM/FT/2B/22
#Lim Chun Yu (1625273) DISM/FT/2B/22
import random
import re
import time
import socket
import threading
from wgEngine2017 import *

TIMEOUT = 10 # default 10 seconds timeout for keyboard input.
PENALTY = 20
NON_USED = 2
SLOW_PENALTY = 5
REJECT_OR_TMOUT = 10
HALT_NOW = 20
WINNING_SCORE = 50
MAX_ROUND = 50
RESPONSE_LIMIT=40
SLOW_RESPONSE = 30
PORT = 8899

def my_input(con,tm=TIMEOUT,defval=None):
	# receives client input and timesout after specified time
	try:
		con.settimeout(float(tm))
		name = con.recv(255).decode()
		if name == None:
			name=defval
		return name
	except Exception as inst:
		# timeout
		return defval

def aiTurn(buf,maindict,engine,pnum,ai):
	# aiTurn returns a True or False
	# Return False only when ai is leading more than 20 points.
	GRN=BColors.GRN
	RED=BColors.RED
	BLU=BColors.BLU
	ENDC=BColors.ENDC
	startAt = time.time()
	buf = sendData("\n"+engine.players[pnum]["name"]+"'s turn => ",dataBuffer=buf,end='')
	if engine.players[1]["score"] - engine.players[0]["score"]<PENALTY:
		#It is not leading enough to quit and win.
		input=ai.findMutation(engine.curword,engine.mydict)
	else:
		input='q' # ai will quit the game when it is winning.
	buf = sendData(input,dataBuffer=buf)
	duration = time.time()-startAt
	if duration >= RESPONSE_LIMIT:
		duration = 40.00
	buf = sendData("{0}response time : {1:0.2f} s.{2}".format(GRN,duration,ENDC),dataBuffer=buf)
	if input == None:
		engine.players[pnum]["score"] = engine.players[pnum]["score"] - REJECT_OR_TMOUT
		buf = sendData("\n{0}Input time out. {1} points penalty. {2}".format(RED,REJECT_OR_TMOUT,ENDC),dataBuffer=buf)
		return buf, True
	if input == 'q':
		# special marks reduction for this.
		engine.players[pnum]["score"] = engine.players[pnum]["score"] - HALT_NOW
		buf = sendData("\n{0}Termination Request Accepted. {1} points penalty. {2}".format(RED,HALT_NOW,ENDC),dataBuffer=buf)
		return buf, False  # user wants to quit immediately.
	isok, mesg = engine.isValid(input,maindict)
	if (not isok):
		buf = sendData("{0}{1} {2} points penalty. {3}".format(RED,mesg,REJECT_OR_TMOUT,ENDC),dataBuffer=buf)
		engine.players[pnum]["score"] = engine.players[pnum]["score"] - REJECT_OR_TMOUT
		return buf, True
	# The input is accepted.
	# need to compute the score
	c_score,score_str=engine.compute_score(input)
	buf = sendData(score_str,dataBuffer=buf)
	if duration > SLOW_RESPONSE:
		buf = sendData("{0}Response too slow.{1} points penalty.{2}".format(RED,SLOW_PENALTY,ENDC),dataBuffer=buf)
		c_score = c_score - SLOW_PENALTY
	engine.players[pnum]["score"] = engine.players[pnum]["score"] + c_score
	# add the input into mydict
	engine.add_used_word(input)
	# replace curword with input
	engine.curword = input
	return buf, True

def usersTurn(con,maindict,engine,pnum=0):
	# usersTurn returns a True or False
	# Return False only when user enters a single 'q' letter.
	try:
		GRN=BColors.GRN
		RED=BColors.RED
		BLU=BColors.BLU
		ENDC=BColors.ENDC
		
		startAt = time.time()
		input = my_input(con,tm=RESPONSE_LIMIT)
		duration = time.time()-startAt
		if duration >= RESPONSE_LIMIT:
			duration = 40.00
		buf = sendData("{0}response time : {1:0.2f} s.{2}".format(GRN,duration,ENDC),dataBuffer='')
		if input == None:
			engine.players[pnum]["score"] = engine.players[pnum]["score"] - REJECT_OR_TMOUT
			buf = sendData("\n{0}Input time out. {1} points penalty. {2}".format(RED,REJECT_OR_TMOUT,ENDC),dataBuffer=buf)
			return buf, True
		if input == 'q':
			# special marks reduction for this.
			engine.players[pnum]["score"] = engine.players[pnum]["score"] - HALT_NOW
			buf = sendData("\n{0}Termination Request Accepted. {1} points penalty. {2}".format(RED,HALT_NOW,ENDC),dataBuffer=buf)
			print("Players connected : {}".format(threading.active_count()-2))
				
			return buf, False  # user wants to quit immediately.
		isok, mesg = engine.isValid(input,maindict)
		if (not isok):
			buf = sendData("{0}{1} {2} points penalty. {3}".format(RED,mesg,REJECT_OR_TMOUT,ENDC),dataBuffer=buf)
			engine.players[pnum]["score"] = engine.players[pnum]["score"] - REJECT_OR_TMOUT
			return buf, True
		# The input is accepted.
		# need to compute the score
		c_score,score_str=engine.compute_score(input)
		buf = sendData(score_str,dataBuffer=buf)
		if duration > SLOW_RESPONSE:
			buf = sendData("{0}Response too slow.{1} points penalty.{2}".format(RED,SLOW_PENALTY,ENDC),dataBuffer=buf)
			c_score = c_score - SLOW_PENALTY
		engine.players[pnum]["score"] = engine.players[pnum]["score"] + c_score
		# add the input into mydict
		engine.add_used_word(input)
		# replace curword with input
		engine.curword = input
		return buf, True
	except Exception as e:
		pass

def sendData(data,dataBuffer='',end='\n'):
	#appends data to buffer for socket sendall
	dataBuffer += data+end
	return(dataBuffer)

def playgame(maindict,engine,con):
	try:
		GRN=BColors.GRN
		RED=BColors.RED
		BLU=BColors.BLU
		ENDC=BColors.ENDC
		engine.curword = random.choice(list(maindict.mDict.keys()))
		engine.add_used_word(engine.curword)    # add in the first word into mydict
		pname0 = con.recv(255).decode()
		#player 1 is the ai.
		#need to create a aiMutationFinder
		ai = MutationFinder(maindict)
		engine.players[0]["name"]=pname0
		engine.players[1]["name"]='betaGone' # overwrite the default player name.
		buf = ''
		while True:
			pnum=(engine.round + 1 ) % 2
			buf = sendData("\nAt Round "+str(engine.round),dataBuffer=buf)
			for i in range(2):
				buf = sendData("{0} scores: {1}   ".format(engine.players[i]["name"],engine.players[i]["score"]),dataBuffer=buf,end="")
			buf += '\n'
			buf = sendData("Current word: {0}{1}{2}".format(BLU,engine.curword,ENDC),dataBuffer=buf)
			if not pnum:
				clientData = buf.encode()
				con.sendall(clientData)
				
				# Awaits client input
				buf, conti = usersTurn(con,maindict,engine,pnum)
				if not conti:
					break
			else:
				buf, conti = aiTurn(buf,maindict,engine,pnum,ai)
				if not conti:
					break
		 
			# only check for winner at the end of an 'even' ROUND.
			if engine.round % 2 == 0:
				if engine.players[0]["score"] >= WINNING_SCORE or engine.players[1]["score"] >= WINNING_SCORE:
					break
			if engine.round >= MAX_ROUND:
				break                     # game ends at 50th round
			engine.round=engine.round+1
		# end of while loop
		
		buf = sendData("{0}{1}".format(BLU,engine.get_final_scores()),dataBuffer=buf)
		if engine.isDrawn():
			buf = sendData("Wow, what a close fight, both of you are winners!{0}".format(ENDC),dataBuffer=buf,end='')
			print("Players connected : {}".format(threading.active_count()-2))
            
		elif engine.isPlayerWon():
			buf = sendData("Congratulation to "+engine.players[0]["name"]+ " , you are the champion!{0}".format(ENDC),dataBuffer=buf,end='')
			print("Players connected : {}".format(threading.active_count()-2))
		else:
			buf = sendData(engine.players[0]["name"]+ ", you have put up a good fight, try harder next time.{0}".format(ENDC),dataBuffer=buf,end='')
			print("Players connected : {}".format(threading.active_count()-2))
		buf = sendData('*',dataBuffer=buf,end='')
		clientData = buf.encode()
		con.sendall(clientData)
		con.close()
		return
	except Exception as e:
		print("Players connected : {}".format(threading.active_count()-2))
			

def main():
	serversocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	i=0
	try:
		#listening on port for client
		print('Listening on port {}...'.format(PORT))
		print('Press control-c to shutdown server')
		serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		serversocket.bind(('0.0.0.0',PORT))
		serversocket.listen(5)
		while True:
			myengine = WGEngine()
			maindict = MainDict()
			#accept socket and start thread
			connection, address = serversocket.accept()
			#makes new thread when client connects
			t = threading.Thread(target=playgame, args=(maindict,myengine,connection))
			#start thread for client
			t.start()
			print("Players connected : {}".format(threading.active_count()-1))
	except KeyboardInterrupt:
		print('\nServer shutting down!')
	except socket.error:
		print('Socket encountered some error!')
	except Exception as e:
		print('Runtime error:\n',e)
	finally:
		serversocket.close()
#main program start here
#
if __name__ == '__main__':
	main()
