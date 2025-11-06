from OpenGL import GL, GLUT
from ..util import Vec3d, Vec2i
from ..primitives import draw_box, draw_rect_z

# Global state (will be updated by main.py)
window_size = Vec2i(800, 600)
camera_pos = Vec3d(0, 1.7, -5)

porta_size = Vec3d(2.8, 3.2, 0.0)
botao_size = Vec2i(100, 50)

# ANIMAÇÃO DAS PORTAS
door_angle = 0.0
door_target = 0.0  # 0 fechada, 90 aberta
door_max = 90.0
door_speed = 180.0 / 60.0  # ~3°/frame @60Hz


def step_door() -> bool:
    global door_angle
    before = door_angle
    if door_angle < door_target:
        door_angle += door_speed
        if door_angle > door_target:
            door_angle = door_target
    elif door_angle > door_target:
        door_angle -= door_speed
        if door_angle < door_target:
            door_angle = door_target
    return before != door_angle


def on_loop() -> bool:
    return step_door()


# helpers
def color_wood_base():
    GL.glColor3ub(120, 78, 48)  # marrom base


def color_wood_highlight():
    GL.glColor3ub(139, 94, 62)  # partes salientes


def color_wood_inset():
    GL.glColor3ub(97, 67, 42)  # painéis rebaixados


def color_wood_frame():
    GL.glColor3ub(150, 108, 72)  # moldura dos painéis


def color_wood_jamb():
    GL.glColor3ub(90, 60, 40)  # junta central


def color_metal():
    GL.glColor3ub(80, 80, 80)  # maçaneta


def draw_box_esp(w: float, h: float, t: float):
    GL.glNormal3i(0, 0, -1)
    GL.glRectd(0, 0, w, h)  # frente z=0
    GL.glNormal3i(0, 0, 1)
    draw_rect_z(0, 0, w, h, t)  # trás  z=t

    GL.glPushMatrix()
    GL.glRotated(-90, 0, 1, 0)
    GL.glNormal3i(-1, 0, 0)
    GL.glRectd(0, 0, t, h)
    GL.glPopMatrix()  # lado esq

    GL.glPushMatrix()
    GL.glTranslated(w, 0, 0)
    GL.glRotated(-90, 0, 1, 0)
    GL.glNormal3i(-1, 0, 0)
    GL.glRectd(0, 0, t, h)
    GL.glPopMatrix()  # lado dir

    GL.glPushMatrix()
    GL.glRotated(90, 1, 0, 0)
    GL.glNormal3i(0, 1, 0)
    GL.glRectd(0, 0, w, t)
    GL.glPopMatrix()  # base

    GL.glPushMatrix()
    GL.glTranslated(0, h, 0)
    GL.glRotated(90, 1, 0, 0)
    GL.glNormal3i(0, 1, 0)
    GL.glRectd(0, 0, w, t)
    GL.glPopMatrix()  # topo


def draw_framed_inset(
    x: float, y: float, w: float, h: float, t: float, moldura: float, rebaixo: float
):
    z_lift = -0.003  # saliência à frente da face

    # moldura plana saliente
    GL.glPushMatrix()
    GL.glTranslated(0, 0, z_lift)
    GL.glNormal3i(0, 0, -1)
    color_wood_frame()
    GL.glBegin(GL.GL_QUADS)
    # esquerda
    GL.glVertex3d(x, y, 0)
    GL.glVertex3d(x + moldura, y, 0)
    GL.glVertex3d(x + moldura, y + h, 0)
    GL.glVertex3d(x, y + h, 0)
    # direita
    GL.glVertex3d(x + w - moldura, y, 0)
    GL.glVertex3d(x + w, y, 0)
    GL.glVertex3d(x + w, y + h, 0)
    GL.glVertex3d(x + w - moldura, y + h, 0)
    # topo
    GL.glVertex3d(x + moldura, y + h - moldura, 0)
    GL.glVertex3d(x + w - moldura, y + h - moldura, 0)
    GL.glVertex3d(x + w - moldura, y + h, 0)
    GL.glVertex3d(x + moldura, y + h, 0)
    # base
    GL.glVertex3d(x + moldura, y, 0)
    GL.glVertex3d(x + w - moldura, y, 0)
    GL.glVertex3d(x + w - moldura, y + moldura, 0)
    GL.glVertex3d(x + moldura, y + moldura, 0)
    GL.glEnd()
    GL.glPopMatrix()

    # painel rebaixado (entra no volume)
    GL.glPushMatrix()
    GL.glTranslated(x + moldura, y + moldura, t * rebaixo)
    color_wood_inset()
    draw_box_esp(w - 2 * moldura, h - 2 * moldura, t * 0.12)
    GL.glPopMatrix()


def draw_door_leaf(folha_w: float, folha_h: float, t: float, is_right_leaf: bool):
    z_lift = -0.003  # saliências à frente

    # corpo
    color_wood_base()
    draw_box_esp(folha_w, folha_h, t)

    # stiles/rails
    stile = 0.18
    rail_top = 0.16
    rail_mid = 0.22
    rail_bot = 0.16

    y_mid0 = (folha_h - rail_mid) * 0.5

    GL.glPushMatrix()
    GL.glTranslated(0, 0, z_lift)
    GL.glNormal3i(0, 0, -1)
    color_wood_highlight()
    GL.glBegin(GL.GL_QUADS)
    # stiles
    GL.glVertex3d(0, 0, 0)
    GL.glVertex3d(stile, 0, 0)
    GL.glVertex3d(stile, folha_h, 0)
    GL.glVertex3d(0, folha_h, 0)
    GL.glVertex3d(folha_w - stile, 0, 0)
    GL.glVertex3d(folha_w, 0, 0)
    GL.glVertex3d(folha_w, folha_h, 0)
    GL.glVertex3d(folha_w - stile, folha_h, 0)
    # rails topo/meio/base
    GL.glVertex3d(stile, folha_h - rail_top, 0)
    GL.glVertex3d(folha_w - stile, folha_h - rail_top, 0)
    GL.glVertex3d(folha_w - stile, folha_h, 0)
    GL.glVertex3d(stile, folha_h, 0)

    GL.glVertex3d(stile, y_mid0, 0)
    GL.glVertex3d(folha_w - stile, y_mid0, 0)
    GL.glVertex3d(folha_w - stile, y_mid0 + rail_mid, 0)
    GL.glVertex3d(stile, y_mid0 + rail_mid, 0)

    GL.glVertex3d(stile, 0, 0)
    GL.glVertex3d(folha_w - stile, 0, 0)
    GL.glVertex3d(folha_w - stile, rail_bot, 0)
    GL.glVertex3d(stile, rail_bot, 0)
    GL.glEnd()
    GL.glPopMatrix()

    # painéis rebaixados
    mold = 0.08
    rel = 0.35

    top_h = folha_h - rail_top - (y_mid0 + rail_mid)
    draw_framed_inset(
        stile, y_mid0 + rail_mid, folha_w - 2 * stile, top_h, t, mold, rel
    )

    base_region_h = y_mid0
    lower1_h = base_region_h * 0.55
    lower2_h = base_region_h * 0.35
    gap_v = base_region_h - (lower1_h + lower2_h)

    draw_framed_inset(
        stile, gap_v + lower2_h, folha_w - 2 * stile, lower1_h, t, mold, rel
    )
    draw_framed_inset(
        stile, 0.02 + mold * 0.25, folha_w - 2 * stile, lower2_h - 0.02, t, mold, rel
    )

    # junta central e maçaneta na folha direita
    if is_right_leaf:
        jamb = 0.025
        GL.glPushMatrix()
        GL.glTranslated(0, 0, z_lift)
        GL.glNormal3i(0, 0, -1)
        color_wood_jamb()
        GL.glBegin(GL.GL_QUADS)
        GL.glVertex3d(folha_w - jamb, 0, 0)
        GL.glVertex3d(folha_w, 0, 0)
        GL.glVertex3d(folha_w, folha_h, 0)
        GL.glVertex3d(folha_w - jamb, folha_h, 0)
        GL.glEnd()
        GL.glPopMatrix()

        color_metal()
        knob_w = 0.06
        knob_h = 0.06
        knob_t = 0.04
        GL.glPushMatrix()
        GL.glTranslated(
            folha_w - 0.12 - knob_w,
            y_mid0 + rail_mid * 0.5 - knob_h * 0.5,
            knob_t * 0.5,
        )
        draw_box_esp(knob_w, knob_h, knob_t)
        GL.glPopMatrix()


def draw_portas_frente(x_antes_porta: float):
    leaf_w = porta_size.x * 0.5
    leaf_h = porta_size.y
    thickness = 0.06
    z_gap = 0.004

    # Folha esquerda: rotação NEGATIVA → entra para +Z
    GL.glPushMatrix()
    GL.glTranslated(x_antes_porta, 0, z_gap)
    GL.glRotated(-door_angle, 0, 1, 0)
    draw_door_leaf(leaf_w, leaf_h, thickness, False)
    GL.glPopMatrix()

    # Folha direita: rotação POSITIVA (após levar pivô à borda direita)
    GL.glPushMatrix()
    GL.glTranslated(x_antes_porta + porta_size.x, 0, z_gap)
    GL.glRotated(+door_angle, 0, 1, 0)
    GL.glTranslated(-leaf_w, 0, 0)
    draw_door_leaf(leaf_w, leaf_h, thickness, True)
    GL.glPopMatrix()


def draw_porta(x_antes_porta: float):
    # batente do vão (leve saliência)
    z_lift = -0.002
    GL.glColor3ub(210, 170, 170)
    GL.glPushMatrix()
    GL.glTranslated(0, 0, z_lift)
    GL.glNormal3i(0, 0, -1)
    b = 0.08
    GL.glBegin(GL.GL_QUADS)
    # esq
    GL.glVertex3d(x_antes_porta - b, 0, 0)
    GL.glVertex3d(x_antes_porta, 0, 0)
    GL.glVertex3d(x_antes_porta, porta_size.y, 0)
    GL.glVertex3d(x_antes_porta - b, porta_size.y, 0)
    # dir
    GL.glVertex3d(x_antes_porta + porta_size.x, 0, 0)
    GL.glVertex3d(x_antes_porta + porta_size.x + b, 0, 0)
    GL.glVertex3d(x_antes_porta + porta_size.x + b, porta_size.y, 0)
    GL.glVertex3d(x_antes_porta + porta_size.x, porta_size.y, 0)
    # topo
    GL.glVertex3d(x_antes_porta - b, porta_size.y, 0)
    GL.glVertex3d(x_antes_porta + porta_size.x + b, porta_size.y, 0)
    GL.glVertex3d(x_antes_porta + porta_size.x + b, porta_size.y + b, 0)
    GL.glVertex3d(x_antes_porta - b, porta_size.y + b, 0)
    GL.glEnd()
    GL.glPopMatrix()

    draw_portas_frente(x_antes_porta)


def draw_bitmap_string(font, x: int, y: int, s: str):
    GL.glRasterPos2i(x, y)
    for c in s:
        GLUT.glutBitmapCharacter(font, ord(c))


def draw_botao():
    if camera_pos.x < -5 or camera_pos.x > 5 or camera_pos.z < -5 or camera_pos.z > 5:
        return

    GL.glMatrixMode(GL.GL_PROJECTION)
    GL.glPushMatrix()
    GL.glLoadIdentity()
    GL.glOrtho(0, window_size.x, window_size.y, 0, -1, 1)

    GL.glMatrixMode(GL.GL_MODELVIEW)
    GL.glPushMatrix()
    GL.glLoadIdentity()

    lighting_was = GL.glIsEnabled(GL.GL_LIGHTING)
    depth_was = GL.glIsEnabled(GL.GL_DEPTH_TEST)
    if lighting_was:
        GL.glDisable(GL.GL_LIGHTING)
    if depth_was:
        GL.glDisable(GL.GL_DEPTH_TEST)

    start_x = window_size.x - botao_size.x - 50
    start_y = window_size.y - botao_size.y - 50

    GL.glColor3ub(80, 130, 190)
    GL.glRectd(start_x, start_y, start_x + botao_size.x, start_y + botao_size.y)

    font = GLUT.GLUT_BITMAP_HELVETICA_18
    GL.glColor3ub(255, 255, 255)
    text = "Fechar" if door_target > 0 else "Abrir"
    draw_bitmap_string(font, start_x + 30, start_y + 30, text)

    if depth_was:
        GL.glEnable(GL.GL_DEPTH_TEST)
    if lighting_was:
        GL.glEnable(GL.GL_LIGHTING)

    # restaura matrizes
    GL.glMatrixMode(GL.GL_PROJECTION)
    GL.glPopMatrix()
    GL.glMatrixMode(GL.GL_MODELVIEW)
    GL.glPopMatrix()


def on_mouse_press(button: int, state: int, x: int, y: int) -> bool:
    global door_target
    start_x = window_size.x - botao_size.x - 50
    start_y = window_size.y - botao_size.y - 50

    if (
        button == GLUT.GLUT_LEFT_BUTTON
        and state == GLUT.GLUT_DOWN
        and start_x < x < start_x + botao_size.x
        and start_y < y < start_y + botao_size.y
    ):
        door_target = 0.0 if door_target > 0.0 else door_max
        return True

    return False
