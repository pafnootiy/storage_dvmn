#!/usr/bin/env python

import logging
import os

from dotenv import load_dotenv
from telegram import (KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove,
                      Update)
from telegram.ext import (CallbackContext, CommandHandler, ConversationHandler,
                          Filters, MessageHandler, Updater)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

AGREEMENT, GET_NUMBER, GET_NAME, MENU, ORDERS, ORDER_ADDRESS, ORDER_NEW, \
    ORDER_APPROX_SIZE, ORDER_DATE, ORDER_APPROVE, ORDER_SIZE, \
    ORDER_SEND = range(12)


def start(update: Update, context: CallbackContext) -> int:
    """Starts the conversation and asks the user about their gender."""

    print(update)
    reply_keyboard = [['Далее']]
    update.message.reply_text(
        'Добро пожаловать в сервис SELF_STORAGE!\n'
        'Мы делаем хранение вещей удобным и доступным.\n\n'
        'Приступим?',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True
        ),
    )

    return AGREEMENT


def agreement(update: Update, context: CallbackContext) -> int:
    # if not check_if_agreement(user.id):
    # create_db_user(tg_id=user.id)
    update.message.reply_text(
        'Давайте знакомиться! Как мне к Вам обращаться?\n'
        'ВНИМАНИЕ! Отправляя данные вы соглашаетесь '
        'с обработкой персональных данных.\n'
        'Подробнее об этом по ссылке:\n'
        'https//agreement.ru', reply_markup=ReplyKeyboardRemove()
    )
    return GET_NAME
    # return MAIN


def get_phone(update: Update, context: CallbackContext) -> int:
    """Get user number"""
    user = update.message.from_user
    print(update)
    contact_keyboard = KeyboardButton('Перейти в личный кабинет ➡️')
    reply_keyboard = [[contact_keyboard]]
    update.message.reply_text(
        'Спасибо! \n'
        'Ваш личный кабинет создан 👍',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            one_time_keyboard=True)
    )
    logger.info("Phone of %s: %s", user.username, update.message.text)

    return MENU


def get_name(update: Update, context: CallbackContext) -> int:
    """Get user name"""
    user = update.message.from_user
    contact_keyboard = KeyboardButton('Отправить свой номер',
                                      request_contact=True
                                      )
    reply_keyboard = [[contact_keyboard]]
    # update_db_user(tg_id=user.id, name=user.name)
    logger.info("Name of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(f'Приятно познакомиться, {update.message.text}\n'
                              'Поделитесь, пожалуйста, Вашим номером, '
                              'чтобы мы могли связаться с вами',
                              reply_markup=ReplyKeyboardMarkup(
                                  reply_keyboard,
                                  one_time_keyboard=True)
                              )

    return GET_NUMBER


def menu(update: Update, context: CallbackContext) -> int:
    print(f'Вы в меню {update}')
    # if not check_if_agreement(user.id):
    # create_db_user(tg_id=user.id)
    reply_keyboard = [['Новый заказ'], ['Мои хранения'], ['О сервисе']]
    update.message.reply_text(
        'Личный кабинет Алексендра Распа\n\n'
        'Все боксов арендовано: 5\n'
        'Ближайшая оплата: 24.12.2020\n'
        'Чтобы вы хотели сейчас сделать?',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True)
    )
    return MENU


def new(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [['Привезу сам. Посмотреть адреса складов'],
                      ['Хочу, чтобы забрал курьер'],
                      ['Тарифы'],
                      ['Личный кабинет']]
    print(update)
    update.message.reply_text(
        '''
ОФОРМИТЬ НОВЫЙ ЗАКАЗ
Здесь вы сможете оформить новый заказ!

Есть 2 опции:
1) Самостоятельно привезти груз на склад
2) Оформить бесплатный вывоз курьером

Как действуем?''',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True)
    )
    return ORDER_NEW


def selfstorage(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [['Хочу, чтобы забрал курьер'],
                      ['Тарифы'],
                      ['Назад']]
    update.message.reply_text(
        '''
Здесь адреса складов''',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True)
    )
    return ORDER_NEW


def get_order_adress(update: Update, context: CallbackContext) -> int:
    """Get adress"""
    # order_id = create_db_order(tg_id=used.id)
    # user_data
    # update_db_order(id=order_id, name=user.name)
    update.message.reply_text('Введите адрес, с которого надо забрать груз\n'
                              'Пример команды:\n\n'
                              'Красная площадь, дом 3, кв 1')

    return ORDER_DATE


def get_order_date(update: Update, context: CallbackContext) -> int:
    """Get addres"""
    user = update.message.from_user
    # order_id = create_db_order(tg_id=used.id)
    # user_data
    # update_db_order(id=order_id, name=user.name)
    logger.info("Name of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Введите удобную дату и время доставки\n'
                              'Пример команды:\n\n'
                              '23.12 с 18:00-23:00')

    return ORDER_APPROX_SIZE


def get_order_approx_size(update: Update, context: CallbackContext) -> int:
    """Get addres"""
    reply_keyboard = [['Легковой авто'],
                      ['Газель'],
                      ['Мега-газель (несколько боксов)']]
    update.message.reply_text(
        '''
Укажите ориентировочный размер груза:

Легковой: до 5 коробок 1х1х1 метра
Газель: до 4х3х2 метра
Мега-Газель: до 6х3х2 метра

Насколько у вас много барахла?''',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True)
    )

    print(f'Размер груза: {update.message.reply_text}')
    return ORDER_APPROVE


def get_order_approve(update: Update, context: CallbackContext) -> int:
    """Get addres"""
    reply_keyboard = [['Отправить заказ'],
                      ['Изменить (не работает пока)'],
                      ['Отменить (не работает пока)']]
    update.message.reply_text(
        '''
ПРОВЕРЬТЕ ДАННЫЕ ЗАКАЗА

Адрес: {{order.adress}}
Дата: {{order.date}}
Приблизительный размер: {{order.app_size}}

        ''',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True)
    )
    return ORDER_SEND


def send_order(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [['Вернуться в личный кабинет'],
                      ['Оформить новый заказ']]
    update.message.reply_text(
        '''
Ваш заказ отправлен!
Уже скоро мы его обработаем, и его статус обновится!

Спасибо за пользование нашим сервисом!
  ''',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True)
    )
    return MENU


def about(update: Update, context: CallbackContext) -> int:
    """About service"""
    print(f'Вы в ABOUT {update}')
    reply_keyboard = [['Тарифы'],
                      ['Правила сервиса'],
                      ['Список запрещенных вещей'],
                      ['Личный кабинет']]
    update.message.reply_text(
        '''
ХРАНЕНИЕ ЛИЧНЫЙ ВЕЩЕЙ
Сервис SELF_STORAGE предлагает услуги по хранению вещей для частных лиц.\n
Мы заберём ваши вещи на наш склад, сохраним и
привезём обратно в **любую точку Москвы.**''',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True)
    )
    return MENU


def rules(update: Update, context: CallbackContext) -> int:
    """Sevice rules"""
    reply_keyboard = [['Тарифы'],
                      ['Список запрещенных вещей'],
                      ['Личный кабинет']]
    update.message.reply_text(
        '''Хранение в компании Кладовкин - это легко и удобно.

Все , что Вам нужно сделать, это 4 простых шага:

+ Выберите размер бокса
+ Позвоните и договоритесь о времени Вашего визита в центр хранения Кладовкин
+ Упакуйте свои вещи
+ Перевезите их на Self Storage

Шаг 1. Выберите бокс для хранения

Выберите размер бокса
Мы предлагаем площади от 1 до 20 квадратных метров.
Разобраться в том, какой размер бокса Вам нужен,\
легко с нашей оценкой размера. Он сделает все расчеты за вас.
Кроме того, вы можете получить совет от одного из наших экспертов.
Звоните: 8 (495) 181-55-45

Если у вас окажется больше или меньше вещей для хранения, \
чем предполагалось изначально, не волнуйтесь, мы предложим Вам подходящий бокс.
Вы всегда можете поменять свой бокс на бокс большего или меньшего размера.

Шаг 2. Зарезервируйте бокс

Когда вы резервируете свое помещение по телефону, вы также резервируете\
его цену и специальные предложения.
Мы будем держать бронь для Вас в течение 3-х дней.
Мы не берем оплату за бронирование. \
Вам даже не нужно давать нам кредитную карту для бронирования - \
достаточно вашего имени и номера телефона.
Если у вас изменяться планы Вы можете изменить или\
отменить бронирование в любое время.

Шаг 3. Упакуйте свои вещи

Правильно упакованные вещи, сделают ваш переезд более комфортным и удобным.
Узнайте, как упаковать более легко, следуя нашим советам по упаковке.

Шаг 4. Доставка и оформление договора

Наши специалисты встретят Вас на складе, и максимально \
быстро и комфортно организуют процесс разгрузки и \
оформления необходимых документов.
Процесс оформления договора займет не более 10 минут, \
а оборудованная зона разгрузки позволит Вам быстро \
и без труда переместить вещи в бокс.

''',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True)
    )
    return MENU


def prohobited(update: Update, context: CallbackContext) -> int:
    """prohibited things"""
    reply_keyboard = [['Тарифы'], ['Правила сервиса'], ['Личный кабинет'], ]
    update.message.reply_text(
        '''
Мы не примем на Self_Storage:
• скоропортящиеся продукты;
• ювелирные изделия;
• Воспламеняющиеся и взрывоопасные вещества;
• предметы искусства и другие вещи, которые\
 требуют специальных условий хранения;
• электронику (айфоны, айпэды и другие устройства,
излучающие электромагнитные волны и передающие информацию);
• химические и горюче-смазочные вещества;
• промышленные и бытовые краски в негерметичной \
упаковке или ранее вскрытой упаковке;
• жидкости, кроме закрытых герметично;
• наркотики, оружие, боеприпасы и другие вещи, \
запрещенные законом РФ или подлежащие изъятию у владельца по решению суда;
• растения;
• животных или чучела животных.''',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True)
    )
    return MENU


def tariffs(update: Update, context: CallbackContext) -> int:
    """Service Tariffs"""
    reply_keyboard = [['Оформить новый заказ'],
                      ['Правила сервиса'],
                      ['Список запрещенных вещей'],
                      ['Личный кабинет']]
    update.message.reply_text(
        '''Тарифы, описание и цена

**Мотоцикл S** (до 200 куб. см) — 1500 руб. в мес.
**Мотоцикл M** (от 201 до 1200 куб. см) — 2500 руб. в мес.
**Мотоцикл L** (от 1201 куб. см) — 4000 руб. в мес.

**Сезонное хранение шин** — 499 руб. в мес.

**ТарифШкаф**  = 5 коробок Чердака) —
990 руб. в мес.

**Тариф Балкон** = 15 коробок Чердака) —
1990 руб. в мес.
**Тариф Кладовка** = 30 коробок Чердака) —
3490 руб. в мес.
**Тариф Комната**  = 60 коробок Чердака) —
6490 руб. в мес.
**Тариф Гараж**  = 90 коробок Чердака) — 8990 руб. в мес.
**Тариф Чердак** = 180 коробок Чердака) — 15840 руб. в мес.
При превышении тарифа «Чердак» + 1000 руб. за 1 куб. м.
''',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True)
    )
    return MENU


def orders(update: Update, context: CallbackContext) -> int:
    print(f'Вы в моих заказах {update}')
    reply_keyboard = [['Мои хранения']]
    update.message.reply_text(
        'вы в моих заказах\n',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True)
    )
    return ORDERS


def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.",
                user.first_name
                )
    update.message.reply_text(
        'Bye! I hope we can talk again some day.',
        reply_markup=ReplyKeyboardRemove()
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
        entry_points=[CommandHandler('start', start),
                      CommandHandler('lk', menu),
                      CommandHandler('tariffs', tariffs),
                      CommandHandler('rules', rules),
                      CommandHandler('prohobited', prohobited),
                      CommandHandler('new', new)],
        states={
            AGREEMENT: [MessageHandler(Filters.regex('^(Далее)$'),
                                       agreement)],
            GET_NUMBER: [MessageHandler(Filters.contact,
                                        get_phone)],
            GET_NAME: [MessageHandler(Filters.text & ~Filters.command,
                                      get_name)],
            MENU: [MessageHandler(Filters.regex('^(О сервисе)$'),
                                  about),
                   MessageHandler(Filters.regex('^(Правила сервиса)$'),
                                  rules),
                   MessageHandler(Filters.regex('овый заказ'),
                                  new),
                   MessageHandler(Filters.regex('^(Мои хранения)$'),
                                  orders),
                   MessageHandler(Filters.regex('запрещенных'),
                                  prohobited),
                   MessageHandler(Filters.regex('^(Тарифы)$'),
                                  tariffs),
                   CommandHandler('menu', menu),
                   MessageHandler(Filters.regex('кабинет'),
                                  menu),
                   ],
            ORDERS: [CommandHandler('orders',
                                    orders)],
            ORDER_NEW: [CommandHandler('orders',
                                       orders),
                        MessageHandler(Filters.regex('адреса складов'),
                                       selfstorage),
                        MessageHandler(Filters.regex('азад'),
                                       new),
                        MessageHandler(Filters.regex('курьер'),
                                       get_order_adress),
                        MessageHandler(Filters.regex('^(Тарифы)$'),
                                       tariffs)
                        ],
            ORDER_ADDRESS: [MessageHandler(Filters.text & ~Filters.command,
                                           get_order_adress)],
            ORDER_DATE: [MessageHandler(Filters.text & ~Filters.command,
                                        get_order_date)],
            ORDER_APPROX_SIZE: [MessageHandler(Filters.text & ~Filters.command,
                                               get_order_approx_size)],
            ORDER_APPROVE: [MessageHandler(Filters.text & ~Filters.command,
                                           get_order_approve)],
            ORDER_SIZE: [MessageHandler(Filters.text & ~Filters.command,
                                        get_order_approx_size)],
            ORDER_SEND: [MessageHandler(Filters.regex('тправить заказ'),
                                        send_order)
                         ]
        },
        fallbacks=[CommandHandler('cancel',
                                  cancel)],
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
