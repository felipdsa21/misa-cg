import math
from OpenGL import GL, GLU, GLUT
from .util import Vec3d, PI
from .primitives import draw_box, draw_rect_z

# Global quadric object (initialized in draw.py)
# This will be set by draw.init()
q = None


def draw_arch_ring(
    cx: float,
    cy: float,
    outer_r: float,
    inner_r: float,
    z_front: float,
    depth: float,
    segments: int,
):
    z_back = z_front - depth

    # Anel frontal
    GL.glBegin(GL.GL_TRIANGLE_STRIP)
    for i in range(segments + 1):
        a = PI * i / segments
        xo = math.cos(a) * outer_r
        yo = math.sin(a) * outer_r
        xi = math.cos(a) * inner_r
        yi = math.sin(a) * inner_r
        GL.glVertex3d(cx + xo, cy + yo, z_front)
        GL.glVertex3d(cx + xi, cy + yi, z_front)
    GL.glEnd()

    # Anel traseiro
    GL.glBegin(GL.GL_TRIANGLE_STRIP)
    for i in range(segments + 1):
        a = PI * i / segments
        xo = math.cos(a) * outer_r
        yo = math.sin(a) * outer_r
        xi = math.cos(a) * inner_r
        yi = math.sin(a) * inner_r
        GL.glVertex3d(cx + xo, cy + yo, z_back)
        GL.glVertex3d(cx + xi, cy + yi, z_back)
    GL.glEnd()

    # Lateral externa
    GL.glBegin(GL.GL_QUAD_STRIP)
    for i in range(segments + 1):
        a = PI * i / segments
        xo = math.cos(a) * outer_r
        yo = math.sin(a) * outer_r
        GL.glVertex3d(cx + xo, cy + yo, z_front)
        GL.glVertex3d(cx + xo, cy + yo, z_back)
    GL.glEnd()

    # Lateral interna
    GL.glBegin(GL.GL_QUAD_STRIP)
    for i in range(segments + 1):
        a = PI * i / segments
        xi = math.cos(a) * inner_r
        yi = math.sin(a) * inner_r
        GL.glVertex3d(cx + xi, cy + yi, z_back)
        GL.glVertex3d(cx + xi, cy + yi, z_front)
    GL.glEnd()


def draw_janela_com_arco(width: float, height: float, depth: float):
    frame = 0.22
    radius = width / 2.0  # Arco semicircular

    if height <= radius:
        height = radius + 0.01

    rect_h = height - radius  # Parte reta
    seg = 48
    epsilon = 0.002  # evita z-fighting
    z_front = 0

    # Moldura (tom rosado)
    GL.glColor3ub(191, 124, 124)
    # ombreiras (laterais) e peitoril (base)
    draw_box(Vec3d(0, 0, z_front), Vec3d(frame, rect_h, depth))
    draw_box(Vec3d(width - frame, 0, z_front), Vec3d(frame, rect_h, depth))
    draw_box(Vec3d(0, 0, z_front), Vec3d(width, frame, depth))

    # Arco superior
    cx = radius
    cy = rect_h
    draw_arch_ring(cx, cy, radius, radius - frame, z_front, depth, seg)

    # Vidro translúcido
    GL.glEnable(GL.GL_BLEND)
    GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
    GL.glColor4ub(199, 222, 245, 64)  # azul claro com alpha

    # Retângulo de vidro (parte reta)
    GL.glBegin(GL.GL_QUADS)
    GL.glVertex3d(frame, frame, z_front - epsilon)
    GL.glVertex3d(width - frame, frame, z_front - epsilon)
    GL.glVertex3d(width - frame, rect_h - frame, z_front - epsilon)
    GL.glVertex3d(frame, rect_h - frame, z_front - epsilon)
    GL.glEnd()

    # Vidro do arco
    GL.glBegin(GL.GL_TRIANGLE_FAN)
    GL.glVertex3d(cx, cy, z_front - epsilon)
    for i in range(seg + 1):
        a = PI * i / seg
        xi = math.cos(a) * (radius - frame)
        yi = math.sin(a) * (radius - frame)
        GL.glVertex3d(cx + xi, cy + yi, z_front - epsilon)
    GL.glEnd()

    GL.glDisable(GL.GL_BLEND)

    # Travessas internas (caixilhos)
    GL.glColor3ub(191, 124, 124)
    bar = frame * 0.45
    inner_w = width - 2.0 * frame
    glass_bottom = frame
    glass_top_rect = rect_h - frame

    # Montante vertical central
    draw_box(
        Vec3d(width / 2.0 - bar / 2.0, glass_bottom, z_front - epsilon),
        Vec3d(bar, (glass_top_rect - glass_bottom), epsilon * 2.0),
    )

    # Travessa horizontal central (forma o "+")
    center_y = (glass_bottom + glass_top_rect) / 2.0 - bar / 2.0
    draw_box(
        Vec3d(frame, center_y, z_front - epsilon), Vec3d(inner_w, bar, epsilon * 2.0)
    )

    # Travessa horizontal próxima ao arco (mantida)
    draw_box(
        Vec3d(frame, rect_h - frame - bar / 2.0, z_front - epsilon),
        Vec3d(inner_w, bar, epsilon * 2.0),
    )


def draw_janela_retangular(width: float, height: float, depth: float):
    frame = 0.22
    epsilon = 0.002  # evita z-fighting

    # Moldura
    GL.glColor3ub(191, 124, 124)
    draw_box(Vec3d(0, 0, 0), Vec3d(frame, height, depth))
    draw_box(Vec3d(width - frame, 0, 0), Vec3d(frame, height, depth))
    draw_box(Vec3d(0, 0, 0), Vec3d(width, frame, depth))
    draw_box(Vec3d(0, height - frame, 0), Vec3d(width, frame, depth))

    # Vidro
    GL.glColor3ub(199, 222, 245)
    GL.glBegin(GL.GL_QUADS)
    GL.glVertex3d(frame, frame, -epsilon)
    GL.glVertex3d(width - frame, frame, -epsilon)
    GL.glVertex3d(width - frame, height - frame, -epsilon)
    GL.glVertex3d(frame, height - frame, -epsilon)
    GL.glEnd()

    # Travessas internas (caixilhos)
    GL.glColor3ub(191, 124, 124)
    bar = frame * 0.5
    inner_w = width - 2.0 * frame
    glass_top_rect = height - frame

    # Montante vertical central
    montante_pos = Vec3d(width / 2 - bar / 2, frame, -epsilon)
    montante_size = Vec3d(bar, (glass_top_rect - frame), epsilon * 2)
    draw_box(montante_pos, montante_size)

    # Travessa horizontal central (forma o "+")
    center_y = (frame + glass_top_rect) / 2 - bar / 2
    draw_box(Vec3d(frame, center_y, -epsilon), Vec3d(inner_w, bar, epsilon * 2))


def draw_box_local(w: float, h: float, t: float):
    GL.glNormal3i(0, 0, -1)
    GL.glRectd(0, 0, w, h)  # frente z=0
    GL.glNormal3i(0, 0, 1)
    draw_rect_z(0, 0, w, h, t)  # trás  z=t

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

    GL.glPushMatrix()
    GL.glTranslated(x, y, z)

    # base madeira escura
    GL.glColor3ub(70, 42, 25)
    draw_box_local(base_w, base_h, base_w)

    # pedestal amarelo
    GL.glTranslated((base_w - pedestal_w) / 2.0, base_h, (base_w - pedestal_w) / 2.0)
    GL.glColor3ub(225, 197, 126)
    draw_box_local(pedestal_w, pedestal_h, pedestal_w)

    # moldura branca
    GL.glTranslated(
        -(mold_w - pedestal_w) / 2.0, pedestal_h, -(mold_w - pedestal_w) / 2.0
    )
    GL.glColor3ub(240, 240, 240)
    draw_box_local(mold_w, mold_h, mold_w)

    # fuste (cilindro fechado, alinhado ao eixo Y)
    GL.glTranslated(mold_w / 2.0, mold_h, mold_w / 2.0)
    GL.glColor3ub(225, 197, 126)
    GL.glPushMatrix()
    GL.glRotatef(-90, 1, 0, 0)  # GLU usa +Z → vira para +Y
    GLU.gluCylinder(q, fuste_r, fuste_r, altura_fuste, 32, 1)
    GLU.gluDisk(q, 0.0, fuste_r, 32, 1)  # tampa inferior
    GL.glTranslatef(0, 0, altura_fuste)
    GLU.gluDisk(q, 0.0, fuste_r, 32, 1)  # tampa superior
    GL.glPopMatrix()

    # anel branco no topo do fuste
    GL.glPushMatrix()
    GL.glTranslated(0, altura_fuste, 0)
    GL.glColor3ub(240, 240, 240)
    GL.glRotatef(-90, 1, 0, 0)
    GLU.gluCylinder(q, anel_r, anel_r, anel_h, 32, 1)
    GLU.gluDisk(q, 0.0, anel_r, 32, 1)
    GL.glTranslatef(0, 0, anel_h)
    GLU.gluDisk(q, 0.0, anel_r, 32, 1)
    GL.glPopMatrix()

    # prato verde que toca o teto
    GL.glPushMatrix()
    GL.glTranslated(0, altura_fuste + anel_h, 0)
    GL.glColor3ub(126, 168, 146)
    GL.glRotatef(-90, 1, 0, 0)
    GLU.gluCylinder(q, prato_r, prato_r, prato_h, 32, 1)
    GLU.gluDisk(q, 0.0, prato_r, 32, 1)
    GL.glTranslatef(0, 0, prato_h)
    GLU.gluDisk(q, 0.0, prato_r, 32, 1)
    GL.glPopMatrix()

    GL.glPopMatrix()
