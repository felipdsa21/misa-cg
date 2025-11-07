from OpenGL import GL

from .. import primitives, util
from . import constantes


def draw_pisos():
    GL.glNormal3i(0, 1, 0)
    draw_piso_terreo()
    draw_piso_primeiro_andar()


def draw_piso_terreo():
    espaco_porta_size = util.Vec2d(3, 3)
    espaco_porta_x = util.Vec2d(
        (constantes.parte_central_size.x - espaco_porta_size.x) / 2,
        (constantes.parte_central_size.x + espaco_porta_size.x) / 2,
    )

    primitives.setup_stencil_mask()

    with primitives.push_matrix():
        # Marcar espaço da porta na parte central
        GL.glTranslated(constantes.asa_size.x, 0, -constantes.asa_z_offset)
        mascarar_retangulo_piso(espaco_porta_x.x, 0, espaco_porta_x.y, espaco_porta_size.y, constantes.piso_y)

    primitives.setup_stencil_draw()

    # Asa direita
    with primitives.push_matrix():
        GL.glTranslated(0, 0, constantes.asa_z_offset)
        draw_piso(0, 0, constantes.asa_size.x, constantes.asa_size.z, constantes.piso_y)

    # Parte central completa
    with primitives.push_matrix():
        GL.glTranslated(constantes.asa_size.x, 0, 0)
        draw_piso(0, 0, constantes.parte_central_size.x, constantes.parte_central_size.z, constantes.piso_y)
        draw_piso(espaco_porta_x.x, 0, espaco_porta_x.y, espaco_porta_size.y, util.EPSILON * 2)

    # Asa esquerda
    with primitives.push_matrix():
        GL.glTranslated(constantes.asa_size.x + constantes.parte_central_size.x, 0, constantes.asa_z_offset)
        draw_piso(0, 0, constantes.asa_size.x, constantes.asa_size.z, constantes.piso_y)

    primitives.free_stencil()


def draw_piso_primeiro_andar():
    abertura_escada_size = util.Vec2d(1, 3)

    with primitives.push_matrix():
        GL.glNormal3i(0, 1, 0)
        GL.glTranslated(constantes.asa_size.x, 0, 0)

        primitives.setup_stencil_mask()

        # Marcar abertura da escada
        limite_x = constantes.parte_central_size.x - abertura_escada_size.x
        limite_z = constantes.parte_central_size.z / 2
        fim_abertura_z = limite_z + abertura_escada_size.y
        mascarar_retangulo_piso(
            limite_x, limite_z, constantes.parte_central_size.x, fim_abertura_z, constantes.segundo_andar_y
        )

        primitives.setup_stencil_draw()

        draw_piso(
            0, 0, constantes.parte_central_size.x, constantes.parte_central_size.z, constantes.segundo_andar_y
        )

        primitives.free_stencil()


def mascarar_retangulo_piso(x1: float, z1: float, x2: float, z2: float, y: float):
    with primitives.begin(GL.GL_QUADS):
        GL.glVertex3d(x1, y, z1)
        GL.glVertex3d(x2, y, z1)
        GL.glVertex3d(x2, y, z2)
        GL.glVertex3d(x1, y, z2)


def draw_piso(x1: float, z1: float, x2: float, z2: float, y: float):
    GL.glColor3ub(150, 108, 72)
    primitives.draw_rect_y(x1, z1, x2, z2, y)

    GL.glColor3ub(97, 67, 42)
    espacamento = 0.45
    x = x1 + espacamento

    with primitives.begin(GL.GL_LINES):
        while x < x2:
            GL.glVertex3d(x, y + util.EPSILON, z1)
            GL.glVertex3d(x, y + util.EPSILON, z2)
            x += espacamento
