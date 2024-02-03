import math 
import numpy as np
import pygame

class Vector:
    """
    A class representing a vector in 2 dimensions.

    Attributes:
        x : float or int
        y : float or int

    Methods:
        __init__(self, x, y, z)
        __str__(self)
        Operator +
        Operator *
        abs(self)
    """

    def __init__(self, x, y):
        """
        Initialize a new instance of vector
        """
        self.x = x
        self.y = y

    def __str__(self):
        """
        return a string for the class vector as "Vector(x,y,z)"
        """
        return f"Vector({self.x}, {self.y})"

    def __add__(self,other):
        """
        Overload the + Operator for the class Vector
        Implements the summation of two instances of class Vector
        """
        return Vector(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        if isinstance(other, self.__class__):
            return Vector(self.x - other.x, self.y - other.y)
        return Vector(self.x - other, self.y - other)
    
    def __str__(self):
        """
        return a string for the class vector as "Vector(x,y,z)"
        """
        return f"Vector({self.x}, {self.y})"

    def __mul__(self,other):
        """ 
        Overload the * Operator for the class Vector including
        Type-based dispatch:
            - multiplication of two instances of class Vector:
              returns a float/int,  the scalar product
            - multiplication of an instance of class Vector and a scalar (float or int):
              returns a Vector, each component of the Vector is multiplied with the value
        """
        if isinstance(other, Vector):
            return self.mul_vector(other)
        if isinstance(other, float):
            return self.mul_scalar(other)
        if isinstance(other, int):
            return self.mul_scalar(other)
        
    def mul_vector(self, other):
        return float(self.x*other.x + self.y*other.y)

    def mul_scalar(self, other):
        return Vector(self.x*other, self.y*other)
    
    def __mul__(self, other):
        if isinstance(other, self.__class__):
            return Vector(self.x * other.x, self.y * other.y)
        return Vector(self.x * other, self.y * other)
    
    def __truediv__(self, scalar):
        return Vector(self.x / scalar, self.y / scalar)

    def abs(self):
        """
        Return the absolute value of the Vector instance.
        """
        return float(np.sqrt((self.x*self.x + self.y*self.y)))
    
    def rotate(self, angle):
        """
        Returns:
            rotatted vector, angle in degrees
        """
        angle_radians = math.radians(angle)
        new_x = self.x * math.cos(angle_radians) - self.y * math.sin(angle_radians)
        new_y = self.x * math.sin(angle_radians) + self.y * math.cos(angle_radians)
        return Vector(new_x, new_y)
    
    def int_tuple(self):
        return int(self.x), int(self.y)
    
    def cross(self, other):
        return self.x * other.y - self.y * other.x
    
    def dot(self, other):
        return self.x * other.x + self.y * other.y
    
    def length(self):
        return math.sqrt(self.x**2 + self.y**2)

    def normalize(self):
        length = self.abs()
        if length != 0:
            self.x /= length
            self.y /= length
        return Vector(self.x, self.y)
    