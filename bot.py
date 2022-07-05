#!/usr/bin/env python

import logging
import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'storage_dvmn.settings')
django.setup()

from dotenv import load_dotenv
from telegram import (KeyboardButton, LabeledPrice, ReplyKeyboardMarkup,
                      ReplyKeyboardRemove, ShippingOption, Update, InlineKeyboardButton,
                      InlineKeyboardMarkup)
from telegram.ext import (CallbackContext, CommandHandler, ContextTypes,
                          ConversationHandler, Filters, CallbackQueryHandler,
                          MessageHandler,
                          PreCheckoutQueryHandler, ShippingQueryHandler,
                          Updater)

from catalog.models import (Order, Storage, Tariff, User, check_if_agreement,
                            create_db_order, create_db_user, get_db_tariff,
                            get_db_user, get_nearest_storage, update_db_order,
                            update_db_user)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

AGREEMENT, GET_NUMBER, GET_NAME, MENU, ORDERS, ORDER_ADDRESS, ORDER_NEW, \
    GET_TARIFF, ORDER_DATE, ORDER_APPROVE, ORDER_SIZE, \
    ORDER_SEND, CHECKOUT = range(13)


def start(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [['Далее']]
    update.message.reply_text(
        'Добро пожаловать в сервис SELF_STORAGE!\n'
        'Мы делаем хранение вещей удобным и доступным.\n\n'
        'Приступим?',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, resize_keyboard=True, one_time_keyboard=True
        ),
    )
    if not check_if_agreement(update):
        return AGREEMENT
    return MENU


def agreement(update: Update, context: CallbackContext) -> int:
    create_db_user(update)
    update_db_user(tg_id=update.message.chat.id, agreement=True)
    update.message.reply_text(
        'Давайте знакомиться! Как мне к Вам обращаться?\n\n'
        'ВНИМАНИЕ! Отправляя данные вы соглашаетесь '
        'с обработкой персональных данных.\n'
        'Подробнее об этом по ссылке:\n'
        'https//agreement.ru/agr.pdf', reply_markup=ReplyKeyboardRemove()
    )
    return GET_NAME
    # return MAIN


def get_phone(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    print(update)
    contact_keyboard = KeyboardButton('Перейти в личный кабинет ➡️')
    reply_keyboard = [[contact_keyboard]]
    update.message.reply_text(
        'Спасибо! \n'
        'Ваш личный кабинет создан 👍',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, resize_keyboard=True,
            one_time_keyboard=True)
    )
    logger.info("Phone of %s: %s", user.username, update.message.text)

    return MENU


def get_name(update: Update, context: CallbackContext) -> int:
    update_db_user(tg_id=update.message.chat.id, name=update.message.text)
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
                                  reply_keyboard, resize_keyboard=True,
                                  one_time_keyboard=True)
                              )

    return GET_NUMBER


def menu(update: Update, context: CallbackContext) -> int:
    user = get_db_user(update)
    orders_qty = Order.objects.filter(user=user).count()
    reply_keyboard = [['Новый заказ'], ['Мои хранения'], ['О сервисе']]
    update.message.reply_text(
        f'Личный кабинет: {user.name}\n\n'
        f'Всего хранений: {orders_qty}\n'
        '\n'
        'Чтобы вы хотели сейчас сделать?',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, resize_keyboard=True,
            one_time_keyboard=True)
    )
    return MENU


def new(update: Update, context: CallbackContext) -> int:
    context.user_data['order_id'] = create_db_order(update)
    reply_keyboard = [['Привезу сам. Посмотреть адреса складов'],
                      ['Хочу, чтобы забрал курьер'],
                      ['Тарифы'],
                      ['Личный кабинет']]
    update.message.reply_text(
        '''
ОФОРМИТЬ НОВЫЙ ЗАКАЗ
Здесь вы сможете оформить новый заказ!

Есть 2 опции:
1) Самостоятельно привезти груз на склад
2) Оформить бесплатный вывоз курьером

Как действуем?''',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, resize_keyboard=True,
            one_time_keyboard=True)
    )
    return ORDER_NEW


def get_location(update: Update, context: CallbackContext) -> int:
    print(update)
    location = update.message.location
    nearest_storage_id = get_nearest_storage(location)
    context.user_data['storage'] = nearest_storage_id
    nearest_storage = Storage.objects.get(id=nearest_storage_id)
    reply_keyboard = [['Ок! Выбрать этот склад'],
                      ['Выбрать другой склад']
                      ]

    update.message.reply_text(f'''
Ваш ближайший склад:
{nearest_storage.title}
По адресу:
{nearest_storage.address}
Ок?
''', reply_markup=ReplyKeyboardMarkup(
        reply_keyboard, resize_keyboard=True,
        one_time_keyboard=True))
    return ORDER_NEW


def selfstorage(update: Update, context: CallbackContext) -> int:
    print(context.user_data)
    location_keyboard = KeyboardButton('Определить ближайший автоматически',
                                       request_location=True
                                       )
    reply_keyboard = [[location_keyboard],
                      ['Склад на Ленинградке'],
                      ['Склад на Рязанке'],
                      ['Склад на Варшавке']]
    update.message.reply_text(
        '''
АДРЕСА СКЛАДОВ
Режим работы:
Ежедневно c 08.00 - 22.00

СКЛАД НА Ленинградке
Ленинградское шоссе, 54

Схема проезда:
https://yandex.ru/maps/-/CCUNm-QpGB

СКЛАД НА ВАРШАВКЕ
Варшавское шоссе, 121

Схема проезда:
https://yandex.ru/maps/-/CCUNm-QpGB

СКЛАД НА Рязанке
Рязанский проспект, 79

Схема проезда:
https://yandex.ru/maps/-/CCUNm-QpGB

Выберите подходящий склад:''',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, resize_keyboard=True,
            one_time_keyboard=True)
    )
    print(update)
    return ORDER_NEW


def get_order_adress(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Введите адрес, с которого надо забрать груз\n\n'
                              'Пример команды:\n\n'
                              'Красная площадь, дом 3, кв 1')

    return ORDER_DATE


def get_order_date(update: Update, context: CallbackContext) -> int:
    print(context.user_data)
    id = context.user_data['order_id']
    update_db_order(id=id, address=update.message.text)
    user = update.message.from_user
    # order_id = create_db_order(tg_id=used.id)
    # user_data
    # update_db_order(id=order_id, name=user.name)
    logger.info("Адрес of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Введите удобную дату и время доставки\n'
                              'Пример команды:\n\n'
                              '23.12 с 18:00-23:00')
    return GET_TARIFF


def send_order_success(update: Update, context: CallbackContext) -> int:
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


def choose_storage(update: Update, context: CallbackContext):
    if update.message.text == 'Склад на Ленинградке':
        context.user_data['storage'] = 1
    if update.message.text == 'Склад на Рязанке':
        context.user_data['storage'] = 2
    if update.message.text == 'Склад на Варшавке':
        context.user_data['storage'] = 3


def get_tariff(update: Update, context: CallbackContext):
    id = context.user_data['order_id']
    print(context.user_data)
    update_db_order(id=id, address=update.message.text)
    choose_storage(update=update, context=context)
    print(context.user_data)
    reply_keyboard = [['Тариф Балкон - 1890 руб'],
                      ['Тариф Балкон - 3490 руб'],
                      ['Тариф Балкон - 8990 руб']]
    update.message.reply_text(
        '''
Выберите подходящий тариф
Срок хранения - 30 дней

ТАРИФЫ

1 коробка имеет размер 50х50х50 см

**Тариф Балкон** = 15 коробок —
1990 руб. в мес.

**Тариф Кладовка** = 30 коробок —
3490 руб. в мес.

**Тариф Гараж**  = 90 коробок —
8990 руб. в мес.

''',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, resize_keyboard=True,
            one_time_keyboard=True)
    )
    return ORDER_NEW


def get_tariff_id(update, context):
    if update.message.text == 'Тариф Балкон - 1890 руб':
        context.user_data['tariff_id'] = 1
    if update.message.text == 'Тариф Балкон - 3490 руб':
        context.user_data['tariff_id'] = 2
    if update.message.text == 'Тариф Балкон - 8990 руб':
        context.user_data['tariff_id'] = 3


def get_qr(update, context: CallbackContext):
    print(update)
    query = update.callback_query
    order_id = query.data
    print(query.message.chat.id)
    # `CallbackQueries` требует ответа, даже если
    # уведомление для пользователя не требуется, в противном
    #  случае у некоторых клиентов могут возникнуть проблемы.
    # смотри https://core.telegram.org/bots/api#callbackquery.
    query.answer()
    # редактируем сообщение, тем самым кнопки
    # в чате заменятся на этот ответ.
    qr_core_url = 'http://a1480.phobos.apple.com/us/r30/Purple3/v4/fb/59/cf/fb59cf06-' \
                  '0cf9-fc66-7407-7773231070c9/pr_source.png?downloadKey=1413818465_' \
                  '86a7cb3f5224397e9d01a712aa6cea91'
    context.bot.send_message(query.message.chat.id, f'Заказ №{order_id}.\n'
                                                    f'QR-код для получения')
    context.bot.send_photo(query.message.chat.id, qr_core_url)


def send_invoice(update: Update, context: CallbackContext) -> None:
    get_tariff_id(update=update, context=context)
    tariff_id = context.user_data['tariff_id']
    tariff = get_db_tariff(tariff_id)
    chat_id = update.message.chat_id
    print(context.user_data)
    title = "SELF-STORAGE"
    description = f"Оплата тарифа {tariff.title} - {tariff.days} дней"
    payload = "Custom-Payload"
    provider_token = "381764678:TEST:39427"
    currency = "RUB"
    prices = [LabeledPrice(f'{tariff.title}-{tariff.days} дней',
                           tariff.price * 100)]
    context.bot.send_invoice(
        chat_id,
        title,
        description,
        payload,
        provider_token,
        currency,
        prices,
        need_name=False,
        need_phone_number=False,
        need_email=False,
        is_flexible=True,
    )


def precheckout_callback(update: Update, _: CallbackContext) -> None:
    query = update.pre_checkout_query
    if query.invoice_payload != 'Custom-Payload':
        query.answer(ok=False, error_message="Something went wrong...")
    else:
        query.answer(ok=True)


def successful_payment_callback(update: Update,
                                context: CallbackContext) -> None:
    print('Ваш заказ оформлен')
    print(update)
    print(context.bot_data)
    update.message.reply_text("Thank you for your payment!")


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
            reply_keyboard, resize_keyboard=True,
            one_time_keyboard=True)
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
            reply_keyboard, resize_keyboard=True,
            one_time_keyboard=True)
    )
    return MENU


def prohobited(update: Update, context: CallbackContext) -> int:
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
            reply_keyboard, resize_keyboard=True,
            one_time_keyboard=True)
    )
    return MENU


def tariffs(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [['Оформить новый заказ'],
                      ['Правила сервиса'],
                      ['Список запрещенных вещей'],
                      ['Личный кабинет']]
    update.message.reply_text(
        '''
ТАРИФЫ

1 коробка имеет размер 50х50х50 см

**Тариф Балкон** = 15 коробок —
1990 руб. в мес.

**Тариф Кладовка** = 30 коробок —
3490 руб. в мес.

**Тариф Гараж**  = 90 коробок —
8990 руб. в мес.
''',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, resize_keyboard=True,
            one_time_keyboard=True)
    )
    return MENU


def orders(update: Update, context: CallbackContext) -> int:
    user = User.objects.get(tg_id=update.message.chat.id)
    orders = Order.objects.filter(user=user)
    for order in orders:
        keyboard = [
            [
                InlineKeyboardButton("Больше информации", callback_data=order.id),
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(f'Заказ номер {order.id}'
                                  f'\n'
                                  f'Тариф: Чердак'
                                  f'Оплачен до: 03.08', reply_markup=reply_markup)
    reply_keyboard = [['Личный кабинет']]
    update.message.reply_text(
        'Вернуться в личный кабинет?',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, resize_keyboard=True,
            one_time_keyboard=True)
    )
    return MENU


def cancel(update: Update, context: CallbackContext) -> int:
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

    dispatcher.add_handler(PreCheckoutQueryHandler(precheckout_callback))
    dispatcher.add_handler(MessageHandler(Filters.successful_payment,
                                          successful_payment_callback))
    dispatcher.add_handler(CallbackQueryHandler(get_qr))
    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start),
                      CommandHandler('lk', menu),
                      CommandHandler('tariffs', tariffs),
                      CommandHandler('rules', rules),
                      CommandHandler('prohobited', prohobited),
                      CommandHandler('new', new),
                      CommandHandler('check_out', send_invoice)],
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
                   MessageHandler(Filters.regex('Далее'), menu),
                   MessageHandler(Filters.regex('кабинет'),
                                  menu)
                   ],
            ORDERS: [CommandHandler('orders',
                                    orders)],
            ORDER_NEW: [CommandHandler('orders',
                                       orders),
                        MessageHandler(Filters.regex('адреса складов'),
                                       selfstorage),
                        MessageHandler(Filters.regex('Выбрать другой склад'),
                                       selfstorage),
                        MessageHandler(Filters.regex('Ок! Выбрать этот склад'),
                                       get_tariff),
                        MessageHandler(Filters.regex('азад'),
                                       new),
                        MessageHandler(Filters.location,
                                       get_location),
                        MessageHandler(Filters.regex('курьер'),
                                       get_order_adress),
                        MessageHandler(Filters.regex('^(Тарифы)$'),
                                       tariffs),
                        MessageHandler(Filters.regex('Склад на Ленинградке'),
                                       get_tariff),
                        MessageHandler(Filters.regex('Склад на Рязанке'),
                                       get_tariff),
                        MessageHandler(Filters.regex('Склад на Варшавке'),
                                       get_tariff),
                        MessageHandler(Filters.regex('Тариф Балкон - 1890 руб'),
                                       send_invoice),
                        MessageHandler(Filters.regex('Тариф Балкон - 3490 руб'),
                                       send_invoice),
                        MessageHandler(Filters.regex('Тариф Балкон - 8990 руб'),
                                       send_invoice),
                        CommandHandler('start',
                                       start),
                        ],
            CHECKOUT: [MessageHandler(Filters.text & ~Filters.command,
                                      send_invoice)
                       ],
            ORDER_ADDRESS: [MessageHandler(Filters.text & ~Filters.command,
                                           get_order_adress)],
            ORDER_DATE: [MessageHandler(Filters.text & ~Filters.command,
                                        get_order_date)],
            GET_TARIFF: [MessageHandler(Filters.text & ~Filters.command,
                                        selfstorage)],
            ORDER_SEND: [MessageHandler(Filters.regex('тправить заказ'),
                                        send_order_success)
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
