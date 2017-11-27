import unittest
from ddt import ddt, data
import de_nada

@ddt
class TestDeNada(unittest.TestCase):
    @data(
        'de nada',
        'de   nada',
        'de\nnada',
        '   de nada ',
        'não há de quê',
        'não   há de quê',
        'não há    de quê',
        'não há de     quê',
        'não   há  de  quê',
        '   não   há  de  quê ',
        'disponha',
        '  \ndisponha  ',
        'por nada',
        'por   nada',
        'por\n nada',
        'Por\n nada',
        'não ha de quê',
    )
    def test_de_nada_classico_ok(self, valor):
        self.assertTrue(de_nada.has_de_nada(valor))

    @data(
        '',
	None,
        'de tudo',
        'do nada',
        'que nada',
        'denada',
    )
    def test_de_nada_classico_None(self, valor):
        self.assertFalse(de_nada.has_de_nada(valor))
