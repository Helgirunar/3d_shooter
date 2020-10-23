from Base3DObjects import *
from math import * # trigonometry
from Matrices import *

class Bullet():
    def __init__(self,damage, direction, pos):
#       print('New bullet on : (' + str(direction.x) + ',' + str(direction.z) + ")")
        self.damage = damage
        self.forward = direction
        self.startPos = Point(pos.x,pos.y,pos.z)
        self.position = pos
        self.sphere = Sphere()

    def collide(self, player):
        x = self.position.x - player.position.x
        z = self.position.z - player.position.z
        distance = math.sqrt(x*x + z*z)
        if(distance <= 0.2):
            return True
        return False
    def collideDict(self, player):
        x = self.position.x - player["player"]["position"]["x"]
        z = self.position.z - player["player"]["position"]["z"]
        distance = math.sqrt(x*x + z*z)
        if(distance <= 0.2):
            return True
        return False
    
    def move(self, delta_time):
        self.position += self.forward * delta_time * 25