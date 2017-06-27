#!/usr/bin/env python

import math
from decimal import Decimal, getcontext

getcontext().prec = 30

class Vector(object):
  """
  Vector class
  Yeah
  """

  def __init__(self, coordinates):
    try:
      if not coordinates:
        raise ValueError
      self.coordinates = tuple([Decimal(x) for x in coordinates])
      self.dimension = len(coordinates)

    except ValueError:
      raise ValueError('The coordinates must be nonempty')

    except TypeError:
      raise TypeError('The coordinates must be an iterable')

  def __str__(self):
    return 'Vector: {}'.format(self.coordinates)

  def __eq__(self, v):
    return self.coordinates == v.coordinates

  @staticmethod
  def add(x, y):
    if (x.dimension != y.dimension):
        raise ValueError

    outputArr = [a + b for a, b in zip(x.coordinates, y.coordinates)]
    return Vector(outputArr)

  @staticmethod
  def sub(x, y):
    if (x.dimension != y.dimension):
        raise ValueError
    outputArr = [a - b for a, b in zip(x.coordinates, y.coordinates)]

    return Vector(outputArr)

  @staticmethod
  def mult(scalar, vector):
    outputArr = [a * Decimal(scalar) for a in vector.coordinates]

    return Vector(outputArr)

  def magnitude(self):
    magSquared = Decimal(0)
    for x in self.coordinates:
      magSquared += x * x

    return Decimal(math.sqrt(magSquared))

  def direction(self):
    magnitude = self.magnitude()
    if (magnitude == 0):
      raise Exception ("Magnitude is zero")

    return Vector.mult(Decimal(1)/magnitude, self)

  def dot(self, other):
    return sum([x * y for x, y in zip (self.coordinates, other.coordinates)])

  def angle(self, other, in_degrees=False):
    try:
      angle_in_radians = math.acos(self.direction().dot(other.direction()))
      if (in_degrees):
        return (angle_in_radians * 180. / math.pi)
      else:
        return angle_in_radians
    except Exception as e:
        if (e.message == "Magnitude is zero"):
          return 0
        raise e

  def isParallelTo(self, v):
    try:
      ratios = [round(x/y, 3) for x,y in zip(self.coordinates, v.coordinates)]

      first = ratios[0]
      for i in range(self.dimension):
        if (ratios[i] != first):
          return False

      return True
    except:
      return True

  def isOrthogonalTo(self, v):
    return round(self.dot(v), 6) == 0

  def getProjectionOnto(self, v):
    vNorm = v.direction()
    return Vector.mult(self.dot(vNorm), vNorm)

  def getOrthogonoalFrom(self, v):
    return Vector.sub(self, self.getProjectionOnto(v))

  def getCross(self, v):
    if (self.dimension != 3 or v.dimension != 3):
      raise Exception("Must have 3 dimensions")

    return Vector(
            [(self.coordinates[1] * v.coordinates[2]) - (self.coordinates[2] * v.coordinates[1]),
             (self.coordinates[2] * v.coordinates[0]) - (self.coordinates[0] * v.coordinates[2]),
             (self.coordinates[0] * v.coordinates[1]) - (self.coordinates[1] * v.coordinates[0])])

  def parallelogramArea(self, v):
    cross = self.getCross(v)
    return cross.magnitude()

  def areaOfTraingle(self, v):
    return self.parallelogramArea(v) / 2

def crossProducts():
  print Vector([8.462, 7.893, -8.187]).getCross(Vector([6.984, -5.975, 4.778]))
  print Vector([-8.987, -9.838, 5.031]).parallelogramArea(Vector([-4.268, -1.861, -8.866]))
  print Vector([1.5, 9.547, 3.691]).areaOfTraingle(Vector([-6.007, 0.124, 5.772]))

def projecteAndOrthog():
  print (Vector([3.039, 1.879]).getProjectionOnto(Vector([0.825, 2.036])))
  print (Vector([-9.88, -3.264, -8.159]).getOrthogonoalFrom(Vector([-2.155, -9.353, -9.473])))
  print (Vector([3.009, -6.172, 3.692, -2.51]).getProjectionOnto(Vector([6.404, -9.144, 2.759, 8.718])))
  print (Vector([3.009, -6.172, 3.692, -2.51]).getOrthogonoalFrom(Vector([6.404, -9.144, 2.759, 8.718])))
  #print (Vector([1,0]).getProjectionOnto(Vector([1,1])))
  #print (Vector([1,0]).getOrthogonoalFrom(Vector([1,1])))

def ParallelAndOrthogonal():
  print (Vector([-7.579, -7.88]).isParallelTo(Vector([22.737, 23.64])))
  print (Vector([-2.029, 9.97, 4.172]).isParallelTo(Vector([-9.231, -6.639, -7.245])))
  print (Vector([-2.328, -7.284, -1.214]).isParallelTo(Vector([-1.821, 1.072, -2.94])))
  print (Vector([2.118, 4.827]).isParallelTo(Vector([0,0])))
  print (Vector([-7.579, -7.88]).isOrthogonalTo(Vector([22.737, 23.64])))
  print (Vector([-2.029, 9.97, 4.172]).isOrthogonalTo(Vector([-9.231, -6.639, -7.245])))
  print (Vector([-2.328, -7.284, -1.214]).isOrthogonalTo(Vector([-1.821, 1.072, -2.94])))
  print (Vector([2.118, 4.827]).isOrthogonalTo(Vector([0,0])))
#  print (Vector([1,0]).isParallelTo(Vector([2,0])))
#  print (Vector([1,1]).isParallelTo(Vector([2,0])))
#  print (Vector([1,0]).isOrthogonalTo(Vector([2,0])))
#  print (Vector([1,1]).isOrthogonalTo(Vector([2,0])))
#  print (Vector([0,1]).isOrthogonalTo(Vector([2,0])))

def dotAndAngle():
  print (Vector([7.887, 4.138]).dot(Vector([-8.802, 6.776])))
  print (Vector([-5.955, -4.904, -1.874]).dot(Vector([-4.496, -8.755, 7.103])))

  print (Vector([3.183, -7.627]).angle(Vector([-2.668, 5.319])))
  print (Vector([7.35, 0.221, 5.188]).angle(Vector([2.751, 8.259, 3.985]), True))

def magnitudeAndDirection():
  print(Vector([-0.221, 7.437]).magnitude())
  print(Vector([8.813, -1.331, -6.247]).magnitude())
  print(Vector([5.581, -2.136]).direction())
  print(Vector([1.996, 3.108, -4.554]).direction())

def sumVectors():
  vector1 = Vector([8.218, -9.341])
  vector2 = Vector([-1.129, 2.111])

  vectorSum = Vector.add(vector1, vector2)
  print ("1: ", vectorSum.__str__())

  print ("2: ", Vector.sub(Vector([7.119, 8.215]), Vector([-8.223,0.878])).__str__())
  print ("3: ", Vector.mult(7.41, Vector([1.671, -1.012, -0.318])).__str__())

def run():
  crossProducts()

if __name__ == '__main__':
  run()
