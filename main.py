# This example uses Python 2.7 and the python-request library.
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.bot import api
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from db import use_db
from config import url, token, cmc_token
from classesTl import addCrypto, selectCrypto, removeCrypto
import json

logging.basicConfig(level=logging.INFO)
loger = logging.getLogger(__name__)

PATCHED_URL = "https://telegg.ru/orig/bot{token}/{method}"
setattr(api, 'API_URL', PATCHED_URL)

bot = Bot(
	token=token
)

dp = Dispatcher(
	bot=bot, storage=MemoryStorage()
)

#parser crypto
infoUrl = url + 'v1/cryptocurrency/listings/historical'

headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': cmc_token,
}

session = Session()
session.headers.update(headers)

str = 'ADA'

parameters = {
    'date': '',
    'symbol': str.upper()
}

try:
    response = session.get(infoUrl, params=parameters)
    data = json.loads(response.text)
    print(data)
except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)

@dp.message_handler(commands=['start'])
async def send_welcom(message: types.Message):
	await message.reply(text='''
Привет!
Ты находишься в боте, который будет записывать, обновлять и удалять данные о криптовалюте которые ты захочешь
Для продолжения пиши данные команды:
/add 
    - Добавить данные о криптовалюте
    - Обновить уже добавленные данные
/select - Выбрать криптовалютут из уже добавленных
/delete_token - Удалить токен
		''', reply=False)


    # await message.answer()

@dp.message_handler(Command('select'), state=None)
async def enter_test(message: types.Message):
    await message.answer('Напишите токен криптовалюты для получения информации: ')
    await selectCrypto.s1.set()

@dp.message_handler(state=selectCrypto.s1)
async def enter_test(message: types.Message, state: FSMContext):
    data = []
    str = 'ada'

    parameters = {
        'symbol': str.upper()
    }

    try:
        response = session.get(infoUrl, params=parameters)
        data = json.loads(response.text)
        print(data['data'])
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

    cryptoToken = message.text
    st = use_db('select', message['from']['id'], cryptoToken.upper())
    if st != []:
        await message.answer('Токен:' + ("%70s" % st[0]).strip() + ' Колличество: ' + ("%70s" % st[2]).strip() + ' Ср. цена: ' + ("%70s" % st[1]).strip() + ', Нынешняя цена: ')
    else:
        await message.answer('Нет такого токена')

    await state.finish()

@dp.message_handler(Command('delete_token'), state=None)
async def enter_test(message: types.Message):
    await message.answer('Напишите токен криптовалюты: ')
    await removeCrypto.Dc1.set()

@dp.message_handler(state=removeCrypto.Dc1)
async def enter_test(message: types.Message, state: FSMContext):
    cryptoToken = message.text
    await state.update_data(crToken = cryptoToken.upper())

    await message.answer('Напишите прайс токена на момент покупки: ')
    await removeCrypto.Dc2.set()

@dp.message_handler(state=removeCrypto.Dc2)
async def enter_test(message: types.Message, state: FSMContext):
    price_buy = message.text
    await state.update_data(priceBuy = price_buy)

    await message.answer('Напишите колличество токенов: ')
    await removeCrypto.Dc3.set()

@dp.message_handler(state=removeCrypto.Dc3)
async def enter_test(message: types.Message, state: FSMContext):
    c = message.text
    await state.update_data(c = c)

    await message.answer('Спасибо! Информация добавлена, вот ваша статистика:')
    data = await state.get_data()
    crToken = data.get('crToken')
    priceBuy = data.get('priceBuy')
    id = message['from']['id']

    use_db('delete_token', id, crToken, priceBuy, c)
    await message.answer(crToken + ":" + priceBuy + ":" + c)
    await state.finish()

@dp.message_handler(Command('add'), state=None)
async def enter_test(message: types.Message):
    await message.answer('Напишите токен криптовалюты: ')
    await addCrypto.Ac1.set()

@dp.message_handler(state=addCrypto.Ac1)
async def enter_test(message: types.Message, state: FSMContext):
    cryptoToken = message.text
    await state.update_data(crToken = cryptoToken.upper())

    await message.answer('Напишите прайс токена на момент покупки: ')
    await addCrypto.Ac2.set()

@dp.message_handler(state=addCrypto.Ac2)
async def enter_test(message: types.Message, state: FSMContext):
    price_buy = message.text
    await state.update_data(priceBuy = price_buy)

    await message.answer('Напишите колличество токенов: ')
    await addCrypto.Ac3.set()

@dp.message_handler(state=addCrypto.Ac3)
async def enter_test(message: types.Message, state: FSMContext):
    c = message.text
    await state.update_data(c = c)

    await message.answer('Спасибо! Информация добавлена, вот ваша статистика:')
    data = await state.get_data()
    crToken = data.get('crToken')
    priceBuy = data.get('priceBuy')
    id = message['from']['id']

    use_db('add', id, crToken, priceBuy, c)
    await message.answer(crToken + ":" + priceBuy + ":" + c)
    await state.finish()

def main():
	executor.start_polling(
		dispatcher=dp)

if __name__ == '__main__':
	main()
