# -*- encoding: utf-8 -*-

import unittest
from ddt import ddt, data

import shorts
import telegram

def utf16len(text):
    return len(text.encode('utf-16-le'))

@ddt
class TestShorts(unittest.TestCase):
    @data(('https://youtube.com/shorts/CgS7O1KJpq8?feature=share', 'CgS7O1KJpq8'))
    def test_contem_shorts(self, data):
        url, id = data
        message = telegram.Message(message_id=1, date=None, chat=None,
                                   text=url,
                                   entities=[
                                       telegram.MessageEntity(
                                           'url', offset=0,
                                           length=utf16len(url))])
        print(url, id)
        print(message)
        print(shorts.find_shorts_ids(message))

