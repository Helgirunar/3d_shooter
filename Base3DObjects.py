
import random
import numpy
from random import *

from OpenGL.GL import *
from OpenGL.GLU import *

import math
from math import *


class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)
    def __str__(self):
        return str(self.__dict__)

    def toDict(self):
        return self.__dict__

class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def __len__(self):
        return sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def __str__(self):
        return str(self.__dict__)
    
    def normalize(self):
        length = self.__len__()
        self.x /= length
        self.y /= length
        self.z /= length


    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        return Vector(self.y*other.z - self.z*other.y, self.z*other.x - self.x*other.z, self.x*other.y - self.y*other.x)

class Cube:
    def __init__(self):
        self.point = (0,0,0)
        self.position_array = [-0.5, -0.5, -0.5,
                            -0.5, 0.5, -0.5,
                            0.5, 0.5, -0.5,
                            0.5, -0.5, -0.5,
                            -0.5, -0.5, 0.5,
                            -0.5, 0.5, 0.5,
                            0.5, 0.5, 0.5,
                            0.5, -0.5, 0.5,
                            -0.5, -0.5, -0.5,
                            0.5, -0.5, -0.5,
                            0.5, -0.5, 0.5,
                            -0.5, -0.5, 0.5,
                            -0.5, 0.5, -0.5,
                            0.5, 0.5, -0.5,
                            0.5, 0.5, 0.5,
                            -0.5, 0.5, 0.5,
                            -0.5, -0.5, -0.5,
                            -0.5, -0.5, 0.5,
                            -0.5, 0.5, 0.5,
                            -0.5, 0.5, -0.5,
                            0.5, -0.5, -0.5,
                            0.5, -0.5, 0.5,
                            0.5, 0.5, 0.5,
                            0.5, 0.5, -0.5]
        self.normal_array = [0.0, 0.0, -1.0,
                            0.0, 0.0, -1.0,
                            0.0, 0.0, -1.0,
                            0.0, 0.0, -1.0,
                            0.0, 0.0, 1.0,
                            0.0, 0.0, 1.0,
                            0.0, 0.0, 1.0,
                            0.0, 0.0, 1.0,
                            0.0, -1.0, 0.0,
                            0.0, -1.0, 0.0,
                            0.0, -1.0, 0.0,
                            0.0, -1.0, 0.0,
                            0.0, 1.0, 0.0,
                            0.0, 1.0, 0.0,
                            0.0, 1.0, 0.0,
                            0.0, 1.0, 0.0,
                            -1.0, 0.0, 0.0,
                            -1.0, 0.0, 0.0,
                            -1.0, 0.0, 0.0,
                            -1.0, 0.0, 0.0,
                            1.0, 0.0, 0.0,
                            1.0, 0.0, 0.0,
                            1.0, 0.0, 0.0,
                            1.0, 0.0, 0.0]
        self.uv_array =    [0.0, 0.0,
                            0.0, 1.0,
                            1.0, 1.0,
                            1.0, 0.0,
                            0.0, 0.0,
                            0.0, 1.0,
                            1.0, 1.0,
                            1.0, 0.0,
                            0.0, 0.0,
                            0.0, 1.0,
                            1.0, 1.0,
                            1.0, 0.0,
                            0.0, 0.0,
                            0.0, 1.0,
                            1.0, 1.0,
                            1.0, 0.0,
                            0.0, 0.0,
                            0.0, 1.0,
                            1.0, 1.0,
                            1.0, 0.0,
                            0.0, 0.0,
                            0.0, 1.0,
                            1.0, 1.0,
                            1.0, 0.0]

    def set_vertices(self, shader):        
        shader.set_position_attribute(self.position_array)
        shader.set_normal_attribute(self.normal_array)
        shader.set_uv_attribute(self.uv_array)

    def setPos(self, point):
        self.point = point

    def draw(self):
        for i in range(6):
            glDrawArrays(GL_TRIANGLE_FAN, 4*i, 4)

class Sphere:
    def __init__(self, stacks=12, slices =24):
        vertex_array = []
        self.slices= slices
        stack_interval = pi/stacks
        slice_interval = 2*pi/slices
        self.vertex_count = 0

        for stack_count in range(stacks):
            stack_angle = stack_count*stack_interval
            for slice_count in range(slices +1):
                slice_angle = slice_count*slice_interval
                for _ in range(2):
                    vertex_array.append(sin(stack_angle)*cos(slice_angle))
                    vertex_array.append(cos(stack_angle))
                    vertex_array.append(sin(stack_angle)*sin(slice_angle))
                for _ in range(2):
                    vertex_array.append(sin(stack_angle+stack_interval)*cos(slice_angle))
                    vertex_array.append(cos(stack_angle+stack_interval))
                    vertex_array.append(sin(stack_angle+stack_interval)*sin(slice_angle))

                self.vertex_count+= 2
        
        self.vertex_buffer_id = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer_id)
        glBufferData(GL_ARRAY_BUFFER, numpy.array(vertex_array, dtype='float32'), GL_STATIC_DRAW)
        
        vertex_array= None 

    
    def set_vertices(self, shader):
        shader.set_attribute_buffers(self.vertex_buffer_id)

    def draw(self):
        for i in range (0, self.vertex_count, (self.slices +1)*2):
            glDrawArrays(GL_TRIANGLE_STRIP, i, (self.slices +1)*2)
        glBindBuffer(GL_ARRAY_BUFFER, 0)