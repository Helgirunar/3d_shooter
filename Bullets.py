from Base3DObjects import *
from math import * # trigonometry
from Matrices import *
from Bullet import Bullet

class Bullets():
    def __init__(self):
        self.bullets = []

    def move(self, delta_time):
        self.position += self.forward * delta_time * 25

    def appendBullet(self, bullet):
        self.bullets.append(Bullet(bullet["dmg"],bullet["forward"],bullet["position"]))


    def updateBullets(self, delta_time, enemyTeam, server):
        tmpBullets = []
        for y in self.bullets:
            y.move(delta_time)
            for i in enemyTeam:
                if(y.collideDict(i)):
                    server.Send({"action": "tookDamage", "player": i, "dmg": y.damage})
            if(y.position.z >= 0 or y.position.y >= 10 or y.position.x >= 0 or y.position.z <= -30 or y.position.y <= -1 or y.position.x <= -30):
                pass
            else:
                tmpBullets.append(y)
            self.bullets = tmpBullets

