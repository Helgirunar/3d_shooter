from Base3DObjects import *
from math import * # trigonometry
from Matrices import *
from Bullet import Bullet

class Gun():
    def __init__(self,name, rpm, dmg, pos, capacity):
        self.name = name
        self.rpm = rpm
        self.dmg = dmg
        self.magazine = capacity
        self.capacity = capacity
        self.position = pos

        self.forward = Vector(0,0,1)
        self.back = Vector(0,0,-1)
        self.right = Vector(-1,0,0)
        self.up = Vector(0,1,0)
        self.rotationY = 0
        self.rotationX = 0
        self.bullets = []
        self.reloadTimeTotal = 3
        self.reloadTimeLeft = 3
        self.delay = rpm / 1000.0
        self.beingHeld = False
        self.position_array = [-0.2, -0.2, -0.5,
                            -0.2, 0.2, -0.5,
                            0.2, 0.2, -0.5,
                            0.2, -0.2, -0.5,
                            -0.2, -0.2, 1.5,
                            -0.2, 0.2, 1.5,
                            0.2, 0.2, 1.5,
                            0.2, -0.2, 1.5,
                            -0.2, -0.2, -0.5,
                            0.2, -0.2, -0.5,
                            0.2, -0.2, 1.5,
                            -0.2, -0.2, 1.5,
                            -0.2, 0.2, -0.5,
                            0.2, 0.2, -0.5,
                            0.2, 0.2, 1.5,
                            -0.2, 0.2, 1.5,
                            -0.2, -0.2, -0.5,
                            -0.2, -0.2, 1.5,
                            -0.2, 0.2, 1.5,
                            -0.2, 0.2, -0.5,
                            0.2, -0.2, -0.5,
                            0.2, -0.2, 1.5,
                            0.2, 0.2, 1.5,
                            0.2, 0.2, -0.5,
                            -0.2,-0.2,-0.5,
                            -0.2,-0.2,-0.25,
                            -0.2,-0.7,-0.25,
                            -0.2,-0.7,-0.5,
                            0.2,-0.2,-0.5,
                            0.2,-0.2,-0.25,
                            0.2,-0.7,-0.25,
                            0.2,-0.7,-0.5,
                            -0.2,-0.2,-0.5,
                            0.2,-0.2,-0.5,
                            -0.2,-0.7,-0.5,
                            0.2,-0.7,-0.5,
                            -0.2,-0.2,-0.25,
                            0.2,-0.2,-0.25,
                            -0.2,-0.7,-0.25,
                            0.2,-0.7,-0.25,
                            -0.2,-0.7,-0.25,
                            0.2,-0.7,-0.25,
                            -0.2,-0.7,-0.5,
                            0.2,-0.7,-0.5,
                            -0.2,-0.2, 0.15,
                            0.2,-0.2, 0.15,
                            -0.2,-0.55, 0.15,
                            0.2,-0.55, 0.15,
                            -0.2,-0.2, 0.30,
                            0.2,-0.2, 0.30,
                            -0.2,-0.55, 0.30,
                            0.2,-0.55, 0.30,
                            0.2,-0.2, 0.15,
                            0.2,-0.55, 0.15,
                            0.2,-0.55, 0.30,
                            0.2,-0.2, 0.30,
                            -0.2,-0.2, 0.15,
                            -0.2,-0.55, 0.15,
                            -0.2,-0.55, 0.30,
                            -0.2,-0.2, 0.30,
                            -.2,-0.55, 0.15,
                            0.2,-0.55, 0.15,
                            -.2,-0.55, 0.30,
                            0.2,-0.55, 0.30,]
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
                            1.0, 0.0, 0.0,
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
                            1.0, 0.0, 0.0,
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

    def shoot(self):
        if(self.magazine != 0):
            self.bullets.append(Bullet(self.dmg,self.forward, self.position))
            self.magazine = self.magazine-1

    def aiming(self, looking, position):
        self.position = position
    def reload(self, player, delta_time):
        self.reloadTimeLeft -= delta_time
        if(self.reloadTimeLeft <= 0):
            self.reloadTimeLeft = self.reloadTimeTotal
            self.magazine = self.capacity
            player.reloading = False
        pass

    def __str__(self):
        Dict = {
            "name": self.name,
            "rpm": self.rpm,
            "damage": self.dmg
        }
        return str(Dict)
    def toStr(self):
        Dict = {
            "name": self.name,
            "rpm": self.rpm,
            "damage": self.dmg
        }
        return str(Dict)

    def collide(self, player):# Collision check
        x = self.position.x - player.position.x
        z = self.position.z - player.position.z
        distance = math.sqrt(x*x + z*z)
        if(distance <= 0.15):
            player.pickUp(self)
            self.beingHeld = True
            return True
        return False

    def set_vertices(self, shader):        
        shader.set_position_attribute(self.position_array)
        shader.set_normal_attribute(self.normal_array)
        shader.set_uv_attribute(self.uv_array)

    def setOrientation(self, pos, forward, right, back, up):# Sets the orientation of the gun. This handles the pitch, yaw and positioning of the gun.
        self.position = pos
        self.forward = forward
        self.right = right
        self.back = back
        self.up = up

    def draw(self, shader):
        glDrawArrays(GL_TRIANGLE_FAN, 0, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 4, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 8, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 12, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 16, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 20, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 24, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 28, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 32, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 36, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 40, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 44, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 48, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 52, 4)

    def toDict(self):
        return self.__dict__