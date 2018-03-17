import telegram.ext
from telegram.ext.dispatcher import run_async
import logging
import de_nada
import stickers

SEND_MESSAGE_TIMEOUT = 30
STICKER_TIMEOUT = 120

def load_file(filename):
    with open(filename, 'r') as file_content:
        return [m.strip() for m in file_content.readlines()]

def load_token():
    return load_file('bot.token')[0]

def load_masters():
    return [int(i) for i in load_file('masters.list')]

def load_allowed_groups():
    return [int(i) for i in load_file('allowed_groups.list')]

def register_handlers(dispatcher, masters=[], allowed_groups=[]):
    MessageHandler = telegram.ext.MessageHandler
    dispatcher.add_handler(MessageHandler(chat_with_sticker_filter(), chat_with_sticker))
    dispatcher.add_handler(MessageHandler(chat_from_master_filter(masters), chat_from_master))
    dispatcher.add_handler(MessageHandler(telegram.ext.Filters.private, chat_from_strangers))
    dispatcher.add_handler(MessageHandler(allowed_group_filter(allowed_groups), update_on_allowed_group))
    dispatcher.add_handler(MessageHandler(telegram.ext.Filters.group, strange_group_update))
    dispatcher.add_handler(MessageHandler(telegram.ext.Filters.all, unhandled_update))
    dispatcher.add_error_handler(error_callback)

def chat_with_sticker_filter():
    Filters = telegram.ext.Filters
    return Filters.private & Filters.sticker

def chat_from_master_filter(masters):
    Filters = telegram.ext.Filters
    chat = Filters.user(user_id=masters)
    private = Filters.private
    return chat & private

def allowed_group_filter(allowed_groups):
    Filters = telegram.ext.Filters
    chat = Filters.chat(chat_id=allowed_groups)
    group = Filters.group
    return chat & group

def chat_with_sticker(bot, update):
    set_name = update.message.sticker.set_name
    print('Recebi um sticker.')
    if set_name:
        async_send_message(
            bot,
            chat_id=update.message.chat_id,
            reply_to_message_id=update.message.message_id,
            text='Guentae que estou trabalhando nisso',
            timeout=SEND_MESSAGE_TIMEOUT)
        print('Sticker faz parte de um set, fornecendo set')
        try:
            stickers.provide_sticker_pack(
                bot,
                update.message.chat_id,
                set_name,
                timeout=STICKER_TIMEOUT)
        except:
            async_send_message(
                bot,
                chat_id=update.message.chat_id,
                reply_to_message_id=update.message.message_id,
                text='Falhei mizeravelmente. Desculpe',
                timeout=SEND_MESSAGE_TIMEOUT)
    else:
        print('Sticker não faz parte de um set')
        async_send_message(
            bot,
            chat_id=update.message.chat_id,
            reply_to_message_id=update.message.message_id,
            text='Oops, não sei o que fazer com esse sticker',
            timeout=SEND_MESSAGE_TIMEOUT)

@run_async
def async_send_message(bot, *args, **kwargs):
    bot.send_message(*args, **kwargs)

@run_async
def chat_from_master(bot, update):
    print('Falando com o mestre')
    bot.send_message(
        chat_id=update.message.chat_id,
        text='Olá, mestre',
        timeout=SEND_MESSAGE_TIMEOUT)

@run_async
def chat_from_strangers(bot, update):
    print('Falando com um estranho')
    bot.send_message(
        chat_id=update.message.chat_id,
        text='Desapareça da minha frente. Só converso com meu mestre.',
        timeout=SEND_MESSAGE_TIMEOUT)

@run_async
def update_on_allowed_group(bot, update):
    print('Estou em um grupo permitido %s' % update.effective_chat)
    if update.message and de_nada.has_de_nada(update.message.text):
        bot.send_message(
            chat_id=update.effective_chat.id,
            text='https://youtu.be/oIfXG_kscH4',
            reply_to_message_id=update.message.message_id,
            timeout=SEND_MESSAGE_TIMEOUT)

@run_async
def strange_group_update(bot, update):
    print('Deixando chat (effective_chat = %s)' % update.effective_chat)
    bot.send_message(
        chat_id=update.effective_chat.id,
        text='Detesto estar nesse grupo.',
        timeout=SEND_MESSAGE_TIMEOUT)
    update.effective_chat.leave()

@run_async
def unhandled_update(bot, update):
    print('Nao sei o que fazer com esse: %s' % update)

@run_async
def error_callback(bot, update, error):
    print('Ocorreu um erro não tratado: %s' % error)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    token = load_token()
    masters = load_masters()
    allowed_groups = load_allowed_groups()

    updater = telegram.ext.Updater(token)
    register_handlers(updater.dispatcher, masters, allowed_groups)
    updater.start_polling()
    updater.idle()
