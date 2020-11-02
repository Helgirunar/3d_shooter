from Base3DObjects import *
from math import * # trigonometry
from Matrices import *

class Bullet():
    def __init__(self,damage, direction, pos):
#       print('New bullet on : (' + str(direction.x) + ',' + str(direction.z) + ")")
        self.damage = damage
        self.forward = Vector(direction["x"],direction["y"],direction["z"])
        self.startPos = Point(pos["x"],pos["y"],pos["z"])
        self.position = Point(pos["x"],pos["y"],pos["z"])
        self.sphere = Sphere()

    def collide(self, player):
        x = self.position.x - player.position.x
        z = self.position.z - player.position.z
        distance = math.sqrt(x*x + z*z)
        if(distance <= 0.2):
            return True
        return False
    def collide_box(self, boxes):
        for box in boxes:
            if box.pos.x-0.5-0.1<self.position.x<box.pos.x+0.5+0.1:
                if box.pos.z-0.5-0.1<self.position.z<box.pos.z+0.5+0.1:
                    if box.pos.y-box.size[2]/2-0.1<self.position.y<box.pos.y+box.size[2]/2+0.1:
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