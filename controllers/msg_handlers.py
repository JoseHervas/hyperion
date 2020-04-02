# -*- coding: utf-8 -*-
import json
from chatterbot.comparisons import LevenshteinDistance
from chatterbot.conversation import Statement
botParams = json.load(open('config/bot.json'))

def search_commands(message, commandList):
	for commandName in commandList:
		for commandString in commandList[commandName]['Sentences']:
			Levenshtein = LevenshteinDistance.compare('self', Statement(text=commandString), Statement(text=message.text))
			if (Levenshtein > float(botParams['min_confidence_rate'])):
				return commandName
	return False

def generic_text_message(bot, message, telegramClient):
	chat_id = message.chat.id
	response = bot.get_response(message.text)
	if (float(response.confidence) < float(botParams['min_confidence_rate'])):
		response1 = 'Lo siento, no sé qué responder a este mensaje. ¿Podrías enseñarme a responder a este tipo de mensajes?' 
		telegramClient.send_message(chat_id, response1)
	else:
		telegramClient.send_message(chat_id, response)
	return 