# -*- coding: utf-8 -*-

from modules import bot_manager, userfinder

def handle_command(command, mssg, telegramClient, chat_id, bot):
	if (command == 'Ajustar conf rate'):
		bot_manager.change_conf_rate(mssg, telegramClient, chat_id)
	if (command == 'Investigar username'):
		userfinder.check_username(mssg, telegramClient, chat_id)


