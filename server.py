import PodSixNet, time
from time import sleep
from PodSixNet.Channel import Channel
from PodSixNet.Server import Server
players = []
damage = []
class ClientChannel(Channel):

    def Network(self, data):
        pass
    def Network_addPlayer(self, data):# Adds player
        print(data["player"]["name"] + " has joined the server")
        players.append(data["player"])
    def Network_updatePlayer(self, data):# Updates player position
        for x, item in enumerate(players):
            if(data["player"]["name"] == item["name"]):
                players[x] = data["player"]
    def Network_playerLeave(self, data):# Removes player
        for x, item in enumerate(players):
            if(data["player"]["name"] == item["name"]):
                print(data["player"]["name"] + " has left the server")
                players.remove(data["player"])
                return
    def Network_tookDamage(self, data):# Inserts damage to the damage list.
        damage.append(data)

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
        print(newConnection)

    def updatePlayers(self):# Sends all clients information about all players positions, and damage taken. 
        global damage
        packet = {
            "action": "updatePlayer",
            "players": players,
            "damage": damage
        }
        for x in self.connections:
            x["channel"].Send(packet)
        #After we send the damage, we want to clear the list so we don't deal the same damage twice.
        damage = []

# use the localaddr keyword to tell the server to listen on port 1337
myserver = MyServer(localaddr=("0.0.0.0", 1337))

while True:
    myserver.Pump()
    if(len(players) > 0):# Only update clients with the server information if somebody is connected.
        myserver.updatePlayers()
    sleep(0.01)