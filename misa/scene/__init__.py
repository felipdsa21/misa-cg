from OpenGL import GL

from .. import primitives
from . import chao, constantes, lampadas, objetos, paredes, pilastras, pisos, porta, sacada, telhado


def init() -> None:
    # Céu noturno (azul escuro)
    GL.glClearColor(0.05, 0.05, 0.15, 1.0)

    GL.glEnable(GL.GL_DEPTH_TEST)
    GL.glEnable(GL.GL_LIGHTING)
    GL.glEnable(GL.GL_NORMALIZE)
    GL.glEnable(GL.GL_COLOR_MATERIAL)
    GL.glEnable(GL.GL_STENCIL_TEST)
    GL.glEnable(GL.GL_TEXTURE_2D)

    GL.glShadeModel(GL.GL_SMOOTH)
    GL.glColorMaterial(GL.GL_FRONT_AND_BACK, GL.GL_AMBIENT_AND_DIFFUSE)
    GL.glClearStencil(0)

    # Somente lâmpadas: sem luz global/direcional
    # Zera a luz ambiente do modelo para evitar brilho base
    GL.glLightModelfv(GL.GL_LIGHT_MODEL_AMBIENT, [0.0, 0.0, 0.0, 1.0])
    
    # Inicializar lâmpadas internas
    lampadas.init_lampadas()


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
        lampadas.draw_lampadas()

    porta.draw_botao()


def on_setup_camera() -> None:
    # Atualizar posições das lâmpadas (deve ser após configurar câmera e com a mesma translação do draw)
    with primitives.push_matrix():
        GL.glTranslated(-(constantes.parte_central_size.x / 2 + constantes.asa_size.x), 0, 0)
        lampadas.update_lampadas_positions()


def on_loop() -> bool:
    return porta.on_loop()


def on_mouse_press(button: int, state: int, x: int, y: int) -> bool:
    return porta.on_mouse_press(button, state, x, y)
