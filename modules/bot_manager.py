import json, re
botParams = json.load(open('config/bot.json'))
from chatterbot.conversation import Statement

def change_conf_rate(mssg, telegramClient, chat_id):
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

def learn_new_response(mssg, bot):
	"""
	Finds the input and the output from the mssg argument by searching for double quotation marks 
	(1st capturing group is the input, 2nd is the output). Teaches the bot the assotiation between 
	those menssages.
	"""
	input_mssg = re.search(r'([\"])(?:(?=(\\?))\2.)*?\1', mssg.text).group(0).replace('"',"")
	output_mssg = re.search(r'([\"])(?:(?=(\\?))\2.)*?\1', mssg.text).group(1).replace('"',"")
	bot.learn_response(Statement(output_mssg), Statement(input_mssg))