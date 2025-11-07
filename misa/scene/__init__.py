from OpenGL import GL

from .. import primitives
from . import chao, constantes, objetos, paredes, pilastras, pisos, porta, sacada, telhado


def init() -> None:
    GL.glClearColor(0.53, 0.81, 0.98, 1.0)

    GL.glEnable(GL.GL_DEPTH_TEST)
    GL.glEnable(GL.GL_LIGHTING)
    GL.glEnable(GL.GL_LIGHT0)
    GL.glEnable(GL.GL_NORMALIZE)
    GL.glEnable(GL.GL_COLOR_MATERIAL)
    GL.glEnable(GL.GL_STENCIL_TEST)
    GL.glEnable(GL.GL_TEXTURE_2D)

    GL.glShadeModel(GL.GL_SMOOTH)
    GL.glColorMaterial(GL.GL_FRONT_AND_BACK, GL.GL_AMBIENT_AND_DIFFUSE)
    GL.glClearStencil(0)

    luz_ambiente = [0.15, 0.15, 0.15, 1.0]
    luz_difusa = [0.8, 0.8, 0.8, 1.0]
    luz_especular = [0.1, 0.1, 0.1, 1.0]
    GL.glLightfv(GL.GL_LIGHT0, GL.GL_AMBIENT, luz_ambiente)
    GL.glLightfv(GL.GL_LIGHT0, GL.GL_DIFFUSE, luz_difusa)
    GL.glLightfv(GL.GL_LIGHT0, GL.GL_SPECULAR, luz_especular)


def draw() -> None:
    chao.draw_terreno()

    with primitives.push_matrix():
        GL.glTranslated(-(constantes.parte_central_size.x / 2 + constantes.asa_size.x), 0, 0)

        chao.draw_chao()
        pisos.draw_pisos()
        paredes.draw_paredes()
        pilastras.draw_pilastras_internas()
        sacada.draw_sacada()
        telhado.draw_telhado()
        objetos.draw_objetos()

    porta.draw_botao()


def on_setup_camera() -> None:
    posicao_luz = [0.0, 1.7, -5.0, 0.0]
    GL.glLightfv(GL.GL_LIGHT0, GL.GL_POSITION, posicao_luz)


def on_loop() -> bool:
    return porta.on_loop()


def on_mouse_press(button: int, state: int, x: int, y: int) -> bool:
    return porta.on_mouse_press(button, state, x, y)
