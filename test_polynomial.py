import unittest
from unittest import TestCase
from polynomial import Polynomial

class TestPolynomial(TestCase):
    def setUp(self):
        self.p0 = Polynomial('2x4 -9x8 + 0x12')

    def test_print(self):
        poly_string = repr(self.p0)
        self.assertEqual(poly_string,'-9X^8 +2X^4')


if __name__ == '__main__':
    unittest.main()
    
    