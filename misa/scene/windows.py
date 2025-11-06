"""Window drawing functions - Rectangular and arched windows."""

import math
from OpenGL.GL import *
from ..util import Vec3d, PI
from ..primitives import draw_box


def draw_arch_ring(
    cx: float,
    cy: float,
    outer_r: float,
    inner_r: float,
    z_front: float,
    depth: float,
    segments: int,
):
    """Draw an arch ring (torus segment) for arched windows."""
    z_back = z_front - depth

    # Anel frontal
    glBegin(GL_TRIANGLE_STRIP)
    for i in range(segments + 1):
        a = PI * i / segments
        xo = math.cos(a) * outer_r
        yo = math.sin(a) * outer_r
        xi = math.cos(a) * inner_r
        yi = math.sin(a) * inner_r
        glVertex3d(cx + xo, cy + yo, z_front)
        glVertex3d(cx + xi, cy + yi, z_front)
    glEnd()

    # Anel traseiro
    glBegin(GL_TRIANGLE_STRIP)
    for i in range(segments + 1):
        a = PI * i / segments
        xo = math.cos(a) * outer_r
        yo = math.sin(a) * outer_r
        xi = math.cos(a) * inner_r
        yi = math.sin(a) * inner_r
        glVertex3d(cx + xo, cy + yo, z_back)
        glVertex3d(cx + xi, cy + yi, z_back)
    glEnd()

    # Lateral externa
    glBegin(GL_QUAD_STRIP)
    for i in range(segments + 1):
        a = PI * i / segments
        xo = math.cos(a) * outer_r
        yo = math.sin(a) * outer_r
        glVertex3d(cx + xo, cy + yo, z_front)
        glVertex3d(cx + xo, cy + yo, z_back)
    glEnd()

    # Lateral interna
    glBegin(GL_QUAD_STRIP)
    for i in range(segments + 1):
        a = PI * i / segments
        xi = math.cos(a) * inner_r
        yi = math.sin(a) * inner_r
        glVertex3d(cx + xi, cy + yi, z_back)
        glVertex3d(cx + xi, cy + yi, z_front)
    glEnd()


def draw_janela_com_arco(width: float, height: float, depth: float):
    """Draw an arched window with frame, glass, and mullions."""
    frame = 0.22
    radius = width / 2.0  # Arco semicircular

    if height <= radius:
        height = radius + 0.01

    rect_h = height - radius  # Parte reta
    seg = 48
    epsilon = 0.002  # evita z-fighting
    z_front = 0

    # Moldura (tom rosado)
    glColor3ub(191, 124, 124)
    # ombreiras (laterais) e peitoril (base)
    draw_box(Vec3d(0, 0, z_front), Vec3d(frame, rect_h, depth))
    draw_box(Vec3d(width - frame, 0, z_front), Vec3d(frame, rect_h, depth))
    draw_box(Vec3d(0, 0, z_front), Vec3d(width, frame, depth))

    # Arco superior
    cx = radius
    cy = rect_h
    draw_arch_ring(cx, cy, radius, radius - frame, z_front, depth, seg)

    # Vidro translúcido
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glColor4ub(199, 222, 245, 64)  # azul claro com alpha

    # Retângulo de vidro (parte reta)
    glBegin(GL_QUADS)
    glVertex3d(frame, frame, z_front - epsilon)
    glVertex3d(width - frame, frame, z_front - epsilon)
    glVertex3d(width - frame, rect_h - frame, z_front - epsilon)
    glVertex3d(frame, rect_h - frame, z_front - epsilon)
    glEnd()

    # Vidro do arco
    glBegin(GL_TRIANGLE_FAN)
    glVertex3d(cx, cy, z_front - epsilon)
    for i in range(seg + 1):
        a = PI * i / seg
        xi = math.cos(a) * (radius - frame)
        yi = math.sin(a) * (radius - frame)
        glVertex3d(cx + xi, cy + yi, z_front - epsilon)
    glEnd()

    glDisable(GL_BLEND)

    # Travessas internas (caixilhos)
    glColor3ub(191, 124, 124)
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
    """Draw a rectangular window with frame, glass, and mullions."""
    frame = 0.22
    epsilon = 0.002  # evita z-fighting

    # Moldura
    glColor3ub(191, 124, 124)
    draw_box(Vec3d(0, 0, 0), Vec3d(frame, height, depth))
    draw_box(Vec3d(width - frame, 0, 0), Vec3d(frame, height, depth))
    draw_box(Vec3d(0, 0, 0), Vec3d(width, frame, depth))
    draw_box(Vec3d(0, height - frame, 0), Vec3d(width, frame, depth))

    # Vidro
    glColor3ub(199, 222, 245)
    glBegin(GL_QUADS)
    glVertex3d(frame, frame, -epsilon)
    glVertex3d(width - frame, frame, -epsilon)
    glVertex3d(width - frame, height - frame, -epsilon)
    glVertex3d(frame, height - frame, -epsilon)
    glEnd()

    # Travessas internas (caixilhos)
    glColor3ub(191, 124, 124)
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
