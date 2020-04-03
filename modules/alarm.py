# -*- coding: utf-8 -*-

from apscheduler.schedulers.background import BackgroundScheduler
import re

sched = BackgroundScheduler()

def job_function(telegramClient, chat_id):
    telegramClient.send_message(chat_id, "Buenos días, levántate!!")

sched.start()

def wakeup(mssg, telegramClient, chat_id):

    hour = int(re.search(r'(\d{1,2}):', mssg.text).group().replace(":", "").strip())
    minute = int(re.search(r':(\d{1,2})', mssg.text).group().replace(":", "").strip())

    sched.add_job(
        job_function,
        trigger='cron',
        hour=hour,
        minute=minute,
        args=[telegramClient, chat_id]
    )
