from OpenGL import GL

from .. import primitives, util
from . import constantes


def draw_pisos() -> None:
    GL.glBindTexture(GL.GL_TEXTURE_2D, primitives.load_texture_from_file("wood.jpg"))
    draw_piso_terreo()
    draw_piso_primeiro_andar()
    GL.glBindTexture(GL.GL_TEXTURE_2D, 0)


def draw_piso_terreo() -> None:
    espaco_porta_size = util.Vec2d(3, 3)
    espaco_porta_x = util.Vec2d(
        (constantes.parte_central_size.x - espaco_porta_size.x) / 2,
        (constantes.parte_central_size.x + espaco_porta_size.x) / 2,
    )

    primitives.setup_stencil_mask()

    with primitives.push_matrix():
        # Marcar espaço da porta na parte central
        GL.glTranslated(constantes.asa_size.x, 0, 0)
        primitives.mascarar_retangulo_xz(
            espaco_porta_x.x, 0, espaco_porta_x.y, espaco_porta_size.y, constantes.piso_y
        )

    primitives.setup_stencil_draw()

    # Asa direita
    with primitives.push_matrix():
        GL.glTranslated(0, 0, constantes.asa_z_offset)
        draw_piso(0, 0, constantes.asa_size.x, constantes.asa_size.z, constantes.piso_y)

    # Parte central completa
    with primitives.push_matrix():
        GL.glTranslated(constantes.asa_size.x, 0, 0)
        draw_piso(0, 0, constantes.parte_central_size.x, constantes.parte_central_size.z, constantes.piso_y)

    # Asa esquerda
    with primitives.push_matrix():
        GL.glTranslated(constantes.asa_size.x + constantes.parte_central_size.x, 0, constantes.asa_z_offset)
        draw_piso(0, 0, constantes.asa_size.x, constantes.asa_size.z, constantes.piso_y)

    primitives.free_stencil()

    with primitives.push_matrix():
        GL.glTranslated(constantes.asa_size.x, 0, 0)
        draw_piso(espaco_porta_x.x, 0, espaco_porta_x.y, espaco_porta_size.y, constantes.epsilon * 2)

        desenhar_degraus_porta(espaco_porta_x, espaco_porta_size)

        GL.glNormal3i(-1, 0, 0)
        primitives.draw_rect_x(0, 0, constantes.piso_y, espaco_porta_size.y, espaco_porta_x.x)

        GL.glNormal3i(1, 0, 0)
        primitives.draw_rect_x(0, 0, constantes.piso_y, espaco_porta_size.y, espaco_porta_x.y)


def draw_piso_primeiro_andar() -> None:
    abertura_escada_size = util.Vec2d(1, 3)

    with primitives.push_matrix():
        GL.glTranslated(constantes.asa_size.x, 0, 0)

        primitives.setup_stencil_mask()

        # Marcar abertura da escada
        limite_x = constantes.parte_central_size.x - abertura_escada_size.x
        limite_z = constantes.parte_central_size.z / 2
        fim_abertura_z = limite_z + abertura_escada_size.y
        primitives.mascarar_retangulo_xz(
            limite_x, limite_z, constantes.parte_central_size.x, fim_abertura_z, constantes.segundo_andar_y
        )

        primitives.setup_stencil_draw()

        draw_piso(
            0, 0, constantes.parte_central_size.x, constantes.parte_central_size.z, constantes.segundo_andar_y
        )

        primitives.free_stencil()


def desenhar_degraus_porta(espaco_porta_x: util.Vec2d, espaco_porta_size: util.Vec2d) -> None:
    qtd_degraus = 2
    altura_total = constantes.piso_y - constantes.epsilon
    degrau_altura = altura_total / qtd_degraus
    degrau_profundidade = espaco_porta_size.y / 4

    for i in range(qtd_degraus):
        degrau_y_base = constantes.piso_y - (i + 1) * degrau_altura
        degrau_y = constantes.piso_y - i * degrau_altura
        degrau_z_start = espaco_porta_size.y - i * degrau_profundidade
        degrau_z_end = espaco_porta_size.y - (i + 1) * degrau_profundidade

        # Topo do degrau
        draw_piso(espaco_porta_x.x, degrau_z_start, espaco_porta_x.y, degrau_z_end, degrau_y)

        # Frente do degrau
        GL.glNormal3i(0, 0, -1)
        primitives.draw_rect_z(espaco_porta_x.x, degrau_y_base, espaco_porta_x.y, degrau_y, degrau_z_end)


def draw_piso(x1: float, z1: float, x2: float, z2: float, y: float) -> None:
    GL.glNormal3i(0, 1, 0)
    primitives.draw_rect_y(x1, z1, x2, z2, y)
