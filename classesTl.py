from aiogram.dispatcher.filters.state import StatesGroup, State

class addCrypto(StatesGroup):
    Ac1 = State()
    Ac2 = State()
    Ac3 = State()

class selectCrypto(StatesGroup):
    s1 = State()
    s2 = State()
    s3 = State()

class removeCrypto(StatesGroup):
    Dc1 = State()
    Dc2 = State()
    Dc3 = State()