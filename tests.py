import unittest
from diff import Differentiator

class TestDifferentiator(unittest.TestCase):
    def setUp(self):
        self.diff = Differentiator()

    def test_polynomials(self):
        self.assertEqual(self.diff.differentiate("x^2"), "2.0x")
        self.assertEqual(self.diff.differentiate("3x^4"), "12.0x^3")
        self.assertEqual(self.diff.differentiate("-5x^3"), "-15.0x^2")
        self.assertEqual(self.diff.differentiate("x"), "1.0")
        self.assertEqual(self.diff.differentiate("2x"), "2.0")
        self.assertEqual(self.diff.differentiate("-x"), "-1.0")

    def test_multiple_terms(self):
        self.assertEqual(self.diff.differentiate("x^2 + 3x + 5"), "2.0x + 3.0")
        self.assertEqual(self.diff.differentiate("2x^3 - 4x^2 + x - 7"), "6.0x^2 - 8.0x + 1.0")
        self.assertEqual(self.diff.differentiate("x^5 - x^4 + x^3 - x^2 + x - 1.0"),
                         "5.0x^4 - 4.0x^3 + 3.0x^2 - 2.0x + 1.0")

    def test_fractional_exponents(self):
        self.assertEqual(self.diff.differentiate("x^1/2"), "0.5x^-1/2")
        self.assertEqual(self.diff.differentiate("3x^2/3"), "2.0x^-1/3")

    def test_constants(self):
        self.assertEqual(self.diff.differentiate("5"), "0")
        self.assertEqual(self.diff.differentiate("-3.14"), "0")
        self.assertEqual(self.diff.differentiate("0"), "0")

    def test_trigonometric_functions(self):
        self.assertEqual(self.diff.differentiate("sin(x)"), "cos(x)")
        self.assertEqual(self.diff.differentiate("cos(x)"), "-sin(x)")
        self.assertEqual(self.diff.differentiate("-tan(x)"), "-sec^2(x)")
        self.assertEqual(self.diff.differentiate("cot(x)"), "-csc^2(x)")
        self.assertEqual(self.diff.differentiate("sec(x)"), "sec(x)tan(x)")
        self.assertEqual(self.diff.differentiate("csc(x)"), "-csc(x)cot(x)")

    def test_exponential_logarithmic(self):
        self.assertEqual(self.diff.differentiate("e^x"), "e^x")
        self.assertEqual(self.diff.differentiate("ln(x)"), "1/x")
        self.assertEqual(self.diff.differentiate("-e^x"), "-e^x")
        self.assertEqual(self.diff.differentiate("-ln(x)"), "-1/x")

    def test_invalid_input(self):
        self.assertEqual(self.diff.differentiate("sin(y)"), "ERROR")
        self.assertEqual(self.diff.differentiate("sapdof"), "ERROR")
        self.assertEqual(self.diff.differentiate(""), "0")

    def test_mixed_expressions(self):
        self.assertEqual(self.diff.differentiate("2x^3 + sin(x) - ln(x)"), "6.0x^2 + cos(x) - 1/x")
        self.assertEqual(self.diff.differentiate("cos(x) + e^x - 5x^2"), "-sin(x) + e^x - 10.0x")


if __name__ == "__main__":
    unittest.main()