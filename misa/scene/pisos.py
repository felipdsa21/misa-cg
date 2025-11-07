from OpenGL import GL

from .. import primitives, util
from . import constantes


def draw_piso(x1: float, z1: float, x2: float, z2: float, y: float):
    GL.glColor3ub(150, 108, 72)
    primitives.draw_rect_y(x1, z1, x2, z2, y)

    GL.glColor3ub(97, 67, 42)
    spacing = 0.45

    GL.glBegin(GL.GL_LINES)
    x = x1 + spacing
    while x < x2:
        GL.glVertex3d(x, y + util.EPSILON, z1)
        GL.glVertex3d(x, y + util.EPSILON, z2)
        x += spacing
    GL.glEnd()


def draw_pisos():
    abertura_escada_size = util.Vec2d(1, 3)
    espaco_porta_size = util.Vec2d(3, 3)

    GL.glNormal3i(0, 1, 0)
    GL.glPushMatrix()

    # Asa direita
    GL.glTranslated(0, 0, constantes.asa_z_offset)
    draw_piso(0, 0, constantes.asa_size.x, constantes.asa_size.z, constantes.piso_y)

    # Parte central
    GL.glTranslated(constantes.asa_size.x, 0, -constantes.asa_z_offset)

    espaco_porta_x_start = (constantes.parte_central_size.x - espaco_porta_size.x) / 2
    espaco_porta_x_end = (constantes.parte_central_size.x + espaco_porta_size.x) / 2
    # Espaço para porta
    draw_piso(
        0,
        espaco_porta_size.y,
        constantes.parte_central_size.x,
        constantes.parte_central_size.z,
        constantes.piso_y,
    )
    draw_piso(0, 0, espaco_porta_x_start, espaco_porta_size.y, constantes.piso_y)
    draw_piso(espaco_porta_x_end, 0, constantes.parte_central_size.x, espaco_porta_size.y, constantes.piso_y)
    draw_piso(espaco_porta_x_start, 0, espaco_porta_x_end, espaco_porta_size.y, util.EPSILON * 2)

    # Segundo andar
    limite_x = constantes.parte_central_size.x - abertura_escada_size.x
    limite_z = constantes.parte_central_size.z / 2
    fim_abertura_z = limite_z + abertura_escada_size.y

    draw_piso(0, 0, limite_x, constantes.parte_central_size.z, constantes.segundo_andar_y)
    draw_piso(limite_x, 0, constantes.parte_central_size.x, limite_z, constantes.segundo_andar_y)
    draw_piso(
        limite_x,
        fim_abertura_z,
        constantes.parte_central_size.x,
        constantes.parte_central_size.z,
        constantes.segundo_andar_y,
    )
    draw_piso(
        constantes.parte_central_size.x - 0.1,
        limite_z,
        constantes.parte_central_size.x,
        fim_abertura_z,
        constantes.segundo_andar_y,
    )

    # Asa esquerda
    GL.glTranslated(constantes.parte_central_size.x, 0, constantes.asa_z_offset)
    draw_piso(0, 0, constantes.asa_size.x, constantes.asa_size.z, constantes.piso_y)

    GL.glPopMatrix()
