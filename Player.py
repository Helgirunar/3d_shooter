from Base3DObjects import *
from math import * # trigonometry
from Gun import Gun
import random as rand
import pygame

class Player():
    def __init__(self,start, name, team, spawns):
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
        self.spawns = spawns
        self.emptyGun = Gun('template',1, 1, Point(0,0,0), 0, False, 0)
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

    def slide(self, del_right, del_up, del_back,server):# Movement
        self.position += self.right * del_right + self.up * del_up + self.back * del_back
        self.gunPos = self.position + Vector(0,-0.10,0) + self.forward * 0.2 + self.right * 0.1
        self.selected.position = self.gunPos
        if(self.selected.beingHeld):
            server.Send({"action": "updateGun","newPos": self.selected.position.toDict(), "beingHeld": self.selected.beingHeld, "id": self.selected.id, "forward": self.forward.toDict()})
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

    def pickUp(self, gun, server):# Picks up a gun
        self.haveGun = True
        if(gun.beingHeld == False and gun.id != self.selected.id):
            if(len(self.guns) == 0):
                self.selected = gun
                gun.setOrientation(self.gunPos, self.forward, self.right, self.back, self.up)
                server.Send({"action": "updateGun","newPos": gun.position.toDict(), "beingHeld": True, "id": self.selected.id, "forward": self.forward.toDict()})
            else:
                gun.position = Point(0,0,0)
                self.holstered = gun
                server.Send({"action": "updateGun","newPos": gun.position.toDict(), "beingHeld": True, "id": self.holstered.id, "forward": self.forward.toDict()})
            self.guns.append(gun)
    def drop(self, server):
        if(self.selected.name != "template"):
            tmpGun = self.selected
            tmpGun.setOrientation(Point(self.gunPos.x, 0.2, self.gunPos.z), self.forward, self.right, self.back, self.up)
            self.selected = self.emptyGun
            self.guns.remove(tmpGun)
            server.Send({"action": "updateGun","newPos": Point(self.gunPos.x, 0.2, self.gunPos.z).toDict(), "beingHeld": False, "id": tmpGun.id, "forward": self.forward.toDict()})
            if(self.holstered.name != "template"):
                self.selected = self.holstered
                server.Send({"action": "updateGun","newPos": self.selected.position.toDict(), "beingHeld": True, "id": self.selected.id, "forward": self.forward.toDict()})
                self.holstered = self.emptyGun

    def changeGun(self, nr, server):# If the player is trying to swap between his primary and secondary gun.
        if(nr == 1 and len(self.guns) > 0):
            self.selected = self.guns[0]
            self.selected.setOrientation(self.gunPos, self.looking, self.right, self.back, self.up)
            server.Send({"action": "updateGun","newPos": self.selected.position.toDict(), "beingHeld": True, "id": self.selected.id, "forward": self.forward.toDict()})
            if(len(self.guns) == 2):
                self.holstered = self.guns[1]
                self.holstered.position = Point(0,0,0)
                server.Send({"action": "updateGun","newPos": self.holstered.position.toDict(), "beingHeld": True, "id": self.holstered.id, "forward": self.forward.toDict()})
        elif(len(self.guns) == 2):
            self.selected = self.guns[1]
            self.selected.setOrientation(self.gunPos, self.looking, self.right, self.back, self.up)
            server.Send({"action": "updateGun","newPos": self.selected.position.toDict(), "beingHeld": True, "id": self.selected.id, "forward": self.forward.toDict()})
            self.holstered = self.guns[0]
            self.holstered.position = Point(0,0,0)
            server.Send({"action": "updateGun","newPos": self.holstered.position.toDict(), "beingHeld": True, "id": self.holstered.id, "forward": self.forward.toDict()})
    
    def updatePlayer(self, delta_time,server):# Update function for the player
        self.lastFired -= delta_time * 5
        if(self.shooting and self.lastFired <= 0 and self.reloading == False):
            self.lastFired = self.selected.delay
            self.selected.shoot(server)
        elif(self.reloading):
            player = self
            self.selected.reload(player, delta_time)

    def death(self, server):
        for x in self.guns:
            dropTo = Point(self.gunPos.x, 0.2, self.gunPos.z).toDict()
            server.Send({"action": "updateGun","newPos": dropTo, "beingHeld": False, "id": x.id, "forward": self.forward.toDict()})
        self.selected = self.emptyGun
        self.holstered = self.emptyGun
        self.guns = []
        self.position = self.spawns[rand.randint(0,4)]
        self.health = 100
        self.dead = False

    def takeDamage(self, dmg, server):# Deals damage, only if the player is still alive.
        if(self.health > 0):
            self.health -= dmg
        if(self.health <= 0 and self.dead != True):
            self.death(server)
            self.deaths += 1
            self.dead = True
            self.position.y = 0

    def yaw(self, angle,server):# Moves the player Horizontally
        c = cos(angle)
        s = sin(angle)
        tmp_back = self.back * c + self.right * s
        self.right = self.back * -s + self.right * c
        self.back = tmp_back
        self.forward = tmp_back * -1
        self.looking = Vector(self.forward.x, self.looking.y, self.forward.z)
        self.gunPos = self.position + Vector(0,-0.10,0) + self.forward * 0.2 + self.right * 0.1
        self.selected.setOrientation(self.gunPos, self.looking, self.right, self.back, self.up)
        server.Send({"action": "updateGun","newPos": self.selected.position.toDict(), "beingHeld": self.selected.beingHeld, "id": self.selected.id, "forward": self.forward.toDict()})

    def pitch(self, angle, server):# Moves the player Vertically
        c = cos(angle)
        s = sin(angle)
        self.looking = self.up * s + self.looking * c
        self.gunPos = self.position + Vector(0,-0.10,0) + self.forward * 0.2 + self.right * 0.1
        self.selected.setOrientation(self.gunPos, self.looking, self.right, self.back, self.up)
        server.Send({"action": "updateGun","newPos": self.selected.position.toDict(), "beingHeld": self.selected.beingHeld, "id": self.selected.id, "forward": self.forward.toDict()})

    def toDict(self):# Creates a dict with useful information that the server needs.
        return {
            "name": self.name,
            "position": self.position.toDict(),
            "health": self.health,
            "team": self.team
        }