# current problem -(1200d-2040p)X^2 -(6)+122a+18p) -> the output i am getting

class AlgebraicTerm:
    NUMBERS = '+-0123456789'
    def __init__(self,a = None,b = None):
        if a is None and b is None:
        # i.e. no argument is passed into constructor
            # create an AlgebraicTerm '0|'
            # '|' is a placeholder for a null variable
            self._number = 0
            self._variable = '|'
        elif a is not None and b is None:
        # i.e. argument is an algebraic_string
            self._number = ''
            # remove etraneous terms from the algbraic_string
            a = self._clean_up(a.lower())
            # extract the numbers from the algebraic_string
            index = 0
            for l in a:
                if l in self.NUMBERS:
                    self._number += l
                    index +=1
            # if number is just a sign i.e algebraic_string was of the form '-a','+a'
            # set number to 1
            if self._number in ['-','+']:
                self._number += '1'
            # what is left of the algebraic_string is the variable so we extract that
            self._variable =''
            while index < len(a):
                self._variable += a[index]
                index +=1
        else:
        # i.e. number and variable are passed as arguments
            self._number = a
            self._variable = b

    def __repr__(self):
        number = str(self._number)
        if number[0] not in '+-0':
            # every AlgebraicTerm should be rendered with sign
            number = '+{}'.format(number)
        if self._variable !='|':
            return '{}{}'.format(number, self._variable)
        else:
            return '{}'.format(number)

    def __add__(self, other):
        if self._variable == other._variable:
            number = int(self._number) + int(other._number)
            variable = self._variable
        else:
            raise ValueError('Can only add AlgebraicTerms of same variable')
        return AlgebraicTerm(number, variable)
    def __sub__(self, other):
        if self._variable == other._variable:
            number = int(self._number) - int(other._number)
            variable = self._variable
        else:
            raise ValueError('Can only add AlgebraicTerms of same variable')
        return AlgebraicTerm(number, variable)
    def __mul__(self, other):
        if type(self) == type(other):
            number = int(self._number) * int(other._number)
            variable = self._variable + other._variable
        elif type(other) in [type(1), type(1.0)]:
            number = int(self._number) * other
            variable = self. _variable
        return AlgebraicTerm(number, variable)
    def __rmul__(self, other):
        if type(self) == type(other):
            number = int(self._number) * other
            variable = self. _variable
        elif type(other) in [type(1), type(1.0)]:
            number = int(self._number) * other
            variable = self. _variable
        return AlgebraicTerm(number, variable)
    def __neg__(self):
        number = -int(self._number)
        variable = self._variable
        return AlgebraicTerm(number, variable)
    def __eq__(self, other):
        if type(self) == type(other):
            return self._number == other._number and self._variable == other._variable
        elif type(other) in [type(1), type(1.0)]:
            return int(self._number) == other and self._variable == '|'
    def __neq__(self, other):
        if type(self) == type(other):
            return self._number != other._number or self._variable != other._variable
        elif type(other) in [type(1), type(1.0)]:
            return int(self._number) != other or self._variable != '|'

    @staticmethod
    def _clean_up(s):
        # removes extraneous terms e.g '^', ' '
        new_s = ''
        for l in s:
            if l != ' ':
                new_s += l
        return new_s


class AlgebraicExpression(AlgebraicTerm):
    def __init__(self,s):
        s = str(s)
        self._terms = []
        if type(s) == type(AlgebraicTerm()):
            self._terms.append(s)
        else:
            raw_terms = self._split_into_terms(s)
            for term in raw_terms:
                self._terms.append(AlgebraicTerm(term))
    def __repr__(self):
        algebraic_string = ''
        for index,term in enumerate(self._terms):
            if int(term._number) != 0:
                if index == 0 and len(self) >1:
                    algebraic_string += repr(term).replace('+','')
                else:
                    algebraic_string += repr(term)
        if len(algebraic_string) == 0:
            algebraic_string += '0'
        return algebraic_string
    def __len__(self):
        return len(self._terms)
    def __getitem__(self, index):
        return self._terms[index]
    def __add__(self, other):
        other = AlgebraicExpression(repr(other))
        variables_list = set(self._get_variables_list()+ other._get_variables_list())
        algebraic_string = ''
        for variable in variables_list:
            self_term = self._get_term_by_variable(variable)
            other_term = other._get_term_by_variable(variable)
            algebraic_string += repr(self_term + other_term)
        return AlgebraicExpression(algebraic_string)
    # do i really need this?
    def __radd__(self, other):
        other = AlgebraicExpression(repr(other))
        variables_list = set(self._get_variables_list()+ other._get_variables_list())
        algebraic_string = ''
        for variable in variables_list:
            self_term = self._get_term_by_variable(variable)
            other_term = other._get_term_by_variable(variable)
            algebraic_string += repr(self_term + other_term)
        return AlgebraicExpression(algebraic_string)
    def __sub__(self, other):
        variables_list = set(self._get_variables_list()+ other._get_variables_list())
        algebraic_string = ''
        for variable in variables_list:
            self_term = self._get_term_by_variable(variable)
            other_term = other._get_term_by_variable(variable)
            algebraic_string += repr(self_term - other_term)
        return AlgebraicExpression(algebraic_string)
    def __mul__(self, other):
        algebraic_string = ''
        for term in self._terms:
            algebraic_string += repr(other * term)
        return AlgebraicExpression(algebraic_string)
    def __rmul__(self, other):
        algebraic_string = ''
        for term in self._terms:
            algebraic_string += repr(other * term)
        return AlgebraicExpression(algebraic_string)
    def __neg__(self):
        for i,_ in enumerate(self):
            self._terms[i] = -self._terms[i]
        return self
    def __eq__(self, other):
        if type(self) == type(other):
            for self_term, other_term in zip(self, other):
                if self_term != other_term:
                    return False
                return True
        elif type(other) in [type(1), type(1.0)]:
            if len(self) != 1:
                return False
            return True if self[0] == other else False
        return False
    def __neq__(self, other):
        if type(self) == type(other):
            for self_term, other_term in zip(self, other):
                if self_term == other_term:
                    return False
                return True
        elif type(other) in [type(1), type(1.0)]:
            return self[0] != other
        return True

    def _get_variables_list(self):
        variables_list = []
        for term in self._terms:
            if term._variable is None:
                term._variable = '|'
            variables_list.append(term._variable)
        return variables_list
    def _get_term_by_variable(self, variable):
        for term in self._terms:
            if term._variable == variable:
                return term
        return AlgebraicTerm(0,variable)
    def _split_into_terms(self, s):
        terms = []
        term = ''
        for index,l in enumerate(s):
            if index == len(s) -1:
                if l!= ')':
                    term += l
                terms.append(term)
            if l in '+-' and index >0:
                terms.append(term)
                term = l
            else:
                term += l
        for index,_ in enumerate(terms):
            if terms[index][0] not in '+-':
                terms[index] = '+' + terms[index]
        return terms
    def factor_out_minus_sign(self):
        if repr(self[0])[0] == '-':
            self = -self
            return '-({})'.format(self)
        return '+({})'.format(self)
    @staticmethod
    def _open_parentheses(s):
        if not '(' in s:
            return s
        new_s =''
        if s[0] in '+(':
            for i,l in enumerate(s):
                if l not in ' ()':
                    if i > 0:
                        new_s += l
        elif s[0] == '-':
            for i,l in enumerate(s) :
                if l not in ' ()':
                    if i > 0:
                        if l == '+':
                            l= '-'
                        elif l == '-':
                            l = '+'
                        new_s += l
            new_s = '-'+ new_s
        return new_s
        

class PolynomialTerm:
    def __init__(self, a= None, b= None):
        # attributes: _coeff, _power
        if a is None and b is None:
            # sets polynomial to 0X^0
            self._coeff = AlgebraicExpression(0)
            self._power = 0
        elif a is not None and b is None:
            # i.e. the polynomial term is passed as a string
            # remove extraneous symbols e.g. '^', ' '
            a = self._clean_up(a.lower())
            self._coeff, self._power = self._get_coeff_and_power(a)
            # print(self._coeff, self._power)
        else:
            # i.e polynomial term is passed as (coeff, power)
            self._coeff, self._power = AlgebraicExpression(a), b

    def __repr__(self):
        coeff = self._coeff
        if repr(coeff) == '0':
            return '0'
        if len(coeff) >1:
            coeff = coeff.factor_out_minus_sign()
        power = self._power
        if power == 0:
            # dsiplay only constant
            poly_term = '{}'.format(coeff)
        elif power == 1:
            # display only coeff and X
            poly_term = '{}X'.format(coeff)
        else:
            # display full polynomial term AX^b
            poly_term = '{}X^{}'.format(coeff, power)
        return poly_term
    
    def __add__(self, other):
        if not self._same_order(other):
            raise ValueError('Cannot add Polynomial terms of different orders')
        coeff = repr(self._coeff + other._coeff)
        power = self._power
        return PolynomialTerm(coeff, power)

    def __sub__(self, other):
        if not self._same_order(other):
            raise ValueError('Cannot subtract Polynomial terms of different orders')
        coeff = repr(self._coeff - other._coeff)
        power = self._power
        return PolynomialTerm(coeff, power)

    def __mul__(self,other):
        if type(self) == type(other):
            coeff = repr(self._coeff *other._coeff)
            power = int(self._power) + int(other._power)
        elif type(other) in [type(1), type(1.0)]:
            coeff = repr(self._coeff * other)
            power = self._power
        else:
            raise ValueError('Polynomial can only be multiplied by Polynomial or numeric types')
        return PolynomialTerm(coeff, power)
    def __rmul__(self,other):
        if type(self) == type(other):
            coeff = repr(self._coeff *other)
            power = self._power
        elif type(other) in [type(1), type(1.0)]:
            coeff = repr(self._coeff * other)
            power = self._power
        else:
            raise ValueError('Polynomial can only be multiplied by Polynomial or numeric types')
        return PolynomialTerm(coeff, power)
    def __pow__(self, power):
        base = PolynomialTerm(1,0)
        for _ in range(power):
            base *= self
        return base

    #TODO pow()
    def __gt__(self, other):
        return self._power > other._power
    def __lt__(self, other):
        return self._power < other._power
    def __eq__(self, other):
        return self._coeff == other._coeff and self._power == other._power
    def __neq__(self, other):
        return self._coeff != other._coeff or self._power != other._power
    def __call__(self, value):
        return self._coeff*value**int(self._power)
    def derivative(self):
        if self._power == 0:
            return PolynomialTerm()
        coeff = int(self._power) * self._coeff
        power = int(self._power) - 1
        return PolynomialTerm(coeff, power)
    def integral(self):
        power = self._power + 1
        coeff = self._coeff/power
        return PolynomialTerm(coeff, power)

        
    # utility modifiers
    @staticmethod
    def _clean_up(s):
        # removes extraneous terms e.g '^', ' '
        new_s = ''
        for l in s:
            if l not in '^ ':
                new_s += l
        return new_s
    def _get_coeff_and_power(self,s):
        # constant term
        if not 'x' in s: 
            coeff, power  = AlgebraicExpression(s), 0
            return coeff, power
        # other terms
        split_poly_term = s.split('x') # [coeff] [X] [power]
        coeff, power = split_poly_term[0], split_poly_term[1]
        if coeff == '' or coeff == '+':
            # i.e. polynomial takes the form x^a or +x^a
            coeff = '+1'
            # so that polynomial now takes the form +1x^a
        elif coeff == '-':
            coeff = '-1'
        if power == '':
            power = '1'
        coeff = AlgebraicExpression(0)._open_parentheses(coeff)
        coeff = AlgebraicExpression(coeff)
        return coeff, power
    def _attempt_conversion_to_float(self,other):
        # try to convert both coefficients to floats
        try:
            self_coeff = float(self._coeff)
            other_coeff = float(other._coeff)
        # failure means that one of them is a string so we retain the strings
        except:
            self_coeff = self._coeff
            other_coeff = other._coeff
        return self_coeff, other_coeff




    # checkers
    def _same_order(self, other):
        return int(self._power) == int(other._power)

        
class Polynomial(PolynomialTerm):
    def __init__(self, s=None):
        if s is None:
            self._terms = [PolynomialTerm()]
        else:
            raw_terms = []
            for term in self._split_into_terms(s):
                raw_terms.append(PolynomialTerm(term))
            self._terms = self._shrink_terms(raw_terms)
        
    def __repr__(self):
        poly_string = ''
        for i,term in enumerate(self._terms):
            if repr(term) != '0':
                poly_string += repr(term)
                if i != len(self)-1:
                    poly_string += ' '
        return poly_string

    def __len__(self):
        return len(self._terms)
    def __getitem__(self, index):
        return self._terms[index]
    def __add__(self, other):
        self,other = self._conform(other)
        poly_string = ''
        for term_self, term_other in zip(self, other):
            poly_string += repr(term_self + term_other)
        return Polynomial(poly_string)
    def __radd__(self, other):
        self,other = self._conform(other)
        poly_string = ''
        for term_self, term_other in zip(self, other):
            poly_string += repr(term_self + term_other)
        return Polynomial(poly_string)
    def __sub__(self, other):
        self,other = self._conform(other)
        poly_string = ''
        for term_self, term_other in zip(self, other):
            poly_string += repr(term_self - term_other)
        return Polynomial(poly_string)
    def __rsub__(self, other):
        self,other = self._conform(other)
        poly_string = ''
        for term_self, term_other in zip(self, other):
            poly_string += repr(term_self - term_other)
        return Polynomial(poly_string)
    def __neg__(self):
        return Polynomial() - self
    def __mul__(self, other):
        if type(other) in [type(1), type(1.0)]:
            poly_string = ''
            for term in self._terms:
                poly_string += repr(term*other)
        elif type(other) == type(self):
            poly_string = ''
            for self_term in self:
                for other_term in other:
                    poly_string += repr(self_term * other_term)
        else:
            raise ValueError('Polynomial can only be multiplied by Polynomial or numeric types')
        return Polynomial(poly_string)
    def __rmul__(self, other):
        if type(other) in [type(1), type(1.0)]:
            poly_string = ''
            for term in self._terms:
                poly_string += repr(term*other)
        elif type(other) == type(self):
            poly_string = ''
            for self_term in self:
                for other_term in other:
                    poly_string += repr(self_term * other_term)
        else:
            raise ValueError('Polynomial can only be multiplied by Polynomial or numeric types')
        return Polynomial(poly_string)
    def __pow__(self, value):
        poly = self
        for _ in range(value-1):
            poly *= self
        return poly

    def __gt__(self, other):
        return True if self.order() > other.order() else False
    def __lt__(self, other):
        return True if self.order() < other.order() else False
    def __call__(self, value):
        """ Evaluates a polynomial with the given value """
        sum = AlgebraicExpression(0)
        for term in self:
            sum+= term(value)
        return sum

    
    #public methods
    def order(self):
        """ Returns the highest power of the Polynomial  """
        return self._terms[0]._power
    def least_non_zero_power(self):
        return self._terms[len(self._terms)-1]._power
    def derivative(self):
        """ Returns the first order derivative of the polynomial """
        poly_string = ''
        for poly in self:
            if poly.derivative() is not None:
                poly_string += repr(poly.derivative())
        return Polynomial(poly_string)
    
    def nth_derivative(self,order = 1):
        if order == 0:
            return self
        poly = self
        for _ in range(order):
            d_poly = poly.derivative()
            poly = d_poly
        return poly
    def integral(self):
        poly_string = ''
        for term in self:
            poly_string += repr(term.integral())
        return Polynomial(poly_string)
    # utility modifiers
    def _split_into_terms(self, s):
        # split Polynomial into individual polynomial terms
        terms = []
        term = ''
        inside_parentheses = False
        for index,l in enumerate(s):
            if l == '(':
                inside_parentheses = True
            elif l == ')':
                inside_parentheses = False
            if index == len(s) -1:
                term += l
                terms.append(term)
            elif l in '+-' and not inside_parentheses:
                terms.append(term)
                term = l
            else:
                term += l
        return terms

    def _sort_powers(self,d):
        # sort the dictionary of powers and their positions
        sorted_keys = sorted(d, reverse=True)
        new_d = {}
        for key in sorted_keys:
            new_d[key] = d[key]
        return new_d

    def _shrink_terms(self, terms):
        # collect like terms and evaluate
        powers = [ int(term._power) for term in terms ]
        powers_set = set(powers)
        # a dict to store powers and the positions in which they occcur in the polynomial
        powers_and_positions = {}
        for power in powers_set:
            powers_and_positions[power] = []
            for index,present_power in enumerate(powers):
                if power == present_power:
                    powers_and_positions[power].append(index)
        # sort the dict
        powers_and_positions = self._sort_powers(powers_and_positions)
        shrunk_terms = []
        for power,positions in zip(powers_and_positions.keys(), powers_and_positions.values()):
            # if the current power occurs in only one position, just add that term to the list
            if len(positions) == 1:
                shrunk_terms.append(terms[positions[0]])
            # if not, sum all the terms at the given positions
            else:
                # create a base for adding -> 0x^p
                sum = PolynomialTerm(0,power)
                for position in positions:
                    sum += terms[position]
                # ignore zero coefficient terms
                if sum._coeff != 0:
                    shrunk_terms.append(sum)
        return shrunk_terms
    def _conform(self, other):
        if type(other) in [type(1), type(1.0)]:
            other = Polynomial(str(other)+'x0')
        self, other = self._match_polynomials(self, other)
        return self, other

    @staticmethod
    def _match_polynomials(p1, p2):
        # fill in the gaps in both polynomials i.e (x2 - 1) -> (x2 +0x -1)
        p1._middle_pad()
        p2._middle_pad()
        # both polynomials might not be of the same order so pad the lower order one up to the higher order one
        if p1 < p2:
            p1._left_pad_to_power(p2.order())
        elif p1 > p2:
            p2._left_pad_to_power(p1.order())
        p1_least_power = p1.least_non_zero_power()
        p2_least_power = p2.least_non_zero_power()

        # if they have different least powers pad the higher least power one down to the lower least power one
        if p1_least_power > p2_least_power:
            p1._right_pad_to_power(p2_least_power)

        elif p1_least_power <p2_least_power:
            p2._right_pad_to_power(p1_least_power)
        return p1,p2

    def _left_pad_to_power(self,n):
        poly_order = self.order()
        while poly_order < n:
            poly_order += 1
            self._terms.insert(0,PolynomialTerm(0,poly_order))

    def _right_pad_to_power(self, n):
        least_power = self.least_non_zero_power()
        if least_power <= n:
            return
        while least_power >n:
            least_power -= 1
            self._terms.append(PolynomialTerm(0,least_power))
    def _middle_pad(self):
        order = int(self.order())
        least_power = int(self.least_non_zero_power())
        i = 1
        while order > least_power:
            order -= 1
            if self[i]._power != order:
                self._terms.insert(i, PolynomialTerm(0, order))
            i+=1

if __name__ == '__main__':
    # p0 = PolynomialTerm('-23jkx2')
    # p = PolynomialTerm('-x2')
    # p1 = PolynomialTerm('-cmnx2')
    # p2 = PolynomialTerm('(23c-4d)x2')
    # print(2*p1*p2 *3*p0*p**2)
    # a = 2
    # b = AlgebraicExpression('-33')
    # c = AlgebraicExpression('-7z + 3')
    # print(b * c)

    p = Polynomial('34px5 -20dx5-(2a-3p +1)x4 -12 +123')
    print(p.nth_derivative(0))









