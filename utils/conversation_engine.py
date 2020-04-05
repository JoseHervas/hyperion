# -*- coding: utf-8 -*-
from sys import argv
from chatterbot import ChatBot
from chatterbot.response_selection import get_most_frequent_response
from utils import custom_comparisons

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
    database_uri='sqlite:///db.sqlite3',
    read_only=True
)

# Initial training (if needed)
if ("-train" in argv):
    from chatterbot.trainers import ChatterBotCorpusTrainer
    print("Training the mastermind...")
    trainer = ChatterBotCorpusTrainer(bot)
    trainer.train("chatterbot.corpus.spanish")

print("Conversational engine ready...")