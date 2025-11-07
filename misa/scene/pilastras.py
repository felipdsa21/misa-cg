from OpenGL import GL, GLU

from .. import primitives
from . import constantes


def desenhar_cilindro_fechado(radius: float, height: float):
    """Desenha um cilindro fechado (com tampas) alinhado ao eixo Y."""
    GL.glRotatef(-90, 1, 0, 0)  # GLU usa +Z → vira para +Y
    GLU.gluCylinder(constantes.q, radius, radius, height, 32, 1)
    GLU.gluDisk(constantes.q, 0.0, radius, 32, 1)  # tampa inferior
    GL.glTranslatef(0, 0, height)
    GLU.gluDisk(constantes.q, 0.0, radius, 32, 1)  # tampa superior


def desenhar_caixa_local(w: float, h: float, t: float):
    GL.glNormal3i(0, 0, -1)
    GL.glRectd(0, 0, w, h)  # frente z=0
    GL.glNormal3i(0, 0, 1)
    primitives.draw_rect_z(0, 0, w, h, t)  # trás  z=t

    GL.glPushMatrix()
    GL.glRotatef(-90, 0, 1, 0)
    GL.glNormal3i(-1, 0, 0)
    GL.glRectd(0, 0, t, h)
    GL.glPopMatrix()  # lado esq

    GL.glPushMatrix()
    GL.glTranslated(w, 0, 0)
    GL.glRotatef(-90, 0, 1, 0)
    GL.glNormal3i(-1, 0, 0)
    GL.glRectd(0, 0, t, h)
    GL.glPopMatrix()  # lado dir

    GL.glPushMatrix()
    GL.glRotatef(90, 1, 0, 0)
    GL.glNormal3i(0, 1, 0)
    GL.glRectd(0, 0, w, t)
    GL.glPopMatrix()  # base

    GL.glPushMatrix()
    GL.glTranslated(0, h, 0)
    GL.glRotatef(90, 1, 0, 0)
    GL.glNormal3i(0, 1, 0)
    GL.glRectd(0, 0, w, t)
    GL.glPopMatrix()  # topo


def draw_pilastra(x: float, y: float, z: float, altura_fuste: float):
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

    GL.glPushMatrix()
    GL.glTranslated(x, y, z)

    # base madeira escura
    GL.glColor3ub(70, 42, 25)
    desenhar_caixa_local(base_w, base_h, base_w)

    # pedestal amarelo
    GL.glTranslated((base_w - pedestal_w) / 2.0, base_h, (base_w - pedestal_w) / 2.0)
    GL.glColor3ub(225, 197, 126)
    desenhar_caixa_local(pedestal_w, pedestal_h, pedestal_w)

    # moldura branca
    GL.glTranslated(-(mold_w - pedestal_w) / 2.0, pedestal_h, -(mold_w - pedestal_w) / 2.0)
    GL.glColor3ub(240, 240, 240)
    desenhar_caixa_local(mold_w, mold_h, mold_w)

    # fuste (cilindro fechado, alinhado ao eixo Y)
    GL.glTranslated(mold_w / 2.0, mold_h, mold_w / 2.0)
    GL.glColor3ub(225, 197, 126)
    GL.glPushMatrix()
    desenhar_cilindro_fechado(fuste_r, altura_fuste)
    GL.glPopMatrix()

    # anel branco no topo do fuste
    GL.glPushMatrix()
    GL.glTranslated(0, altura_fuste, 0)
    GL.glColor3ub(240, 240, 240)
    desenhar_cilindro_fechado(anel_r, anel_h)
    GL.glPopMatrix()

    # prato verde que toca o teto
    GL.glPushMatrix()
    GL.glTranslated(0, altura_fuste + anel_h, 0)
    GL.glColor3ub(126, 168, 146)
    desenhar_cilindro_fechado(prato_r, prato_h)
    GL.glPopMatrix()

    GL.glPopMatrix()


def draw_pilastras_internas():
    altura_fuste = (constantes.segundo_andar_y - constantes.piso_y) - 1.07  # compensa base+anel+prato
    offset_lateral = 2.0  # distância da parede interna lateral
    primeira_z = 3.8  # posição ao longo do eixo Z dentro da parte central (frente=0)
    distancia_entre_pares = 6.0  # separar par frontal do traseiro

    x_esq = constantes.asa_size.x + offset_lateral
    x_dir = constantes.asa_size.x + constantes.parte_central_size.x - offset_lateral

    for i in range(2):
        z = primeira_z + i * distancia_entre_pares - constantes.asa_z_offset  # compensar deslocamento asa
        draw_pilastra(x_esq, constantes.piso_y, z, altura_fuste)
        draw_pilastra(x_dir, constantes.piso_y, z, altura_fuste)
