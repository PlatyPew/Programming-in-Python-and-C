#!/usr/bin/env python3

import random
from wgValidate import *
from wgScore import *

def validation(orig,word,wordsUsed):
	if validate.validLength(word):
		return False
	elif validate.newLetters(orig,word):
		return False
	elif validate.noRepeats(word,wordsUsed):
		return False
	elif validate.noEndWithING(word):
		return False
	return True

class ai:
	def easy(orig,wordsUsed,wordlist):
		wordSent = None
		randomLine = random.randrange(int(len(wordlist) * 0.75))
		for i in range(randomLine,len(wordlist)):
			string,points = score.sameLetters(orig,wordlist[i].strip())
			if validation(orig,wordlist[i].strip(),wordsUsed) and points <= 15:
				wordSent = wordlist[i].strip()
				break
		print("AI's turn => " + wordSent)
		return wordSent

	def hard(orig,wordsUsed,wordlist):
		wordSent = None
		diff = 0
		randomLine = random.randrange(int(len(wordlist) * 0.75))
		for i in range(randomLine,len(wordlist)):
			string,points = score.sameLetters(orig,wordlist[i].strip())
			if validation(orig,wordlist[i].strip(),wordsUsed) and points > 15:
				wordSent = wordlist[i].strip()
				break
		print("AI's turn => " + wordSent)
		return wordSent

	def impossible(orig,wordsUsed,wordlist):
		diff = 0
		finalword = ""
		current = 0
		for word in wordlist:
			if validation(orig,word.strip(),wordsUsed):
				string,points = score.sameLetters(orig,word.strip())
				diff += points
				string,points = score.missingLetters(orig,word.strip())
				if points:
					diff -= points
				if diff > current :
					current = diff
					finalword = word.strip()
				diff = 0
		print("AI's turn => "+finalword)
		return finalword