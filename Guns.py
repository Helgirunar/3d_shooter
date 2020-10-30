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
    def toDict(self):
        return __dict__
