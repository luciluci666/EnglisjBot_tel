from random import randint
from models import *
from dispatcher import bot, scheduler

import asyncio

def random_message(topic_id, amount):
   
    database = connect_db()
    objects = []
    rows = database.query(Word).filter(Word.topic_id == topic_id).count()
    for i in range(amount):
        
        id = randint(1,rows) - 1
        object = database.query(Word).filter(Word.topic_id == topic_id).all()[id]
        objects.append(f'{object.word} - {object.translation}')

    message = 'Hey, wassap! 🇬🇧 I have some new words for you: \n' + "\n".join(objects)
    
    return message


async def send_message(chanel_id, topic_id=2, amount=5):
    await bot.send_message(chanel_id, random_message(topic_id, amount))


async def chat_sheduler(chat):
    if 'cron' in chat.interval:
        hour = int(chat.interval.replace('cron ', ''))
        try:
            scheduler.remove_job(str(chat.id))
        except:
            pass
        finally:
            scheduler.add_job(send_message, 'cron', (chat.chat_tg_id, chat.topic_id, chat.amount), hour=hour, id=str(chat.id))

    elif 'interval' in chat.interval:
        interval = (chat.interval.replace('interval ', ''))
        hour = 0
        min = 0
        sec = 0
        for el in interval.split():
            if '-h' in el:
                hour = int(el.replace('-h', ''))
            elif '-m' in el:
                min = int(el.replace('-m', ''))
            elif '-s' in el:
                sec = int(el.replace('-s', ''))
            else:
                await bot.send_message(chat.user_tg_id, 'Choose correct interval pls!')
        try:
            scheduler.remove_job(str(chat.id))
        except:
            pass
        finally:
            scheduler.add_job(send_message, 'interval', (chat.chat_tg_id, chat.topic_id, chat.amount), hours=hour, minutes=min, seconds=sec, id=str(chat.id))

    else:
        await bot.send_message(chat.user_tg_id, 'Choose correct interval pls!')

    await bot.send_message(chat.user_tg_id, 'Chat was shedualed!')


async def shedual_all():
    database = connect_db() 
  
    for chat in database.query(Chat).all():
        await chat_sheduler(chat)

    scheduler.start()

