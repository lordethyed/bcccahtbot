from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from aiogram.dispatcher.filters.state import State, StatesGroup

from db import db_request
from security import PASSWORD_FOR_OP


class OperatorLoginState(StatesGroup):
    password = State()


class OperatorWorkState(StatesGroup):
    status = State()
    work = State()


async def is_operator(mes: Message):
    try:
        conn, res = db_request(f"""
            SELECT id FROM operators WHERE id = {mes.from_user.id}
        """)
        if res.fetchone():
            await mes.answer("Please write a password")
            await OperatorLoginState.password.set()
            conn.commit()
            conn.close()
        else:
            await mes.answer("You are not in operator list(/start)")
            conn.commit()
            conn.close()

    except Exception as e:
        print(e)


async def is_operator_password(mes: Message, state: FSMContext):
    if mes.text == PASSWORD_FOR_OP:
        await mes.answer('You logged successfully(to logout use !logout)')
        conn, res = db_request(F"""
            UPDATE operators SET status = 'In Work' WHERE id = {mes.from_user.id}
        """)

        conn.commit()
        conn.close()
        await state.finish()

        await OperatorWorkState.work.set()
    else:
        await mes.answer('You not logged - Wrong password')
        await state.finish()


async def logout_operator(mes: Message, state: FSMContext):
    if mes.text == '!logout':
        try:
            conn, res = db_request(f"""
                UPDATE operators SET status = 'NOT In Work' WHERE id = {mes.from_user.id}
            """)
            conn.commit()
            conn.close()
            await mes.answer('You are logged out, good luck')
        except Exception as e:
            print(e)


def set_handlers_operator(dp):
    dp.register_message_handler(is_operator, commands=['operator'])
    dp.register_message_handler(is_operator_password, state=OperatorLoginState.password)
    dp.register_message_handler(logout_operator, state=OperatorWorkState.work)
