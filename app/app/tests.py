"""
Sample Tests
"""

from django.test import SimpleTestCase
from app import calc


class CalcTest(SimpleTestCase):
    """Test calc module"""

    def test_add_nmber(self):
        """Test adding numbers together"""
        res = calc.add(5, 1)
        self.assertEqual(res, 6)

    def test_subtract_numbers(self):
        """Test subtracting numbers"""

        res = calc.subtract(10, 15)
        self.assertEqual(res, 5)
