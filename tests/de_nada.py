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
    def test_de_nada_reconhece(self, valor):
        self.assertTrue(de_nada.has_de_nada(valor))

    @unittest.expectedFailure # ainda não sei falar grego
    def test_de_nada_grego(self):
        self.assertTrue(de_nada.has_de_nada('D\u0395 \u039d\u0391D\u0391'))

    @data(
        '',
	None,
        'de tudo',
        'do nada',
        'que nada',
        'denada',
        'Esse bot não entende nada',
        'Entende nadar?',
    )
    def test_de_nada_rejeita(self, valor):
        self.assertFalse(de_nada.has_de_nada(valor))
