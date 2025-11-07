import contextlib
import functools
import os.path

import PIL.Image
from OpenGL import GL

from . import util


@contextlib.contextmanager
def push_matrix():
    GL.glPushMatrix()
    try:
        yield
    finally:
        GL.glPopMatrix()


@contextlib.contextmanager
def begin(mode: int):
    GL.glBegin(mode)
    try:
        yield
    finally:
        GL.glEnd()


def setup_stencil_mask() -> None:
    GL.glColorMask(GL.GL_FALSE, GL.GL_FALSE, GL.GL_FALSE, GL.GL_FALSE)
    GL.glDepthMask(GL.GL_FALSE)
    GL.glStencilMask(0xFF)
    GL.glClear(GL.GL_STENCIL_BUFFER_BIT)
    GL.glStencilFunc(GL.GL_ALWAYS, 1, 0xFF)
    GL.glStencilOp(GL.GL_KEEP, GL.GL_KEEP, GL.GL_REPLACE)


def setup_stencil_draw() -> None:
    GL.glColorMask(GL.GL_TRUE, GL.GL_TRUE, GL.GL_TRUE, GL.GL_TRUE)
    GL.glDepthMask(GL.GL_TRUE)
    GL.glStencilFunc(GL.GL_EQUAL, 0, 0xFF)
    GL.glStencilOp(GL.GL_KEEP, GL.GL_KEEP, GL.GL_KEEP)


def free_stencil() -> None:
    GL.glStencilFunc(GL.GL_ALWAYS, 0, 0xFF)


def mascarar_retangulo_xy(x1: float, y1: float, x2: float, y2: float, z: float = 0.0) -> None:
    GL.glDisable(GL.GL_TEXTURE_2D)
    with begin(GL.GL_QUADS):
        GL.glVertex3d(x1, y1, z)
        GL.glVertex3d(x2, y1, z)
        GL.glVertex3d(x2, y2, z)
        GL.glVertex3d(x1, y2, z)
    GL.glEnable(GL.GL_TEXTURE_2D)


def mascarar_retangulo_yz(y1: float, z1: float, y2: float, z2: float, x: float = 0.0) -> None:
    GL.glDisable(GL.GL_TEXTURE_2D)
    with begin(GL.GL_QUADS):
        GL.glVertex3d(x, y1, z1)
        GL.glVertex3d(x, y2, z1)
        GL.glVertex3d(x, y2, z2)
        GL.glVertex3d(x, y1, z2)
    GL.glEnable(GL.GL_TEXTURE_2D)


def mascarar_retangulo_xz(x1: float, z1: float, x2: float, z2: float, y: float = 0.0) -> None:
    GL.glDisable(GL.GL_TEXTURE_2D)
    with begin(GL.GL_QUADS):
        GL.glVertex3d(x1, y, z1)
        GL.glVertex3d(x2, y, z1)
        GL.glVertex3d(x2, y, z2)
        GL.glVertex3d(x1, y, z2)
    GL.glEnable(GL.GL_TEXTURE_2D)


def draw_rect_x(y1: float, z1: float, y2: float, z2: float, x: float) -> None:
    with begin(GL.GL_QUADS):
        GL.glTexCoord2d(0.0, 0.0)
        GL.glVertex3d(x, y1, z1)
        GL.glTexCoord2d(0.0, y2 - y1)
        GL.glVertex3d(x, y2, z1)
        GL.glTexCoord2d(z2 - z1, y2 - y1)
        GL.glVertex3d(x, y2, z2)
        GL.glTexCoord2d(z2 - z1, 0.0)
        GL.glVertex3d(x, y1, z2)


def draw_rect_y(x1: float, z1: float, x2: float, z2: float, y: float) -> None:
    with begin(GL.GL_QUADS):
        GL.glTexCoord2d(x1, z1)
        GL.glVertex3d(x1, y, z1)
        GL.glTexCoord2d(x2, z1)
        GL.glVertex3d(x2, y, z1)
        GL.glTexCoord2d(x2, z2)
        GL.glVertex3d(x2, y, z2)
        GL.glTexCoord2d(x1, z2)
        GL.glVertex3d(x1, y, z2)


def draw_rect_z(x1: float, y1: float, x2: float, y2: float, z: float) -> None:
    with begin(GL.GL_QUADS):
        GL.glTexCoord2d(x1, y1)
        GL.glVertex3d(x1, y1, z)
        GL.glTexCoord2d(x2, y1)
        GL.glVertex3d(x2, y1, z)
        GL.glTexCoord2d(x2, y2)
        GL.glVertex3d(x2, y2, z)
        GL.glTexCoord2d(x1, y2)
        GL.glVertex3d(x1, y2, z)


def draw_box(pos: util.Vec3d, size: util.Vec3d) -> None:
    with begin(GL.GL_QUADS):
        # Frente
        GL.glVertex3d(pos.x, pos.y, pos.z)
        GL.glVertex3d(pos.x + size.x, pos.y, pos.z)
        GL.glVertex3d(pos.x + size.x, pos.y + size.y, pos.z)
        GL.glVertex3d(pos.x, pos.y + size.y, pos.z)

        # Trás
        GL.glVertex3d(pos.x, pos.y, pos.z - size.z)
        GL.glVertex3d(pos.x + size.x, pos.y, pos.z - size.z)
        GL.glVertex3d(pos.x + size.x, pos.y + size.y, pos.z - size.z)
        GL.glVertex3d(pos.x, pos.y + size.y, pos.z - size.z)

        # Esquerda
        GL.glVertex3d(pos.x, pos.y, pos.z)
        GL.glVertex3d(pos.x, pos.y, pos.z - size.z)
        GL.glVertex3d(pos.x, pos.y + size.y, pos.z - size.z)
        GL.glVertex3d(pos.x, pos.y + size.y, pos.z)

        # Direita
        GL.glVertex3d(pos.x + size.x, pos.y, pos.z)
        GL.glVertex3d(pos.x + size.x, pos.y, pos.z - size.z)
        GL.glVertex3d(pos.x + size.x, pos.y + size.y, pos.z - size.z)
        GL.glVertex3d(pos.x + size.x, pos.y + size.y, pos.z)

        # Topo
        GL.glVertex3d(pos.x, pos.y + size.y, pos.z)
        GL.glVertex3d(pos.x + size.x, pos.y + size.y, pos.z)
        GL.glVertex3d(pos.x + size.x, pos.y + size.y, pos.z - size.z)
        GL.glVertex3d(pos.x, pos.y + size.y, pos.z - size.z)

        # Base
        GL.glVertex3d(pos.x, pos.y, pos.z)
        GL.glVertex3d(pos.x + size.x, pos.y, pos.z)
        GL.glVertex3d(pos.x + size.x, pos.y, pos.z - size.z)
        GL.glVertex3d(pos.x, pos.y, pos.z - size.z)


@functools.cache
def load_texture_from_file(name: str) -> int:
    img = PIL.Image.open(os.path.join("textures", name))
    return load_texture_from_image(img)


def load_texture_from_image(img: PIL.Image) -> int:
    img = img.convert("RGBA")
    img_data = img.tobytes("raw", "RGBA", 0, -1)

    texture_id = GL.glGenTextures(1)
    GL.glBindTexture(GL.GL_TEXTURE_2D, texture_id)

    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_REPEAT)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_REPEAT)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)

    GL.glTexImage2D(
        GL.GL_TEXTURE_2D, 0, GL.GL_RGBA, img.width, img.height, 0, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, img_data
    )
    GL.glGenerateMipmap(GL.GL_TEXTURE_2D)

    return texture_id
