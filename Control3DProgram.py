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
from Shaders import *
from Matrices import *
from Player import Player
from Guns import Guns
from Gun import Gun

class GraphicsProgram3D(ConnectionListener):
    def __init__(self):
        pygame.init() 
        self.screen = pygame.display.set_mode((800,600), pygame.OPENGL|pygame.DOUBLEBUF)
#       Length and width of the playing field.
        self.length = 30
        self.width = 30

#       Shader
        self.shader = Shader3D()
        self.shader.use()

#       Inputs from player, pick a team from red or blue, then set your name.
        self.pickedTeam = "red"
        self.playerName = "Player1"

#       Player Height
        self.playerHeight = 0.75


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
        else:
            self.PlayerStartPos = self.teamBlueSpawns[rand.randint(0,4)]            

#       This is my player, it takes parameters (poisition, name, team)
        self.player = Player(self.PlayerStartPos, self.playerName, self.pickedTeam)

#       extra            
        self.model_matrix = ModelMatrix()
        self.globalSpeed = 5
        self.globalSpeedSide = 4
        self.view_matrix = ViewMatrix()
        self.view_matrix_top = ViewMatrix()
        self.displayCenter = [self.screen.get_size()[i] // 2 for i in range(2)]
        self.projection_matrix = ProjectionMatrix()
        self.fov = pi / 4
        self.projection_matrix.set_perspective(self.fov, 800/600, 0.5, 1000)
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())
        self.cube = Cube()
        self.clock = pygame.time.Clock()
        self.clock.tick(60)
        self.guns = Guns()

#       Create guns for red side
        for x in range(1,8):
            self.guns.addGun(Gun("AK-47", 600, 32,Point(-self.length + 3,0.2,-self.width + 2 * x),30))
            self.guns.addGun(Gun("m4-a1", 700, 28,Point(-self.length + 3,0.2,-self.width + 4 * x),35))

#       Create guns for blue side
        for x in range(1,8):
            self.guns.addGun(Gun("AK-47", 600, 32,Point(-3,0.2,-self.width + 2 * x),30))
            self.guns.addGun(Gun("m4-a1", 700, 28,Point(-3,0.2,-self.width + 4 * x),35))

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
        self.texture_id01 = self.load_texture("dirt")
        self.texture_id02 = self.load_texture("box")
        self.texture_id03 = self.load_texture("gunColor")

#       Connect to the server
        self.Connect(('127.0.0.1', 1337))        

#       Adding the player to the server's player list.
        self.Send({"action": "addPlayer", "player": self.player.toDict()})

#   loads texture
    def load_texture(self, name):
        surface = pygame.image.load(sys.path[0] + "/textures/" + name + ".png")
        txt_string = pygame.image.tostring(surface, "RGBA", 1)
        width = surface.get_width()
        height = surface.get_height()
        tex_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, txt_string)
        return tex_id
#   This is the function that receives the data from the server.
    def Network_updatePlayer(self, data):
        for x in data["players"]:
            if x["name"] == self.player.name:
                pass
            else:
                if(x["team"] == "red"):
                    tempfound = False
                    for idx, item in enumerate(self.redTeam):
                        if x["name"] == item["name"]:
                            self.redTeam[idx] = x
                            tempfound = True
                    if(not tempfound):
                        self.redTeam.append(x)
                elif(x["team"] == "blue"):
                    tempfound = False
                    for idx, item in enumerate(self.blueTeam):
                        if x["name"] == item["name"]:
                            self.blueTeam[idx] = x
                            tempfound = True
                    if(not tempfound):
                        self.blueTeam.append(x)

        for x in data["damage"]:
            if x["player"]["name"] == self.player.name:
                self.player.takeDamage(x["dmg"])

    def update(self):
        connection.Pump()
        self.Pump()
#       Updates the player position.
        self.Send({"action": "updatePlayer", "player": self.player.toDict()})

        delta_time = self.clock.tick() / 1000.0
#       For testing purpose, so we can run 2 clients on the same computer.
        if self.infocus:
            pygame.mouse.set_pos(self.displayCenter)
        self.angle += delta_time
#       For picking up guns.
        for x in self.guns.guns:
            if(x.beingHeld != True and len(self.player.guns) != 2):
                x.collide(self.player)

#       Get the rotation from the mouse
        self.angleY = -math.atan(self.mouseMove[0]) * delta_time * 1.5
        self.angleYRotate += -math.atan(self.mouseMove[0]) * delta_time * 1.5
        self.angleX = -math.atan(self.mouseMove[1]) * delta_time * 1.5
        self.angleXRotate += -math.atan(self.mouseMove[1]) * delta_time * 1.5
        self.player.yaw(self.angleY * 1.3)# Horizontal
        self.player.pitch(self.angleX * 1.3)# Vertical

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
            self.player.slide(0, 0, -speed * delta_time)
        if self.S_key_down:
            self.player.slide(0, 0, 4 * delta_time * 1.3)
        if self.A_key_down:
            self.player.slide(-4 * delta_time/2 * 1.3, 0,0)
        if self.D_key_down:
            self.player.slide(5 * delta_time/2 * 1.3, 0, 0)
#       updates the player and then does collision for each bullet inside the each gun.
        self.player.updatePlayer(delta_time)
#       Reason for why I take the teams as parameters, I am only supposed to be able to hit enemy members.
        if(self.pickedTeam == "red"):
            self.guns.updateGuns(delta_time, self.blueTeam, self)
        else:
            self.guns.updateGuns(delta_time, self.redTeam, self)

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
        self.shader.set_light_pos(Point(25 * sin(self.angle/100), 14 + 25 * (sin(self.angle/100)),-self.length/2))
        self.shader.set_shininess(100)
        self.model_matrix.load_identity()
        self.cube.set_vertices(self.shader)

        
#       Guns
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture_id03)
        for x in self.guns.guns:
            self.model_matrix.push_matrix()
            self.model_matrix.add_translation(x.position.x,x.position.y, x.position.z)
            self.model_matrix.add_scale(0.10, 0.10, 0.10)
            if(x.beingHeld):
                x.rotationY = self.angleYRotate * 1.3
                x.rotationX = self.angleXRotate * 1.3
            self.model_matrix.add_rotation_y(x.rotationY)
            self.model_matrix.add_rotation_x(-x.rotationX)
            self.shader.set_model_matrix(self.model_matrix.matrix)
            x.set_vertices(self.shader)
            x.draw(self.shader)
            self.model_matrix.pop_matrix()
#       bullets / They're currently only cubes.
        self.cube.set_vertices(self.shader)
        for x in self.guns.guns:
            for y in x.bullets:
                self.model_matrix.push_matrix()
                self.model_matrix.add_translation(y.position.x,y.position.y, y.position.z)
                self.model_matrix.add_scale(0.05, 0.05, 0.05)
                self.shader.set_model_matrix(self.model_matrix.matrix)
                y.cube.draw(self.shader)
                self.model_matrix.pop_matrix()
                
#       other players?
        for x in self.blueTeam:
            self.model_matrix.push_matrix()
            self.model_matrix.add_translation(x["position"]["x"], x["position"]["y"], x["position"]["z"])
            self.model_matrix.add_scale(0.25, 0.5, 0.25)
            self.shader.set_model_matrix(self.model_matrix.matrix)
            self.cube.draw(self.shader) #placeholder, hopefully / It's only cubes.
            self.model_matrix.pop_matrix()
        for x in self.redTeam:
            self.model_matrix.push_matrix()
            self.model_matrix.add_translation(x["position"]["x"], x["position"]["y"], x["position"]["z"])
            self.model_matrix.add_scale(0.25, 0.5, 0.25)
            self.shader.set_model_matrix(self.model_matrix.matrix)
            self.cube.draw(self.shader) #placeholder, hopefully / It's only cubes.
            self.model_matrix.pop_matrix()

#       sun?, Also a cube 
        self.model_matrix.push_matrix()
        self.shader.set_mat_diffuse(1.0, 1.0, 0.0)
        self.shader.set_mat_specular(1.0,1.0,0.0)
        self.model_matrix.add_translation(10 + 25 * sin(self.angle/100), 25 + 25 * (sin(self.angle/100)),10 + -self.length/2)
        self.model_matrix.add_scale(2.0, 2.0, 2.0)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw(self.shader)
        self.model_matrix.pop_matrix()

#       sand supposed to a little bit shine, so decent specular.
        self.cube.set_vertices(self.shader)
        glBindTexture(GL_TEXTURE_2D, self.texture_id01)
        glActiveTexture(GL_TEXTURE1)
        self.shader.set_diffuse_texture()
        
        self.shader.set_mat_diffuse(1.0, 1.0, 1.0)
        self.shader.set_mat_specular(0.4,0.4,0.4)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(-self.length/2, 0.0, -self.width/2)
        self.model_matrix.add_scale(self.length, 0.2, self.width)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw(self.shader)
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
                        self.player.drop()
                    if event.key == K_2:
                        self.player.changeGun(2)
                    if event.key == K_1:
                        self.player.changeGun(1)
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
    GraphicsProgram3D().start()