# from OpenGL.GL import *
# from OpenGL.GLU import *
from math import *

import pygame
from pygame.locals import *
import PodSixNet
from PodSixNet.Connection import ConnectionListener, connection
from time import sleep

import sys
import time
import random as rand
from Shaders import Shader3D
from Matrices import *
from Player import Player
from Guns import Guns
from Gun import Gun
from Texture import Texture
from Box import Box
from Bullets import Bullets

from load_models import load_obj_file

class GraphicsProgram3D(ConnectionListener):
    def __init__(self, team_name= "red", player_name= "Player1"):
        pygame.init() 
        self.screen = pygame.display.set_mode((800,600), pygame.OPENGL|pygame.DOUBLEBUF)
#       Length and width of the playing field.
        self.length = 30
        self.width = 30

#       Shader
        self.shader = Shader3D()
        self.shader.use()

#       Inputs from player, pick a team from red or blue, then set your name.
        self.pickedTeam = team_name
        self.playerName = player_name
        # Set caption
        pygame.display.set_caption("Some weird gun game? \t({})".format(self.playerName))


#       Player Height
        self.playerHeight = 0.75

#       load player model
        self.bluePlayer = load_obj_file(sys.path[0] + "/models", "player_blue.obj")
        self.redPlayer = load_obj_file(sys.path[0] + "/models", "player_red.obj")
#       Random Spawns for each team. On each side of the playing field.
        self.teamRedSpawns =[Point(-self.length + 3,self.playerHeight,-self.width + 2),
                             Point(-self.length + 3,self.playerHeight,-self.width + 6),
                             Point(-self.length + 3,self.playerHeight,-self.width + 10),
                             Point(-self.length + 3,self.playerHeight,-self.width + 14),
                             Point(-self.length + 3,self.playerHeight,-self.width + 18)]
        self.teamBlueSpawns =[Point(-3,self.playerHeight,-self.width + 2),
                              Point(-3,self.playerHeight,-self.width + 6),
                              Point(-3,self.playerHeight,-self.width + 10),
                              Point(-3,self.playerHeight,-self.width + 14),
                              Point(-3,self.playerHeight,-self.width + 18)]

#       Places you in either team and  gives you a randomized spawn.
        self.blueTeam = []
        self.redTeam = []
        if(self.pickedTeam == "red"):
            self.PlayerStartPos = self.teamRedSpawns[rand.randint(0,4)]
#          This is my player, it takes parameters (poisition, name, team, teamSpawns)
            self.player = Player(self.PlayerStartPos, self.playerName, self.pickedTeam, self.teamRedSpawns)
        else:
            self.PlayerStartPos = self.teamBlueSpawns[rand.randint(0,4)]            
#           This is my player, it takes parameters (poisition, name, team, teamSpawns)
            self.player = Player(self.PlayerStartPos, self.playerName, self.pickedTeam, self.teamBlueSpawns)


#       extra            
        self.model_matrix = ModelMatrix()
        self.globalSpeed = 5
        self.globalSpeedSide = 4
        self.view_matrix = ViewMatrix()
        self.view_matrix_top = ViewMatrix()
        self.displayCenter = [300, 400]#[self.screen.get_size()[i] // 2 for i in range(2)]
        self.projection_matrix = ProjectionMatrix()
        self.fov = pi / 4
        self.projection_matrix.set_perspective(self.fov, 800/600, 0.5, 1000)
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())
        self.cube = Cube()
        self.sphere = Sphere()
        self.clock = pygame.time.Clock()
        self.clock.tick(60)
        self.guns = Guns()
        self.boxes= list()
        self.bullets = Bullets()
#       For movement        
        self.angle = 0
        self.angleY = 0
        self.angleX = 0
        self.angleXRotate = 0
        self.angleYRotate = 0
        self.angleYRotateOld = 0
        self.mouseMove = [0,0]

        self.UP_key_down = False
        self.W_key_down = False
        self.A_key_down = False
        self.D_key_down = False
        self.S_key_down = False
        self.running = False
        self.crouching = False
        self.infocus = True
        self.time = 1
        pygame.mouse.set_pos(self.displayCenter)
        pygame.mouse.set_visible(not self.infocus)

#       Load in the textures we want. Maybe we might want to have it a list incase it gets too big.
        self.texture_id01 = Texture("dirt")
        self.texture_id03 = Texture("gunColor")
        self.texture_id02 = Texture("wood")

#       Connect to the server
        self.Connect(('127.0.0.1', 1337))        

#       Adding the player to the server's player list.
        self.Send({"action": "addPlayer", "player": self.player.toDict()})

    def Network_spawnGuns(self, data):
        print('spawning guns')
        for x,item in enumerate(data["position"]):
            if x % 2:
                self.guns.addGun(Gun("AK-47", 600, 32,Point(item["Point"]["x"],item["Point"]["y"],item["Point"]["z"]),30, item["beingHeld"], item["id"]))
            else:
                self.guns.addGun(Gun("M4-A1", 700, 27,Point(item["Point"]["x"],item["Point"]["y"],item["Point"]["z"]),30, item["beingHeld"], item["id"]))
    
    def Network_spawnBoxes(self, data):
        print('spawning boxes')
        for _,item in enumerate(data["position"]):
            if item["Point"]["z"] % 2:
                self.boxes.append(Box((1,1,1),Point(item["Point"]["x"],0.5,item["Point"]["z"])))
            else:
                self.boxes.append(Box((1,0.5,1),Point(item["Point"]["x"],0.25,item["Point"]["z"])))


    def Network_removeGun(self, data):
        for x, item in enumerate(self.guns.guns):
            if item.position.x == data["gun"]["x"] and item.position.z == data["gun"]["z"]:
                self.guns.guns.remove(item)
    def Network_notifyLeave(self, data):
        print(data)
        if(data["player"]["team"] == "red"):
            for x, item in enumerate(self.redTeam):
                print(item)
                if item["player"]["name"] == data["player"]["name"]:
                    self.redTeam.remove(item)  
        elif(data["player"]["team"] == "blue"):
            for x, item in enumerate(self.blueTeam):
                print(item)
                if item["player"]["name"] == data["player"]["name"]:
                    self.blueTeam.remove(item)
            

#   This is the function that receives the data from the server.
    def Network_updatePlayer(self, data):
        for x in data["players"]:
            if x["player"]["name"] == self.player.name:
                #Do nothing so I don't render myself. You have to have a unique name.
                pass
            else:
                if(x["player"]["team"] == "red"):
                    tempfound = False
                    for idx, item in enumerate(self.redTeam):
                        if x["player"]["name"] == item["player"]["name"]:
                            self.redTeam[idx] = x
                            tempfound = True
                    if(not tempfound):
                        self.redTeam.append(x)
                elif(x["player"]["team"] == "blue"):
                    tempfound = False
                    for idx, item in enumerate(self.blueTeam):
                        if x["player"]["name"] == item["player"]["name"]:
                            self.blueTeam[idx] = x
                            tempfound = True
                    if(not tempfound):
                        self.blueTeam.append(x)
        for x in data["damage"]:
            if x["player"]["player"]["name"] == self.player.name:
                self.player.takeDamage(x["dmg"], self)
        for x,item in enumerate(data["gunsPos"]):
            for y in self.guns.guns:
                #Only update if the position has changed or if he has pickedup or dropped a gun
                if item["id"] == y.id and item["Point"]["x"] != y.position.x and item["Point"]["z"] != y.position.z or item["id"] == y.id and item["beingHeld"] != y.beingHeld:
                    y.update(Point(item["Point"]["x"],item["Point"]["y"],item["Point"]["z"]), item["beingHeld"], item["angle"])

        for x in data["bulletsPos"]:
            self.bullets.appendBullet(x)
    def update(self):
        connection.Pump()
        self.Pump()
#       Updates the player position.
        self.Send({"action": "updatePlayer", "player": self.player.toDict()})

        delta_time = self.clock.tick() / 1000.0
#       For testing purpose, so we can run 2 clients on the same computer.
        if self.infocus:
            pygame.mouse.set_pos(self.displayCenter)
        self.angle += delta_time/3
#       For picking up guns.
        for x in self.guns.guns:
            if(x.beingHeld != True):
                x.collide(self.player, self)

#       Get the rotation from the mouse
        self.angleY = -math.atan(self.mouseMove[0]) * delta_time * 1.5
        self.angleYRotate += -math.atan(self.mouseMove[0]) * delta_time * 1.5
        self.angleX = -math.atan(self.mouseMove[1]) * delta_time * 1.5
        self.angleXRotate += -math.atan(self.mouseMove[1]) * delta_time * 1.5
        self.player.yaw(self.angleY * 1.3, self,self.angleYRotate *1.3)# Horizontal
        self.player.pitch(self.angleX * 1.3,self, self.angleXRotate*1.3)# Vertical

#       Crouch and sprint.
        speed = self.globalSpeed
        speedSide = self.globalSpeedSide
        if(self.crouching):
            speed = speed / 2
            speedSide = speedSide / 2
        if(self.running):
            speed = speed * 1.3
            speedSide = speedSide * 1.3

#       Movement
        if self.W_key_down:
            if self.can_move(0, -speed * delta_time):
                self.player.slide(0, 0, -speed * delta_time, self)
            else:
                v= self.choos_slide_vector() 
                if self.can_move(self.player.right.angle(v)*-speed*delta_time/2,self.player.forward.angle(v)*-speed*delta_time/2):
                    self.player.slide_(delta_time, self, v, -speed/2)
                elif self.can_move(self.player.right.angle(v)*speed*delta_time/2,self.player.forward.angle(v)*speed*delta_time/2):
                    self.player.slide_(delta_time, self, v, speed/2)
                else:
                    v1=self.choos_slide_vector({v}) 
                    if self.can_move(self.player.right.angle(v1)*-speed*delta_time/2,self.player.forward.angle(v1)*-speed*delta_time/2):
                        self.player.slide_(delta_time, self, v1, -speed/2)
                    elif self.can_move(self.player.right.angle(v1)*speed*delta_time/2,self.player.forward.angle(v1)*speed*delta_time/2):
                        self.player.slide_(delta_time, self, v1, speed/2)
                            

        if self.S_key_down:
            if self.can_move(0,4 * delta_time * 1.3):
                self.player.slide(0, 0, 4 * delta_time * 1.3, self)
            else:
                v= self.choos_slide_vector() 
                if self.can_move(self.player.right.angle(v)*-speed*delta_time/2,self.player.forward.angle(v)*-speed*delta_time/2):
                    self.player.slide_(delta_time, self, v, -speed/2)
                elif self.can_move(self.player.right.angle(v)*speed*delta_time/2,self.player.forward.angle(v)*speed*delta_time/2):
                    self.player.slide_(delta_time, self, v, speed/2)
                else:
                    v1=self.choos_slide_vector({v}) 
                    if self.can_move(self.player.right.angle(v1)*-speed*delta_time/2,self.player.forward.angle(v1)*-speed*delta_time/2):
                        self.player.slide_(delta_time, self, v1, -speed/2)
                    elif self.can_move(self.player.right.angle(v1)*speed*delta_time/2,self.player.forward.angle(v1)*speed*delta_time/2):
                        self.player.slide_(delta_time, self, v1, speed/2)
        if self.A_key_down:
            if self.can_move(-4 * delta_time/2 * 1.3,0):
                self.player.slide(-4 * delta_time/2 * 1.3, 0,0, self)
            else:
                v= self.choos_slide_vector() 
                if self.can_move(self.player.right.angle(v)*-speed*delta_time/2,self.player.forward.angle(v)*-speed*delta_time/2):
                    self.player.slide_(delta_time, self, v, -speed/2)
                elif self.can_move(self.player.right.angle(v)*speed*delta_time/2,self.player.forward.angle(v)*speed*delta_time/2):
                    self.player.slide_(delta_time, self, v, speed/2)
                else:
                    v1=self.choos_slide_vector({v}) 
                    if self.can_move(self.player.right.angle(v1)*-speed*delta_time/2,self.player.forward.angle(v1)*-speed*delta_time/2):
                        self.player.slide_(delta_time, self, v1, -speed/2)
                    elif self.can_move(self.player.right.angle(v1)*speed*delta_time/2,self.player.forward.angle(v1)*speed*delta_time/2):
                        self.player.slide_(delta_time, self, v1, speed/2)
        if self.D_key_down:
            if self.can_move(5 * delta_time/2 * 1.3,0):
                self.player.slide(5 * delta_time/2 * 1.3, 0, 0, self)
            else:
                v= self.choos_slide_vector() 
                if self.can_move(self.player.right.angle(v)*-speed*delta_time/2,self.player.forward.angle(v)*-speed*delta_time/2):
                    self.player.slide_(delta_time, self, v, -speed/2)
                elif self.can_move(self.player.right.angle(v)*speed*delta_time/2,self.player.forward.angle(v)*speed*delta_time/2):
                    self.player.slide_(delta_time, self, v, speed/2)
                else:
                    v1=self.choos_slide_vector({v}) 
                    if self.can_move(self.player.right.angle(v1)*-speed*delta_time/2,self.player.forward.angle(v1)*-speed*delta_time/2):
                        self.player.slide_(delta_time, self, v1, -speed/2)
                    elif self.can_move(self.player.right.angle(v1)*speed*delta_time/2,self.player.forward.angle(v1)*speed*delta_time/2):
                        self.player.slide_(delta_time, self, v1, speed/2)
#       updates the player and then does collision for each bullet inside the each gun.
        self.player.updatePlayer(delta_time, self)
#       Reason for why I take the teams as parameters, I am only supposed to be able to hit enemy members.
        if(self.pickedTeam == "red"):
            self.bullets.updateBullets(delta_time, self.blueTeam, self)
        else:
            self.bullets.updateBullets(delta_time, self.redTeam, self)

    def can_move(self, stepx, stepz):
        new_pos = self.player.position + self.player.right * stepx + self.player.back * stepz
        if -0.25>new_pos.x >-self.width+0.25:
            if -0.25>new_pos.z >-self.length+0.25:
                for box in self.boxes:
                    if box.pos.x-0.75<new_pos.x<box.pos.x+0.75:
                        if box.pos.z-0.75<new_pos.z<box.pos.z+0.75:
                            return False
                return True
        return False
    def choos_slide_vector(self,N=set()):
        V= {Vector(1,0,0), Vector(-1,0,0),Vector(0,0,1), Vector(0,0,-1)}
        V, temp_min,temp_vector= V-N, 90, Vector(1,0,0)
        for v in V:
            ang= self.player.forward.angle(v)
            if ang<=temp_min:
                temp_min, temp_vector = ang,v
        return temp_vector

    def display(self):
        glEnable(GL_DEPTH_TEST)  
        glClearColor(0.10,0.15,0.3, 1.0) #Sky
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)         
        self.projection_matrix.set_perspective(self.fov, 800/600, 0.015, 100)
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())

#       player camera
        glViewport(0, 0, 800, 600)
        eye = self.player.position
        if(self.crouching):
            self.player.position.y = 0.5
        else:
            self.player.position.y = self.playerHeight
        self.view_matrix.look(eye, self.player.position + self.player.looking, self.player.up)
        self.shader.set_view_matrix(self.view_matrix.get_matrix())
        self.renderEnviornment(self.view_matrix)
        pygame.display.flip()


    def renderEnviornment(self, viewMatrix):
#       eye
        self.shader.set_eye_pos(self.view_matrix.eye)

#       Lights
        self.shader.set_light_diffuse(1.0,1.0,1.0)
        self.shader.set_light_specular(1.0,1.0,1.0)
        self.shader.set_light_pos(Point(-self.length/2 + 25 * cos(self.angle),10 ,25 * (sin(self.angle))))
        self.shader.set_shininess(100)
        self.model_matrix.load_identity()
        self.cube.set_vertices(self.shader)

        
#       Guns
        self.texture_id03.use_texture()
        for x in self.guns.guns:
            self.model_matrix.push_matrix()
            self.model_matrix.add_translation(x.position.x,x.position.y, x.position.z)
            self.model_matrix.add_scale(0.10, 0.10, 0.10)
            self.model_matrix.add_rotation_y(x.rotationY)
            self.model_matrix.add_rotation_x(-x.rotationX)
            self.shader.set_model_matrix(self.model_matrix.matrix)
            x.set_vertices(self.shader)
            x.draw()
            self.model_matrix.pop_matrix()
     
#       bullets
        self.sphere.set_vertices(self.shader)
        for y in self.bullets.bullets:
            self.model_matrix.push_matrix()
            self.model_matrix.add_translation(y.position.x,y.position.y, y.position.z)
            self.model_matrix.add_scale(0.05, 0.05, 0.05)
            self.shader.set_model_matrix(self.model_matrix.matrix)
            y.sphere.draw()
            self.model_matrix.pop_matrix()

#       other players?
        self.shader.set_mat_diffuse(1.0, 0.1, 0.0)
        self.shader.set_mat_specular(0.0,0.0,0.0)
        self.sphere.set_vertices(self.shader)
        for x in self.blueTeam:
            # print(Point(x["player"]["position"]["x"], x["player"]["position"]["y"], x["player"]["position"]["z"]))
            self.model_matrix.push_matrix()
            self.model_matrix.add_translation(x["player"]["position"]["x"], x["player"]["position"]["y"]/2-0.2, x["player"]["position"]["z"])
            # self.model_matrix.add_scale(0.25, 0.5, 0.25)
            self.model_matrix.add_rotation_y(90 + x["player"]["angle"])
            self.shader.set_model_matrix(self.model_matrix.matrix)
            self.bluePlayer.draw(self.shader) 
            self.model_matrix.pop_matrix()
        self.shader.set_mat_diffuse(0.0, 0.0, 1.0)
        self.shader.set_mat_specular(0.0,0.0,1.0)
        for x in self.redTeam:
            # print(Point(x["player"]["position"]["x"], x["player"]["position"]["y"], x["player"]["position"]["z"]))
            self.model_matrix.push_matrix()
            self.model_matrix.add_translation(x["player"]["position"]["x"], x["player"]["position"]["y"]/2-0.2, x["player"]["position"]["z"])
            #self.model_matrix.add_scale(0.25, 0.5, 0.25)
            self.model_matrix.add_rotation_y(90 + x["player"]["angle"])
            self.shader.set_model_matrix(self.model_matrix.matrix)
            self.redPlayer.draw(self.shader) 
            self.model_matrix.pop_matrix()

#       sun
        self.model_matrix.push_matrix()
        self.sphere.set_vertices(self.shader)
        self.shader.set_mat_diffuse(1.0, 1.0, 0.0)
        self.shader.set_mat_specular(1.0,1.0,0.0)
        self.model_matrix.add_translation(-self.length/2 + 25 * cos(self.angle),100 ,25 * (sin(self.angle)))
        self.model_matrix.add_scale(5.0, 5.0, 5.0)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.sphere.draw()
        self.model_matrix.pop_matrix()

#       sand supposed to a little bit shine, so decent specular.
        self.cube.set_vertices(self.shader)
        self.texture_id01.use_texture()
        self.shader.set_diffuse_texture()
        
        self.shader.set_mat_diffuse(1.0, 1.0, 1.0)
        self.shader.set_mat_specular(0.4,0.4,0.4)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(-self.length/2, 0.0, -self.width/2)
        self.model_matrix.add_scale(self.length, 0.2, self.width)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw()
        self.model_matrix.pop_matrix()

#       Boxes
        for box in self.boxes:
            box.draw(self)
        
#       Fence
        self.texture_id02.use_texture()
        self.cube.set_vertices(self.shader)
        for i in range(2*self.width):
            self.model_matrix.push_matrix()
            self.model_matrix.add_translation(0.25,(1+((i%3)+1)/3)/2,-(0.25+i*0.5))
            self.model_matrix.add_scale(0.5, 1+((i%3)+1)/3, 0.5)
            self.shader.set_model_matrix(self.model_matrix.matrix)
            self.cube.draw()
            self.model_matrix.pop_matrix()
            self.model_matrix.push_matrix()
            self.model_matrix.add_translation(-0.25-self.length,(1+((i%3)+1)/3)/2,-(0.25+i*0.5))
            self.model_matrix.add_scale(0.5, 1+((i%3)+1)/3, 0.5)
            self.shader.set_model_matrix(self.model_matrix.matrix)
            self.cube.draw()
            self.model_matrix.pop_matrix()
            self.model_matrix.push_matrix()
            self.model_matrix.add_translation(-(0.25+i*0.5),(1+((i%3)+1)/3)/2,0.25)
            self.model_matrix.add_scale(0.5, 1+((i%3)+1)/3, 0.5)
            self.shader.set_model_matrix(self.model_matrix.matrix)
            self.cube.draw()
            self.model_matrix.pop_matrix()
            self.model_matrix.push_matrix()
            self.model_matrix.add_translation(-(0.25+i*0.5),(1+((i%3)+1)/3)/2,-0.25-self.width)
            self.model_matrix.add_scale(0.5, 1+((i%3)+1)/3, 0.5)
            self.shader.set_model_matrix(self.model_matrix.matrix)
            self.cube.draw()
            self.model_matrix.pop_matrix()


    def program_loop(self):
        exiting = False
        while not exiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Quitting!")
                    exiting = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:    
                        self.player.death(self)
                        self.Send({"action": "playerLeave", "player": self.player.toDict()})
                        print("Escaping!")
                        exiting = True
                    if event.key == K_UP:
                        self.UP_key_down = True
                    if event.key == K_w:
                        self.W_key_down = True
                    if event.key == K_a:
                        self.A_key_down = True
                    if event.key == K_d:
                        self.D_key_down = True
                    if event.key == K_s:
                        self.S_key_down = True
                    if event.key == K_LSHIFT:
                        self.running = True
                    if event.key == K_LCTRL:
                        self.crouching = True
                    if event.key == K_g:
                        self.player.drop(self)
                    if event.key == K_2:
                        self.player.changeGun(2, self)
                    if event.key == K_1:
                        self.player.changeGun(1, self)
                    if event.key == K_r:
                        self.player.reloading = True
                    if event.key == K_p:
                        self.infocus = not self.infocus
                elif event.type == pygame.MOUSEMOTION and self.infocus:
                    self.mouseMove = [event.pos[i] - self.displayCenter[i] for i in range(2)]
                elif event.type == pygame.KEYUP:
                    if event.key == K_UP:
                        self.UP_key_down = False
                    if event.key == K_w:
                        self.W_key_down = False
                    if event.key == K_a:
                        self.A_key_down = False
                    if event.key == K_d:
                        self.D_key_down = False
                    if event.key == K_s:
                        self.S_key_down = False
                    if event.key == K_LSHIFT:
                        self.running = False
                    if event.key == K_LCTRL:
                        self.crouching = False
                elif pygame.mouse.get_pressed()[0]:
                    self.player.shooting = True
                elif pygame.mouse.get_pressed()[0] == 0:
                    self.player.shooting = False
            self.update()
            self.display()

        #OUT OF GAME LOOP
        pygame.quit()

    def start(self):
        self.program_loop()

if __name__ == "__main__":
    args = sys.argv
    print(args)
    if len(args)>1: GraphicsProgram3D(args[1], args[2]).start()
    else:           GraphicsProgram3D().start()