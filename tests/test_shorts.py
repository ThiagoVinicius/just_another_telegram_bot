# -*- encoding: utf-8 -*-

import unittest
from ddt import ddt, data

import shorts
import telegram

def utf16len(text):
    return len(text.encode('utf-16-le'))

@ddt
class TestShorts(unittest.TestCase):
    @data(
        ('https://youtube.com/shorts/CgS7O1KJpq8?feature=share', 'CgS7O1KJpq8'),
        ('https://youtube.com/shorts/1Yiit_-cxL8', '1Yiit_-cxL8'),
        ('https://youtube.com/shorts/c6Zb4cW5hOY?feature=share', 'c6Zb4cW5hOY'),
        ('https://youtube.com/shorts/PzWDiSvyNQk?feature=share', 'PzWDiSvyNQk'),
        ('https://www.youtube.com/shorts/Qm4oU1omaX0', 'Qm4oU1omaX0'),
        ('https://www.youtube.com/shorts/jEUrytdOFWI', 'jEUrytdOFWI'),
    )
    def test_contem_shorts(self, data):
        url, id = data
        message = telegram.Message(message_id=1, date=None, chat=None,
                                   text=url,
                                   entities=[
                                       telegram.MessageEntity(
                                           'url', offset=0,
                                           length=utf16len(url))])

        self.assertEqual([id], shorts.find_shorts_ids(message))

