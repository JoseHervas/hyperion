# -*- coding: utf-8 -*-

# Configuration
import json
apiParams = json.load(open('config/apis.json'))
available_commands = json.load(open('commands.json', encoding='utf-8'))
userParams = json.load(open('config/user.json'))

# General utils
from sys import argv
from pathlib import Path
import random

# Conversational engine
from chatterbot import ChatBot
from chatterbot.comparisons import jaccard_similarity 
from chatterbot.response_selection import get_most_frequent_response
from chatterbot.trainers import ChatterBotCorpusTrainer
from controllers import command_handlers, msg_handlers
from utils import custom_comparisons


# Telegram API
import telebot
telegram = telebot.TeleBot(apiParams['Telegram']['API-key'])

# Arise, my champion! - Whitemane
bot = ChatBot(
    'Hyperion',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        'utils.custom_logic_adapters.BM_external_confidence'
    ],
    preprocessors=[
        'utils.custom_preprocessors.skip_name'
    ],
    statement_comparison_function=custom_comparisons.jaccard,
    response_selection_method=get_most_frequent_response,
    database_uri='sqlite:///db/db.sqlite3',
    read_only=True
)

# Initial training (if needed)
if ("-train" in argv):
    print("Training the mastermind...")
    for p in Path(".").glob("db.sqlite3*"):
        p.unlink()
    trainer = ChatterBotCorpusTrainer(bot)
    trainer.train("chatterbot.corpus.spanish")

# This will decide to which controller call
def handle_message(message):
    mssg = message[0]
    chat_id = mssg.chat.id
    username = mssg.chat.username
    # Don't talk to strangers, kids!
    if (username == userParams['username']):
        # Are you asking for a command?
        command = msg_handlers.search_commands(mssg, available_commands)
        if (command):
            # 1.) Execute the command's script
            command_handlers.handle_command(command, mssg, telegram, chat_id, bot)
            # 2.) Send one of the command's standard responses
            response = random.choice(available_commands[command]['Responses'])
            telegram.send_message(chat_id, response)
            return
        # Not a command? then call the generic function
        else:
            msg_handlers.generic_text_message(bot, mssg, telegram)
    else:
        response = 'Lo siento, no estoy autorizado para responder a tus mensajes.'
        telegram.send_message(chat_id, response)

# This will attach the handle_message fuction to every message sent by Telegram
telegram.set_update_listener(handle_message)


telegram.polling(none_stop=True)

