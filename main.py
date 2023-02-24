from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from security import TOKEN
from db import setup_db
from django.shortcuts import render

from user import set_handlers_user
from op import set_handlers_operator


bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


def start():
    setup_db()
    set_handlers_user(dp)
    set_handlers_operator(dp)
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    start()
