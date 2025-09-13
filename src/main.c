#include <ctype.h>
#include <stdbool.h>
#include <stdlib.h>

#include <GL/freeglut_std.h>
#include <GL/gl.h>
#include <GL/glu.h>
#include <GL/freeglut_ext.h>

#include "draw.h"
#include "util.h"

// https://learnopengl.com/Getting-started/Camera
static const Vec3d cameraUp = {.x = 0, .y = 1, .z = 0};
static const double mouseSensitivity = 0.1;
static const double walkSpeed = 0.07195;

/* non-static */ Vec2i windowSize = {.x = 800, .y = 600};
static Vec2i lastMousePos = {};
static bool firstMouse = true;
static bool cameraFocused = true;
static bool keyState[256] = {};
static bool specialKeyState[256] = {};

/* non-static */ Vec3d cameraPos = {.x = 0, .y = 1.7, .z = -5};
static double pitch = 0, yaw = 90;

static void handleDisplay(void) {
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
  draw();
  glutSwapBuffers();
}

static void setupCamera(void) {
  glMatrixMode(GL_MODELVIEW);
  glLoadIdentity();
  Vec3d centerPos = sum3d(cameraPos, calcDirectionVec(toRadians(pitch), toRadians(yaw)));

  gluLookAt(
    cameraPos.x, cameraPos.y, cameraPos.z, centerPos.x, centerPos.y, centerPos.z, cameraUp.x, cameraUp.y,
    cameraUp.z
  );

  onSetupCamera();
}

static void handleReshape(int w, int h) {
  firstMouse = true;
  windowSize = (Vec2i){.x = w, .y = h};
  glViewport(0, 0, windowSize.x, windowSize.y);

  glMatrixMode(GL_PROJECTION);
  glLoadIdentity();
  gluPerspective(70, (double)windowSize.x / (double)windowSize.y, 0.1, 50);

  setupCamera();
}

static void moveCamera(bool perpendicular, bool negative) {
  Vec3d direction = calcDirectionVec(toRadians(pitch), toRadians(yaw));
  direction.y = 0;
  direction = normalize3d(direction);

  if (perpendicular) {
    direction = crossProduct3d(direction, cameraUp);
    direction.y = 0;
    direction = normalize3d(direction);
  }

  double speed = negative ? -walkSpeed : walkSpeed;
  direction = scalarMult3d(speed, direction);
  cameraPos = sum3d(cameraPos, direction);
}

static void setCameraFocused(bool value) {
  if (cameraFocused == value) {
    return;
  }

  cameraFocused = value;
  glutSetCursor(value ? GLUT_CURSOR_NONE : GLUT_CURSOR_INHERIT);

  if (value) {
    firstMouse = true;
  }
}

static void handleTimer(int value) {
  (void)value;

  if (keyState['\x1b']) {
    glutLeaveMainLoop();
    return;
  }

  bool changed = false;

  if (keyState['a']) {
    moveCamera(true, true);
    changed = true;
  }

  if (keyState['d']) {
    moveCamera(true, false);
    changed = true;
  }

  if (keyState['s']) {
    moveCamera(false, true);
    changed = true;
  }

  if (keyState['w']) {
    moveCamera(false, false);
    changed = true;
  }

  if (keyState[' ']) {
    cameraPos.y += walkSpeed;
    changed = true;
  }

  if (specialKeyState[GLUT_KEY_SHIFT_L]) {
    cameraPos.y -= walkSpeed;
    changed = true;
  }

  if (specialKeyState[GLUT_KEY_CTRL_L]) {
    setCameraFocused(false);
  }

  if (onLoop()) {
    changed = true;
  }

  if (changed) {
    setupCamera();
    glutPostRedisplay();
  }

  glutTimerFunc(1000 / 60, handleTimer, 0);
}

static void handleKeyboard(unsigned char key, int x, int y) {
  (void)x;
  (void)y;
  keyState[tolower(key)] = true;
}

static void handleKeyboardUp(unsigned char key, int x, int y) {
  (void)x;
  (void)y;
  keyState[tolower(key)] = false;
}

static void handleSpecial(int key, int x, int y) {
  (void)x;
  (void)y;
  specialKeyState[key] = true;
}

static void handleSpecialUp(int key, int x, int y) {
  (void)x;
  (void)y;
  specialKeyState[key] = false;
}

static void handleMotion(int x, int y) {
  if (firstMouse) {
    lastMousePos = (Vec2i){x, y};
    firstMouse = false;
    return;
  } else if (!cameraFocused) {
    lastMousePos = (Vec2i){x, y};
    return;
  }

  int dx = x - lastMousePos.x;
  int dy = lastMousePos.y - y;

  yaw += dx * mouseSensitivity;
  pitch = clamp(pitch + (dy * mouseSensitivity), -89.9, 89.9);

  // https://gamedev.stackexchange.com/a/98024
  if (x < 100 || x > windowSize.x - 100 || y < 100 || y > windowSize.y - 100) {
    int newX = windowSize.x / 2, newY = windowSize.y / 2;
    glutWarpPointer(newX, newY);
    lastMousePos = (Vec2i){newX, newY};
  } else {
    lastMousePos = (Vec2i){x, y};
  }

  setupCamera();
  glutPostRedisplay();
}

static void handleMouse(int button, int state, int x, int y) {
  if (!cameraFocused && !onMousePress(button, state, x, y) && button == GLUT_LEFT_BUTTON &&
      state == GLUT_DOWN) {
    setCameraFocused(true);
  }
}

int main(int argc, char *argv[]) {
  glutInit(&argc, argv);

  glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH | GLUT_MULTISAMPLE);
  glutInitWindowSize(windowSize.x, windowSize.y);
  glutCreateWindow("MISA");
  glutIgnoreKeyRepeat(1);
  glutSetCursor(GLUT_CURSOR_NONE);

  glutDisplayFunc(handleDisplay);
  glutReshapeFunc(handleReshape);
  glutTimerFunc(1000 / 60, handleTimer, 0);
  glutKeyboardFunc(handleKeyboard);
  glutKeyboardUpFunc(handleKeyboardUp);
  glutSpecialFunc(handleSpecial);
  glutSpecialUpFunc(handleSpecialUp);
  glutMotionFunc(handleMotion);
  glutPassiveMotionFunc(handleMotion);
  glutMouseFunc(handleMouse);

  glEnable(GL_DEPTH_TEST);
  init();
  glutMainLoop();

  return EXIT_SUCCESS;
}
