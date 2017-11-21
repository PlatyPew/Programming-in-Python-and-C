class score:
	def sameLetters(curword,word):
		curword = list(curword)
		word = list(word)
		addedLetters = sorted(list(set(word) - set(curword)))
		scoring = []
		score = 0
		for letters in word:
			found = True
			for extra in addedLetters:
				if letters == extra:
					found = False
			if found:
				score += 2
				scoring.append(letters + '(2)')
			else:
				scoring.append(letters + '(0)')
		return scoring,score


	def missingLetters(curword,word):
		missingLetters = list(set(curword) - set(word))
		score = len(missingLetters)
		return missingLetters,score