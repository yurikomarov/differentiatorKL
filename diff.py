import re
from fractions import Fraction

class Differentiator:
    def __init__(self):
        self.derivatives_table = {
            'sin(x)': 'cos(x)',
            'cos(x)': '-sin(x)',
            'tan(x)': 'sec^2(x)',
            'cot(x)': '-csc^2(x)',
            'sec(x)': 'sec(x)tan(x)',
            'csc(x)': '-csc(x)cot(x)',
            'e^x': 'e^x',
            'ln(x)': '1/x'
        }

    def parse_term(self, term):
        if term in self.derivatives_table:
            return self.derivatives_table[term], "-"
        elif term[1:] in self.derivatives_table:
            return f"-{self.derivatives_table[term[1:]]}", "-"

        term = term.replace(" ", "")
        if 'x' not in term:
            return float(term), 0

        if term == 'x':
            return 1, 1

        match = re.match(r'([\-\d\.]*)(x(?:\^(-?[\d]+))?)', term)
        if not match:
            raise ValueError("Некорректный формат выражения")

        coef = match.group(1)
        exp = match.group(3)

        coef = float(coef) if coef and coef != '-' else (-1.0 if coef == '-' else 1.0)
        exp = Fraction(exp) if exp else Fraction(1)

        return coef, exp

    def differentiate(self, expression):
        try:
            terms = expression.replace("-", "+-").split("+")

            if '' in terms:
                terms.remove('')

            derivative_terms = []

            for term in terms:
                term = str(term).replace(" ", "")
                coef, exp = self.parse_term(term)

                if exp == 0:
                    continue

                if exp == "-":
                    derivative_terms.append(coef)
                    continue

                new_coef = coef * exp
                #print(new_coef, exp)
                new_exp = exp - Fraction(1)
                #print(new_exp)
                if new_exp == 0:
                    derivative_terms.append(str(float(new_coef)))
                elif new_exp == 1:
                    derivative_terms.append(f"{float(new_coef)}x")
                else:
                    derivative_terms.append(f"{float(new_coef)}x^{new_exp}")

            derivative = ""
            for term in derivative_terms:
                if str(term).startswith('--'):
                    derivative += " + " + str(term).replace("--", "")
                elif str(term).startswith('-'):
                    derivative += " - " + str(term).replace("-","")
                else:
                    derivative += " + " + str(term)

            if derivative.startswith(" +"):
                return derivative.replace(" + ", "", 1)
            elif derivative.startswith(" -"):
                return derivative.replace(" - ", "-", 1)
            elif derivative == "":
                return "0"
            return derivative

        except Exception:
            return "ERROR"

if __name__ == "__main__":
    diff = Differentiator()
    expression = input("Exp: ")
    print(f"f'= {diff.differentiate(expression)}")