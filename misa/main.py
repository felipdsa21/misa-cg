import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from .util import (
    Vec2i,
    Vec3d,
    clamp,
    to_radians,
    calc_direction_vec,
    sum3d,
    normalize3d,
    scalar_mult3d,
    cross_product3d,
)
from . import draw
from .scene import door

GLUT_KEY_SHIFT_L = 112
GLUT_KEY_CTRL_L = 114

# Camera constants
camera_up = Vec3d(0, 1, 0)
mouse_sensitivity = 0.1
walk_speed = 0.07195

# Global state
window_size = Vec2i(800, 600)
last_mouse_pos = Vec2i(0, 0)
first_mouse = True
camera_focused = True
key_state = {}
special_key_state = {}

camera_pos = Vec3d(0, 1.7, -5)
pitch = 0.0
yaw = 90.0


def handle_display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    draw.draw()
    glutSwapBuffers()


def setup_camera():
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    center_pos = sum3d(
        camera_pos, calc_direction_vec(to_radians(pitch), to_radians(yaw))
    )

    gluLookAt(
        camera_pos.x,
        camera_pos.y,
        camera_pos.z,
        center_pos.x,
        center_pos.y,
        center_pos.z,
        camera_up.x,
        camera_up.y,
        camera_up.z,
    )

    draw.on_setup_camera()


def handle_reshape(w: int, h: int):
    global first_mouse, window_size, camera_pos
    first_mouse = True
    window_size = Vec2i(w, h)
    # Update porta module globals
    door.window_size = window_size
    door.camera_pos = camera_pos

    glViewport(0, 0, window_size.x, window_size.y)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(70, window_size.x / window_size.y, 0.1, 50)

    setup_camera()


def move_camera(perpendicular: bool, negative: bool):
    global camera_pos
    direction = calc_direction_vec(to_radians(pitch), to_radians(yaw))
    direction.y = 0
    direction = normalize3d(direction)

    if perpendicular:
        direction = cross_product3d(direction, camera_up)
        direction.y = 0
        direction = normalize3d(direction)

    speed = -walk_speed if negative else walk_speed
    direction = scalar_mult3d(speed, direction)
    camera_pos = sum3d(camera_pos, direction)


def set_camera_focused(value: bool):
    global camera_focused, first_mouse
    if camera_focused == value:
        return

    camera_focused = value
    glutSetCursor(GLUT_CURSOR_NONE if value else GLUT_CURSOR_INHERIT)

    if value:
        first_mouse = True


def handle_timer(value: int):
    global camera_pos, camera_focused, window_size
    # Update porta module globals
    door.window_size = window_size
    door.camera_pos = camera_pos

    if key_state.get(27, False):  # ESC
        sys.exit(0)

    changed = False

    if key_state.get(ord("a"), False) or key_state.get(ord("A"), False):
        move_camera(True, True)
        changed = True

    if key_state.get(ord("d"), False) or key_state.get(ord("D"), False):
        move_camera(True, False)
        changed = True

    if key_state.get(ord("s"), False) or key_state.get(ord("S"), False):
        move_camera(False, True)
        changed = True

    if key_state.get(ord("w"), False) or key_state.get(ord("W"), False):
        move_camera(False, False)
        changed = True

    if key_state.get(ord(" "), False):
        camera_pos.y += walk_speed
        changed = True

    if special_key_state.get(GLUT_KEY_SHIFT_L, False):
        camera_pos.y -= walk_speed
        changed = True

    if special_key_state.get(GLUT_KEY_CTRL_L, False):
        set_camera_focused(False)

    if door.on_loop():
        changed = True

    if changed:
        setup_camera()
        glutPostRedisplay()

    glutTimerFunc(1000 // 60, handle_timer, 0)


def handle_keyboard(key: int, x: int, y: int):
    key_state[ord(key)] = True


def handle_keyboard_up(key: int, x: int, y: int):
    key_state[ord(key)] = False


def handle_special(key: int, x: int, y: int):
    special_key_state[key] = True


def handle_special_up(key: int, x: int, y: int):
    special_key_state[key] = False


def handle_motion(x: int, y: int):
    global first_mouse, last_mouse_pos, pitch, yaw, window_size, camera_pos
    # Update porta module globals
    door.window_size = window_size
    door.camera_pos = camera_pos

    if first_mouse:
        last_mouse_pos = Vec2i(x, y)
        first_mouse = False
        return
    elif not camera_focused:
        last_mouse_pos = Vec2i(x, y)
        return

    dx = x - last_mouse_pos.x
    dy = last_mouse_pos.y - y

    yaw += dx * mouse_sensitivity
    pitch = clamp(pitch + (dy * mouse_sensitivity), -89.9, 89.9)

    # https://gamedev.stackexchange.com/a/98024
    if x < 100 or x > window_size.x - 100 or y < 100 or y > window_size.y - 100:
        new_x = window_size.x // 2
        new_y = window_size.y // 2
        glutWarpPointer(new_x, new_y)
        last_mouse_pos = Vec2i(new_x, new_y)
    else:
        last_mouse_pos = Vec2i(x, y)

    setup_camera()
    glutPostRedisplay()


def handle_mouse(button: int, state: int, x: int, y: int):
    global camera_focused
    if (
        not camera_focused
        and not door.on_mouse_press(button, state, x, y)
        and button == GLUT_LEFT_BUTTON
        and state == GLUT_DOWN
    ):
        set_camera_focused(True)


def main():
    global window_size, camera_pos
    glutInit(sys.argv)

    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH | GLUT_MULTISAMPLE)
    glutInitWindowSize(window_size.x, window_size.y)
    glutCreateWindow(b"MISA")
    glutIgnoreKeyRepeat(1)
    glutSetCursor(GLUT_CURSOR_NONE)

    glutDisplayFunc(handle_display)
    glutReshapeFunc(handle_reshape)
    glutTimerFunc(1000 // 60, handle_timer, 0)
    glutKeyboardFunc(handle_keyboard)
    glutKeyboardUpFunc(handle_keyboard_up)
    glutSpecialFunc(handle_special)
    glutSpecialUpFunc(handle_special_up)
    glutMotionFunc(handle_motion)
    glutPassiveMotionFunc(handle_motion)
    glutMouseFunc(handle_mouse)

    glEnable(GL_DEPTH_TEST)
    draw.init()
    glutMainLoop()


if __name__ == "__main__":
    main()
