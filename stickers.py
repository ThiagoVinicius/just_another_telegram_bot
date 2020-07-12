import zipfile
import os.path
import io
import hashlib

PERSISTENT_STORAGE_PATH = 'data', 'persistent'

def _download_sticker_set(bot, set_id, timeout):
    packed_output = io.BytesIO()
    stickerset = bot.get_sticker_set(set_id)
    with zipfile.ZipFile(packed_output, mode='w') as zip_output:
        for sticker in stickerset.stickers:
            sticker_file = bot.get_file(sticker.file_id, timeout=timeout)
            sticker_img = sticker_file.download_as_bytearray() # deveria ter timeout
            path_in_zip = os.path.basename(sticker_file.file_path)
            zip_output.writestr(path_in_zip, sticker_img)
    return packed_output.getvalue()

def _upload_and_send(bot, chat_id, name, contents, timeout):
    print('enviando novo')
    stream = io.BytesIO(contents)
    sent = bot.send_document(
        chat_id=chat_id,
        document=stream,
        filename=name,
        timeout=timeout)
    return sent.document.file_id

def _send_existing(bot, chat_id, file_id):
    print('enviando existente')
    bot.send_document(chat_id=chat_id, document=file_id)

def _upload_id_filename(set_id):
    digest = hashlib.sha256(bytes(set_id, 'utf-8')).hexdigest()
    return os.path.join(*PERSISTENT_STORAGE_PATH, 'sticker_set_db', digest)

def _store_upload_id(set_id, file_id):
    file_name = _upload_id_filename(set_id)
    with open(file_name, 'x') as storage:
        storage.write(file_id)
    with open('%s_name' % file_name, 'x') as storage:
        # para debug
        storage.write(set_id)

def _get_upload_id(set_id):
    file_name = _upload_id_filename(set_id)
    try:
        with open(file_name, 'r') as storage:
            return storage.read()
    except:
        return None

def provide_sticker_pack(bot, chat_id, set_id, timeout=None):
    upload_id = _get_upload_id(set_id)
    if upload_id:
        _send_existing(bot, chat_id, upload_id)
    else:
        pack = _download_sticker_set(bot, set_id, timeout)
        filename = '%s.zip' % set_id
        upload_id = _upload_and_send(bot, chat_id, filename, pack, timeout)
        _store_upload_id(set_id, upload_id)

if __name__ == '__main__':
    import telegram
    with open('bot.token') as token:
        bot = telegram.Bot(token.readlines()[0].strip())
    #zipado = download_sticker_set(bot, 'avioesemusicas')
    #with open('zipado.zip', 'wb') as saida:
    #    saida.write(zipado)

    upload_id = get_upload_id('teste')
    if upload_id:
        send_existing(bot, upload_id)
    else:
        upload_id = upload_and_send(bot, 'teste.txt', b'isso eh um teste')
        store_upload_id('teste', upload_id)
