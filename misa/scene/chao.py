from OpenGL import GL

from .. import primitives, util
from . import constantes


def draw_terreno() -> None:
    grama_size = 50

    GL.glColor3ub(65, 152, 10)
    GL.glNormal3i(0, 1, 0)
    primitives.draw_rect_y(-grama_size, -grama_size, grama_size, grama_size, 0)


def draw_chao() -> None:
    tamanho = util.Vec2d(
        constantes.parte_central_size.x + constantes.asa_size.x * 2,
        constantes.parte_central_size.z + constantes.asa_size.z * 2,
    )

    GL.glColor3ub(156, 146, 143)
    GL.glNormal3i(0, 1, 0)
    primitives.draw_rect_y(-2, -2, tamanho.x + 2, tamanho.y + 2, constantes.epsilon)
