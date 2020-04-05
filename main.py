# -*- coding: utf-8 -*-

# Configuration
import json
apiParams = json.load(open('config/apis.json'))
available_commands = json.load(open('commands.json', encoding='utf-8'))
userParams = json.load(open('config/user.json'))

# General utils
import random
from utils import printer
printer.print_banner()

# Conversational engine
from utils import conversation_engine
bot = conversation_engine.bot

# Controllers
from controllers import command_handlers, msg_handlers

# Telegram API
import telebot
telegram = telebot.TeleBot(apiParams['Telegram']['API-key'])

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
print("Telegram client ready...")

telegram.polling(none_stop=True)

