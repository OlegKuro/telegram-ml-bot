import apiai, json
from envparse import env
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

env.read_envfile()
token = env('TELEGRAM_TOKEN')
# http_proxy = env('HTTP_PROXY')
# https_proxy = env('HTTPS_PROXY')
dialogflow_token = env('DIALOGFLOW_CLIENT_TOKEN')
lang = env('BOT_LANG')


def main():
    updater = Updater(token=token)  # Токен API к Telegram
    dispatcher = updater.dispatcher

    # Обработка команд
    def startCommand(bot, update):
        bot.send_message(chat_id=update.message.chat_id, text='Привет, давай пообщаемся?')

    def textMessage(bot, update):
        request = apiai.ApiAI(dialogflow_token).text_request()
        request.lang = lang
        request.session_id = 'BatlabAIBot' # ID Сессии диалога (нужно, чтобы потом учить бота)
        request.query = update.message.text # Посылаем запрос к ИИ с сообщением от юзера
        responseJson = json.loads(request.getresponse().read().decode('utf-8'))
        response = responseJson['result']['fulfillment']['speech'] # Разбираем JSON и вытаскиваем ответ
        # Если есть ответ от бота - присылаем юзеру, если нет - бот его не понял
        if response:
            bot.send_message(chat_id=update.message.chat_id, text=response)
        else:
            bot.send_message(chat_id=update.message.chat_id, text='Я Вас не совсем понял!')

    # Хендлеры
    start_command_handler = CommandHandler('start', startCommand)
    text_message_handler = MessageHandler(Filters.text, textMessage)
    # Добавляем хендлеры в диспетчер
    dispatcher.add_handler(start_command_handler)
    dispatcher.add_handler(text_message_handler)
    # Начинаем поиск обновлений
    updater.start_polling(clean=True)
    # Останавливаем бота, если были нажаты Ctrl + C
    updater.idle()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()