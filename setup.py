# -*- coding: utf-8 -*-

import os
import stat
import sys
import json
from utils import printer

printer.print_banner()


def print_instructions():
    print("\n")
    print("Usage: python setup.py [args]")
    print("args:")
    print("--install : creates the needed files and folders for the bot")
    print("--build   : creates the command controllers based on the commands.json file")


def create_config_files():
    os.mkdir('config')

    telegram_username = input("Your telegram username: ")
    bot_name = input("Name for your bot: ")
    language = input("Language (default: 'english'): ")
    language = "english" if language == "" else language
    telegram_key = input("Your telegram API key: ")

    # User config file
    with open('config/user.json', 'w') as f:
        template = {
            "username": telegram_username
        }
        json.dump(template, f)

    # Bot config file
    with open('config/bot.json', 'w') as f:
        template = {
            "name": bot_name,
            "min_confidence_rate": "0.20",
            "language": language
        }
        json.dump(template, f)

    # External APIs config file
    with open('config/apis.json', 'w') as f:
        template = {
            "Telegram": {
                "API-key": telegram_key
            }
        }
        json.dump(template, f)


def create_command_handlers():

    class CodeBlock():
        def __init__(self, head, block):
            self.head = head
            self.block = block

        def __str__(self, indent=""):
            result = indent + self.head + ":\n"
            indent += "    "
            for block in self.block:
                if isinstance(block, CodeBlock):
                    result += block.__str__(indent)
                else:
                    result += indent + block + "\n"
            return result

    commands = json.load(open('commands.json'))

    modules = []

    ifBlocks = []

    for command in commands:
        filename = commands[command]['File'].replace('.py', '')
        modules.append(filename)
        ifBlocks.append(
            CodeBlock(
                'if (command == "%s")' % command,
                ['%s.%s(mssg, telegramClient, chat_id, bot)' %
                 (filename, commands[command]['Method'])]
            )
        )

    main_function = CodeBlock(
        'def handle_command(command, mssg, telegramClient, chat_id, bot)',
        ifBlocks
    )

    lines = []

    lines.append('# -*- coding: utf-8 -*-')
    lines.append('from modules import %s' % ','.join(modules))
    lines.append(str(main_function))
    lines = "\n\n".join(lines)

    with open("controllers/command_handlers.py", "w") as f:
        f.write(lines)


if (len(sys.argv) == 1):
    print_instructions()

if ("--build" in sys.argv):
    create_command_handlers()

if ("--install" in sys.argv):
    create_config_files()
    create_command_handlers()
    # Make main.py executable
    st = os.stat('main.py')
    os.chmod('main.py', st.st_mode | stat.S_IEXEC)
    print("\nYour bot is ready! Run main.py --train to start using it.")
