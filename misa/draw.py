from OpenGL import GL, GLU
from .util import Vec2d, Vec3d
from .scene.door import draw_botao
from .scene.balcony import *
from .scene.door import *
from .scene.floors import *
from .scene.ground import *
from .scene.objects import *
from .scene.pillars import *
from .scene.roof import *
from .scene.walls import *
from .scene.windows import *

# Global quadric object
q = None

grama_size = 50
luz_ambiente = [0.15, 0.15, 0.15, 1.0]
luz_difusa = [0.8, 0.8, 0.8, 1.0]
luz_especular = [0.1, 0.1, 0.1, 1.0]
posicao_luz = [0.0, 1.7, -5.0, 0.0]

piso_y = 1.0
segundo_andar_y = 7.0
abertura_escada_size = Vec2d(1, 3)

parte_central_size = Vec3d(13, 12.5, 20)
asa_size = Vec3d(10.5, 7, 15)
asa_z_offset = 1.0

porta_size = Vec3d(2.8, 3.2, 0)
espaco_porta_size = Vec2d(3, 3)

janela_com_arco = Vec3d(1.2, 2.6, 0.3)
janela_retangular_size = Vec3d(1.2, 2, 0.3)
janela_baixo_y_offset = 1.4
janela_cima_y_offset = janela_baixo_y_offset + 1.6 + 3.2


# Scene object functions moved to misa.scene submodule
# Imported at top of file


def init():
    global q
    from . import obj
    from .scene import pillars

    GL.glClearColor(0.53, 0.81, 0.98, 1.0)

    GL.glEnable(GL.GL_LIGHTING)
    GL.glEnable(GL.GL_LIGHT0)
    GL.glEnable(GL.GL_NORMALIZE)
    GL.glShadeModel(GL.GL_SMOOTH)

    GL.glEnable(GL.GL_COLOR_MATERIAL)
    GL.glColorMaterial(GL.GL_FRONT_AND_BACK, GL.GL_AMBIENT_AND_DIFFUSE)
    GL.glLightfv(GL.GL_LIGHT0, GL.GL_AMBIENT, luz_ambiente)
    GL.glLightfv(GL.GL_LIGHT0, GL.GL_DIFFUSE, luz_difusa)
    GL.glLightfv(GL.GL_LIGHT0, GL.GL_SPECULAR, luz_especular)

    q = GLU.gluNewQuadric()
    GLU.gluQuadricNormals(q, GLU.GLU_SMOOTH)
    obj.q = q  # Share quadric with obj module
    pillars.q = q  # Share quadric with pillars module

    GL.glClearStencil(0)
    GL.glEnable(GL.GL_STENCIL_TEST)


def on_setup_camera():
    GL.glLightfv(GL.GL_LIGHT0, GL.GL_POSITION, posicao_luz)


def draw():
    draw_grama()

    GL.glPushMatrix()
    GL.glTranslated(-(parte_central_size.x / 2 + asa_size.x), 0, 0)

    draw_chao()
    draw_pisos()
    draw_parte_externa(draw_asa, draw_parte_central)
    draw_parte_externa(draw_janelas_asa, draw_janelas_parte_central)
    draw_pilastras_internas()
    draw_sacada()
    draw_telhado()
    draw_objetos()

    GL.glPopMatrix()
    draw_botao()
