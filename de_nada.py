import unicodedata, re

DE_NADA_REGEXES = tuple(re.compile(r, re.IGNORECASE) for r in
    (
        r'de\s+nada',
        r'disponha',
        r'por\s+nada',
        r'nao\s+ha\s+de\s+que',
    )
)

def has_de_nada(text):
    text = text or ''
    return any(r.search(_remove_diacriticos(text)) for r in DE_NADA_REGEXES)

def _remove_diacriticos(text):
    if text:
        return str(unicodedata.normalize('NFD', text).encode('ascii', 'ignore'), encoding='ascii')
    else:
        return text
