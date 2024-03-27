import telebot
from config import keys, TOKEN
from extensions import APIException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def beginning(message: telebot.types.Message):
    text = ("* Чтобы начать работу, введите команду в следующем формате:\n<имя валюты, цену которой Вы хотите узнать> <имя валюты, в которой надо узнать цену первой валюты> <количество первой валюты>\n"
            "\n* Например: доллар рубль 100 = цена 100 долларов в рублях\n"
            "\n* Чтобы узнать все доступные валюты, введите команду /values")

    bot.reply_to(message, text)

@bot.message_handler(commands=['help'])
def beginning(message: telebot.types.Message):
    text = ("* Чтобы начать работу, нажмите -> /start"
            "\n* Чтобы узнать все доступные валюты, нажмите -> /values")

    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message:telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['voice'])
def repeat(message: telebot.types.Message):
    bot.send_message(message.chat.id, "У Вас очень красивый голос, но, к сожалению, я умею распознавать только текст  :)")

@bot.message_handler(content_types=['photo'])
def say_lmao(message: telebot.types.Message):
    bot.reply_to(message, 'Прекрасная картинка, но я умею распознавать только текст. Напишите, чем я могу Вам помочь?')

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Bоспользуйтесь командами /start или /help или введите данные в правильном формате')

        quote, base, amount = values
        get_price = CurrencyConverter.convert(quote, base, amount)

    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя: \n {e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду \n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} = {get_price}'
        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)