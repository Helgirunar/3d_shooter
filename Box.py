from Base3DObjects import Cube, Point
from Texture import Texture

class Box():
    def __init__(self, size= (1,1,1), pos = Point(0,0.5,0), _id=0,tex= 'box'):
        self.size = size
        self.pos= pos
        self.tex= Texture(tex)
        self.cube= Cube()
        self.cube.setPos(pos)
        self.id= _id
    
    def draw(self, game):
        self.tex.use_texture()
        self.cube.set_vertices(game.shader)
        game.model_matrix.push_matrix()
        game.model_matrix.add_translation(self.pos.x, self.pos.y, self.pos.z)
        game.model_matrix.add_scale(*self.size)
        game.shader.set_model_matrix(game.model_matrix.matrix)
        self.cube.draw()
        game.model_matrix.pop_matrix()
        