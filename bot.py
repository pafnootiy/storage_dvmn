#!/usr/bin/env python

import logging
import os

from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, KeyboardButton
from telegram.ext import (CallbackContext, CommandHandler, ConversationHandler,
                          Filters, MessageHandler, Updater)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

AGREEMENT, GET_NUMBER, GET_NAME, MENU, ORDERS, ADRESS = range(6)


def start(update: Update, context: CallbackContext) -> int:
    """Starts the conversation and asks the user about their gender."""

    print(update)
    reply_keyboard = [['Далее']]

    update.message.reply_text(
        'Добро пожаловать в сервис SELF_STORAGE!'
        'Мы делаем хранение вещей удобным и доступным.\n\n'
        'Приступим?',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Boy or Girl?'
        ),
    )

    return AGREEMENT


def agreement(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    # if not check_if_agreement(user.id):
    # create_db_user(tg_id=user.id)
    contact_keyboard = KeyboardButton('Отправить свой номер', request_contact=True)
    reply_keyboard = [[contact_keyboard]]
    update.message.reply_text(
        'Давайте знакомиться! Пришлите, пожалуйтса, ваш номер телефона.\n'
        'ВНИМАНИЕ! Отправляя данные вы соглашаетесь с обработкой персональных данных.\n '
        'Подробнее об этом по ссылке:\n'
        'https//agreement.ru', reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True)

    )
    return GET_NUMBER
    # return MAIN


def get_phone(update: Update, context: CallbackContext) -> int:
    """Get user number"""
    user = update.message.from_user
    phone = update.message.contact
    print(update)
    update.message.reply_text(
        'Супер! Как нам к Вам обращаться?',
        reply_markup=ReplyKeyboardRemove(),
    )
    logger.info("Gender of %s: %s", user.first_name, update.message.text)

    return GET_NAME


def get_name(update: Update, context: CallbackContext) -> int:
    """Get user name"""
    user = update.message.from_user
    reply_keyboard = [['Приступим!']]
    # update_db_user(tg_id=user.id, name=user.name)
    logger.info("Name of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(f'Приятно познакомиться, {update.message.text}\n'
                              f'Переходите в личный кабинет для начала работы',
                              reply_markup=ReplyKeyboardMarkup(
                                  reply_keyboard,
                                  one_time_keyboard=True)
                              )

    return MENU


def menu(update: Update, context: CallbackContext) -> int:
    print(f'Вы в меню {update}')
    user = update.message.from_user
    # if not check_if_agreement(user.id):
    # create_db_user(tg_id=user.id)
    reply_keyboard = [['Новый заказ'], ['Мои хранения'], ['О сервисе']]
    update.message.reply_text(
        f'Личный кабинет Алексендра Распа\n\n'
        f'Все боксов арендовано: 5\n'
        f'Ближайшая оплата: 24.12.2020\n'
        f'Чтобы вы хотели сейчас сделать?',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True)
    )
    return MENU


def new(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    reply_keyboard = [['Привезу сам. Посмотреть адреса складов'],
                      ['Хочу, чтобы забрал курьер'],
                      ['Назад']]
    update.message.reply_text(
        f'Оформляем новый заказ\n'
        f'Тут указание тарифов\n',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True)
    )
    return ADRESS


def get_adress(update: Update, context: CallbackContext) -> int:
    """Get addres"""
    user = update.message.from_user
    # order_id = create_db_order(tg_id=used.id)
    # user_data
    # update_db_order(id=order_id, name=user.name)
    logger.info("Name of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(f'Введите адрес, с которого надо забрать груз\n'
                              f'Пример команды:\n\n'
                              f'Красноя площадь, дом 3, кв 1')

    return MENU


def about(update: Update, context: CallbackContext) -> int:
    print(f'Вы в ABOUT {update}')
    user = update.message.from_user
    reply_keyboard = [['Личный кабинет'], ['Тарифы'], ['Правила сервиса'], ['Список запрещенных вещей']]
    update.message.reply_text(
        f'О компании трали вали\n',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True)
    )
    return MENU


def rules(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    reply_keyboard = [['Личный кабинет'], ['Тарифы'], ['Список запрещенных вещей']]
    update.message.reply_text(
        f'Здесь указаны правила сервиса\n',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True)
    )
    return MENU


def prohobited(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    reply_keyboard = [['Личный кабинет'], ['Тарифы'], ['Список запрещенных вещей']]
    update.message.reply_text(
        f'Здесь список запрещенных веществ\n',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True)
    )
    return MENU


def tariffs(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    reply_keyboard = [['Оформить новый заказ'], ['Личный кабинет'], ['Правила сервиса'], ['Список запрещенных вещей']]
    update.message.reply_text(
        f'''Тарифы, описание и цена

Мотоцикл S (до 200 куб. см) — 1500 руб. в мес.
Мотоцикл M (от 201 до 1200 куб. см) — 2500 руб. в мес.
Мотоцикл L (от 1201 куб. см) — 4000 руб. в мес.

Сезонное хранение шин — 499 руб. в мес.

ТарифШкаф  = 5 коробок Чердака) — 
990 руб. в мес.

Тариф Балкон = 15 коробок Чердака) — 
1990 руб. в мес.

Тариф Кладовка = 30 коробок Чердака) — 
3490 руб. в мес.

Тариф Комната  = 60 коробок Чердака) — 
6490 руб. в мес.

Тариф Гараж  = 90 коробок Чердака) — 8990 руб. в мес.
Тариф Чердак = 180 коробок Чердака) — 15840 руб. в мес.
При превышении тарифа «Чердак» + 1000 руб. за 1 куб. м.

''',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True)
    )
    return MENU


def orders(update: Update, context: CallbackContext) -> int:
    print(f'Вы в моих заказах {update}')
    user = update.message.from_user
    reply_keyboard = [['Мои хранения']]
    update.message.reply_text(
        f'вы в моих заказах\n',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True)
    )
    return ORDERS


def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    load_dotenv()
    token = os.getenv('TG_TOKEN')
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            AGREEMENT: [MessageHandler(Filters.regex('^(Далее)$'), agreement)],
            GET_NUMBER: [MessageHandler(Filters.contact, get_phone)],
            GET_NAME: [MessageHandler(Filters.text & ~Filters.command, get_name)],
            MENU: [MessageHandler(Filters.regex('^(О сервисе)$'), about),
                   MessageHandler(Filters.regex('^(Правила сервиса)$'), rules),
                   MessageHandler(Filters.regex('^(Создать новый заказ)$'), about),
                   MessageHandler(Filters.regex('^(Мои хранения)$'), orders),
                   MessageHandler(Filters.regex('^(Тарифы)$'), tariffs),
                   CommandHandler('menu', menu),
                   MessageHandler(Filters.regex('^(Приступим!)$'), menu),
                   MessageHandler(Filters.regex('^(Оформить новый заказ)$'), new)
                   ],
            ORDERS: [CommandHandler('orders', orders)],
            ADRESS: [MessageHandler(Filters.text & ~Filters.command, get_adress)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
