"""Wall drawing functions - Building walls with windows and doors."""

import math
from OpenGL.GL import *
from ..util import Vec3d, PI
from ..primitives import draw_rect_y, draw_rect_z
from .windows import draw_janela_com_arco, draw_janela_retangular


def mask_rect(x1: float, y1: float, w: float, h: float):
    """Helper function to create a rectangular mask for stencil."""
    glBegin(GL_QUADS)
    glVertex3d(x1, y1, 0)
    glVertex3d(x1 + w, y1, 0)
    glVertex3d(x1 + w, y1 + h, 0)
    glVertex3d(x1, y1 + h, 0)
    glEnd()


def mask_janela_arco(x: float, y_base: float, total_w: float, total_h: float, seg: int):
    """Helper function to create an arched window mask for stencil."""
    radius = total_w * 0.5  # raio = metade da largura
    rect_h = total_h - radius  # altura da parte reta
    mask_rect(x, y_base, total_w, rect_h)  # parte reta
    cx = x + radius
    cy = y_base + rect_h
    glBegin(GL_TRIANGLE_FAN)
    glVertex3d(cx, cy, 0)
    for i in range(seg + 1):
        a = PI * i / seg
        glVertex3d(cx + math.cos(a) * radius, cy + math.sin(a) * radius, 0)
    glEnd()


def draw_janela_com_arco_ajustado(pos: Vec3d):
    """Draw an arched window at a specific position."""
    from ..draw import janela_com_arco

    glPushMatrix()
    glTranslated(pos.x, pos.y, pos.z)
    draw_janela_com_arco(janela_com_arco.x, janela_com_arco.y, janela_com_arco.z)
    glPopMatrix()


def draw_janela_retangular_ajustado(pos: Vec3d):
    """Draw a rectangular window at a specific position."""
    from ..draw import janela_retangular_size

    glPushMatrix()
    glTranslated(pos.x, pos.y, pos.z)
    draw_janela_retangular(
        janela_retangular_size.x, janela_retangular_size.y, janela_retangular_size.z
    )
    glPopMatrix()


def draw_asa():
    """Draw a wing wall with rectangular windows."""
    from ..draw import (
        asa_size,
        janela_retangular_size,
        janela_baixo_y_offset,
    )

    # Calcula posições das 3 janelas retangulares na asa (distribuição uniforme pelo dist_base)
    win_w = janela_retangular_size.x
    win_h = janela_retangular_size.y
    base_y = janela_baixo_y_offset
    top_y = base_y + win_h
    dist_base = 3  # distância progressiva usada já no desenho das janelas
    win_x = []
    cursor = -win_w
    for i in range(3):
        cursor += dist_base
        win_x.append(cursor)

    # Modo preciso: usa stencil para recortar exatamente os retângulos das janelas
    glNormal3i(0, 0, -1)
    # Preparar stencil: marcamos 1 onde haverá janela
    glColorMask(GL_FALSE, GL_FALSE, GL_FALSE, GL_FALSE)
    glDepthMask(GL_FALSE)
    glStencilMask(0xFF)
    glClear(GL_STENCIL_BUFFER_BIT)
    glStencilFunc(GL_ALWAYS, 1, 0xFF)
    glStencilOp(GL_KEEP, GL_KEEP, GL_REPLACE)
    glBegin(GL_QUADS)
    for i in range(3):  # máscara cada janela
        glVertex3d(win_x[i], base_y, 0)
        glVertex3d(win_x[i] + win_w, base_y, 0)
        glVertex3d(win_x[i] + win_w, top_y, 0)
        glVertex3d(win_x[i], top_y, 0)
    glEnd()
    # Desenha parede exceto onde stencil == 1
    glColorMask(GL_TRUE, GL_TRUE, GL_TRUE, GL_TRUE)
    glDepthMask(GL_TRUE)
    glStencilFunc(GL_EQUAL, 0, 0xFF)
    glStencilOp(GL_KEEP, GL_KEEP, GL_KEEP)
    glRectd(0, 0, asa_size.x, asa_size.y)
    glStencilFunc(GL_ALWAYS, 0, 0xFF)  # libera

    # Atrás
    glNormal3i(0, 0, 1)
    draw_rect_z(0, 0, asa_size.x, asa_size.y, asa_size.z)

    # Lado
    glPushMatrix()
    glRotatef(-90, 0, 1, 0)
    glNormal3i(-1, 0, 0)
    glRectd(0, 0, asa_size.z, asa_size.y)
    glPopMatrix()

    # Cima
    glNormal3i(0, 1, 0)
    draw_rect_y(0, 0, asa_size.x, asa_size.z, asa_size.y)


def draw_parte_central():
    """Draw the central part wall with door and arched windows."""
    from ..draw import (
        parte_central_size,
        porta_size,
        janela_com_arco,
        janela_baixo_y_offset,
        janela_cima_y_offset,
    )
    from .door import draw_porta

    x_antes_porta = (
        parte_central_size.x - porta_size.x
    ) / 2.0  # início da porta na fachada frontal
    # Parâmetros das janelas com arco
    jw = janela_com_arco.x  # largura total
    jh = janela_com_arco.y  # altura total (reta + arco)
    y_low = janela_baixo_y_offset  # base das janelas inferiores
    y_top_base = janela_cima_y_offset  # base das janelas superiores
    dist_lado = (
        x_antes_porta - jw
    ) / 2.0  # deslocamento lateral entre borda e primeira janela
    dist_centro = x_antes_porta + (porta_size.x - jw) / 2.0  # janela central superior
    right_start = (
        x_antes_porta + porta_size.x + dist_lado
    )  # primeira janela lado direito

    # --- STENCIL (modo preciso) ---
    glNormal3i(0, 0, -1)
    glColorMask(GL_FALSE, GL_FALSE, GL_FALSE, GL_FALSE)
    glDepthMask(GL_FALSE)
    glStencilMask(0xFF)
    glClear(GL_STENCIL_BUFFER_BIT)
    glStencilFunc(GL_ALWAYS, 1, 0xFF)
    glStencilOp(GL_KEEP, GL_KEEP, GL_REPLACE)
    # Porta (retângulo)
    mask_rect(x_antes_porta, 0, porta_size.x, porta_size.y)
    # Janelas arco (5): esquerda baixa/alta, central alta, direita baixa/alta
    seg = 48
    mask_janela_arco(dist_lado, y_low, jw, jh, seg)
    mask_janela_arco(dist_lado, y_top_base, jw, jh, seg)
    mask_janela_arco(dist_centro, y_top_base, jw, jh, seg)
    mask_janela_arco(right_start, y_low, jw, jh, seg)
    mask_janela_arco(right_start, y_top_base, jw, jh, seg)

    # Desenha parede exceto onde máscara = 1
    glColorMask(GL_TRUE, GL_TRUE, GL_TRUE, GL_TRUE)
    glDepthMask(GL_TRUE)
    glStencilFunc(GL_EQUAL, 0, 0xFF)
    glStencilOp(GL_KEEP, GL_KEEP, GL_KEEP)
    glRectd(0, 0, parte_central_size.x, parte_central_size.y)
    glStencilFunc(GL_ALWAYS, 0, 0xFF)

    # Porta (folhas) desenhada depois da parede para aparecer no vão
    glPushAttrib(GL_CURRENT_BIT)
    draw_porta(x_antes_porta)
    glPopAttrib()

    # Atrás
    glNormal3i(0, 0, 1)
    draw_rect_z(0, 0, parte_central_size.x, parte_central_size.y, parte_central_size.z)

    # Cima
    glNormal3i(0, 1, 0)
    draw_rect_y(0, 0, parte_central_size.x, parte_central_size.z, parte_central_size.y)

    # Lados
    from ..draw import asa_z_offset, asa_size

    z_depois_asa = asa_z_offset + asa_size.z
    glPushMatrix()
    glRotatef(-90, 0, 1, 0)

    glNormal3i(-1, 0, 0)
    glRectd(0, 0, asa_z_offset, asa_size.y)  # Em frente a asa
    glRectd(0, asa_size.y, z_depois_asa, parte_central_size.y)  # Cima
    glRectd(z_depois_asa, 0, parte_central_size.z, parte_central_size.y)  # Atrás

    glTranslated(0, 0, -parte_central_size.x)
    glNormal3i(-1, 0, 0)
    glRectd(0, 0, asa_z_offset, asa_size.y)  # Em frente a asa
    glRectd(0, asa_size.y, z_depois_asa, parte_central_size.y)  # Cima
    glRectd(z_depois_asa, 0, parte_central_size.z, parte_central_size.y)  # Atrás

    glPopMatrix()


def draw_parte_externa(asa_func, parte_central_func):
    """Draw the external walls (wings and central part) with a function for each."""
    from ..draw import asa_size, parte_central_size, asa_z_offset

    glColor3ub(228, 206, 211)
    glPushMatrix()

    # Asa direita
    glTranslated(0, 0, asa_z_offset)
    asa_func()

    # Parte central
    glTranslated(asa_size.x, 0, -asa_z_offset)
    parte_central_func()

    # Asa esquerda
    glTranslated(parte_central_size.x, 0, asa_z_offset)
    glTranslated(asa_size.x, 0, 0)
    glScalef(-1, 1, 1)  # Espelha
    asa_func()

    glPopMatrix()


def draw_janelas_asa():
    """Draw rectangular windows on wing walls."""
    from ..draw import janela_retangular_size, janela_baixo_y_offset

    dist_base = 3

    janela_pos = Vec3d(-janela_retangular_size.x, janela_baixo_y_offset, 0)

    for i in range(3):
        janela_pos.x += dist_base
        draw_janela_retangular_ajustado(janela_pos)


def draw_janelas_parte_central():
    """Draw arched windows on the central part wall."""
    from ..draw import (
        parte_central_size,
        porta_size,
        janela_com_arco,
        janela_baixo_y_offset,
        janela_cima_y_offset,
    )

    # Frente
    x_antes_porta = (parte_central_size.x - porta_size.x) / 2
    glNormal3i(0, 0, -1)

    dist_lado = (x_antes_porta - janela_com_arco.x) / 2
    dist_centro = x_antes_porta + (porta_size.x - janela_com_arco.x) / 2

    janela_pos = Vec3d(dist_lado, janela_baixo_y_offset, 0)
    draw_janela_com_arco_ajustado(janela_pos)
    janela_pos.y = janela_cima_y_offset
    draw_janela_com_arco_ajustado(janela_pos)

    janela_pos.x = dist_centro
    draw_janela_com_arco_ajustado(janela_pos)

    janela_pos.x = x_antes_porta + porta_size.x + dist_lado
    janela_pos.y = janela_baixo_y_offset
    draw_janela_com_arco_ajustado(janela_pos)
    janela_pos.y = janela_cima_y_offset
    draw_janela_com_arco_ajustado(janela_pos)
