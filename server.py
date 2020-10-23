import PodSixNet, time
from time import sleep
from PodSixNet.Channel import Channel
from PodSixNet.Server import Server
from Base3DObjects import *

players = []
playerLeft = False
whoLeft = None
damage = []
length = 30
width = 30
gunsPos = []
#       Create guns for red side
for x in range(0,10):
    gunsPos.append({"Point": Point(-length + 3,0.2,-width + 2 * x).toDict(), "beingHeld": False, "id": 1+2*x})
    gunsPos.append({"Point": Point(-3,0.2,-width + 4 * x).toDict(), "beingHeld": False, "id": 2+ 2*x})
    
class ClientChannel(Channel):

    def Network(self, data):
        pass
    def Network_addPlayer(self, data):# Adds player
        global newPlayer
        print(data["player"]["name"] + " has joined the server")
        tmpPlayer = {
            "id": len(players),
            "player": data["player"]
        }
        players.append(tmpPlayer)
        newPlayer = True
    def Network_updatePlayer(self, data):# Updates player position
        for x, item in enumerate(players):
            if(data["player"]["name"] == item["player"]["name"]):
                players[x] = {
                    "player":data["player"],
                    "id": item["id"]
                }
    def Network_playerLeave(self, data):# Removes player
        global whoLeft, playerLeft
        for x, item in enumerate(players):
            if(data["player"]["name"] == item["player"]["name"]):
                print(data["player"]["name"] + " has left the server")
                players.remove({
                    "id": item["id"],
                    "player": data["player"]})
        playerLeft = True
        whoLeft = data["player"]

    def Network_tookDamage(self, data):# Inserts damage to the damage list.
        damage.append(data)
    def Network_updateGun(self, data):
        for x,item in enumerate(gunsPos):
            if(item["id"] == data["id"]):
                gunsPos.remove(item)
                new = {
                    "Point": data["newPos"],
                    "beingHeld": data["beingHeld"],
                    "id": data["id"]
                }
                gunsPos.append(new)
    def Network_dropGun(self, data):
        for x,item in enumerate(gunsPos):
            if(item["id"] == data["id"]):
                gunsPos.remove(item)
                new = {
                    "Point": data["newPos"],
                    "beingHeld": data["beingHeld"],
                    "id": data["id"]
                }
                gunsPos.append(new)

class MyServer(Server):
    channelClass = ClientChannel
    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)
        self.connections = []

    def Connected(self, channel, addr):# This happens when we connect.
        newConnection = {
            "id": len(players),
            "channel": channel            
        }
        self.connections.append(newConnection)
        channel.Send({"action": "spawnGuns", "position": gunsPos})
        print(newConnection)

    def updatePlayers(self):# Sends all clients information about all players positions, and damage taken. 
        global damage
        global newPlayer
        packet = {
            "action": "updatePlayer",
            "players": players,
            "damage": damage,
            "gunsPos": gunsPos
        }
        for x in self.connections:
            x["channel"].Send(packet)
            
        #After we send the damage, we want to clear the list so we don't deal the same damage twice.
        damage = []

    def notifyLeave(self):
        global playerLeft
        global whoLeft
        packet = {
            "action": "notifyLeave",
            "player": whoLeft
        }
        for x in self.connections:
            x["channel"].Send(packet)
        playerLeft = False
        whoLeft = None

# use the localaddr keyword to tell the server to listen on port 1337
# try:
address=input("Host:Port (localhost:1337): ")
if not address:
    host, port="localhost", 1337
else:
    host,port=address.split(":")
myserver = MyServer(localaddr=(host, int(port)))

while True:
    myserver.Pump()
    if(playerLeft):
        myserver.notifyLeave()
    if(len(players) > 0):# Only update clients with the server information if somebody is connected.
        myserver.updatePlayers()
    sleep(0.01)