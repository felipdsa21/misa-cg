"""Roof drawing functions - Main roof, gables, and decorative elements."""

import math
from OpenGL.GL import *
from ..util import Vec3d, PI
from ..primitives import draw_box


def draw_telhado():
    """Draw the complete roof system including wing roofs, central roof, frieze, and gable."""
    from ..draw import (
        asa_size,
        parte_central_size,
        asa_z_offset,
        janela_com_arco,
        janela_cima_y_offset,
    )

    y_base = asa_size.y + 0.05
    beiral = 0.25
    ridge_alt = 0.9
    z_front = asa_z_offset - beiral
    z_back = asa_z_offset + asa_size.z + beiral
    z_ridge = (z_front + z_back) / 2.0

    glColor3ub(120, 50, 45)
    glBegin(GL_QUADS)
    x_a = 0
    x_b = asa_size.x
    ridge_y = y_base + ridge_alt
    glNormal3d(0, ridge_alt, (z_ridge - z_front))
    glVertex3d(x_a, y_base, z_front)
    glVertex3d(x_b, y_base, z_front)
    glVertex3d(x_b, ridge_y, z_ridge)
    glVertex3d(x_a, ridge_y, z_ridge)
    glNormal3d(0, ridge_alt, (z_back - z_ridge) * -1)
    glVertex3d(x_a, ridge_y, z_ridge)
    glVertex3d(x_b, ridge_y, z_ridge)
    glVertex3d(x_b, y_base, z_back)
    glVertex3d(x_a, y_base, z_back)
    x_a = asa_size.x + parte_central_size.x
    x_b = x_a + asa_size.x
    glNormal3d(0, ridge_alt, (z_ridge - z_front))
    glVertex3d(x_a, y_base, z_front)
    glVertex3d(x_b, y_base, z_front)
    glVertex3d(x_b, ridge_y, z_ridge)
    glVertex3d(x_a, ridge_y, z_ridge)
    glNormal3d(0, ridge_alt, (z_back - z_ridge) * -1)
    glVertex3d(x_a, ridge_y, z_ridge)
    glVertex3d(x_b, ridge_y, z_ridge)
    glVertex3d(x_b, y_base, z_back)
    glVertex3d(x_a, y_base, z_back)
    glEnd()

    # Telhado central (duas águas mais alto que asas)
    centro_base_y = parte_central_size.y + 0.05  # topo bloco central
    centro_ridge_alt = 2.4  # altura extra
    centro_beiral = 0.35
    c_front = -centro_beiral
    c_back = parte_central_size.z + centro_beiral
    c_ridge_z = (c_front + c_back) / 2.0
    c_ridge_y = centro_base_y + centro_ridge_alt
    c_start_x = asa_size.x - centro_beiral
    c_end_x = asa_size.x + parte_central_size.x + centro_beiral
    glColor3ub(110, 40, 38)
    glBegin(GL_QUADS)
    glNormal3d(0, centro_ridge_alt, (c_ridge_z - c_front))
    glVertex3d(c_start_x, centro_base_y, c_front)
    glVertex3d(c_end_x, centro_base_y, c_front)
    glVertex3d(c_end_x, c_ridge_y, c_ridge_z)
    glVertex3d(c_start_x, c_ridge_y, c_ridge_z)
    glNormal3d(0, centro_ridge_alt, (c_back - c_ridge_z) * -1)
    glVertex3d(c_start_x, c_ridge_y, c_ridge_z)
    glVertex3d(c_end_x, c_ridge_y, c_ridge_z)
    glVertex3d(c_end_x, centro_base_y, c_back)
    glVertex3d(c_start_x, centro_base_y, c_back)
    glEnd()

    # Friso (linha branca) acima das janelas superiores – percorre largura parte central
    glColor3ub(245, 240, 235)
    friso_alt = 0.30
    friso_y = janela_cima_y_offset + janela_com_arco.y + 0.25  # base do friso
    if friso_y > parte_central_size.y - 0.4:
        friso_y = parte_central_size.y - 0.4  # não invadir telhado central
    draw_box(
        Vec3d(asa_size.x, friso_y, 0.02), Vec3d(parte_central_size.x, friso_alt, 0.18)
    )

    # Frontão curvo mais baixo (mantido)
    frontao_larg = parte_central_size.x * 0.65
    frontao_alt = 1.8
    frontao_esp = 0.16
    frontao_base_x = asa_size.x + (parte_central_size.x - frontao_larg) / 2.0
    frontao_base_y = friso_y + friso_alt * 0.15
    frontao_base_z = 0.05
    seg = 32
    raio = frontao_larg / 2.0
    arco_h = frontao_alt * 0.65
    arco_base_y = frontao_base_y + frontao_alt * 0.35
    cx = frontao_base_x + raio
    glColor3ub(235, 222, 210)
    draw_box(
        Vec3d(frontao_base_x, frontao_base_y, frontao_base_z),
        Vec3d(frontao_larg, frontao_alt * 0.35, frontao_esp),
    )
    glBegin(GL_QUADS)
    for i in range(seg):
        a1 = PI * i / seg
        a2 = PI * (i + 1) / seg
        x1 = cx + math.cos(a1) * raio
        y1 = arco_base_y + math.sin(a1) * arco_h
        x2 = cx + math.cos(a2) * raio
        y2 = arco_base_y + math.sin(a2) * arco_h
        glVertex3d(x1, y1, frontao_base_z)
        glVertex3d(x2, y2, frontao_base_z)
        glVertex3d(x2, y2, frontao_base_z + frontao_esp)
        glVertex3d(x1, y1, frontao_base_z + frontao_esp)
    glEnd()
    glBegin(GL_TRIANGLE_FAN)
    glVertex3d(cx, arco_base_y, frontao_base_z)
    for i in range(seg + 1):
        a = PI * i / seg
        glVertex3d(
            cx + math.cos(a) * raio, arco_base_y + math.sin(a) * arco_h, frontao_base_z
        )
    glEnd()
    glBegin(GL_TRIANGLE_FAN)
    glVertex3d(cx, arco_base_y, frontao_base_z + frontao_esp)
    for i in range(seg + 1):
        a = PI * i / seg
        glVertex3d(
            cx + math.cos(a) * raio,
            arco_base_y + math.sin(a) * arco_h,
            frontao_base_z + frontao_esp,
        )
    glEnd()
