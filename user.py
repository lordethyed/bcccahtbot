from aiogram.dispatcher import FSMContext
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types.web_app_info import WebAppInfo
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot

from db import db_request
from security import TOKEN
from userutils import choice_language, start_cmd_back, qtm_r1_open, qtm_r_dict, qtm_r1, qtm_r2_open, qtm_r2, \
    qtm_r3_open, qtm_r3, qtm_r4_open, qtm_r4, qtm_r5_open, qtm_r5, qtm_r6, qtm_r6_open, qtm_r7, qtm_r7_open, \
    quick_translate_menu_k_list, qtm_k1, qtm_k2, qtm_k3, qtm_k4, qtm_k5, qtm_k6, qtm_k7, qtm_k7_open, qtm_k6_open, \
    qtm_k5_open, qtm_k4_open, qtm_k3_open, qtm_k2_open, qtm_k1_open
from userutils import quick_translate_menu_k, quick_translate_menu_r
from userutils import quick_translate_menu_r_list, gtm_k_dict

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
    if mes.text == '🇷🇺Русский':
        try:
            await mes.answer(f'@{mes.from_user.username}! Выберите какие продукты банка вас интересует?',
                             reply_markup=quick_translate_menu_r)
            await state.finish()
        except Exception as e:
            print(e)
    elif mes.text == '🇰🇿Қазақша':
        try:
            await mes.answer(f'@{mes.from_user.username}! Сізге қандай банк өнімдері қызықтыратынын таңдаңыз??',
                             reply_markup=quick_translate_menu_k)
            await state.finish()
        except Exception as e:
            print(e)
    else:
        await mes.answer(f'Мәзірден опцияны таңдаңыз!',
                         reply_markup=start_cmd_back)
        await state.finish()


async def help_answers(mes: Message):
    if mes.text == 'Связаться с оператором' or mes.text == 'Операторға қосылу':
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
                except Exception as e:
                    print(e)
            else:
                await mes.answer('Вы в очереди на оператора!')
        except Exception as e:
            print(e)
    elif mes.text == 'Біздің банктің картасын ашу💳' or mes.text == 'Открыть карту нашего банка💳':
        karta_keyboard = InlineKeyboardMarkup()
        webapp_karta = InlineKeyboardButton(text='Картаны ашу Открыть карту',
                                            web_app=WebAppInfo(url=('https://www.bcc.kz/kartakarta/')))
        karta_keyboard.add(webapp_karta)

        await mes.answer(
            text='Картаны ашу үшін төмендегі сілтемеге өтіңіз\n\nЧто бы открыть карту перейдите по ссылке ниже',
            reply_markup=karta_keyboard)
    elif mes.text == 'Ближайшее отделении и банкоматы🏦' or mes.text == 'Ең жақын бөлімше және банкомат🏦':
        raspolozhenie_keyboard = InlineKeyboardMarkup()
        webapp_raspolozhenie = InlineKeyboardButton(text='Картаны ашу Открыть карту',
                                                    web_app=WebAppInfo(url=('https://m.bcc.kz/nearest-bank')))

        raspolozhenie_keyboard.add(webapp_raspolozhenie)

        await mes.answer(
            text='''Ең жақын филиалдар мен банкоматтардың картасын ашу үшін төмендегі сілтеме бойынша өтіңіз\n\nЧто бы открыть карту ближайших отделении и банкоматы перейдите по ссылке ниже''',
            reply_markup=raspolozhenie_keyboard)
        raspolozhenie_keyboard.add(webapp_raspolozhenie)
    elif mes.text == 'Оставить заявку на депозит нашего банка💴' or mes.text == 'Біздің банктің депозитіне өтінім қалдырыңыз💴':
        depozit_keyboard = InlineKeyboardMarkup()
        webapp_depozit = InlineKeyboardButton(text='Заявка на депозит  Депозитіке өтінім',
                                                    web_app=WebAppInfo(url=('https://www.bcc.kz/product/rakhmet/')))
        depozit_keyboard.add(webapp_depozit)

        await mes.answer(
            text='''Біздің банктің депозитіне өтінім қалдыру үшін төмендегі сілтеме бойынша өтіңіз\n\nЧто бы оставить заявку на депозит нашего банка перейдите по ссылке ниже''',
            reply_markup=depozit_keyboard)
    elif mes.text == '/operator':
        pass
    elif mes.text == '/start':
        await mes.answer(f'Саламатсызба @{mes.from_user.username} \nҚызмет көрсету тілін таңдаңыз',
                         reply_markup=choice_language)
        await ClientState.language.set()
    elif mes.text in quick_translate_menu_r_list:
        if mes.text == qtm_r1.text:
            await mes.answer('Выберите направление', reply_markup=qtm_r1_open)
        elif mes.text == qtm_r2.text:
            await mes.answer('Выберите направление', reply_markup=qtm_r2_open)
        elif mes.text == qtm_r3.text:
            await mes.answer('Выберите направление', reply_markup=qtm_r3_open)
        elif mes.text == qtm_r4.text:
            await mes.answer('Выберите направление', reply_markup=qtm_r4_open)
        elif mes.text == qtm_r5.text:
            await mes.answer('Выберите направление', reply_markup=qtm_r5_open)
        elif mes.text == qtm_r6.text:
            await mes.answer('Выберите направление', reply_markup=qtm_r6_open)
        elif mes.text == qtm_r7.text:
            await mes.answer('Выберите направление', reply_markup=qtm_r7_open)
    elif mes.text in quick_translate_menu_k_list:
        if mes.text == qtm_k1.text:
            await mes.answer('Бағытты таңдаңыз', reply_markup=qtm_k1_open)
        elif mes.text == qtm_k2.text:
            await mes.answer('Бағытты таңдаңыз', reply_markup=qtm_k2_open)
        elif mes.text == qtm_k3.text:
            await mes.answer('Бағытты таңдаңыз', reply_markup=qtm_k3_open)
        elif mes.text == qtm_k4.text:
            await mes.answer('Бағытты таңдаңыз', reply_markup=qtm_k4_open)
        elif mes.text == qtm_k5.text:
            await mes.answer('Бағытты таңдаңыз', reply_markup=qtm_k5_open)
        elif mes.text == qtm_k6.text:
            await mes.answer('Бағытты таңдаңыз', reply_markup=qtm_k6_open)
        elif mes.text == qtm_k7.text:
            await mes.answer('Бағытты таңдаңыз', reply_markup=qtm_k7_open)
    elif mes.text == '⬅️Назад' or mes.text == '⬅️Артқа':
        if mes.text == '⬅️Назад':
            await mes.answer('Пожалуйста выберите направление', reply_markup=quick_translate_menu_r)
        else:
            await mes.answer('Бағытты таңдаңыз', reply_markup=quick_translate_menu_k)
    else:
        try:
            if mes.text in qtm_r_dict:
                await mes.answer(qtm_r_dict[mes.text])
            else:
                await mes.answer(gtm_k_dict[mes.text])
        except Exception as e:
            await mes.answer('Мәзірден опцияны таңдаңыз!\n\nПожалуйста выберите опцию с меню!',
                             reply_markup=start_cmd_back)
            print(e)


def set_handlers_user(dp):
    dp.register_message_handler(cmd_start, commands=['start', 'help'], state=None)
    dp.register_message_handler(state_choice_language, state=ClientState.language)
    dp.register_message_handler(help_answers)
