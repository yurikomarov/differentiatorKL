import re
import math

class Differentiator:
    def __init__(self):
        self.variable = 'x'
        self.functions = {
            'sin': self._deriv_sin,
            'cos': self._deriv_cos,
            'tan': self._deriv_tan,
            'ln': self._deriv_ln,
            'lg': self._deriv_lg,
            'sqrt': self._deriv_sqrt,
            'asin': self._deriv_asin,
            'acos': self._deriv_acos,
            'atan': self._deriv_atan,
            'exp': self._deriv_exp,
        }

    def _deriv_sin(self, arg):
        return f"cos({arg})", self._differentiate(arg)

    def _deriv_cos(self, arg):
        return f"-sin({arg})", self._differentiate(arg)

    def _deriv_tan(self, arg):
        return f"(1 + tan({arg})^2)", self._differentiate(arg)

    def _deriv_ln(self, arg):
        return f"1/({arg})", self._differentiate(arg)

    def _deriv_lg(self, arg):
        return f"1/({arg}*ln(10))", self._differentiate(arg)

    def _deriv_sqrt(self, arg):
        return f"1/(2*sqrt({arg}))", self._differentiate(arg)

    def _deriv_asin(self, arg):
        return f"1/sqrt(1-({arg})^2)", self._differentiate(arg)

    def _deriv_acos(self, arg):
        return f"-1/sqrt(1-({arg})^2)", self._differentiate(arg)

    def _deriv_atan(self, arg):
        return f"1/(1+({arg})^2)", self._differentiate(arg)

    def _deriv_exp(self, arg):
        return f"exp({arg})", self._differentiate(arg)

    def _parse_expression(self, expr):
        # добавляем знак умножения, где он указан неявно
        expr = re.sub(r'(\d)([a-zA-Z(])', r'\1*\2', expr)
        expr = re.sub(r'(\))([a-zA-Z\d(])', r'\1*\2', expr)
        tokens = []
        i = 0
        while i < len(expr):
            if expr[i] == ' ':
                i += 1
                continue
            # токенизация на операторы и скобки
            if expr[i] in '+-*/^()':
                tokens.append(expr[i])
                i += 1
            # на функции
            elif expr[i].isalpha():
                j = i
                while j < len(expr) and (expr[j].isalpha() or expr[j].isdigit()):
                    j += 1
                tokens.append(expr[i:j])
                i = j
            # на числа(константы, коэффиценты)
            elif expr[i].isdigit() or expr[i] == '.':
                j = i
                while j < len(expr) and (expr[j].isdigit() or expr[j] == '.'):
                    j += 1
                tokens.append(expr[i:j])
                i = j
        return tokens

    # проверка на константу
    def _is_constant(self, expr):
        return not any(c in expr for c in self.variable)

    # уравновешиваем скобки
    def _find_matching_bracket(self, expr, start_pos):
        balance = 1
        pos = start_pos + 1
        while pos < len(expr) and balance > 0:
            if expr[pos] == '(':
                balance += 1
            elif expr[pos] == ')':
                balance -= 1
            pos += 1
        return pos - 1 if balance == 0 else -1

    def _differentiate(self, expr):
        expr = expr.strip()

        # удаляем пробелы
        while (expr.startswith('(') and expr.endswith(')') and
               self._find_matching_bracket(expr, 0) == len(expr) - 1):
            expr = expr[1:-1]


        if self._is_constant(expr):
            return '0'
        if expr == self.variable:
            return '1'

        # выделяем показатель степени для функций
        func_pow_match = re.match(r'^([a-zA-Z]+\([^)]+\))\^([^+*-]+)$', expr)
        if func_pow_match:
            func_expr = func_pow_match.group(1)
            exponent = func_pow_match.group(2)

            try:
                # пробуем вычислить показатель степени
                exp_num = eval(exponent.replace('^', '**'), {'__builtins__': None, 'math': math}, {})

                # дифференцируем функцию внутри степени
                deriv_func = self._differentiate(func_expr)

                #если 0, то все выражение 0
                if deriv_func == '0':
                    return '0'

                # стандартная формула производной: n*f^(n-1)*f'
                if exp_num == 1:
                    return deriv_func
                elif exp_num == 2:
                    return f"2*{func_expr}*{deriv_func}"
                else:
                    return f"{exp_num}*{func_expr}^({exp_num - 1})*{deriv_func}"
            except:
                # eсли не удалось вычислить показатель, оставляем общий вид
                return f"{exponent}*{func_expr}^({exponent}-1)*{self._differentiate(func_expr)}"

        # дифференцирование функций
        for func_name in self.functions:
            if expr.startswith(func_name + '('):
                arg_start = len(func_name) + 1
                arg_end = self._find_matching_bracket(expr, arg_start - 1)
                if arg_end == -1:
                    raise ValueError(f"Незакрытая скобка в функции {func_name}")
                arg = expr[arg_start:arg_end]
                deriv_func, deriv_arg = self.functions[func_name](arg)
                return f"{deriv_func}*({deriv_arg})" if deriv_arg != '1' else deriv_func

        # разбиваем на слагаемые и вычисляем производную для каждого слагаемого
        if '+' in expr or '-' in expr:
            parts = []
            current = ''
            balance = 0
            for char in expr:
                if char == '(':
                    balance += 1
                elif char == ')':
                    balance -= 1
                if char in '+-' and balance == 0:
                    parts.extend([current, char])
                    current = ''
                else:
                    current += char
            parts.append(current)

            result = []
            sign = '+'
            for part in parts:
                if part in '+-':
                    sign = part
                elif part:
                    deriv = self._differentiate(part)
                    if deriv != '0':
                        result.append(f"{sign}{deriv}")
            return ''.join(result) or '0'

        # дифференцируем произведение
        if '*' in expr:
            balance = 0
            split_pos = -1
            for i, char in enumerate(expr):
                if char == '(':
                    balance += 1
                elif char == ')':
                    balance -= 1
                elif char == '*' and balance == 0:
                    split_pos = i
                    break

            if split_pos != -1:
                u, v = expr[:split_pos], expr[split_pos + 1:]
                du, dv = self._differentiate(u), self._differentiate(v)
                terms = []
                if du != '0':
                    terms.append(f"({du})*{v}")
                if dv != '0':
                    terms.append(f"{u}*({dv})")
                return ' + '.join(terms) or '0'

        # производная частного
        if '/' in expr:
            balance = 0
            split_pos = -1
            for i, char in enumerate(expr):
                if char == '(':
                    balance += 1
                elif char == ')':
                    balance -= 1
                elif char == '/' and balance == 0:
                    split_pos = i
                    break
            if split_pos != -1:
                u, v = expr[:split_pos], expr[split_pos + 1:]
                du, dv = self._differentiate(u), self._differentiate(v)
                numerator = []
                if du != '0':
                    numerator.append(f"({du})*{v}")
                if dv != '0':
                    numerator.append(f"-{u}*({dv})")
                return f"({' + '.join(numerator)})/({v})^2" if numerator else '0'

        # степенная функция
        if '^' in expr:
            balance = 0
            split_pos = -1
            for i, char in enumerate(expr):
                if char == '(':
                    balance += 1
                elif char == ')':
                    balance -= 1
                elif char == '^' and balance == 0:
                    split_pos = i
                    break
            if split_pos != -1:
                base = expr[:split_pos]
                exponent = expr[split_pos + 1:]

                # убираем скобки только для простых оснований
                if not re.search(r'[+\-*/]', base):
                    base = base.strip('()')

                if self._is_constant(exponent):
                    try:
                        exp_expr = exponent.replace('^', '**')
                        exp_num = eval(exp_expr, {'__builtins__': None, 'math': math}, {})
                        deriv_base = self._differentiate(base)
                        if deriv_base == '0':
                            return '0'
                        result = f"{exp_num}*{base}^({exp_num - 1})"
                        if deriv_base != '1':
                            result += f"*({deriv_base})"
                        return result
                    except:
                        pass

                try:
                    exp_num = float(exponent)
                    deriv_base = self._differentiate(base)
                    return f"{exp_num}*{base}^({exp_num - 1})*({deriv_base})"
                except:
                    pass

        raise ValueError(f"Не могу продифференцировать: {expr}")

    # основная функция
    def differentiate(self, expr):
        try:
            expr = expr.strip().replace('**', '^')
            tokens = self._parse_expression(expr)
            parsed_expr = ''.join(tokens)
            if parsed_expr.count('(') != parsed_expr.count(')'):
                raise ValueError("Несбалансированные скобки")
            result = self._differentiate(parsed_expr)
            return self._simplify(result)
        except ValueError as e:
            return f"Ошибка: {str(e)}"

    def _simplify(self, expr):
        prev_expr = None
        while prev_expr != expr:
            prev_expr = expr
            expr = self._basic_simplify(expr)
            expr = self._simplify_powers(expr)
            expr = self._simplify_multipliers(expr)
        if expr.strip() == '':
            return '1'
        return self._basic_simplify(expr)

    def _simplify_powers(self, expr):
        # упрощение (x^a)^b = x^(a*b)
        expr = re.sub(
            r'\(([^)]+)\^([\d.]+)\)\^([\d.]+)',
            lambda m: f"({m.group(1)})^{float(m.group(2)) * float(m.group(3))}",
            expr
        )

        # объединение степеней с одинаковым основанием
        expr = re.sub(
            r'([a-zA-Z(][\w()]+)\^([\d.]+)\*([a-zA-Z(][\w()]+)\^([\d.]+)',
            lambda m: f"{m.group(1)}^{float(m.group(2)) + float(m.group(4))}"
            if m.group(1) == m.group(3) else m.group(0),
            expr
        )
        return expr

    def _simplify_multipliers(self, expr):
        # разделяем выражение на множители и отделяем коэффиценты
        factors = re.split(r'\*', expr)

        numeric_coeffs = []
        other_factors = []
        for factor in factors:
            if re.fullmatch(r'-?\d+\.?\d*', factor):
                numeric_coeffs.append(float(factor))
            else:
                other_factors.append(factor)

        total_coeff = 1.0
        for coeff in numeric_coeffs:
            total_coeff *= coeff

        # собираем упрощённое выражение
        simplified = []
        if abs(total_coeff - 1.0) > 1e-9:
            coeff_str = str(int(total_coeff)) if total_coeff.is_integer() else f"{total_coeff}"
            simplified.append(coeff_str)
        simplified += other_factors

        return '*'.join(simplified)

    def _basic_simplify(self, expr):
        # удаление лишних скобок, точек, "*" и т.д.
        simplifications = [
            (r'\(1\)', '1'),
            (r'\*1(?=\D|$)', ''),
            (r'(?<!\d)1\*', ''),
            (r'\((\b[a-zA-Z]+\d*\b)\)', r'\1'),
            (r'\b0\+', ''),
            (r'\^1(?=\D|$)', ''),
            (r'\+\+', '+'),
            (r'--', '+'),
            (r'(\d+\.?\d*)\*(\d+\.?\d*)', lambda m: str(float(m.group(1)) * float(m.group(2)))),
            (r'\.0+(\D|$)', r'\1'),
            (r'(\d+)\.0+(\D|$)', r'\1\2'),
            (r'\^\((\d+)\)', r'^\1'),
            (r'\((-?\d+\.?\d*)\)\*', r'\1*'),
            (r'\*\((-?\d+\.?\d*)\)', r'*\1'),
            (r'(-?\d+\.?\d*)\*\((-?\d+\.?\d*)\)', lambda m: str(float(m.group(1)) * float(m.group(2)))),
        ]

        for pattern, repl in simplifications:
            expr = re.sub(pattern, repl, expr)

        while True:
            match = re.search(r'(-?\d+\.?\d*)\*\((-?\d+\.?\d*)\*([^)]+)\)', expr)
            if not match:
                break
            coeff1 = float(match.group(1))
            coeff2 = float(match.group(2))
            rest = match.group(3)
            new_coeff = coeff1 * coeff2
            new_coeff_str = str(int(new_coeff)) if new_coeff.is_integer() else f"{new_coeff}"
            expr = expr[:match.start()] + f"{new_coeff_str}*{rest}" + expr[match.end():]

        return expr

if __name__ == "__main__":
    diff = Differentiator()
    while True:
        expr = input("Введите выражение: ").strip()
        if expr.lower() == 'exit':
            break
        print(f"Производная: {diff.differentiate(expr)}")