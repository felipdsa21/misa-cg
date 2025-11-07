import math
import sys

from OpenGL import GL, GLU, GLUT

from . import scene, util

# Não incluido pelo PyOpenGL
GLUT_KEY_SHIFT_L = 112
GLUT_KEY_CTRL_L = 114

# https://learnopengl.com/Getting-started/Camera
camera_up = util.Vec3d(0, 1, 0)
mouse_sensitivity = 0.1
walk_speed = 0.07195

# Estado global
window_size = util.Vec2i(800, 600)
last_mouse_pos = util.Vec2i(0, 0)
first_mouse = True
camera_focused = True
key_state = [False] * 256
special_key_state = [False] * 256

camera_pos = util.Vec3d(0, 1.7, -5)
pitch = 0.0
yaw = 90.0


def handle_display() -> None:
    GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
    scene.draw()
    GLUT.glutSwapBuffers()


def setup_camera() -> None:
    GL.glMatrixMode(GL.GL_MODELVIEW)
    GL.glLoadIdentity()
    direction = util.direction_vector(math.radians(pitch), math.radians(yaw))
    center_pos = camera_pos + direction

    GLU.gluLookAt(
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

    scene.on_setup_camera()


def handle_reshape(w: int, h: int) -> None:
    global first_mouse, window_size, camera_pos
    first_mouse = True

    window_size = util.Vec2i(w, h)
    GL.glViewport(0, 0, window_size.x, window_size.y)

    GL.glMatrixMode(GL.GL_PROJECTION)
    GL.glLoadIdentity()
    GLU.gluPerspective(70, window_size.x / window_size.y, 0.1, 50)
    setup_camera()


def move_camera(perpendicular: bool, negative: bool) -> None:
    global camera_pos
    direction = util.direction_vector(math.radians(pitch), math.radians(yaw))
    direction = direction.with_y(0).normalized()

    if perpendicular:
        direction = direction.cross(camera_up).with_y(0).normalized()

    speed = -walk_speed if negative else walk_speed
    camera_pos = camera_pos + speed * direction


def set_camera_focused(value: bool) -> None:
    global camera_focused, first_mouse
    if camera_focused == value:
        return

    camera_focused = value
    GLUT.glutSetCursor(GLUT.GLUT_CURSOR_NONE if value else GLUT.GLUT_CURSOR_INHERIT)

    if value:
        first_mouse = True


def handle_timer(value: int) -> None:
    global camera_pos, camera_focused, window_size

    if key_state[27]:  # ESC
        GLUT.glutLeaveMainLoop()
        return

    changed = False

    if key_state[ord("a")]:
        move_camera(True, True)
        changed = True

    if key_state[ord("d")]:
        move_camera(True, False)
        changed = True

    if key_state[ord("s")]:
        move_camera(False, True)
        changed = True

    if key_state[ord("w")]:
        move_camera(False, False)
        changed = True

    if key_state[ord(" ")]:
        camera_pos = camera_pos.with_y(camera_pos.y + walk_speed)
        changed = True

    if special_key_state[GLUT_KEY_SHIFT_L]:
        camera_pos = camera_pos.with_y(camera_pos.y - walk_speed)
        changed = True

    if special_key_state[GLUT_KEY_CTRL_L]:
        set_camera_focused(False)

    if scene.on_loop():
        changed = True

    if changed:
        setup_camera()
        GLUT.glutPostRedisplay()

    GLUT.glutTimerFunc(1000 // 60, handle_timer, 0)


def handle_keyboard(key: bytes, x: int, y: int) -> None:
    key_state[ord(key.lower())] = True


def handle_keyboard_up(key: bytes, x: int, y: int) -> None:
    key_state[ord(key.lower())] = False


def handle_special(key: int, x: int, y: int) -> None:
    special_key_state[key] = True


def handle_special_up(key: int, x: int, y: int) -> None:
    special_key_state[key] = False


def handle_motion(x: int, y: int) -> None:
    global first_mouse, last_mouse_pos, pitch, yaw, window_size, camera_pos

    if first_mouse or not camera_focused:
        last_mouse_pos = util.Vec2i(x, y)
        first_mouse = False
        return

    dx = x - last_mouse_pos.x
    dy = last_mouse_pos.y - y

    yaw += dx * mouse_sensitivity
    pitch = util.clamp(pitch + dy * mouse_sensitivity, -89.9, 89.9)

    # Warp do mouse quando próximo das bordas
    # https://gamedev.stackexchange.com/a/98024
    margin = 100
    if not (margin <= x <= window_size.x - margin and margin <= y <= window_size.y - margin):
        new_x = window_size.x // 2
        new_y = window_size.y // 2
        GLUT.glutWarpPointer(new_x, new_y)
        last_mouse_pos = util.Vec2i(new_x, new_y)
    else:
        last_mouse_pos = util.Vec2i(x, y)

    setup_camera()
    GLUT.glutPostRedisplay()


def handle_mouse(button: int, state: int, x: int, y: int) -> None:
    global camera_focused
    if (
        not camera_focused
        and not scene.on_mouse_press(button, state, x, y)
        and button == GLUT.GLUT_LEFT_BUTTON
        and state == GLUT.GLUT_DOWN
    ):
        set_camera_focused(True)


def main() -> None:
    global window_size, camera_pos
    GLUT.glutInit(sys.argv)

    GLUT.glutInitDisplayMode(GLUT.GLUT_DOUBLE | GLUT.GLUT_RGBA | GLUT.GLUT_DEPTH | GLUT.GLUT_MULTISAMPLE)
    GLUT.glutInitWindowSize(window_size.x, window_size.y)
    GLUT.glutCreateWindow(b"MISA")
    GLUT.glutIgnoreKeyRepeat(1)
    GLUT.glutSetCursor(GLUT.GLUT_CURSOR_NONE)

    GLUT.glutDisplayFunc(handle_display)
    GLUT.glutReshapeFunc(handle_reshape)
    GLUT.glutTimerFunc(1000 // 60, handle_timer, 0)
    GLUT.glutKeyboardFunc(handle_keyboard)
    GLUT.glutKeyboardUpFunc(handle_keyboard_up)
    GLUT.glutSpecialFunc(handle_special)
    GLUT.glutSpecialUpFunc(handle_special_up)
    GLUT.glutMotionFunc(handle_motion)
    GLUT.glutPassiveMotionFunc(handle_motion)
    GLUT.glutMouseFunc(handle_mouse)

    GL.glEnable(GL.GL_DEPTH_TEST)
    scene.init()
    GLUT.glutMainLoop()


if __name__ == "__main__":
    main()
