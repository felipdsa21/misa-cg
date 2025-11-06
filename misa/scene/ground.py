"""Ground drawing functions - Grass and floor base."""

from OpenGL.GL import *
from ..util import Vec2d, EPSILON
from ..primitives import draw_rect_y


def draw_grama():
    """Draw the grass ground plane."""
    from ..draw import grama_size

    glColor3ub(65, 152, 10)
    glNormal3i(0, 1, 0)
    draw_rect_y(-grama_size, -grama_size, grama_size, grama_size, 0)


def draw_chao():
    """Draw the concrete floor base around the building."""
    from ..draw import parte_central_size, asa_size

    tamanho = Vec2d(
        parte_central_size.x + asa_size.x * 2, parte_central_size.z + asa_size.z * 2
    )

    glColor3ub(156, 146, 143)
    glNormal3i(0, 1, 0)
    draw_rect_y(-2, -2, tamanho.x + 2, tamanho.y + 2, EPSILON)
