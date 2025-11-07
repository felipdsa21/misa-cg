import math

from OpenGL import GL

from .. import primitives, util
from . import constantes, janelas, porta, procedural

janela_retangular_size = util.Vec3d(1.2, 2, 0.3)


def draw_paredes() -> None:
    GL.glBindTexture(GL.GL_TEXTURE_2D, procedural.load_plaster_texture())
    draw_parte_externa(draw_asa, draw_parte_central)
    draw_parte_externa(draw_janelas_asa, draw_janelas_parte_central)
    GL.glBindTexture(GL.GL_TEXTURE_2D, 0)


def mascarar_retangulo(x1: float, y1: float, w: float, h: float):
    with primitives.begin(GL.GL_QUADS):
        GL.glVertex3d(x1, y1, 0)
        GL.glVertex3d(x1 + w, y1, 0)
        GL.glVertex3d(x1 + w, y1 + h, 0)
        GL.glVertex3d(x1, y1 + h, 0)


def mascarar_janela_arco(x: float, y_base: float, total_w: float, total_h: float, seg: int):
    radius = total_w * 0.5  # raio = metade da largura
    rect_h = total_h - radius  # altura da parte reta
    mascarar_retangulo(x, y_base, total_w, rect_h)  # parte reta
    cx = x + radius
    cy = y_base + rect_h
    with primitives.begin(GL.GL_TRIANGLE_FAN):
        GL.glVertex3d(cx, cy, 0)
        for i in range(seg + 1):
            a = math.pi * i / seg
            GL.glVertex3d(cx + math.cos(a) * radius, cy + math.sin(a) * radius, 0)


def desenhar_janela_com_arco_ajustada(pos: util.Vec3d):
    with primitives.push_matrix():
        GL.glTranslated(pos.x, pos.y, pos.z)
        janelas.draw_janela_com_arco(
            constantes.janela_com_arco.x, constantes.janela_com_arco.y, constantes.janela_com_arco.z
        )


def desenhar_janela_retangular_ajustada(pos: util.Vec3d):
    with primitives.push_matrix():
        GL.glTranslated(pos.x, pos.y, pos.z)
        janelas.draw_janela_retangular(
            janela_retangular_size.x, janela_retangular_size.y, janela_retangular_size.z
        )


def draw_asa():
    # Calcula posições das 3 janelas retangulares na asa (distribuição uniforme pelo dist_base)
    win_w = janela_retangular_size.x
    win_h = janela_retangular_size.y
    base_y = constantes.janela_baixo_y_offset
    top_y = base_y + win_h
    dist_base = 3  # distância progressiva usada já no desenho das janelas
    win_x = [-win_w + dist_base * (i + 1) for i in range(3)]

    # Modo preciso: usa stencil para recortar exatamente os retângulos das janelas
    GL.glNormal3i(0, 0, -1)
    # Preparar stencil: marcamos 1 onde haverá janela
    GL.glColorMask(GL.GL_FALSE, GL.GL_FALSE, GL.GL_FALSE, GL.GL_FALSE)
    GL.glDepthMask(GL.GL_FALSE)
    GL.glStencilMask(0xFF)
    GL.glClear(GL.GL_STENCIL_BUFFER_BIT)
    GL.glStencilFunc(GL.GL_ALWAYS, 1, 0xFF)
    GL.glStencilOp(GL.GL_KEEP, GL.GL_KEEP, GL.GL_REPLACE)
    with primitives.begin(GL.GL_QUADS):
        for i in range(3):  # máscara cada janela
            GL.glVertex3d(win_x[i], base_y, 0)
            GL.glVertex3d(win_x[i] + win_w, base_y, 0)
            GL.glVertex3d(win_x[i] + win_w, top_y, 0)
            GL.glVertex3d(win_x[i], top_y, 0)
    # Desenha parede exceto onde stencil == 1
    GL.glColorMask(GL.GL_TRUE, GL.GL_TRUE, GL.GL_TRUE, GL.GL_TRUE)
    GL.glDepthMask(GL.GL_TRUE)
    GL.glStencilFunc(GL.GL_EQUAL, 0, 0xFF)
    GL.glStencilOp(GL.GL_KEEP, GL.GL_KEEP, GL.GL_KEEP)
    # Adicionar coordenadas de textura
    with primitives.begin(GL.GL_QUADS):
        GL.glTexCoord2f(0, 0)
        GL.glVertex3d(0, 0, 0)
        GL.glTexCoord2f(constantes.asa_size.x / 2, 0)
        GL.glVertex3d(constantes.asa_size.x, 0, 0)
        GL.glTexCoord2f(constantes.asa_size.x / 2, constantes.asa_size.y / 2)
        GL.glVertex3d(constantes.asa_size.x, constantes.asa_size.y, 0)
        GL.glTexCoord2f(0, constantes.asa_size.y / 2)
        GL.glVertex3d(0, constantes.asa_size.y, 0)
    GL.glStencilFunc(GL.GL_ALWAYS, 0, 0xFF)  # libera

    # Atrás
    GL.glNormal3i(0, 0, 1)
    with primitives.begin(GL.GL_QUADS):
        GL.glTexCoord2f(0, 0)
        GL.glVertex3d(0, 0, constantes.asa_size.z)
        GL.glTexCoord2f(constantes.asa_size.x / 2, 0)
        GL.glVertex3d(constantes.asa_size.x, 0, constantes.asa_size.z)
        GL.glTexCoord2f(constantes.asa_size.x / 2, constantes.asa_size.y / 2)
        GL.glVertex3d(constantes.asa_size.x, constantes.asa_size.y, constantes.asa_size.z)
        GL.glTexCoord2f(0, constantes.asa_size.y / 2)
        GL.glVertex3d(0, constantes.asa_size.y, constantes.asa_size.z)

    # Lado
    with primitives.push_matrix():
        GL.glRotatef(-90, 0, 1, 0)
        GL.glNormal3i(-1, 0, 0)
        with primitives.begin(GL.GL_QUADS):
            GL.glTexCoord2f(0, 0)
            GL.glVertex3d(0, 0, 0)
            GL.glTexCoord2f(constantes.asa_size.z / 2, 0)
            GL.glVertex3d(constantes.asa_size.z, 0, 0)
            GL.glTexCoord2f(constantes.asa_size.z / 2, constantes.asa_size.y / 2)
            GL.glVertex3d(constantes.asa_size.z, constantes.asa_size.y, 0)
            GL.glTexCoord2f(0, constantes.asa_size.y / 2)
            GL.glVertex3d(0, constantes.asa_size.y, 0)

    # Cima
    GL.glNormal3i(0, 1, 0)
    primitives.draw_rect_y(0, 0, constantes.asa_size.x, constantes.asa_size.z, constantes.asa_size.y)


def draw_parte_central():
    x_antes_porta = (
        constantes.parte_central_size.x - constantes.porta_size.x
    ) / 2.0  # início da porta na fachada frontal
    # Parâmetros das janelas com arco
    jw = constantes.janela_com_arco.x  # largura total
    jh = constantes.janela_com_arco.y  # altura total (reta + arco)
    y_low = constantes.janela_baixo_y_offset  # base das janelas inferiores
    y_top_base = constantes.janela_cima_y_offset  # base das janelas superiores
    dist_lado = (x_antes_porta - jw) / 2.0  # deslocamento lateral entre borda e primeira janela
    dist_centro = x_antes_porta + (constantes.porta_size.x - jw) / 2.0  # janela central superior
    right_start = x_antes_porta + constantes.porta_size.x + dist_lado  # primeira janela lado direito

    # --- STENCIL (modo preciso) ---
    GL.glNormal3i(0, 0, -1)
    GL.glColorMask(GL.GL_FALSE, GL.GL_FALSE, GL.GL_FALSE, GL.GL_FALSE)
    GL.glDepthMask(GL.GL_FALSE)
    GL.glStencilMask(0xFF)
    GL.glClear(GL.GL_STENCIL_BUFFER_BIT)
    GL.glStencilFunc(GL.GL_ALWAYS, 1, 0xFF)
    GL.glStencilOp(GL.GL_KEEP, GL.GL_KEEP, GL.GL_REPLACE)
    # Porta (retângulo)
    mascarar_retangulo(x_antes_porta, 0, constantes.porta_size.x, constantes.porta_size.y)
    # Janelas arco (5): esquerda baixa/alta, central alta, direita baixa/alta
    seg = 48
    mascarar_janela_arco(dist_lado, y_low, jw, jh, seg)
    mascarar_janela_arco(dist_lado, y_top_base, jw, jh, seg)
    mascarar_janela_arco(dist_centro, y_top_base, jw, jh, seg)
    mascarar_janela_arco(right_start, y_low, jw, jh, seg)
    mascarar_janela_arco(right_start, y_top_base, jw, jh, seg)

    # Desenha parede exceto onde máscara = 1
    GL.glColorMask(GL.GL_TRUE, GL.GL_TRUE, GL.GL_TRUE, GL.GL_TRUE)
    GL.glDepthMask(GL.GL_TRUE)
    GL.glStencilFunc(GL.GL_EQUAL, 0, 0xFF)
    GL.glStencilOp(GL.GL_KEEP, GL.GL_KEEP, GL.GL_KEEP)
    # Adicionar coordenadas de textura
    with primitives.begin(GL.GL_QUADS):
        GL.glTexCoord2f(0, 0)
        GL.glVertex3d(0, 0, 0)
        GL.glTexCoord2f(constantes.parte_central_size.x / 2, 0)
        GL.glVertex3d(constantes.parte_central_size.x, 0, 0)
        GL.glTexCoord2f(constantes.parte_central_size.x / 2, constantes.parte_central_size.y / 2)
        GL.glVertex3d(constantes.parte_central_size.x, constantes.parte_central_size.y, 0)
        GL.glTexCoord2f(0, constantes.parte_central_size.y / 2)
        GL.glVertex3d(0, constantes.parte_central_size.y, 0)
    GL.glStencilFunc(GL.GL_ALWAYS, 0, 0xFF)

    # Porta (folhas) desenhada depois da parede para aparecer no vão
    GL.glPushAttrib(GL.GL_CURRENT_BIT)
    porta.draw_porta(x_antes_porta)
    GL.glPopAttrib()

    # Atrás
    GL.glNormal3i(0, 0, 1)
    with primitives.begin(GL.GL_QUADS):
        GL.glTexCoord2f(0, 0)
        GL.glVertex3d(0, 0, constantes.parte_central_size.z)
        GL.glTexCoord2f(constantes.parte_central_size.x / 2, 0)
        GL.glVertex3d(constantes.parte_central_size.x, 0, constantes.parte_central_size.z)
        GL.glTexCoord2f(constantes.parte_central_size.x / 2, constantes.parte_central_size.y / 2)
        GL.glVertex3d(
            constantes.parte_central_size.x, constantes.parte_central_size.y, constantes.parte_central_size.z
        )
        GL.glTexCoord2f(0, constantes.parte_central_size.y / 2)
        GL.glVertex3d(0, constantes.parte_central_size.y, constantes.parte_central_size.z)

    # Cima
    GL.glNormal3i(0, 1, 0)
    primitives.draw_rect_y(
        0,
        0,
        constantes.parte_central_size.x,
        constantes.parte_central_size.z,
        constantes.parte_central_size.y,
    )

    # Lados
    z_depois_asa = constantes.asa_z_offset + constantes.asa_size.z
    with primitives.push_matrix():
        GL.glRotatef(-90, 0, 1, 0)

        GL.glNormal3i(-1, 0, 0)
        # Em frente a asa
        with primitives.begin(GL.GL_QUADS):
            GL.glTexCoord2f(0, 0)
            GL.glVertex3d(0, 0, 0)
            GL.glTexCoord2f(constantes.asa_z_offset / 2, 0)
            GL.glVertex3d(constantes.asa_z_offset, 0, 0)
            GL.glTexCoord2f(constantes.asa_z_offset / 2, constantes.asa_size.y / 2)
            GL.glVertex3d(constantes.asa_z_offset, constantes.asa_size.y, 0)
            GL.glTexCoord2f(0, constantes.asa_size.y / 2)
            GL.glVertex3d(0, constantes.asa_size.y, 0)
        # Cima
        with primitives.begin(GL.GL_QUADS):
            GL.glTexCoord2f(0, 0)
            GL.glVertex3d(0, constantes.asa_size.y, 0)
            GL.glTexCoord2f((z_depois_asa) / 2, 0)
            GL.glVertex3d(z_depois_asa, constantes.asa_size.y, 0)
            GL.glTexCoord2f((z_depois_asa) / 2, constantes.parte_central_size.y / 2)
            GL.glVertex3d(z_depois_asa, constantes.parte_central_size.y, 0)
            GL.glTexCoord2f(0, constantes.parte_central_size.y / 2)
            GL.glVertex3d(0, constantes.parte_central_size.y, 0)
        # Atrás
        with primitives.begin(GL.GL_QUADS):
            GL.glTexCoord2f(0, 0)
            GL.glVertex3d(z_depois_asa, 0, 0)
            GL.glTexCoord2f((constantes.parte_central_size.z - z_depois_asa) / 2, 0)
            GL.glVertex3d(constantes.parte_central_size.z, 0, 0)
            GL.glTexCoord2f(
                (constantes.parte_central_size.z - z_depois_asa) / 2, constantes.parte_central_size.y / 2
            )
            GL.glVertex3d(constantes.parte_central_size.z, constantes.parte_central_size.y, 0)
            GL.glTexCoord2f(0, constantes.parte_central_size.y / 2)
            GL.glVertex3d(z_depois_asa, constantes.parte_central_size.y, 0)

        GL.glTranslated(0, 0, -constantes.parte_central_size.x)
        GL.glNormal3i(-1, 0, 0)
        # Em frente a asa
        with primitives.begin(GL.GL_QUADS):
            GL.glTexCoord2f(0, 0)
            GL.glVertex3d(0, 0, 0)
            GL.glTexCoord2f(constantes.asa_z_offset / 2, 0)
            GL.glVertex3d(constantes.asa_z_offset, 0, 0)
            GL.glTexCoord2f(constantes.asa_z_offset / 2, constantes.asa_size.y / 2)
            GL.glVertex3d(constantes.asa_z_offset, constantes.asa_size.y, 0)
            GL.glTexCoord2f(0, constantes.asa_size.y / 2)
            GL.glVertex3d(0, constantes.asa_size.y, 0)
        # Cima
        with primitives.begin(GL.GL_QUADS):
            GL.glTexCoord2f(0, 0)
            GL.glVertex3d(0, constantes.asa_size.y, 0)
            GL.glTexCoord2f((z_depois_asa) / 2, 0)
            GL.glVertex3d(z_depois_asa, constantes.asa_size.y, 0)
            GL.glTexCoord2f((z_depois_asa) / 2, constantes.parte_central_size.y / 2)
            GL.glVertex3d(z_depois_asa, constantes.parte_central_size.y, 0)
            GL.glTexCoord2f(0, constantes.parte_central_size.y / 2)
            GL.glVertex3d(0, constantes.parte_central_size.y, 0)
        # Atrás
        with primitives.begin(GL.GL_QUADS):
            GL.glTexCoord2f(0, 0)
            GL.glVertex3d(z_depois_asa, 0, 0)
            GL.glTexCoord2f((constantes.parte_central_size.z - z_depois_asa) / 2, 0)
            GL.glVertex3d(constantes.parte_central_size.z, 0, 0)
            GL.glTexCoord2f(
                (constantes.parte_central_size.z - z_depois_asa) / 2, constantes.parte_central_size.y / 2
            )
            GL.glVertex3d(constantes.parte_central_size.z, constantes.parte_central_size.y, 0)
            GL.glTexCoord2f(0, constantes.parte_central_size.y / 2)
            GL.glVertex3d(z_depois_asa, constantes.parte_central_size.y, 0)


def draw_parte_externa(asa_func, parte_central_func):
    GL.glColor3ub(228, 206, 211)
    with primitives.push_matrix():
        # Asa direita
        GL.glTranslated(0, 0, constantes.asa_z_offset)
        asa_func()

        # Parte central
        GL.glTranslated(constantes.asa_size.x, 0, -constantes.asa_z_offset)
        parte_central_func()

        # Asa esquerda
        GL.glTranslated(constantes.parte_central_size.x, 0, constantes.asa_z_offset)
        GL.glTranslated(constantes.asa_size.x, 0, 0)
        GL.glScalef(-1, 1, 1)  # Espelha
        asa_func()


def draw_janelas_asa():
    dist_base = 3

    janela_pos_x = -janela_retangular_size.x

    for i in range(3):
        janela_pos_x += dist_base
        janela_pos = util.Vec3d(janela_pos_x, constantes.janela_baixo_y_offset, 0)
        desenhar_janela_retangular_ajustada(janela_pos)


def draw_janelas_parte_central():
    # Frente
    x_antes_porta = (constantes.parte_central_size.x - constantes.porta_size.x) / 2
    GL.glNormal3i(0, 0, -1)

    dist_lado = (x_antes_porta - constantes.janela_com_arco.x) / 2
    dist_centro = x_antes_porta + (constantes.porta_size.x - constantes.janela_com_arco.x) / 2

    # Janelas esquerda (baixa e alta)
    for y_offset in (constantes.janela_baixo_y_offset, constantes.janela_cima_y_offset):
        desenhar_janela_com_arco_ajustada(util.Vec3d(dist_lado, y_offset, 0))

    # Janela central (alta)
    desenhar_janela_com_arco_ajustada(util.Vec3d(dist_centro, constantes.janela_cima_y_offset, 0))

    # Janelas direita (baixa e alta)
    x_direita = x_antes_porta + constantes.porta_size.x + dist_lado
    for y_offset in (constantes.janela_baixo_y_offset, constantes.janela_cima_y_offset):
        desenhar_janela_com_arco_ajustada(util.Vec3d(x_direita, y_offset, 0))
