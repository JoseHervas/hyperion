# -*- coding: utf-8 -*-
import json
from chatterbot.conversation import Statement
botParams = json.load(open('config/bot.json'))

def skip_name(statement):
	wordList = statement.replace('.',' ').replace(',', ' ').split(' ')
	if (botParams['name'] in wordList):
		wordList.remove(botParams['name'])
		str1 = ' '.join(wordList)
		output = Statement(text=str1)
	else:
		output = statement
	return output