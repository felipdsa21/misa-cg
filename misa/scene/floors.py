"""Floor drawing functions - All floor levels in the building."""

from OpenGL import GL
from ..util import Vec2d, EPSILON
from ..primitives import draw_rect_y


def draw_piso(x1: float, z1: float, x2: float, z2: float, y: float):
    """Draw a single floor section with wood texture and lines."""
    GL.glColor3ub(150, 108, 72)
    draw_rect_y(x1, z1, x2, z2, y)

    GL.glColor3ub(97, 67, 42)
    spacing = 0.45

    GL.glBegin(GL.GL_LINES)
    x = x1 + spacing
    while x < x2:
        GL.glVertex3d(x, y + EPSILON, z1)
        GL.glVertex3d(x, y + EPSILON, z2)
        x += spacing
    GL.glEnd()


def draw_pisos():
    """Draw all floors including ground floor and second floor."""
    from ..draw import (
        piso_y,
        segundo_andar_y,
        asa_size,
        parte_central_size,
        asa_z_offset,
        espaco_porta_size,
        abertura_escada_size,
    )

    GL.glNormal3i(0, 1, 0)
    GL.glPushMatrix()

    # Asa direita
    GL.glTranslated(0, 0, asa_z_offset)
    draw_piso(0, 0, asa_size.x, asa_size.z, piso_y)

    # Parte central
    GL.glTranslated(asa_size.x, 0, -asa_z_offset)

    espaco_porta_x_start = (parte_central_size.x - espaco_porta_size.x) / 2
    espaco_porta_x_end = (parte_central_size.x + espaco_porta_size.x) / 2
    # Espaço para porta
    draw_piso(
        0, espaco_porta_size.y, parte_central_size.x, parte_central_size.z, piso_y
    )
    draw_piso(0, 0, espaco_porta_x_start, espaco_porta_size.y, piso_y)
    draw_piso(espaco_porta_x_end, 0, parte_central_size.x, espaco_porta_size.y, piso_y)
    draw_piso(
        espaco_porta_x_start, 0, espaco_porta_x_end, espaco_porta_size.y, EPSILON * 2
    )

    # Segundo andar
    limite_x = parte_central_size.x - abertura_escada_size.x
    limite_z = parte_central_size.z / 2
    fim_abertura_z = limite_z + abertura_escada_size.y

    draw_piso(0, 0, limite_x, parte_central_size.z, segundo_andar_y)
    draw_piso(limite_x, 0, parte_central_size.x, limite_z, segundo_andar_y)
    draw_piso(
        limite_x,
        fim_abertura_z,
        parte_central_size.x,
        parte_central_size.z,
        segundo_andar_y,
    )
    draw_piso(
        parte_central_size.x - 0.1,
        limite_z,
        parte_central_size.x,
        fim_abertura_z,
        segundo_andar_y,
    )

    # Asa esquerda
    GL.glTranslated(parte_central_size.x, 0, asa_z_offset)
    draw_piso(0, 0, asa_size.x, asa_size.z, piso_y)

    GL.glPopMatrix()
