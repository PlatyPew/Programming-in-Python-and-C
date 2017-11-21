#!/usr/bin/env python3
# A support module for the ST2411,ST2512 Wordgame2017.
# This module provide basic functions for
# wordgame menu display
# word validation
# score computation
# This module also consists a class, MutationFinder ,which can be used to support player vs machine name.
# 
import random
import re
import signal
import time
import socket
# word game engine in Python3
MATCH_LETTER=2
MISSING_LETTER=1
NEW_LETTER_LIMIT=2
class WGEngine():
     
    def __init__(self):
        self.mydict = {}
        self.smap = {}
        self.oldword =""
        self.curword =""
        self.newword =""
        self.round = 1
# set up an internal storage for the players names and scores
        self.players= { 0:{}, 1:{}}
        self.players[0]['name']='Anonymous'
        self.players[0]['score']=0      
        self.players[1]['name']='BetaGone'
        self.players[1]['score']=0

    @staticmethod    
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
        solo_overview='''
Objective of the game:

This is a player vs machine game. It will first prompt the player to enter his/her
name to start a new game session. A game session begins by showing a random
initial challenging word. The player and the machine will then take turn to enter a new
word to response to the challenge according to the game rules and earn points.
Repeat the above process until the game session is over. 
The game session will be terminated when the player or the machine scores 50 or more
points.
The player (or the machine) in play can also stop the game session by entering
a letter 'q' (subject to a penalty, see below).
The program will display the final scores of the player and the machine.
It also declares the result.
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
        elif x == 'l':
            print(solo_overview)
    def get_final_scores(self):
        result = "\n\nThe final scores:\n"
        for i in range(0,2):
            result +=self.players[i]['name']+": "+str(self.players[i]['score'])+".\n"
        return result
    def isDrawn(self):
        return self.players[0]["score"] == self.players[1]["score"]

    def isPlayerWon(self):
        return self.players[0]["score"]>self.players[1]["score"]

    def add_used_word(self,usedword):
        self.mydict[usedword] = 1
    def checkNewLetter(self,oword,nword):
        newlist = []
        for i in nword:
            if i not in oword and i not in newlist:
                newlist.append(i)
        return newlist
    def isValid(self,newword,fulldict):
        oldword = self.curword
        if len(newword) < 6:
            return False, "input is shorter than 6 characters"
        if re.search(r'[^a-z]+',newword):
            return False,"input contains non-lowercase character"
        if re.search(r'.*ing$',newword):
            return False,"input is ended with -ing-"
        if (not newword in fulldict.mDict.keys()): 
            return False, "input is not a valid word"
        if (newword in self.mydict.keys()):
            return False,"input has been used"
        # last check: if the new word contains more than two new unique letter
        newletters = self.checkNewLetter(oldword,newword)
        if len(newletters) > NEW_LETTER_LIMIT:
            return False,"input contains more than 2 new letters:{0}".format(str(newletters))
        # reach here implies the word is valid.
        return True , "Validation check is cleared"
        
    def compute_score(self,thisword):
        # for each existing letter found in thisword, score MATCH_LETTER else score 0
        # for each existing letter not found in thisword, deduct MISSING_LETTER points
        oldword = self.curword
        total = 0
        score_str = ""
        i = 0
        #debug
        #print("in compute_score old : {} , new :{}".format(self.curword,thisword))
        #first compute earned scores
        for c in thisword:
            i=i+1
            pt = 0
            if c in oldword:
                pt = MATCH_LETTER
            total = total + pt
            score_str = score_str+str(c)+"("+str(pt)+")"
            if i < len(thisword):
                score_str=score_str+"+ "
            else:
                score_str=score_str+" = "+str(total)
        #now compute non used letters penalty.
        nonusedlist = []
        for c in oldword:
            if c not in thisword and c not in nonusedlist:
                nonusedlist.append(c)
        if len(nonusedlist)>0:
            penalty = MISSING_LETTER * len(nonusedlist)
            total=total-penalty
            score_str=score_str+"\n{0} points deduction for not using {1}".format(penalty,str(nonusedlist))
        return total,score_str
        
# end of WGEngine class

class MainDict():
    def __init__(self,wlistfile="wordlist.txt"):
        self.mDict = {}
        self.wordlistfile = wlistfile
        self.loadwords()
    def loadwords(self):
        f=open(self.wordlistfile,"r")
        for word in f:
            newword=word.strip()
            if len(newword)<6:
                continue
            if re.search(r'.*ing$',newword):
                continue
            self.mDict[newword]=1
        f.close()
# end of class MainDict
class BColors:
    HEADER = '\033[95m'
    BLU = '\033[94m'
    GRN = '\033[92m'
    RED = '\033[31m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
#end of class BColors
class MutationFinder():
    def __init__(self, mDict):
        self.iPattern = {}
        self.wordlist = mDict
        self.genIndexing()
        
    def getextra(self,pattern):
        # return a list of mutated extra patterns from the give 'pattern'
        # The rule to get the extra patterns is simple:
        # Take out one and exactly one letter from the 'pattern' (at any position) gets
        # one extra pattern.
        # eg. pattern == 'aple' then the extra patterns are : ['ple','ale','ape', 'apl']
        
        result=[]
        for i in range(len(pattern)):
            w=pattern[:i]+pattern[i+1:]
            result.append(w)
        return result
                
    def getPattern(self,word):
        #The pattern consists of a sorted string that
        #made up by all the unique letters  from the word.
        #This is a supporting function for genIndexing()
        unique=sorted(list(set(word)))
        pat =  ''.join(unique)
        plist = [pat] 
        # we can get more patterns base on this pat.
        extra = self.getextra(pat)
        return plist+extra     
        
    def genIndexing(self):
        #This function will be called once only. It will generate a huge dictionary to map all possible unique patterns
        #with a corresponding matching word list . Key -> [ possible word list ]
        #print("enter genIndexing")
        #print("size of wordlist is {}".format(len(self.wordlist.mDict)))
        for w in self.wordlist.mDict: 
            newPatterns = self.getPattern(w)
            for newPat in newPatterns:
                if not newPat in self.iPattern:
                    self.iPattern[newPat]=[w]
                else:
                    self.iPattern[newPat].append(w)
        #print("size of iPattern is {}".format(len(self.iPattern)))
    def dumpPat(self,word):
        #utility function for debugging purpose
        for p in self.getPattern(word):
            print(p,self.iPattern[p])
            
    def findMutation(self,target,usedwords):
        # print("findM:",target,usedwords)
        # This is the main (and only) function to find and return a replacement word.
        mutation = []
        for p in self.getPattern(target):
            if p in self.iPattern:    # check if there is a corresponding list of words
                mutation += self.iPattern[p]
        mutation = list(set(mutation))
        answers = [ x for x in mutation if not x in usedwords and x != target ]
        if len(answers)>0:
            return random.choice(answers)
        return None
        
# end of class
