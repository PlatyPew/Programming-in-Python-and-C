class validate:
	def validLength(word):
		if len(word) < 6:
			return True # Invalid
		else:
			return False # Valid

	def lowerCase(word):
		return not word.islower()

	def newLetters(orig,word):
		number = len(set(list(word))-set(list(orig)))
		if number > 2:
			return True
		else:
			return False

	def noRepeats(word,wordsUsed):
		for i in wordsUsed:
			if word == i:
				return True
		return False

	def noEndWithING(word):
		if word[-3:] == 'ing':
			return True
		else:
			return False

	def inWordList(word,wordlist):
		for words in wordlist:
			if word == words.strip():
				return False
		return True
