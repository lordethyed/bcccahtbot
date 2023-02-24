from aiogram.dispatcher import FSMContext
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types.web_app_info import WebAppInfo
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot

from db import db_request
from security import TOKEN
from userutils import choice_language, most_popular_questions_rus, most_popular_questions_rus_list, start_cmd_back

bot = Bot(TOKEN)


class ClientState(StatesGroup):
    language = State()
    help = State()
    connect = State()
    karta = State()
    karta_userid = State()


async def cmd_start(mes: Message, state: FSMContext):  # start
    await state.finish()
    await mes.answer(f'Саламатсызба @{mes.from_user.username} \nҚызмет көрсету тілін таңдаңыз',
                     reply_markup=choice_language)
    await ClientState.language.set()
    try:
        conn, res = db_request('''
                    INSERT OR REPLACE INTO users(id, username) VALUES(?,?)
        ''', [mes.from_user.id, mes.chat.full_name])

        conn.commit()
        conn.close()
    except Exception as e:
        print(e)


async def state_choice_language(mes: Message, state: FSMContext):
    if mes.text == 'Русский Язык':
        try:
            await mes.answer(f'@{mes.from_user.username}! Выберите какие продукты банка вас интересует?',
                             reply_markup=most_popular_questions_rus)
            await state.finish()
        except Exception as e:
            print(e)
    elif mes.text == 'Қазақ тілі':
        try:
            await mes.answer(f'{mes.from_user.username}! Сізге қандай банк өнімдері қызықтыратынын таңдаңыз??', )
            await state.finish()
        except Exception as e:
            print(e)
    else:
        await mes.answer(f'Мәзірден опцияны таңдаңыз!',
                         reply_markup=start_cmd_back)
        await state.finish()


async def help_answers(mes: Message):
    if mes.text == 'Связаться с оператором':
        try:
            conn, res = db_request("""
                SELECT id FROM operators WHERE status = 'In Work' ORDER BY ROWID ASC LIMIT 1
            """)
            operator_id = int(str(res.fetchone())[1:-2])
            conn.commit()
            conn.close()
            if operator_id:
                try:
                    conn, res = db_request("""
                                    SELECT id FROM operators WHERE status = 'In Work' ORDER BY ROWID ASC LIMIT 1
                                """)
                    operator_id = int(str(res.fetchone())[1:-2])
                    conn.commit()
                    conn.close()
                    await bot.send_message(chat_id=operator_id,
                                           text=f'We are connecting you with @{mes.from_user.username}')
                    await ClientState.connect.set()
                except Exception as e:
                    print(e)
            else:
                await mes.answer('Вы в очереди на оператора!')
        except Exception as e:
            print(e)
    elif mes.text == 'Открыть карту нашего банка':
        karta_keyboard = InlineKeyboardMarkup()
        webapp_karta = InlineKeyboardButton(text='Открыть карту',
                                            web_app=WebAppInfo(url=('https://www.bcc.kz/kartakarta/')))
        karta_keyboard.add(webapp_karta)

        await mes.answer(text='Что бы открыть карту перейдите по ссылке ниже',
                         reply_markup=karta_keyboard)
    elif mes.text == 'Ближащий отделение и банкомат':
        raspolozhenie_keyboard = InlineKeyboardMarkup()
        webapp_raspolozhenie = InlineKeyboardButton(text='Открыть карту',
                                                    web_app=WebAppInfo(url=('https://m.bcc.kz/nearest-bank')))
        raspolozhenie_keyboard.add(webapp_raspolozhenie)

        await mes.answer(text='Что бы открыть карту перейдите по ссылке ниже',
                         reply_markup=raspolozhenie_keyboard)
    elif mes.text == '/operator':
        pass
    elif mes.text == '/start':
        await mes.answer(f'Саламатсызба @{mes.from_user.username} \nҚызмет көрсету тілін таңдаңыз',
                         reply_markup=choice_language)
        await ClientState.language.set()
    else:
        try:
            await mes.answer(most_popular_questions_rus_list[mes.text])
        except Exception as e:
            await mes.answer('Пожалуйста выберите опцию с меню!',
                             reply_markup=start_cmd_back)
            print(e)


def set_handlers_user(dp):
    dp.register_message_handler(cmd_start, commands=['start', 'help'], state=None)
    dp.register_message_handler(state_choice_language, state=ClientState.language)
    dp.register_message_handler(help_answers)
