import unittest
from diff import Differentiator

class TestDifferentiator(unittest.TestCase):
    def setUp(self):
        self.diff = Differentiator()

    def test_basic(self):
        self.assertEqual(self.diff.differentiate("5"), "0")
        self.assertEqual(self.diff.differentiate("y"), "0")

    def test_power_rules(self):
        self.assertEqual(self.diff.differentiate("x^2"), "2*x")
        self.assertEqual(self.diff.differentiate("x^3"), "3*x^2")
        self.assertEqual(self.diff.differentiate("2^x"), "Ошибка: Не могу продифференцировать: 2^x")

    def test_trigonometric(self):
        self.assertEqual(self.diff.differentiate("sin(x)"), "cosx")
        self.assertEqual(self.diff.differentiate("cos(x)"), "-sinx")
        self.assertEqual(self.diff.differentiate("tan(x)"), "(1 + tanx^2)")

    def test_logarithm(self):
        self.assertEqual(self.diff.differentiate("ln(x)"), "1/x")
        self.assertEqual(self.diff.differentiate("lg(x)"), "1/(x*ln(10))")

    def test_product_rule(self):
        self.assertEqual(self.diff.differentiate("x*sin(x)"), "sinx + x*cosx")
        self.assertEqual(self.diff.differentiate("2*x"), "2")

    def test_quotient_rule(self):
        self.assertEqual(self.diff.differentiate("x/y"), "y/y^2")

    def test_chain_rule(self):
        self.assertEqual(self.diff.differentiate("sin(2*x)"), "2*cos(2*x)")
        self.assertEqual(self.diff.differentiate("ln(x^2)"), "1/(x^2)*(2*x)")

    def test_error_handling(self):
        self.assertEqual(self.diff.differentiate("((x"), "Ошибка: Несбалансированные скобки")
        self.assertEqual(self.diff.differentiate("sin(x"), "Ошибка: Несбалансированные скобки")

if __name__ == "__main__":
    unittest.main()