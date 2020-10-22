
from OpenGL.GL import *
from math import * # trigonometry

import sys

from Base3DObjects import *

class Shader3D:
    def __init__(self):
        vert_shader = glCreateShader(GL_VERTEX_SHADER)
        shader_file = open(sys.path[0] + "/simple3D.vert")
        glShaderSource(vert_shader,shader_file.read())
        shader_file.close()
        glCompileShader(vert_shader)
        result = glGetShaderiv(vert_shader, GL_COMPILE_STATUS)
        if (result != 1): # shader didn't compile
            print("Couldn't compile vertex shader\nShader compilation Log:\n" + str(glGetShaderInfoLog(vert_shader)))

        frag_shader = glCreateShader(GL_FRAGMENT_SHADER)
        shader_file = open(sys.path[0] + "/simple3D.frag")
        glShaderSource(frag_shader,shader_file.read())
        shader_file.close()
        glCompileShader(frag_shader)
        result = glGetShaderiv(frag_shader, GL_COMPILE_STATUS)
        if (result != 1): # shader didn't compile
            print("Couldn't compile fragment shader\nShader compilation Log:\n" + str(glGetShaderInfoLog(frag_shader)))

        self.renderingProgramID = glCreateProgram()
        glAttachShader(self.renderingProgramID, vert_shader)
        glAttachShader(self.renderingProgramID, frag_shader)
        glLinkProgram(self.renderingProgramID)

        self.positionLoc		= glGetAttribLocation(self.renderingProgramID, "a_position")
        glEnableVertexAttribArray(self.positionLoc)

        self.normalLoc			= glGetAttribLocation(self.renderingProgramID, "a_normal")
        glEnableVertexAttribArray(self.normalLoc)

        self.uvLoc			= glGetAttribLocation(self.renderingProgramID, "a_uv")
        glEnableVertexAttribArray(self.uvLoc)

       

        ## ADD CODE HERE ##

        self.modelMatrixLoc			= glGetUniformLocation(self.renderingProgramID, "u_model_matrix")
        self.viewMatrixLoc			= glGetUniformLocation(self.renderingProgramID, "u_view_matrix")
        self.projectionMatrixLoc    = glGetUniformLocation(self.renderingProgramID, "u_projection_matrix")

        #Positions 
        self.lightPosLoc              = glGetUniformLocation(self.renderingProgramID, "u_light_position")
        self.eyePosLoc              = glGetUniformLocation(self.renderingProgramID, "u_eye_position")
        # Light
        self.lightDiffuseLoc          = glGetUniformLocation(self.renderingProgramID, "u_light_diffuse")
        self.lightSpecularLoc          = glGetUniformLocation(self.renderingProgramID, "u_light_specular")
        #Material
        self.matDiffuseLoc            = glGetUniformLocation(self.renderingProgramID, "u_mat_diffuse")
        self.matSpecularLoc            = glGetUniformLocation(self.renderingProgramID, "u_mat_specular")
        #shininess
        self.shininessLoc            = glGetUniformLocation(self.renderingProgramID, "u_shininess")


        self.textureDiffuseLoc           = glGetUniformLocation(self.renderingProgramID, "u_tex01")
        self.textureSpecularLoc           = glGetUniformLocation(self.renderingProgramID, "u_tex02")



    def use(self):
        try:
            glUseProgram(self.renderingProgramID)   
        except OpenGL.error.GLError:
            print(glGetProgramInfoLog(self.renderingProgramID))
            raise

    def set_model_matrix(self, matrix_array):
        glUniformMatrix4fv(self.modelMatrixLoc, 1, True, matrix_array)

    def set_projection_matrix(self, matrix_array):
        glUniformMatrix4fv(self.projectionMatrixLoc, 1, True, matrix_array)

    def set_view_matrix(self, matrix_array):
        glUniformMatrix4fv(self.viewMatrixLoc, 1, True, matrix_array)

    def set_light_pos(self, pos):
        glUniform4f(self.lightPosLoc, pos.x, pos.y, pos.z, 1.0)

    def set_eye_pos(self, pos):
        glUniform4f(self.eyePosLoc, pos.x, pos.y, pos.z, 1.0)

    def set_light_diffuse(self, red, green, blue):
        glUniform4f(self.lightDiffuseLoc, red, green, blue, 1.0)

    def set_light_specular(self, red, green, blue):
        glUniform4f(self.lightSpecularLoc, red, green, blue, 1.0)

    def set_mat_diffuse(self, red, green, blue):
        glUniform4f(self.matDiffuseLoc, red, green, blue, 1.0)

    def set_mat_specular(self, red, green, blue):
        glUniform4f(self.matSpecularLoc, red, green, blue, 1.0)

    def set_shininess(self, shininess):
        glUniform1f(self.shininessLoc, shininess)

    def set_position_attribute(self, vertex_array):
        glVertexAttribPointer(self.positionLoc, 3, GL_FLOAT, False, 0, vertex_array)

    def set_normal_attribute(self, vertex_array):
        glVertexAttribPointer(self.normalLoc, 3, GL_FLOAT, False, 0, vertex_array)

    def set_uv_attribute(self, vertex_array):
        glVertexAttribPointer(self.uvLoc, 2, GL_FLOAT, False, 0, vertex_array)

    def set_diffuse_texture(self):
        glUniform1i(self.textureDiffuseLoc, 0)

    def set_specular_texture(self):
        glUniform1i(self.textureSpecularLoc, 1)