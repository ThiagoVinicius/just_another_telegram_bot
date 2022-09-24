import itertools
import re
import urllib.parse

import telegram

SHORTS_ID_PATTERN = re.compile('.+' + re.escape('shorts/') + r'(\w+)')

URL = telegram.MessageEntity.URL
TEXT_LINK = telegram.MessageEntity.TEXT_LINK

def create_normal_url(id):
    return f'https://youtu.be/{id}'

def find_shorts_ids(message):
    urls1 = (message.parse_entity(x) for x in message.entities if x.type == URL)
    urls2 = (x.url for x in message.entities if x.type == TEXT_LINK)

    result = []
    for u in itertools.chain(urls1, urls2):
        maybe_id = _find_shorts_id(u)
        if maybe_id:
            result.append(maybe_id)

    return result

def _find_shorts_id(url):
    parsed = urllib.parse.urlsplit(url)

    isYoutube = parsed.netloc == 'youtube.com' or parsed.netloc.endswith('.youtube.com')
    isShorts = '/shorts/' in parsed.path

    if isYoutube and isShorts:
        match = SHORTS_ID_PATTERN.match(parsed.path)
        if match:
            groups = match.groups()
            return groups[0] if groups else None

    return None

