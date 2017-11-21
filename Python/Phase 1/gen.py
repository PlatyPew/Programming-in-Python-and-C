from wgAI import *

used = []
with open('wordlist.txt') as f:
	wordlist = f.readlines()
	f.close()

while True:
	word = input('> ')
	if word == 'q':
		break
	used.append(word)
	used.append(ai.impossible(word,used,wordlist))
