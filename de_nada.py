import unicodedata, re

DE_NADA_REGEXES = tuple(re.compile(r, re.IGNORECASE) for r in
    (
        r'\bde\b\s+\bnada\b',
        r'\bdisponha\b',
        r'\bpor\b\s+\bnada\b',
        r'\bnao\b\s+\bha\b\s+\bde\b\s+\bque\b',
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
