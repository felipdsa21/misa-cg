"""Balcony drawing functions - Front balcony with railing and balusters."""

from OpenGL import GL
from ..util import Vec3d
from ..primitives import draw_box


def draw_sacada():
    """Draw the front balcony with slab, railing, and balusters."""
    from ..draw import (
        parte_central_size,
        porta_size,
        janela_cima_y_offset,
    )

    x_antes_porta = (parte_central_size.x - porta_size.x) / 2.0
    largura = porta_size.x + 4.0
    profundidade = 1.25
    espessura = 0.18
    guarda_altura = 0.80
    bala_larg = 0.15
    bala_esp = 0.15
    bala_gap = 0.25

    # Altura: colocar a sacada mais alta (~ entre topo porta 3.2 e base janela superior 4.6)
    base_y = porta_size.y + 1.5
    if base_y + guarda_altura + espessura > janela_cima_y_offset - 0.5:
        guarda_altura = (janela_cima_y_offset - 0.5) - (base_y + espessura)
        if guarda_altura < 0.55:
            guarda_altura = 0.55

    from ..draw import asa_size

    centro_x = asa_size.x + x_antes_porta + porta_size.x / 2.0
    start_x = centro_x - largura / 2.0

    GL.glPushMatrix()
    GL.glTranslated(start_x, base_y, 0)

    # Branco total da sacada
    GL.glColor3ub(245, 245, 245)  # laje
    draw_box(Vec3d(0, 0, 0), Vec3d(largura, espessura, profundidade))
    GL.glColor3ub(235, 235, 235)  # moldura inferior
    draw_box(Vec3d(0, -0.10, 0), Vec3d(largura, 0.10, profundidade * 0.95))

    rail_base_y = espessura
    rail_top_y = rail_base_y + guarda_altura

    GL.glColor3ub(250, 250, 250)  # Top rail
    draw_box(Vec3d(0, rail_top_y - 0.07, -0.14), Vec3d(largura, 0.07, 0.26))

    GL.glColor3ub(250, 250, 250)  # Balaústres
    usable = largura
    count = int(usable / (bala_larg + bala_gap))
    if count < 3:
        count = 3
    spacing = (usable - count * bala_larg) / (count - 1)
    for i in range(count):
        x = i * (bala_larg + spacing)
        draw_box(
            Vec3d(x, rail_base_y, -0.07),
            Vec3d(bala_larg, guarda_altura - 0.12, bala_esp * 0.5),
        )

    GL.glColor3ub(240, 240, 240)  # Rodapé guarda
    draw_box(Vec3d(0, rail_base_y, -0.12), Vec3d(largura, 0.11, 0.22))

    GL.glPopMatrix()
