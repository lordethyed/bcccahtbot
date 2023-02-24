from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

choice_language = ReplyKeyboardMarkup(resize_keyboard=True)
russian_language = KeyboardButton("Қазақ тілі")
english_language = KeyboardButton('Русский Язык')
choice_language.add(russian_language, english_language)

start_cmd_back = ReplyKeyboardMarkup(resize_keyboard=True)
btn_start = KeyboardButton('/start')
start_cmd_back.add(btn_start)

most_popular_questions_rus_list = {
    'Хочу посмотреть мою кредитную историю. Где я могу получить кредитный отчет?' : '''Получить кредитный отчет вы можете:
• на сайтах www.1cb.kz, электронного правительства www.egov.kz,
• в ЦОНах вашего города,
• в офисе Первого кредитного бюро в г. Алматы.
Кредитный отчет предоставляется бесплатно один раз в год.''',

    'Как скачать BCC.KZ?' : """Для установки BCC.KZ на ваще устройстве:
• Для установки на IOS систему - https://apps.apple.com/kz/app/starbusiness/id1452748006?utm_source=bcc.kz&utm_medium=button&utm_campaign=ip_request
• Для установки на Android систему - https://play.google.com/store/apps/details?id=bcc.sapphire&hl=ru&utm_source=bcc.kz&utm_medium=button&utm_campaign=ip_request
"""

}

most_popular_questions_rus = ReplyKeyboardMarkup(resize_keyboard=True)
questions_first_rus = KeyboardButton('Хочу посмотреть мою кредитную историю. Где я могу получить кредитный отчет?')
questions_second_rus = KeyboardButton('Как скачать BCC.KZ?')
connect_option = KeyboardButton('Связаться с оператором')
open_card_question = KeyboardButton('Открыть карту нашего банка')
location_bank = KeyboardButton = KeyboardButton('Ближащий отделение и банкомат')
most_popular_questions_rus.add(questions_first_rus)
most_popular_questions_rus.add(open_card_question)
most_popular_questions_rus.add(location_bank)
most_popular_questions_rus.add(questions_second_rus)
most_popular_questions_rus.add(connect_option)


