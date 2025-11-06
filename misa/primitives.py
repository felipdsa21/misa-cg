from OpenGL import GL
from .util import Vec3d


def draw_rect_y(x1: float, z1: float, x2: float, z2: float, y: float):
    GL.glBegin(GL.GL_QUADS)
    GL.glVertex3d(x1, y, z1)
    GL.glVertex3d(x2, y, z1)
    GL.glVertex3d(x2, y, z2)
    GL.glVertex3d(x1, y, z2)
    GL.glEnd()


def draw_rect_z(x1: float, y1: float, x2: float, y2: float, z: float):
    GL.glBegin(GL.GL_QUADS)
    GL.glVertex3d(x1, y1, z)
    GL.glVertex3d(x2, y1, z)
    GL.glVertex3d(x2, y2, z)
    GL.glVertex3d(x1, y2, z)
    GL.glEnd()


def draw_box(pos: Vec3d, size: Vec3d):
    GL.glBegin(GL.GL_QUADS)

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

    GL.glEnd()
