from Base3DObjects import *
from math import * # trigonometry
from Gun import Gun
import pygame

class Player():
    def __init__(self,start, name, team):
        self.name = name
        self.position = start
        self.team = team
        self.forward = Vector(0,0,1)
        self.back = Vector(0,0,-1)
        self.right = Vector(-1,0,0)
        self.up = Vector(0,1,0)
        self.looking = Vector(0,0,1)
        self.gunPos = self.position + Vector(0,-0.10,0) + self.forward * 0.2 + self.right * 0.1
        self.guns = []
        self.emptyGun = Gun('template',1, 1, Point(0,0,0), 0)
        self.selected = self.emptyGun
        self.holstered = self.emptyGun
        self.shooting = False
        self.dead = False
        self.deaths = 0
        self.health = 100
        self.respawnTimer = 5
        self.haveGun = False
        self.lastFired = 0
        self.reloading = False


    def slide(self, del_right, del_up, del_back):# Movement
        self.position += self.right * del_right + self.up * del_up + self.back * del_back
        self.gunPos = self.position + Vector(0,-0.10,0) + self.forward * 0.2 + self.right * 0.1
        self.selected.position = self.gunPos
        if(self.haveGun):
            self.selected.position = self.gunPos

    def fall(self, speed):# Gravity? If jump is implemented, so he gets pulled back down.
        if(self.position.y > 0.5):
            self.position.y += -1 * speed

    def collide(self, box):# Collide 
        if box != None:
            x = self.position.x - box.x
            z = self.position.z - box.z
            distance = math.sqrt(x*x + z*z)
            if(distance <= 0.64):
                return True
            return False
        else:
            return False

    def pickUp(self, gun):# Picks up a gun
        self.haveGun = True
        if(len(self.guns) == 0):
            self.selected = gun
            gun.setOrientation(self.gunPos, self.forward, self.right, self.back, self.up)
        else:
            gun.position = Point(0,0,0)
        self.guns.append(gun)

    def drop(self):# Drops guns.
        if(self.selected in self.guns):
            self.guns.remove(self.selected)
            self.selected.beingHeld = False
            self.selected.position = Point(self.gunPos.x, 0.2, self.gunPos.z)
            if(len(self.guns) == 1):
                self.selected = self.holstered
                self.selected.setOrientation(self.gunPos, self.looking, self.right, self.back, self.up)
                self.holstered = self.emptyGun
            else:
                self.selected = self.emptyGun

    def changeGun(self, nr):# If the player is trying to swap between his primary and secondary gun.
        if(nr == 1 and len(self.guns) > 0):
            self.selected = self.guns[0]
            self.selected.setOrientation(self.gunPos, self.looking, self.right, self.back, self.up)
            if(len(self.guns) == 2):
                self.holstered = self.guns[1]
                self.holstered.position = Point(0,0,0)
        elif(len(self.guns) > 1):
            self.selected = self.guns[1]
            self.selected.setOrientation(self.gunPos, self.looking, self.right, self.back, self.up)
            self.holstered = self.guns[0]
            self.holstered.position = Point(0,0,0)
    
    def updatePlayer(self, delta_time):# Update function for the player
        self.lastFired -= delta_time * 5
        if(self.shooting and self.lastFired <= 0 and self.reloading == False):
            self.lastFired = self.selected.delay
            self.selected.shoot()
        elif(self.reloading):
            player = self
            self.selected.reload(player, delta_time)
        
    def takeDamage(self, dmg):# Deals damage, only if the player is still alive.
        if(self.health > 0):
            self.health -= dmg
        if(self.health <= 0 and self.dead != True):
            print('I am dead')
            self.deaths += 1
            self.dead = True
            self.position.y = 0

    def yaw(self, angle):# Moves the player Horizontally
        c = cos(angle)
        s = sin(angle)
        tmp_back = self.back * c + self.right * s
        self.right = self.back * -s + self.right * c
        self.back = tmp_back
        self.forward = tmp_back * -1
        self.looking = Vector(self.forward.x, self.looking.y, self.forward.z)
        self.gunPos = self.position + Vector(0,-0.10,0) + self.forward * 0.2 + self.right * 0.1
        self.selected.setOrientation(self.gunPos, self.looking, self.right, self.back, self.up)

    def pitch(self, angle):# Moves the player Vertically
        c = cos(angle)
        s = sin(angle)
        self.looking = self.up * s + self.looking * c
        self.gunPos = self.position + Vector(0,-0.10,0) + self.forward * 0.2 + self.right * 0.1
        self.selected.setOrientation(self.gunPos, self.looking, self.right, self.back, self.up)

    def toDict(self):# Creates a dict from the usefull information that the server might need.
        tempSelf = {
            "name": self.name,
            "position": self.position.toDict(),
            "health": self.health,
            "team": self.team
        }
        return tempSelf