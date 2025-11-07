import math

from OpenGL import GL

from .. import primitives, util


def desenhar_anel_arco(
    cx: float, cy: float, outer_r: float, inner_r: float, z_front: float, depth: float, segments: int
):
    z_back = z_front - depth

    # Anel frontal
    with primitives.begin(GL.GL_TRIANGLE_STRIP):
        for i in range(segments + 1):
            a = math.pi * i / segments
            xo = math.cos(a) * outer_r
            yo = math.sin(a) * outer_r
            xi = math.cos(a) * inner_r
            yi = math.sin(a) * inner_r
            GL.glVertex3d(cx + xo, cy + yo, z_front)
            GL.glVertex3d(cx + xi, cy + yi, z_front)

    # Anel traseiro
    with primitives.begin(GL.GL_TRIANGLE_STRIP):
        for i in range(segments + 1):
            a = math.pi * i / segments
            xo = math.cos(a) * outer_r
            yo = math.sin(a) * outer_r
            xi = math.cos(a) * inner_r
            yi = math.sin(a) * inner_r
            GL.glVertex3d(cx + xo, cy + yo, z_back)
            GL.glVertex3d(cx + xi, cy + yi, z_back)

    # Lateral externa
    with primitives.begin(GL.GL_QUAD_STRIP):
        for i in range(segments + 1):
            a = math.pi * i / segments
            xo = math.cos(a) * outer_r
            yo = math.sin(a) * outer_r
            GL.glVertex3d(cx + xo, cy + yo, z_front)
            GL.glVertex3d(cx + xo, cy + yo, z_back)

    # Lateral interna
    with primitives.begin(GL.GL_QUAD_STRIP):
        for i in range(segments + 1):
            a = math.pi * i / segments
            xi = math.cos(a) * inner_r
            yi = math.sin(a) * inner_r
            GL.glVertex3d(cx + xi, cy + yi, z_back)
            GL.glVertex3d(cx + xi, cy + yi, z_front)


def draw_janela_com_arco(width: float, height: float, depth: float):
    frame = 0.22
    radius = width / 2.0  # Arco semicircular
    height = max(height, radius + 0.01)
    rect_h = height - radius  # Parte reta
    seg = 48
    epsilon = 0.002  # evita z-fighting
    z_front = 0

    # Moldura (tom rosado)
    GL.glColor3ub(191, 124, 124)
    # ombreiras (laterais) e peitoril (base)
    primitives.draw_box(util.Vec3d(0, 0, z_front), util.Vec3d(frame, rect_h, depth))
    primitives.draw_box(util.Vec3d(width - frame, 0, z_front), util.Vec3d(frame, rect_h, depth))
    primitives.draw_box(util.Vec3d(0, 0, z_front), util.Vec3d(width, frame, depth))

    # Arco superior
    cx, cy = radius, rect_h
    desenhar_anel_arco(cx, cy, radius, radius - frame, z_front, depth, seg)

    # Vidro translúcido
    GL.glEnable(GL.GL_BLEND)
    GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
    GL.glColor4ub(199, 222, 245, 64)  # azul claro com alpha

    # Retângulo de vidro (parte reta)
    z_glass = z_front - epsilon
    with primitives.begin(GL.GL_QUADS):
        GL.glVertex3d(frame, frame, z_glass)
        GL.glVertex3d(width - frame, frame, z_glass)
        GL.glVertex3d(width - frame, rect_h - frame, z_glass)
        GL.glVertex3d(frame, rect_h - frame, z_glass)

    # Vidro do arco
    with primitives.begin(GL.GL_TRIANGLE_FAN):
        GL.glVertex3d(cx, cy, z_glass)
        r_inner = radius - frame
        for i in range(seg + 1):
            a = math.pi * i / seg
            GL.glVertex3d(cx + math.cos(a) * r_inner, cy + math.sin(a) * r_inner, z_glass)

    GL.glDisable(GL.GL_BLEND)

    # Travessas internas (caixilhos)
    GL.glColor3ub(191, 124, 124)
    bar = frame * 0.45
    inner_w = width - 2.0 * frame
    glass_bottom = frame
    glass_top_rect = rect_h - frame

    # Montante vertical central
    primitives.draw_box(
        util.Vec3d(width / 2.0 - bar / 2.0, glass_bottom, z_glass),
        util.Vec3d(bar, glass_top_rect - glass_bottom, epsilon * 2.0),
    )

    # Travessa horizontal central (forma o "+")
    center_y = (glass_bottom + glass_top_rect) / 2.0 - bar / 2.0
    primitives.draw_box(util.Vec3d(frame, center_y, z_glass), util.Vec3d(inner_w, bar, epsilon * 2.0))

    # Travessa horizontal próxima ao arco (mantida)
    primitives.draw_box(
        util.Vec3d(frame, rect_h - frame - bar / 2.0, z_glass), util.Vec3d(inner_w, bar, epsilon * 2.0)
    )


def draw_janela_retangular(width: float, height: float, depth: float):
    frame = 0.22
    epsilon = 0.002  # evita z-fighting

    # Moldura
    GL.glColor3ub(191, 124, 124)
    primitives.draw_box(util.Vec3d(0, 0, 0), util.Vec3d(frame, height, depth))
    primitives.draw_box(util.Vec3d(width - frame, 0, 0), util.Vec3d(frame, height, depth))
    primitives.draw_box(util.Vec3d(0, 0, 0), util.Vec3d(width, frame, depth))
    primitives.draw_box(util.Vec3d(0, height - frame, 0), util.Vec3d(width, frame, depth))

    # Vidro
    GL.glColor3ub(199, 222, 245)
    with primitives.begin(GL.GL_QUADS):
        GL.glVertex3d(frame, frame, -epsilon)
        GL.glVertex3d(width - frame, frame, -epsilon)
        GL.glVertex3d(width - frame, height - frame, -epsilon)
        GL.glVertex3d(frame, height - frame, -epsilon)

    # Travessas internas (caixilhos)
    GL.glColor3ub(191, 124, 124)
    bar = frame * 0.5
    inner_w = width - 2.0 * frame
    glass_top_rect = height - frame

    # Montante vertical central
    montante_pos = util.Vec3d(width / 2 - bar / 2, frame, -epsilon)
    montante_size = util.Vec3d(bar, (glass_top_rect - frame), epsilon * 2)
    primitives.draw_box(montante_pos, montante_size)

    # Travessa horizontal central (forma o "+")
    center_y = (frame + glass_top_rect) / 2 - bar / 2
    primitives.draw_box(util.Vec3d(frame, center_y, -epsilon), util.Vec3d(inner_w, bar, epsilon * 2))
