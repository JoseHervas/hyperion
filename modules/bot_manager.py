# -*- coding: utf-8 -*-

import json, re
botParams = json.load(open('config/bot.json'))
from chatterbot.conversation import Statement

def change_conf_rate(mssg, telegramClient, chat_id, bot):
	"""
	This function finds the new confidence rate from the mssg argument, and edits the 
	config/bot.json file with it
	"""
	new_conf_rate = re.search(r'\d{1}.\d{2}', mssg.text)
	if (new_conf_rate):
		botParams['min_confidence_rate'] = new_conf_rate.group()
		try:
			with open('config/bot.json', mode='w') as f:
				f.write(json.dumps(botParams, indent=2))
			return True
		except:
			return False

def learn_new_response(mssg, telegramClient, chat_id, bot):
	"""
	Finds the input and the output from the mssg argument by searching for double quotation marks 
	(1st capturing group is the input, 2nd is the output). Teaches the bot the assotiation between 
	those menssages.
	"""
	texts=re.findall(r'\"(.+?)\"',mssg.text)
	if (len(texts) > 0):
		input_mssg = texts[0].replace('"',"").strip()
		output_mssg = texts[1].replace('"',"").strip()
		bot.learn_response(Statement(output_mssg), Statement(input_mssg))
	else:
		telegramClient.send_message(chat_id, "Disculpa, podrías poner la frase que debo aprender y la frase a la que va asociada entre comillas, porfa?")