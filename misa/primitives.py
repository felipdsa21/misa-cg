from contextlib import contextmanager

from OpenGL import GL

from . import util


@contextmanager
def push_matrix():
    GL.glPushMatrix()
    try:
        yield
    finally:
        GL.glPopMatrix()


@contextmanager
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


def draw_rect_y(x1: float, z1: float, x2: float, z2: float, y: float) -> None:
    with begin(GL.GL_QUADS):
        GL.glVertex3d(x1, y, z1)
        GL.glVertex3d(x2, y, z1)
        GL.glVertex3d(x2, y, z2)
        GL.glVertex3d(x1, y, z2)


def draw_rect_z(x1: float, y1: float, x2: float, y2: float, z: float) -> None:
    with begin(GL.GL_QUADS):
        GL.glVertex3d(x1, y1, z)
        GL.glVertex3d(x2, y1, z)
        GL.glVertex3d(x2, y2, z)
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
