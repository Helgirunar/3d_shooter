from Base3DObjects import *
from math import * # trigonometry
from Matrices import *
from Gun import Gun

class Guns():
    def __init__(self):
        self.guns = []

    def addGun(self, gun):
        self.guns.append(gun)

    def __str__(self):
        Dict = {
            "guns": []
        }
        for x in self.guns:
            Dict["guns"].append(
                x.toStr()                
            )
        return str(Dict)


    def updateGuns(self, delta_time, enemyTeam, server):
        for x in self.guns:
            for y in x.bullets:
                y.move(delta_time)
        for x in self.guns:
            tmpBullets = []
            for y in x.bullets:
                for i in enemyTeam:
                    if(y.collideDict(i)):
                        #If any of the bullets collide with any of the enemy team, it sends to the server that we hit a player.
                        server.Send({"action": "tookDamage", "player": i, "dmg": y.damage})
                if(y.position.z >= 0 or y.position.y >= 10 or y.position.x >= 0 or y.position.z <= -30 or y.position.y <= -1 or y.position.x <= -30):
                    pass
                else:
                    tmpBullets.append(y)
                x.bullets = tmpBullets