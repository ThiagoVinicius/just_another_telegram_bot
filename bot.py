import telegram.ext
import telegram
import logging
import de_nada
import shorts
import stickers
import os.path

SEND_MESSAGE_TIMEOUT = 30
STICKER_TIMEOUT = 120

de_nada_links = None # Inicializado no main

BASE_CONFIG_DIR = 'data', 'config'

def load_file(filename, basename=BASE_CONFIG_DIR):
    fullpath = os.path.join(*basename, filename)
    with open(fullpath, 'r') as file_content:
        return [m.strip() for m in file_content.readlines()]

def load_token():
    return load_file('bot.token')[0]

def load_masters():
    return [int(i) for i in load_file('masters.list')]

def load_allowed_groups():
    return [int(i) for i in load_file('allowed_groups.list')]

def register_handlers(dispatcher, masters=[], allowed_groups=[]):
    MessageHandler = telegram.ext.MessageHandler
    dispatcher.add_handler(MessageHandler(chat_with_sticker_filter(), chat_with_sticker, run_async=True))
    dispatcher.add_handler(MessageHandler(chat_from_master_filter(masters), chat_from_master))
    dispatcher.add_handler(MessageHandler(telegram.ext.Filters.chat_type.private, chat_from_strangers))
    dispatcher.add_handler(MessageHandler(allowed_group_filter(allowed_groups), update_on_allowed_group))
    dispatcher.add_handler(MessageHandler(telegram.ext.Filters.chat_type.groups, strange_group_update))
    dispatcher.add_handler(MessageHandler(telegram.ext.Filters.all, unhandled_update))
    dispatcher.add_error_handler(error_callback)

def chat_with_sticker_filter():
    Filters = telegram.ext.Filters
    return Filters.chat_type.private & Filters.sticker

def chat_from_master_filter(masters):
    Filters = telegram.ext.Filters
    chat = Filters.user(user_id=masters)
    private = Filters.chat_type.private
    return chat & private

def allowed_group_filter(allowed_groups):
    Filters = telegram.ext.Filters
    chat = Filters.chat(chat_id=allowed_groups)
    group = Filters.chat_type.groups
    return chat & group

def chat_with_sticker(update: telegram.Update, context: telegram.ext.CallbackContext):
    bot = context.bot
    set_name = update.message.sticker.set_name
    print('Recebi um sticker.')
    if set_name:
        bot.send_message(
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
            bot.send_message(
                chat_id=update.message.chat_id,
                reply_to_message_id=update.message.message_id,
                text='Falhei mizeravelmente. Desculpe',
                timeout=SEND_MESSAGE_TIMEOUT)
    else:
        print('Sticker não faz parte de um set')
        bot.send_message(
            chat_id=update.message.chat_id,
            reply_to_message_id=update.message.message_id,
            text='Oops, não sei o que fazer com esse sticker',
            timeout=SEND_MESSAGE_TIMEOUT)

def chat_from_master(update: telegram.Update, context: telegram.ext.CallbackContext):
    bot = context.bot
    print('Falando com o mestre')
    bot.send_message(
        chat_id=update.message.chat_id,
        text='Olá, mestre',
        timeout=SEND_MESSAGE_TIMEOUT)

def chat_from_strangers(update: telegram.Update, context: telegram.ext.CallbackContext):
    bot = context.bot
    print('Falando com um estranho')
    bot.send_message(
        chat_id=update.message.chat_id,
        text='Desapareça da minha frente. Só converso com meu mestre.',
        timeout=SEND_MESSAGE_TIMEOUT)

def update_on_allowed_group(update: telegram.Update, context: telegram.ext.CallbackContext):
    bot = context.bot
    print('Estou em um grupo permitido %s' % update.effective_chat)
    if update.message:

        common_params = {
            'chat_id': update.effective_chat.id,
            'reply_to_message_id': update.message.message_id,
            'timeout': SEND_MESSAGE_TIMEOUT
        }

        if de_nada.has_de_nada(update.message.text):
            bot.send_message(**common_params,
                text=de_nada_links.get_link())

        shorts_ids = shorts.find_shorts_ids(update.message)

        if shorts_ids:
            bot.send_message(**common_params,
                text='\n'.join(shorts.create_normal_url(id) for id in shorts_ids))

def strange_group_update(update: telegram.Update, context: telegram.ext.CallbackContext):
    bot = context.bot
    print('Deixando chat (effective_chat = %s)' % update.effective_chat)
    bot.send_message(
        chat_id=update.effective_chat.id,
        text='Detesto estar nesse grupo.',
        timeout=SEND_MESSAGE_TIMEOUT)
    update.effective_chat.leave()

def unhandled_update(update: telegram.Update, context: telegram.ext.CallbackContext):
    print('Nao sei o que fazer com esse: %s' % update)

def error_callback(update: telegram.Update, context: telegram.ext.CallbackContext):
    print('Ocorreu um erro não tratado: %s' % context.error)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    de_nada_links = de_nada.Links(os.path.join(*BASE_CONFIG_DIR, 'de_nada.links'))
    token = load_token()
    masters = load_masters()
    allowed_groups = load_allowed_groups()

    updater = telegram.ext.Updater(token, use_context=True)
    register_handlers(updater.dispatcher, masters, allowed_groups)
    updater.dispatcher.workers = 1
    updater.start_polling()
    updater.idle()
