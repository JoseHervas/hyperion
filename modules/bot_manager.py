import json, re
botParams = json.load(open('config/bot.json'))

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

#TODO: LEARN NEW RESPONSES