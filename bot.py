import telebot
import requests
import json

TOKEN = "5939985499:AAG4OH2OcKRql8XXEW51rWzEitWIaTStagc"

bot = telebot.TeleBot(TOKEN)

keys = {
    'Доллар': 'USD',
    'Евро': 'EUR',
    'Рубль': 'RUR',
}

class ConvertionException(Exception):
    pass

# Обрабатываются все сообщения, содержащие команды '/start' or '/help'.
@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду в следующем формате: \n<название валюты> \
<в какую валюту перевести>\<сумма>\nсписок доступных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values', 'values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text',])
def convert(message: telebot.types.Message):
    values = message.text.split(' ')

    if len(values) > 3:
        raise ConvertionException('Много параметров')

    quote, base, amount = values

    if quote == base:
        raise ConvertionException(f'Невозможно перевести одинаковые валюты {base}')

    try:
        quote_ticker = keys[quote]
    except KeyError:
        raise ConvertionException(f'Не удалось обработать валюту {quote}')

    try:
        base_ticker = keys[base]
    except KeyError:
        raise ConvertionException(f'Не удалось обработать валюту {base}')

    try:
        amount = float(amount)
    except ValueError:
        raise ConvertionException(f'Не удалось обработать количество {amount}')

    quote_ticker, base_ticker = keys[quote], keys[base]
    r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
    total_base = json.loads(r.content)[keys[base]]
    text = f'Цена {amount} {quote} в {base} - {total_base}'
    bot.send_message(message.chat.id, text)


bot.polling()#Чтобы запустить бота, нужно воспользоваться методом polling.
