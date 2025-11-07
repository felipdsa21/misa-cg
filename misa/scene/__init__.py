from OpenGL import GL

from .. import primitives
from . import chao, constantes, lampadas, objetos, paredes, pilastras, pisos, porta, sacada, telhado


def init() -> None:
    # Céu noturno (azul escuro)
    GL.glClearColor(0.05, 0.05, 0.15, 1.0)

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

    # Luz ambiente noturna (extremamente baixa para escuridão)
    luz_ambiente = [0.01, 0.01, 0.02, 1.0]
    luz_difusa = [0.05, 0.05, 0.08, 1.0]
    luz_especular = [0.02, 0.02, 0.02, 1.0]
    GL.glLightfv(GL.GL_LIGHT0, GL.GL_AMBIENT, luz_ambiente)
    GL.glLightfv(GL.GL_LIGHT0, GL.GL_DIFFUSE, luz_difusa)
    GL.glLightfv(GL.GL_LIGHT0, GL.GL_SPECULAR, luz_especular)
    
    # Habilitar atenuação para luzes pontuais
    GL.glLightf(GL.GL_LIGHT0, GL.GL_CONSTANT_ATTENUATION, 1.0)
    GL.glLightf(GL.GL_LIGHT0, GL.GL_LINEAR_ATTENUATION, 0.15)
    GL.glLightf(GL.GL_LIGHT0, GL.GL_QUADRATIC_ATTENUATION, 0.08)
    
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
    posicao_luz = [0.0, 1.7, -5.0, 0.0]
    GL.glLightfv(GL.GL_LIGHT0, GL.GL_POSITION, posicao_luz)
    
    # Atualizar posições das lâmpadas (deve ser após configurar câmera e com a mesma translação do draw)
    with primitives.push_matrix():
        GL.glTranslated(-(constantes.parte_central_size.x / 2 + constantes.asa_size.x), 0, 0)
        lampadas.update_lampadas_positions()


def on_loop() -> bool:
    return porta.on_loop()


def on_mouse_press(button: int, state: int, x: int, y: int) -> bool:
    return porta.on_mouse_press(button, state, x, y)
