import telebot
from django.core.management.base import BaseCommand
from telebot import types

bot = telebot.TeleBot('6398010979:AAFxPibC3gWVnLSOT9eiujMk2SirpYRyAOo')


class Command(BaseCommand):
    # Используется как описание команды обычно
    help = 'Implemented to Django application telegram bot setup command'

    def handle(self, *args, **kwargs):

        @bot.message_handler(commands=['start'])
        def url(message):
            doc = open('Согласие.doc', 'rb')
            bot.send_document(message.from_user.id, doc)
            markup = types.InlineKeyboardMarkup()
            btn = types.InlineKeyboardButton(callback_data='Вернуться в главное меню ⬅️', text='✅')
            markup.add(btn)
            bot.send_message(message.from_user.id,
                             "Нажимая на кнопку ниже, Вы соглашаетесь с условиями Политики и даете согласие на обработку ваших персональных данных",
                             reply_markup=markup)

        @bot.callback_query_handler(func=lambda call: call.data.startswith('Вернуться в главное меню ⬅️'))
        def get_text_messages(message):
            markup = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton(callback_data='Заказать торт 🍰', text='Заказать торт 🍰')
            btn2 = types.InlineKeyboardButton(callback_data='Узнать сроки доставки 🕒', text='Узнать сроки доставки 🕒')
            # if :
            # btn4 = types.KeyboardButton('Детали заказа')
            # btn3 = types.KeyboardButton('Предыдущие заказы')
            markup.add(btn1, btn2)
            bot.send_message(message.from_user.id,
                             '👋 Привет! Я бот пекарни CakeBake. Со мной вы можете собрать свой авторский торт, оформить заказ, а также узнать цены и сроки доставки. Чем могу помочь?',
                             reply_markup=markup)

        @bot.callback_query_handler(func=lambda call: call.data.startswith('Заказать торт 🍰'))
        def order_cake(message):
            if message.data == 'Заказать торт 🍰':
                markup = types.InlineKeyboardMarkup()
                btn1 = types.InlineKeyboardButton(callback_data='Торт A (1000 р.)', text='Торт A (1000 р.)')
                btn2 = types.InlineKeyboardButton(callback_data='Торт B (1400 р.)', text='Торт B (1400 р.)')
                btn3 = types.InlineKeyboardButton(callback_data='Торт C (3000 р.)', text='Торт C (3000 р.)')
                btn4 = types.InlineKeyboardButton(callback_data='Вернуться в главное меню ⬅️',
                                                  text='Вернуться в главное меню ⬅️')
                markup.add(btn1, btn2, btn3, btn4)
                bot.send_message(message.from_user.id, 'Выберите цену', reply_markup=markup)
            elif message.data == 'Вернуться в главное меню ⬅️':
                bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
                                      text='вы вернулись в главное меню', reply_markup=get_text_messages())

        @bot.callback_query_handler(func=lambda call: call.data.startswith('Узнать сроки доставки 🕒'))
        def find_out_delivery_time(message):
            if message.data == 'Узнать сроки доставки 🕒':
                markup = types.InlineKeyboardMarkup()
                btn1 = types.InlineKeyboardButton(callback_data='Вернуться в главное меню ⬅️',
                                                  text='Вернуться в главное меню ⬅️')
                markup.add(btn1)
                bot.send_message(message.from_user.id,
                                 'Центр - 12 часов\nВ пределах МКАДа - 1 день\nВ пределах области - 2 дня',
                                 reply_markup=markup)
            elif message.data == 'Вернуться в главное меню ⬅️':
                bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
                                      text='вы вернулись в главное меню', reply_markup=get_text_messages())

        @bot.callback_query_handler(func=lambda call: call.data.startswith('Торт'))
        # добавить остальные торты
        def choose_cake(call):
            order = {}
            if call.data == 'Торт A (1000 р.)':
                order['price'] = 1000
            if call.data == 'Торт B (1400 р.)':
                order['price'] = 1400
            if call.data == 'Торт C (3000 р.)':
                order['price'] = 3000
            bot.send_message(call.from_user.id, 'Предлагаю ознакомиться с нашими тортами ')
            bot.send_photo(call.from_user.id, photo=open('media/napoleon.jpg', 'rb'))
            bot.send_message(call.from_user.id, 'Наполеон. Описание')
            bot.send_photo(call.from_user.id, photo=open("media/praga.jpg", 'rb'))
            bot.send_message(call.from_user.id, 'Прага. Описание')
            bot.send_photo(call.from_user.id, photo=open("media/murav.jpg", 'rb'))
            bot.send_message(call.from_user.id, 'Муравейник. Описание')
            bot.send_photo(call.from_user.id, photo=open("media/tiramisu.jpg", 'rb'))
            bot.send_message(call.from_user.id, 'Торт Тирамису. Описание')
            bot.send_photo(call.from_user.id, photo=open("media/medovik.png", 'rb'))
            bot.send_message(call.from_user.id, 'Медовик. Описание')
            bot.send_photo(call.from_user.id, photo=open("media/bisquit.jpg", 'rb'))
            bot.send_message(call.from_user.id, 'Бисквитный. Описание')
            markup = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton(callback_data='Выбрать торт из предложенных',
                                              text='Выбрать торт из предложенных')
            btn2 = types.InlineKeyboardButton(callback_data='Собрать свой ', text='Собрать свой ')
            btn3 = types.InlineKeyboardButton(callback_data='Вернуться в главное меню ⬅️',
                                              text='Вернуться в главное меню ⬅️')
            markup.add(btn1, btn2, btn3)
            bot.send_message(call.from_user.id, f'Какой понравился больше всего? Или хотите собрать свой?',
                             reply_markup=markup)
            # bot.register_next_step_handler(message, lambda message: inscription_cake(message, order))

        @bot.callback_query_handler(func=lambda call: call.data.startswith('Собрать свой '))
        def custom_cake(message):
            markup = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton(callback_data='Форма 1 уровень', text='1 уровень (+400 р.)')
            btn2 = types.InlineKeyboardButton(callback_data='Форма 2 уровня', text='2 уровня (+750 р.)')
            btn3 = types.InlineKeyboardButton(callback_data='Форма 3 уровня', text='3 уровня (+1100 р.)')
            btn4 = types.InlineKeyboardButton(callback_data='Вернуться в главное меню ⬅️',
                                              text='Вернуться в главное меню ⬅️')
            markup.add(btn1, btn2, btn3, btn4)
            bot.send_message(message.from_user.id, 'Выберете количество уровней у торта', reply_markup=markup)

        @bot.callback_query_handler(func=lambda call: call.data.startswith('Форма'))
        def custom_cake(message):
            '''if '1 уровень' in message.data:
                price+=400
            if 'круг' in message.data:
                price+=750
            if 'прямоугольник' in message.data:
                price+=1100
            '''
            markup = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton(callback_data='Выбрана форма квадрат ', text='Квадрат (+600 р.)')
            btn2 = types.InlineKeyboardButton(callback_data='Выбрана форма круг', text='Круг (+400 р.)')
            btn3 = types.InlineKeyboardButton(callback_data='Выбрана форма прямоугольник',
                                              text='Прямоугольник (+1000 р.)')
            btn4 = types.InlineKeyboardButton(callback_data='Вернуться в главное меню ⬅️',
                                              text='Вернуться в главное меню ⬅️')
            markup.add(btn1, btn2, btn3, btn4)
            bot.send_message(message.from_user.id, 'Выберете форму торта', reply_markup=markup)

        @bot.callback_query_handler(func=lambda call: call.data.startswith('Выбрана форма '))
        def default_cake(message):
            '''if 'квадрат' in message.data:
                price+=600
            if 'круг' in message.data:
                price+=600
            if 'прямоугольник' in message.data:
                price+=600
            '''
            markup = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton(callback_data='Выбран сироп Без топинга', text='Без топинга (0 р.)')
            btn2 = types.InlineKeyboardButton(callback_data='Выбран сироп Белый соус', text='Белый соус (+200 р.)')
            btn3 = types.InlineKeyboardButton(callback_data='Выбран сироп Карамельный сироп',
                                              text='Карамельный сироп (+180 р.)')
            btn4 = types.InlineKeyboardButton(callback_data='Выбран сироп Кленовый сироп',
                                              text='Кленовый сироп (+200 р.)')
            btn5 = types.InlineKeyboardButton(callback_data='Выбран сироп Клубничный сироп',
                                              text='Клубничный сироп (+300 р.)')
            btn6 = types.InlineKeyboardButton(callback_data='Выбран сироп Черничный сироп',
                                              text='Черничный сироп (+350 р.)')
            btn7 = types.InlineKeyboardButton(callback_data='Выбран сироп Молочный шоколад',
                                              text='Молочный шоколад (+200 р.)')

            btn8 = types.InlineKeyboardButton(callback_data='Вернуться в главное меню ⬅️',
                                              text='Вернуться в главное меню ⬅️')
            markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8)
            bot.send_message(message.from_user.id, f'Какой топинг выберете?', reply_markup=markup)

        @bot.callback_query_handler(func=lambda call: call.data.startswith('Выбран сироп'))
        def default_cake(message):
            '''if 'Белый соус' in message.data or 'Кленовый сироп' in message.data or 'Молочный шоколад' in message.data:
                price+=200
            if 'Карамельный' in message.data:
                price+=180
            if 'Клубничный' in message.data:
                price+=300
            if 'Черничный' in message.data:
                price+=350
            '''
            markup = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton(callback_data='Выбраны ягоды Ежевика', text='Ежевика (+400)')
            btn2 = types.InlineKeyboardButton(callback_data='Выбраны ягоды Малина', text='Малина (+300)')
            btn3 = types.InlineKeyboardButton(callback_data='Выбраны ягоды Голубика', text='Голубика (+450)')
            btn4 = types.InlineKeyboardButton(callback_data='Выбраны ягоды Клубника', text='Клубника (+500)')
            btn5 = types.InlineKeyboardButton(callback_data='Выбраны ягоды Пропустить', text='Пропустить')
            btn8 = types.InlineKeyboardButton(callback_data='Вернуться в главное меню ⬅️',
                                              text='Вернуться в главное меню ⬅️')
            markup.add(btn1, btn2, btn3, btn4, btn5, btn8)
            bot.send_message(message.from_user.id, f'Какими ягодами украсить?', reply_markup=markup)

        @bot.callback_query_handler(func=lambda call: call.data.startswith('Выбраны ягоды'))
        def default_cake(message):
            '''if 'Ежевика' in message.data:
                price+=400
            if 'Малина' in message.data:
                price+=300
            if 'Голубика' in message.data:
                price+=450
            if 'Клубника' in message.data:
                price+=500
            '''
            markup = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton(callback_data='Выбран декор Фисташки (+300)', text='Фисташки (+300 р.)')
            btn2 = types.InlineKeyboardButton(callback_data='Выбран декор Безе (+400)', text='Безе (+400 р.)')
            btn3 = types.InlineKeyboardButton(callback_data='Выбран декор Фундук (+350)', text='Фундук (+350 р.)')
            btn4 = types.InlineKeyboardButton(callback_data='Выбран декор Пекан (+300)', text='Пекан (+300 р.)')
            btn5 = types.InlineKeyboardButton(callback_data='Выбран декор Маршмеллоу (+200)',
                                              text='Маршмеллоу (+200 р.)')
            btn6 = types.InlineKeyboardButton(callback_data='Выбран декор Марципан (+280)', text='Марципан (+280 р.)')
            btn7 = types.InlineKeyboardButton(callback_data='Выбран декор Молочный шоколад',
                                              text='Молочный шоколад (+200 р.)')
            btn4 = types.InlineKeyboardButton(callback_data='Выбран декор Пропустить', text='Пропустить')
            btn8 = types.InlineKeyboardButton(callback_data='Вернуться в главное меню ⬅️',
                                              text='Вернуться в главное меню ⬅️')
            markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8)
            bot.send_message(message.from_user.id, f'Какой декор предпочтёте?', reply_markup=markup)

        @bot.callback_query_handler(func=lambda call: call.data.startswith('Выбран декор'))
        def inscription_cake(message):
            '''if 'Фисташки' in message.data or 'Пекан' in message.data:
                price+=300
            if 'Безе' in message.data:
                price+=400
            if 'Маршмеллоу' in message.data or 'Молочный шоколад' in message.data:
                price+=200
            if 'Марципан' in message.data:
                price+=280
            '''
            markup = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton(callback_data='Перейти к выбору доставки', text='Пропустить')
            btn2 = types.InlineKeyboardButton(callback_data='Вернуться в главное меню ⬅️',
                                              text='Вернуться в главное меню ⬅️')
            markup.add(btn1, btn2)
            bot.send_message(message.from_user.id,
                             'Хотите сделать надпись на торте?   Мы можем разместить на торте любую надпись, например: «С днем рождения!» Введите текст надписи',
                             reply_markup=markup)
            print(types.InlineKeyboardMarkup())

        ''' проверка на пустую и слишком длинную надпись
            if message.data == '':
                bot.send_message(message.from_user.id, 'Вы ввели пустое сообщение, попробуйте ещё раз')
                bot.register_next_step_handler(message, lambda message: inscription_cake(message))
            elif len(message.data) > 30:
                bot.send_message(message.from_user.id, 'Вы ввели слишком длинный текст, попробуйте ещё раз')
                bot.register_next_step_handler(message, lambda message: inscription_cake(message))
        '''

        @bot.callback_query_handler(func=lambda call: call.data.startswith('Выбрать торт из предложенных'))
        def default_cake(message):
            markup = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton(callback_data='Выбран торт', text='Наполеон')
            btn2 = types.InlineKeyboardButton(callback_data='Выбран торт', text='Прага')
            btn3 = types.InlineKeyboardButton(callback_data='Выбран торт', text='Муравейник')
            btn4 = types.InlineKeyboardButton(callback_data='Выбран торт', text='Прага')
            btn5 = types.InlineKeyboardButton(callback_data='Выбран торт', text='Прага')
            btn6 = types.InlineKeyboardButton(callback_data='Выбран торт', text='Прага')
            btn7 = types.InlineKeyboardButton(callback_data='Вернуться в главное меню ⬅️',
                                              text='Вернуться в главное меню ⬅️')
            markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)
            bot.send_message(message.from_user.id, f'Какой торт вы выбираете?', reply_markup=markup)

        @bot.callback_query_handler(func=lambda call: call.data.startswith('Выбран торт '))
        def inscription_cake(message):
            markup = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton(callback_data='Перейти к выбору доставки', text='Пропустить')
            btn2 = types.InlineKeyboardButton(callback_data='Вернуться в главное меню ⬅️',
                                              text='Вернуться в главное меню ⬅️')
            # types.InlineKeyboard()
            markup.add(btn1, btn2)
            bot.send_message(message.from_user.id,
                             'Хотите сделать надпись на торте?   Мы можем разместить на торте любую надпись, например: «С днем рождения!» Введите текст надписи',
                             reply_markup=markup)
            print(types.InlineKeyboardMarkup())

        ''' проверка на пустую и слишком длинную надпись
            if message.data == '':
                bot.send_message(message.from_user.id, 'Вы ввели пустое сообщение, попробуйте ещё раз')
                bot.register_next_step_handler(message, lambda message: inscription_cake(message))
            elif len(message.data) > 30:
                bot.send_message(message.from_user.id, 'Вы ввели слишком длинный текст, попробуйте ещё раз')
                bot.register_next_step_handler(message, lambda message: inscription_cake(message))
        '''

        '''добавил кнопку самовывоза, не понял как datetime рассчитать'''

        @bot.callback_query_handler(func=lambda call: call.data.startswith('Перейти к выбору доставки'))
        def address(message):
            markup = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton(callback_data='Перейти к комментарию', text='Ваш адрес в центре города')
            btn2 = types.InlineKeyboardButton(callback_data='Перейти к комментарию', text='Ваш адрес в пределах МКАДа')
            btn3 = types.InlineKeyboardButton(callback_data='Перейти к комментарию', text='В пределах области')
            btn4 = types.InlineKeyboardButton(callback_data='Перейти к комментарию', text='Самовывоз')
            btn5 = types.InlineKeyboardButton(callback_data='Вернуться в главное меню ⬅️',
                                              text='Вернуться в главное меню ⬅️')
            markup.add(btn1, btn2, btn3, btn4, btn5)
            bot.send_message(message.from_user.id, f'Введите адрес доставки\nСамовывоз возможен с ВремяВремя',
                             reply_markup=markup)

        @bot.callback_query_handler(func=lambda call: call.data.startswith('Перейти к комментарию'))
        def address(message):
            markup = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton(callback_data='Детали заказа', text='Пропустить')
            btn2 = types.InlineKeyboardButton(callback_data='Вернуться в главное меню ⬅️',
                                              text='Вернуться в главное меню ⬅️')
            markup.add(btn1, btn2)
            bot.send_message(message.from_user.id, f'Вы можете добавить комментарий к заказу', reply_markup=markup)

        @bot.callback_query_handler(func=lambda call: call.data.startswith('Детали заказа'))
        def address(message):
            markup = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton(callback_data='Узнать дату доставки', text='Узнать дату доставки')
            btn2 = types.InlineKeyboardButton(callback_data='Вернуться в главное меню ⬅️',
                                              text='Вернуться в главное меню ⬅️')
            markup.add(btn1, btn2)
            bot.send_message(message.from_user.id, 'Ваш заказ сохранён. \nДетали заказа:', reply_markup=markup)

        @bot.callback_query_handler(func=lambda call: call.data.startswith('Узнать дату доставки'))
        def address(message):
            markup = types.InlineKeyboardMarkup()
            # btn1 = types.InlineKeyboardButton(callback_data='Оставить жалобу', text='Оставить жалобу')
            btn2 = types.InlineKeyboardButton(callback_data='Вернуться в главное меню ⬅️',
                                              text='Вернуться в главное меню ⬅️')
            markup.add(btn2)
            bot.send_message(message.from_user.id, 'Торт будет доставлен:', reply_markup=markup)

        bot.polling(none_stop=True, interval=0)

#
