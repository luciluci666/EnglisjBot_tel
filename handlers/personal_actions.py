from aiogram import types
from sqlalchemy import or_
from dispatcher import dp, bot, scheduler
from modules.utils import send_message, chat_sheduler, shedual_all

from models import connect_db, Chat, Topic
import asyncio


@dp.message_handler(commands='startall')
async def start(message: types.Message): 
    await (shedual_all())


@dp.message_handler(commands='start')
async def start(message: types.Message): 
    database = connect_db()

    if database.query(Chat).filter(Chat.user_tg_id == message.from_user.id).one_or_none() is None:
        msg =  ("Hello, I'm English bot. I can help you in learning this beautiful language!\n" +
        "You need to add me in your group and give me Admin rights."
        "Also you need to message me ID of chat and I'll send you some words with the chosen interval.\n" +
        "You can use this command: /chatid (your_id)")
    else:
        msg = "You already have chat with EnglishBot connection!"

    await message.bot.send_message(
        message.from_user.id, msg)

    database.close()

@dp.message_handler(commands='chatid')
async def chatid(message: types.Message): 
    chat = {
        'user_tg_id' : message.from_user.id,
        'chat_tg_id' : message.text.replace('/chatid ', '')
    }

    database = connect_db() 
    if database.query(Chat).filter(or_(Chat.user_tg_id == chat['user_tg_id'], Chat.chat_tg_id == chat['chat_tg_id'])).one_or_none() is None:
     
        # new chat create
        database = connect_db()
        database.add(Chat(
            user_tg_id = chat['user_tg_id'],
            chat_tg_id = chat['chat_tg_id'],
        ))
        database.commit()

        chat_id = database.query(Chat).filter(Chat.chat_tg_id == chat['chat_tg_id']).first().id
        database.close()


        # shedualer job create
        scheduler.add_job(send_message, 'cron', (chat['chat_tg_id'], ), hour=10, id=str(chat_id))
        


        msg = ("Well done! if you have done all I've said, I'm working in your group!\n" + 
                "If you want to set words theme or choose interval or amount of messages, use theese commands:\n" +
                "/time (number in hours)\n" +
                "/amount (number of words)\n" +
                "/topic\n" + "/topic (index)\n")


        await message.bot.send_message(message.from_user.id, msg)

    else:
        msg = "Hey, you or your group is already connected to EnglishBot."
        await message.bot.send_message(message.from_user.id, msg)


@dp.message_handler(commands=['time', 'amount', 'topic', 'stopmsg', 'startmsg', 'send', 'remove'])
async def settings(message: types.Message):  

    database = connect_db()
    chat = database.query(Chat).filter(Chat.user_tg_id == message.from_user.id).one_or_none()

    if chat is not None:
        if 'time' in message.text:
            if 'cron' in message.text:
                try:
                    cron = int(message.text.replace('/time cron ', ''))
                except:
                    return await message.bot.send_message(message.from_user.id, 'Value after cron needs to be integer.')

            chat.interval = message.text.replace('/time ', '')
            database.commit()

            await chat_sheduler(chat)
            
        elif 'amount' in message.text:
            try:
                amount = int(message.text.replace('/amount ', ''))
            except:
                return await message.bot.send_message(message.from_user.id, 'Amount value need to be integer!')

            chat.amount = amount
            database.commit()
            
            
            await chat_sheduler(chat)

        elif 'stopmsg' in message.text:
            try:
                scheduler.remove_job(str(chat.id))
            except:
                pass

        elif 'startmsg' in message.text:
            try:
                scheduler.remove_job(str(chat.id))
            except:
                await chat_sheduler(chat)

        elif 'send' in message.text:
            await send_message(chat.chat_tg_id, chat.topic_id, chat.amount)

        elif 'remove' in message.text:
            try:
                scheduler.remove_job(str(chat.id))
            except:
                pass
            database.query(Chat).filter(Chat.user_tg_id == message.from_user.id).delete()
            database.commit()
        
        else:
            if message.text == '/topic':
                topics = []
                for topic in database.query(Topic).all():
                    topics.append(f'{topic.id} - {topic.name}')

                msg = "Choose topic:\n" + "\n".join(topics)

                database.close()

                return await message.bot.send_message(message.from_user.id, msg)

            else:
                try:
                    topic_id = int(message.text.replace('/topic ', ''))
                except:
                    return await message.bot.send_message(message.from_user.id, 'This id is invalid.')

                topic_name = database.query(Topic).filter(Topic.id == topic_id).one_or_none().name

                chat.topic_id = topic_id
                database.commit()

                await chat_sheduler(chat)

                return await message.bot.send_message(message.from_user.id, f"You succefully change topic to '{topic_name}'!")


                

    else:
        return await message.bot.send_message(message.from_user.id, 'This Telegram account is not connected to EnglishBot!')