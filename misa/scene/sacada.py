from OpenGL import GL

from .. import primitives, util
from . import constantes


def draw_sacada():
    x_antes_porta = (constantes.parte_central_size.x - constantes.porta_size.x) / 2.0
    largura = constantes.porta_size.x + 4.0
    profundidade = 1.25
    espessura = 0.18
    guarda_altura = 0.80
    bala_larg = 0.15
    bala_esp = 0.15
    bala_gap = 0.25
    borda_offset = 0.04  # afastamento da guarda em relação à borda externa da sacada

    # Altura: colocar a sacada mais alta (~ entre topo porta 3.2 e base janela superior 4.6)
    base_y = constantes.porta_size.y + 1.5
    if base_y + guarda_altura + espessura > constantes.janela_cima_y_offset - 0.5:
        guarda_altura = (constantes.janela_cima_y_offset - 0.5) - (base_y + espessura)
        if guarda_altura < 0.55:
            guarda_altura = 0.55

    centro_x = constantes.asa_size.x + x_antes_porta + constantes.porta_size.x / 2.0
    start_x = centro_x - largura / 2.0

    with primitives.push_matrix():
        GL.glTranslated(start_x, base_y, 0)

        # Branco total da sacada
        GL.glColor3ub(245, 245, 245)  # laje
        primitives.draw_box(util.Vec3d(0, 0, 0), util.Vec3d(largura, espessura, profundidade))
        GL.glColor3ub(235, 235, 235)  # moldura inferior
        primitives.draw_box(util.Vec3d(0, -0.10, 0), util.Vec3d(largura, 0.10, profundidade * 0.95))

        rail_base_y = espessura
        rail_top_y = rail_base_y + guarda_altura

        GL.glColor3ub(250, 250, 250)  # Corrimão superior
        corrimao_esp = 0.18
        corrimao_pos_z = -profundidade + borda_offset + corrimao_esp
        primitives.draw_box(util.Vec3d(0, rail_top_y - 0.07, corrimao_pos_z), util.Vec3d(largura, 0.07, corrimao_esp))

        GL.glColor3ub(250, 250, 250)  # Balaústres
        count = max(3, int(largura / (bala_larg + bala_gap)))
        spacing = (largura - count * bala_larg) / (count - 1)
        for i in range(count):
            x = i * (bala_larg + spacing)
            primitives.draw_box(
                util.Vec3d(x, rail_base_y, -profundidade + borda_offset + bala_esp * 0.5),
                util.Vec3d(bala_larg, guarda_altura - 0.12, bala_esp * 0.5),
            )

        GL.glColor3ub(240, 240, 240)  # Rodapé da guarda
        rodape_esp = 0.16
        rodape_pos_z = -profundidade + borda_offset + rodape_esp
        primitives.draw_box(util.Vec3d(0, rail_base_y, rodape_pos_z), util.Vec3d(largura, 0.11, rodape_esp))
