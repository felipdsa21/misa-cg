from OpenGL import GL

from .. import util as util
from . import chao, constantes, objetos, paredes, pilastras, pisos, porta, sacada, telhado
from . import janelas as janelas


def init():
    luz_ambiente = [0.15, 0.15, 0.15, 1.0]
    luz_difusa = [0.8, 0.8, 0.8, 1.0]
    luz_especular = [0.1, 0.1, 0.1, 1.0]

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

    GL.glClearStencil(0)
    GL.glEnable(GL.GL_STENCIL_TEST)


def draw():
    GL.glPushMatrix()
    chao.draw_terreno()

    base_x = -(constantes.parte_central_size.x / 2 + constantes.asa_size.x)
    GL.glTranslated(base_x, 0, 0)

    chao.draw_chao()
    pisos.draw_pisos()
    paredes.draw_parte_externa(paredes.draw_asa, paredes.draw_parte_central)
    paredes.draw_parte_externa(paredes.draw_janelas_asa, paredes.draw_janelas_parte_central)
    pilastras.draw_pilastras_internas()
    sacada.draw_sacada()
    telhado.draw_telhado()
    objetos.draw_objetos()

    GL.glPopMatrix()
    porta.draw_botao()


def on_setup_camera():
    posicao_luz = [0.0, 1.7, -5.0, 0.0]
    GL.glLightfv(GL.GL_LIGHT0, GL.GL_POSITION, posicao_luz)


def on_loop() -> bool:
    return porta.on_loop()


def on_mouse_press(button: int, state: int, x: int, y: int) -> bool:
    return porta.on_mouse_press(button, state, x, y)
