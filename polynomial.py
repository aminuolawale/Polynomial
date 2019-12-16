class AlgebraicTerm:
    NUMBERS = '+-0123456789'
    def __init__(self,a = None,b = None):
        if a is None and b is None:
            self._number = 0
            self._variable = '|'
        elif a is not None and b is None:
            self._number = ''
            a = self._clean_up(a.lower())
            for l in a:
                if l in self.NUMBERS:
                    self._number += l
            self._variable = a[len(a)-1] if a[len(a)-1] not in self.NUMBERS else '|'
        else:
            self._number = a
            self._variable = b

    def __repr__(self):
        number = str(self._number)
        if number[0] not in '+-0':
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
        number = int(self._number) * other
        variable = self. _variable
        return AlgebraicTerm(number, variable)
    def __rmul__(self, other):
        number = int(self._number) * other
        variable = self. _variable
        return AlgebraicTerm(number, variable)
    
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
        raw_terms = self._split_into_terms(s)
        self._terms = []
        for term in raw_terms:
            self._terms.append(AlgebraicTerm(term))
    def __repr__(self):
        algebraic_string = ''
        for term in self._terms:
            algebraic_string += repr(term)
        return algebraic_string
    def __len__(self):
        return len(self._terms)
    def __getitem__(self, index):
        return self._terms[index]
    def __add__(self, other):
        variables_list = set(self._get_variables_list()+ other._get_variables_list())
        algebraic_string = ''
        for variable in variables_list:
            self_term = self._get_term_by_variable(variable)
            other_term = other._get_term_by_variable(variable)
            algebraic_string += repr(self_term + other_term)
        return AlgebraicExpression(algebraic_string)
    # do i really need this?
    def __radd__(self, other):
        variables_list = set(self._get_variables_list()+ other._get_variables_list())
        algebraic_string = ''
        for variable in variables_list:
            self_term = self._get_term_by_variable(variable)
            other_term = other._get_term_by_variable(variable)
            algebraic_string += repr(self_term + other_term)
        return AlgebraicExpression(algebraic_string)

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
        # split Polynomial into individual polynomial terms
        terms = []
        term = ''
        for index,l in enumerate(s):
            if index == len(s) -1:
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



class PolynomialTerm:
    def __init__(self, a= None, b= None):
        # attributes: _coeff, _power
        if a is None and b is None:
            # sets polynomial to 0X^0
            self._coeff = self._power = 0
        elif a is not None and b is None:
            # i.e. the polynomial term is passed as a string
            # remove extraneous symbols e.g. '^', ' '
            a = self._clean_up(a.lower())
            self._coeff, self._power = self._get_coeff_and_power(a)
        else:
            # i.e polynomial term is passed as (coeff, power)
            self._coeff, self._power = a, b

    def __repr__(self):
        is_algebraic = False
        try:
            coeff = float(self._coeff)
        except:
            is_algebraic = True
            coeff =self._coeff
        if not is_algebraic:
            if coeff >=0:
                # if coefficient is 1 print only sign eg. + 1x -> +x
                if coeff == 1:
                    coeff = '+'
                else:
                    coeff = '+' + str(self._coeff)
        # negative coeffs
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
        # try to convert both coefficients to floats
        self_coeff, other_coeff = self._attempt_conversion_to_float(other)
        # if either one is a string, we concatenate them with delimiter '+
        if type(self_coeff) == type('str') or type(other_coeff) ==type('str'):
            # if both coefficients are negative, we factor out the minus sign
            if self_coeff[0] == '-' and other_coeff[0] == '-':
                self_coeff = self_coeff[1:]
                other_coeff = other_coeff[1:]
                coeff = '-({}+{})'.format(self_coeff, other_coeff)

            else:
                if self_coeff[0] == '+':
                    self_coeff = self_coeff[1:]
                coeff = '({}+{})'.format(self_coeff, other_coeff)
            # clean up adjacent signs
            coeff = coeff.replace('+-','-')
            coeff = coeff.replace('++','+')
        # if both coefficients are numerals
        else:
            coeff = float(self._coeff) + float(other._coeff)
        power = self._power
        return PolynomialTerm(coeff, power)

    def __sub__(self, other):
        if not self._same_order(other):
            raise ValueError('Cannot subtract Polynomial terms of different orders')
        self_coeff, other_coeff = self._attempt_conversion_to_float(other)
        # if either one is a string, we concatenate them with delimiter '+
        if type(self_coeff) == type('char') or type(other_coeff) ==type('char'):
            # if both coefficients are negative, we factor out the minus sign
            if self_coeff[0] == '+' and other_coeff[0] == '+':
                self_coeff = self_coeff[1:]
                other_coeff = other_coeff[1:]
                coeff = '+({}-{})'.format(self_coeff, other_coeff)

            else:
                if self_coeff[0] == '+':
                    self_coeff = self_coeff[1:]
                coeff = '+({}-{})'.format(self_coeff, other_coeff)
            # clean up adjacent signs
            coeff = coeff.replace('-+','-')
            coeff = coeff.replace('--','+')
        # if both coefficients are numerals
        else:
            coeff = self_coeff - other_coeff
        power = self._power
        return PolynomialTerm(coeff, power)

    def __mul__(self,other):
        if type(other) in [type(1),type(1.0)]:
            coeff = self._coeff *other
            power = self._power
        elif type(other) == type(self):
            self_coeff, other_coeff = self._attempt_conversion_to_float(other)
            coeff = self_coeff * other_coeff
            power = int(self._power) + int(other._power)
        else:
            raise ValueError('Polynomial can only be multiplied by Polynomial or numeric types')
        return PolynomialTerm(coeff, power)
    def __gt__(self, other):
        return self._power > other._power
    def __lt__(self, other):
        return self._power < other._power
    def __eq__(self, other):
        return self._coeff == other._coeff and self._power == other._power
    def __neq__(self, other):
        return self._coeff != other._coeff or self._power != other._power
    def __call__(self, value):
        return self._coeff*value**self._power
    def derivative(self):
        if self._power == 0:
            return PolynomialTerm()
        coeff = self._power * self._coeff
        power = self._power - 1
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
            coeff, power  = s, 0
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
        return self._power == other._power

        
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
        for term in self._terms:
            if term._coeff !=0:
                poly_string += repr(term) + ' '
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
        sum =0
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
        for index,l in enumerate(s):
            if index == len(s) -1:
                term += l
                terms.append(term)
            if l in '+-' and index >0:
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
        powers = [ term._power for term in terms]
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
    # p = PolynomialTerm('-22x2')
    # p1 = PolynomialTerm('-2cx2')
    # print(p+p1)
    a = 2
    b = AlgebraicExpression('34e- 3d+34  -7n')
    c = AlgebraicExpression('23e-6d    +6z')
    print(b +c)











