"""Pillar drawing functions - Internal pillars for structural support."""

from OpenGL.GL import *
from OpenGL.GLU import *
from ..util import Vec3d
from ..primitives import draw_rect_z

# Global quadric object (set by draw.init())
q = None


def draw_box_local(w: float, h: float, t: float):
    """Helper function to draw a local box aligned to axes."""
    glNormal3i(0, 0, -1)
    glRectd(0, 0, w, h)  # frente z=0
    glNormal3i(0, 0, 1)
    draw_rect_z(0, 0, w, h, t)  # trás  z=t

    glPushMatrix()
    glRotatef(-90, 0, 1, 0)
    glNormal3i(-1, 0, 0)
    glRectd(0, 0, t, h)
    glPopMatrix()  # lado esq

    glPushMatrix()
    glTranslated(w, 0, 0)
    glRotatef(-90, 0, 1, 0)
    glNormal3i(-1, 0, 0)
    glRectd(0, 0, t, h)
    glPopMatrix()  # lado dir

    glPushMatrix()
    glRotatef(90, 1, 0, 0)
    glNormal3i(0, 1, 0)
    glRectd(0, 0, w, t)
    glPopMatrix()  # base

    glPushMatrix()
    glTranslated(0, h, 0)
    glRotatef(90, 1, 0, 0)
    glNormal3i(0, 1, 0)
    glRectd(0, 0, w, t)
    glPopMatrix()  # topo


def draw_pilastra(x: float, y: float, z: float, altura_fuste: float):
    """Draw a complete pillar with base, pedestal, shaft, ring, and plate."""
    global q
    # proporções (m)
    base_w = 0.85
    base_h = 0.12  # base madeira escura
    pedestal_w = 0.70
    pedestal_h = 0.75  # bloco amarelo
    mold_w = 0.90
    mold_h = 0.10  # moldura branca
    fuste_r = 0.20  # coluna cilíndrica
    anel_r = 0.30
    anel_h = 0.06  # anel branco
    prato_r = 0.45
    prato_h = 0.04  # prato verde (teto)

    glPushMatrix()
    glTranslated(x, y, z)

    # base madeira escura
    glColor3ub(70, 42, 25)
    draw_box_local(base_w, base_h, base_w)

    # pedestal amarelo
    glTranslated((base_w - pedestal_w) / 2.0, base_h, (base_w - pedestal_w) / 2.0)
    glColor3ub(225, 197, 126)
    draw_box_local(pedestal_w, pedestal_h, pedestal_w)

    # moldura branca
    glTranslated(-(mold_w - pedestal_w) / 2.0, pedestal_h, -(mold_w - pedestal_w) / 2.0)
    glColor3ub(240, 240, 240)
    draw_box_local(mold_w, mold_h, mold_w)

    # fuste (cilindro fechado, alinhado ao eixo Y)
    glTranslated(mold_w / 2.0, mold_h, mold_w / 2.0)
    glColor3ub(225, 197, 126)
    glPushMatrix()
    glRotatef(-90, 1, 0, 0)  # GLU usa +Z → vira para +Y
    gluCylinder(q, fuste_r, fuste_r, altura_fuste, 32, 1)
    gluDisk(q, 0.0, fuste_r, 32, 1)  # tampa inferior
    glTranslatef(0, 0, altura_fuste)
    gluDisk(q, 0.0, fuste_r, 32, 1)  # tampa superior
    glPopMatrix()

    # anel branco no topo do fuste
    glPushMatrix()
    glTranslated(0, altura_fuste, 0)
    glColor3ub(240, 240, 240)
    glRotatef(-90, 1, 0, 0)
    gluCylinder(q, anel_r, anel_r, anel_h, 32, 1)
    gluDisk(q, 0.0, anel_r, 32, 1)
    glTranslatef(0, 0, anel_h)
    gluDisk(q, 0.0, anel_r, 32, 1)
    glPopMatrix()

    # prato verde que toca o teto
    glPushMatrix()
    glTranslated(0, altura_fuste + anel_h, 0)
    glColor3ub(126, 168, 146)
    glRotatef(-90, 1, 0, 0)
    gluCylinder(q, prato_r, prato_r, prato_h, 32, 1)
    gluDisk(q, 0.0, prato_r, 32, 1)
    glTranslatef(0, 0, prato_h)
    gluDisk(q, 0.0, prato_r, 32, 1)
    glPopMatrix()

    glPopMatrix()


def draw_pilastras_internas():
    """Draw all internal pillars in the central part of the building."""
    from ..draw import (
        piso_y,
        segundo_andar_y,
        asa_size,
        parte_central_size,
        asa_z_offset,
    )

    altura_fuste = (segundo_andar_y - piso_y) - 1.07  # compensa base+anel+prato
    offset_lateral = 2.0  # distância da parede interna lateral
    primeira_z = 3.8  # posição ao longo do eixo Z dentro da parte central (frente=0)
    distancia_entre_pares = 6.0  # separar par frontal do traseiro

    x_esq = asa_size.x + offset_lateral
    x_dir = asa_size.x + (parte_central_size.x - offset_lateral)

    for i in range(2):
        z = (
            primeira_z + i * distancia_entre_pares - asa_z_offset
        )  # compensar deslocamento asa
        draw_pilastra(x_esq, piso_y, z, altura_fuste)
        draw_pilastra(x_dir, piso_y, z, altura_fuste)
