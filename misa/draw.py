import math
import os.path
from OpenGL.GL import *
from OpenGL.GLU import *
from .util import Vec2d, Vec3d, PI, EPSILON
from .obj import draw_pilastra, draw_janela_com_arco, draw_janela_retangular
from .objImporter import load_model, draw_model_faces
from .porta import draw_porta, draw_botao
from .primitives import draw_box, draw_rect_y, draw_rect_z

# Global quadric object
q = None

grama_size = 50
luz_ambiente = [0.15, 0.15, 0.15, 1.0]
luz_difusa = [0.8, 0.8, 0.8, 1.0]
luz_especular = [0.1, 0.1, 0.1, 1.0]
posicao_luz = [0.0, 1.7, -5.0, 0.0]

piso_y = 1.0
segundo_andar_y = 7.0
abertura_escada_size = Vec2d(1, 3)

parte_central_size = Vec3d(13, 12.5, 20)
asa_size = Vec3d(10.5, 7, 15)
asa_z_offset = 1.0

porta_size = Vec3d(2.8, 3.2, 0)
espaco_porta_size = Vec2d(3, 3)

janela_com_arco = Vec3d(1.2, 2.6, 0.3)
janela_retangular_size = Vec3d(1.2, 2, 0.3)
janela_baixo_y_offset = 1.4
janela_cima_y_offset = janela_baixo_y_offset + 1.6 + 3.2


def draw_pilastras_internas():
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


def draw_sacada():
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

    centro_x = asa_size.x + x_antes_porta + porta_size.x / 2.0
    start_x = centro_x - largura / 2.0

    glPushMatrix()
    glTranslated(start_x, base_y, 0)

    # Branco total da sacada
    glColor3ub(245, 245, 245)  # laje
    draw_box(Vec3d(0, 0, 0), Vec3d(largura, espessura, profundidade))
    glColor3ub(235, 235, 235)  # moldura inferior
    draw_box(Vec3d(0, -0.10, 0), Vec3d(largura, 0.10, profundidade * 0.95))

    rail_base_y = espessura
    rail_top_y = rail_base_y + guarda_altura

    glColor3ub(250, 250, 250)  # Top rail
    draw_box(Vec3d(0, rail_top_y - 0.07, -0.14), Vec3d(largura, 0.07, 0.26))

    glColor3ub(250, 250, 250)  # Balaústres
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

    glColor3ub(240, 240, 240)  # Rodapé guarda
    draw_box(Vec3d(0, rail_base_y, -0.12), Vec3d(largura, 0.11, 0.22))

    glPopMatrix()


def draw_telhado():
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


def init():
    global q
    from . import obj

    glClearColor(0.53, 0.81, 0.98, 1.0)

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_NORMALIZE)
    glShadeModel(GL_SMOOTH)

    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    glLightfv(GL_LIGHT0, GL_AMBIENT, luz_ambiente)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, luz_difusa)
    glLightfv(GL_LIGHT0, GL_SPECULAR, luz_especular)

    q = gluNewQuadric()
    gluQuadricNormals(q, GLU_SMOOTH)
    obj.q = q  # Share quadric with obj module

    glClearStencil(0)
    glEnable(GL_STENCIL_TEST)


def on_setup_camera():
    glLightfv(GL_LIGHT0, GL_POSITION, posicao_luz)


def draw_grama():
    glColor3ub(65, 152, 10)
    glNormal3i(0, 1, 0)
    draw_rect_y(-grama_size, -grama_size, grama_size, grama_size, 0)


def draw_chao():
    tamanho = Vec2d(
        parte_central_size.x + asa_size.x * 2, parte_central_size.z + asa_size.z * 2
    )

    glColor3ub(156, 146, 143)
    glNormal3i(0, 1, 0)
    draw_rect_y(-2, -2, tamanho.x + 2, tamanho.y + 2, EPSILON)


def draw_piso(x1: float, z1: float, x2: float, z2: float, y: float):
    glColor3ub(150, 108, 72)
    draw_rect_y(x1, z1, x2, z2, y)

    glColor3ub(97, 67, 42)
    spacing = 0.45

    glBegin(GL_LINES)
    x = x1 + spacing
    while x < x2:
        glVertex3d(x, y + EPSILON, z1)
        glVertex3d(x, y + EPSILON, z2)
        x += spacing
    glEnd()


def draw_pisos():
    glNormal3i(0, 1, 0)
    glPushMatrix()

    # Asa direita
    glTranslated(0, 0, asa_z_offset)
    draw_piso(0, 0, asa_size.x, asa_size.z, piso_y)

    # Parte central
    glTranslated(asa_size.x, 0, -asa_z_offset)

    espaco_porta_x_start = (parte_central_size.x - espaco_porta_size.x) / 2
    espaco_porta_x_end = (parte_central_size.x + espaco_porta_size.x) / 2
    # Espaço para porta
    draw_piso(
        0, espaco_porta_size.y, parte_central_size.x, parte_central_size.z, piso_y
    )
    draw_piso(0, 0, espaco_porta_x_start, espaco_porta_size.y, piso_y)
    draw_piso(espaco_porta_x_end, 0, parte_central_size.x, espaco_porta_size.y, piso_y)
    draw_piso(
        espaco_porta_x_start, 0, espaco_porta_x_end, espaco_porta_size.y, EPSILON * 2
    )

    # Segundo andar
    limite_x = parte_central_size.x - abertura_escada_size.x
    limite_z = parte_central_size.z / 2
    fim_abertura_z = limite_z + abertura_escada_size.y

    draw_piso(0, 0, limite_x, parte_central_size.z, segundo_andar_y)
    draw_piso(limite_x, 0, parte_central_size.x, limite_z, segundo_andar_y)
    draw_piso(
        limite_x,
        fim_abertura_z,
        parte_central_size.x,
        parte_central_size.z,
        segundo_andar_y,
    )
    draw_piso(
        parte_central_size.x - 0.1,
        limite_z,
        parte_central_size.x,
        fim_abertura_z,
        segundo_andar_y,
    )

    # Asa esquerda
    glTranslated(parte_central_size.x, 0, asa_z_offset)
    draw_piso(0, 0, asa_size.x, asa_size.z, piso_y)

    glPopMatrix()


# Helpers para stencil
def mask_rect(x1: float, y1: float, w: float, h: float):
    glBegin(GL_QUADS)
    glVertex3d(x1, y1, 0)
    glVertex3d(x1 + w, y1, 0)
    glVertex3d(x1 + w, y1 + h, 0)
    glVertex3d(x1, y1 + h, 0)
    glEnd()


def mask_janela_arco(x: float, y_base: float, total_w: float, total_h: float, seg: int):
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


def draw_asa():
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


def carregar_modelo(name):
    name = os.path.join(__file__, "..", "..", name)
    return load_model(name)


def draw_objetos():
    obj = load_model("models/Mesa.obj")
    glPushMatrix()
    glTranslatef(10.0, 1.0, 7.0)  # movendo o objeto
    glRotatef(90.0, 0.0, 1.0, 0.0)
    glColor3ub(0, 0, 0)
    draw_model_faces(obj)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(10.0, 1.0, 12.0)  # movendo o objeto
    glRotatef(90.0, 0.0, 1.0, 0.0)
    glColor3ub(0, 0, 0)
    draw_model_faces(obj)
    glPopMatrix()

    obj = load_model("models/Flores.obj")
    glPushMatrix()
    glTranslatef(9.5, 2.0, 6.5)  # movendo o objeto
    glRotatef(0.0, 0.0, 1.0, 0.0)
    glScalef(0.2, 0.2, 0.2)  # reduzindo a escala
    glColor3ub(245, 245, 220)
    draw_model_faces(obj)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(9.5, 2.0, 7.5)  # movendo o objeto
    glRotatef(0.0, 0.0, 1.0, 0.0)
    glScalef(0.2, 0.2, 0.2)  # reduzindo a escala
    glColor3ub(245, 245, 220)
    draw_model_faces(obj)
    glPopMatrix()

    obj = load_model("models/Tv.obj")
    glPushMatrix()
    glTranslatef(9.5, 2.2, 12.5)  # movendo o objeto
    glRotatef(0.0, 0.0, 1.0, 0.0)
    glScalef(0.2, 0.2, 0.2)  # reduzindo a escala
    glColor3ub(0, 245, 220)
    draw_model_faces(obj)
    glPopMatrix()

    obj = load_model("models/Telefone.obj")
    glPushMatrix()
    glTranslatef(9.5, 2.1, 11.5)  # movendo o objeto
    glRotatef(180.0, 0.0, 1.0, 0.0)
    glScalef(0.1, 0.1, 0.1)  # reduzindo a escala
    glColor3ub(0, 0, 255)
    draw_model_faces(obj)
    glPopMatrix()


def draw_janela_com_arco_ajustado(pos: Vec3d):
    glPushMatrix()
    glTranslated(pos.x, pos.y, pos.z)
    draw_janela_com_arco(janela_com_arco.x, janela_com_arco.y, janela_com_arco.z)
    glPopMatrix()


def draw_janela_retangular_ajustado(pos: Vec3d):
    glPushMatrix()
    glTranslated(pos.x, pos.y, pos.z)
    draw_janela_retangular(
        janela_retangular_size.x, janela_retangular_size.y, janela_retangular_size.z
    )
    glPopMatrix()


def draw_janelas_asa():
    dist_base = 3

    janela_pos = Vec3d(-janela_retangular_size.x, janela_baixo_y_offset, 0)

    for i in range(3):
        janela_pos.x += dist_base
        draw_janela_retangular_ajustado(janela_pos)


def draw_janelas_parte_central():
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


def draw():
    draw_grama()

    glPushMatrix()
    glTranslated(-(parte_central_size.x / 2 + asa_size.x), 0, 0)

    draw_chao()
    draw_pisos()
    draw_parte_externa(draw_asa, draw_parte_central)
    draw_parte_externa(draw_janelas_asa, draw_janelas_parte_central)
    draw_pilastras_internas()
    draw_sacada()
    draw_telhado()
    draw_objetos()

    glPopMatrix()
    draw_botao()
