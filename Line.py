#!/usr/bin/env python

from decimal import Decimal, getcontext
from Vector import Vector

getcontext().prec = 30

class Line(object):

    NO_NONZERO_ELTS_FOUND_MSG = 'No nonzero elements found'

    def __init__(self, normal_vector=None, constant_term=None):
        self.dimension = 2

        if not normal_vector:
            all_zeros = ['0']*self.dimension
            normal_vector = Vector(all_zeros)
        self.normal_vector = normal_vector

        if not constant_term:
            constant_term = Decimal('0')
        self.constant_term = Decimal(constant_term)

        self.set_basepoint()


    def set_basepoint(self):
        try:
            n = self.normal_vector
            c = self.constant_term
            basepoint_coords = ['0']*self.dimension

            initial_index = Line.first_nonzero_index(n)
            initial_coefficient = Decimal(n[initial_index])

            basepoint_coords[initial_index] = c/initial_coefficient
            self.basepoint = Vector(basepoint_coords)

        except Exception as e:
            if str(e) == Line.NO_NONZERO_ELTS_FOUND_MSG:
                self.basepoint = None
            else:
                raise e


    def __str__(self):

        num_decimal_places = 3

        def write_coefficient(coefficient, is_initial_term=False):
            coefficient = round(coefficient, num_decimal_places)
            if coefficient % 1 == 0:
                coefficient = int(coefficient)

            output = ''

            if coefficient < 0:
                output += '-'
            if coefficient > 0 and not is_initial_term:
                output += '+'

            if not is_initial_term:
                output += ' '

            if abs(coefficient) != 1:
                output += '{}'.format(abs(coefficient))

            return output

        n = self.normal_vector

        try:
            initial_index = Line.first_nonzero_index(n)
            terms = [write_coefficient(n[i], is_initial_term=(i==initial_index)) + 'x_{}'.format(i+1)
                     for i in range(self.dimension) if round(n[i], num_decimal_places) != 0]
            output = ' '.join(terms)

        except Exception as e:
            if str(e) == self.NO_NONZERO_ELTS_FOUND_MSG:
                output = '0'
            else:
                raise e

        constant = round(self.constant_term, num_decimal_places)
        if constant % 1 == 0:
            constant = int(constant)
        output += ' = {}'.format(constant)

        return output


    @staticmethod
    def first_nonzero_index(iterable):
        for k, item in enumerate(iterable):
            if not MyDecimal(item).is_near_zero():
                return k
        raise Exception(Line.NO_NONZERO_ELTS_FOUND_MSG)

    def is_parallel_to(self, line2):
        return self.normal_vector.is_parallel(line2.normal_vector)

    def __eq__(self, line2):
        if self.normal_vector.is_zero():
            if not line2.normal_vector.is_zero():
                return False
            else:
                diff = self.constant_term - line2.constant_term
                return MyDecimal(diff).is_near_zero()
        if (not self.is_parallel_to(line2)):
            return False

        basepoint_difference = self.basepoint.minus(line2.basepoint)

        return basepoint_difference.is_orthogonal(line2.normal_vector)

    def get_intersection(self, line2):
        if (self.is_parallel_to(line2)):
            if (self == line2):
                return self
            else:
                return None

        n1 = self.normal_vector
        n2 = line2.normal_vector
        k1 = self.constant_term
        k2 = line2.constant_term

        x = (n2[1] * k1 - n1[1] * k2) / (n1[0] * n2[1] - n1[1] * n2[0])
        y = (n1[0] * k2 - n2[0] * k1) / (n1[0] * n2[1] - n1[1] * n2[0])

        return Vector([x,y])

class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps

def lineIntersections2D():
    l1 = Line(Vector([4.046, 2.836]), 1.21)
    l2 = Line(Vector([10.115, 7.09]), 3.025)
    print (l1.get_intersection(l2))

    l1 = Line(Vector([7.204, 3.182]), 8.68)
    l2 = Line(Vector([8.172, 4.114]), 9.883)
    print (l1.get_intersection(l2))

    l1 = Line(Vector([1.182, 5.562]), 6.744)
    l2 = Line(Vector([1.773, 8.343]), 9.525)
    print (l1.get_intersection(l2))

def run():
  lineIntersections()

if __name__ == '__main__':
  run()
