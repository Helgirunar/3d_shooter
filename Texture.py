import sys
import pygame
from OpenGL.GL import *

class Texture():
    def __init__(self, name):
        self.id = self.load_texture(name)
    def load_texture(self, name):
        '''Load texture'''
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
    def use_texture(self):
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.id)