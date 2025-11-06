from OpenGL.GL import *
from .util import Vec3d


def draw_rect_y(x1: float, z1: float, x2: float, z2: float, y: float):
    glBegin(GL_QUADS)
    glVertex3d(x1, y, z1)
    glVertex3d(x2, y, z1)
    glVertex3d(x2, y, z2)
    glVertex3d(x1, y, z2)
    glEnd()


def draw_rect_z(x1: float, y1: float, x2: float, y2: float, z: float):
    glBegin(GL_QUADS)
    glVertex3d(x1, y1, z)
    glVertex3d(x2, y1, z)
    glVertex3d(x2, y2, z)
    glVertex3d(x1, y2, z)
    glEnd()


def draw_box(pos: Vec3d, size: Vec3d):
    glBegin(GL_QUADS)

    # Frente
    glVertex3d(pos.x, pos.y, pos.z)
    glVertex3d(pos.x + size.x, pos.y, pos.z)
    glVertex3d(pos.x + size.x, pos.y + size.y, pos.z)
    glVertex3d(pos.x, pos.y + size.y, pos.z)

    # Trás
    glVertex3d(pos.x, pos.y, pos.z - size.z)
    glVertex3d(pos.x + size.x, pos.y, pos.z - size.z)
    glVertex3d(pos.x + size.x, pos.y + size.y, pos.z - size.z)
    glVertex3d(pos.x, pos.y + size.y, pos.z - size.z)

    # Esquerda
    glVertex3d(pos.x, pos.y, pos.z)
    glVertex3d(pos.x, pos.y, pos.z - size.z)
    glVertex3d(pos.x, pos.y + size.y, pos.z - size.z)
    glVertex3d(pos.x, pos.y + size.y, pos.z)

    # Direita
    glVertex3d(pos.x + size.x, pos.y, pos.z)
    glVertex3d(pos.x + size.x, pos.y, pos.z - size.z)
    glVertex3d(pos.x + size.x, pos.y + size.y, pos.z - size.z)
    glVertex3d(pos.x + size.x, pos.y + size.y, pos.z)

    # Topo
    glVertex3d(pos.x, pos.y + size.y, pos.z)
    glVertex3d(pos.x + size.x, pos.y + size.y, pos.z)
    glVertex3d(pos.x + size.x, pos.y + size.y, pos.z - size.z)
    glVertex3d(pos.x, pos.y + size.y, pos.z - size.z)

    # Base
    glVertex3d(pos.x, pos.y, pos.z)
    glVertex3d(pos.x + size.x, pos.y, pos.z)
    glVertex3d(pos.x + size.x, pos.y, pos.z - size.z)
    glVertex3d(pos.x, pos.y, pos.z - size.z)

    glEnd()
