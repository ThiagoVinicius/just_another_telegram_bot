import unicodedata, re
import json
import logging
import random

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

class Links(object):
    def __init__(self, nome_arquivo='de_nada.links'):
        links_pesos = { 'https://youtu.be/oIfXG_kscH4' : 1 }
        try:
            with open(nome_arquivo) as arquivo:
                links_pesos = json.load(arquivo)
        except json.decoder.JSONDecodeError as e:
            logging.exception('Falha ao ler links do arquivo {}'.format(
                nome_arquivo))
            raise e
        except FileNotFoundError:
            logging.info('Arquivo {} não encontrado. Usando link padrão'.format(
                nome_arquivo))
            logging.debug('Detalhes do erro', exc_info=True)

        self._links = [link for link in links_pesos.keys()]
        self._pesos = [links_pesos[link] for link in self._links]
        print ('[de nada] Configurados os seguintes links e pesos: {}'.format(
            links_pesos))

    def get_link(self):
        return random.choices(self._links, self._pesos)[0]

def _remove_diacriticos(text):
    if text:
        return str(unicodedata.normalize('NFD', text).encode('ascii', 'ignore'), encoding='ascii')
    else:
        return text
