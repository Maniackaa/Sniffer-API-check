import datetime
import logging
import sys
import time
from pathlib import Path

from pyrogram import Client, filters
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message, Chat

from database.add_token import add_token_to_base
from services.func import find_weth


BASEDIR = Path(__file__).parent
print(BASEDIR)


def read_group():
    with open(BASEDIR / '.env', 'r', encoding='UTF-8') as file:
        api_hash = file.readline().strip()
        api_id = int(file.readline().strip())
        bot_token = file.readline().strip()
        chat = file.readline().strip()
    return api_hash, api_id, bot_token, chat


try:
    api_hash, api_id, bot_token, chat = read_group()
except Exception as err:
    time.sleep(5)
    raise err
delay = 1/20

client = Client(name="my_account", api_hash=api_hash, api_id=api_id)
bot = Client(name='bot',
             api_id=api_id,
             api_hash=api_hash,
             bot_token=bot_token)


print(f'Стартовые настройки:\n'
      f'api_hash: {api_hash}\n'
      f'api_id: {api_id}\n'
      f'bot_token: {bot_token}\n'
      f'chat: {chat}\n'
      )


def filter_to_channel(data):
    async def func(flt, client, message):
        chat = await client.get_chat(message.chat.username)
        print('flt.data == chat.username', flt.data == chat.username)
        return flt.data == chat.username
    return filters.create(func, data=data)


@client.on_message(filters.channel & filter_to_channel('uniswapinstant'))
async def send_message(client: Client, message: Message):
    try:
        print(message.text)
        if 'WETH liquidity:' in message.text:
            weth = int(find_weth(message.text))
        else:
            weth = 0

        for entity in message.entities:
            if entity.type == MessageEntityType.TEXT_LINK:
                if 'https://etherscan.io/token/' in entity.url:
                    eth_url = entity.url
                    eth_token = entity.url.split('https://etherscan.io/token/')[1]
                    add_token_to_base(eth_token, eth_url, weth)


    except Exception as err:
        print('Ошибка при обработке сообщения:')
        print(err)


@client.on_message()
async def last_filter(client: Client, message: Message):
    print('Мимо')

try:
    bot.start()
    client.run()
except Exception as err:
    bot.stop()
    print(err)
    input('Ошибка. Нажмите Enter')
    raise err
