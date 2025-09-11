#include <stdbool.h>
#include <stdlib.h>

#include <GL/freeglut_std.h>
#include <GL/gl.h>
#include <GL/glu.h>
#include <GL/freeglut_ext.h>

#include "draw.h"
#include "util.h"

static Vec2sizei windowSize = {};
static Vec2sizei lastMousePos = {};
static bool firstMouse = true;
static bool goingDown = false;

// https://learnopengl.com/Getting-started/Camera
static Vec3d cameraPos = {.x = 0, .y = 0.1, .z = 5};
static const Vec3d cameraUp = {.x = 0, .y = 1, .z = 0};
static GLdouble pitch = 0, yaw = -90;
static const GLdouble mouseSensitivity = 0.1;
static const GLdouble walkSpeed = 0.05;

static void init(void) {
  glClearColor(0, 0, 0, 0);
}

static void display(void) {
  glClear(GL_COLOR_BUFFER_BIT);
  draw();
  glutSwapBuffers();
}

static void setupCamera(void) {
  glMatrixMode(GL_MODELVIEW);
  glLoadIdentity();
  gluPerspective(60, (GLdouble)windowSize.x / (GLdouble)windowSize.y, 0.1, 20);

  Vec3d centerPos = sum3d(cameraPos, calcDirectionVec(radians(pitch), radians(yaw)));

  gluLookAt(
    cameraPos.x, cameraPos.y, cameraPos.z, centerPos.x, centerPos.y, centerPos.z, cameraUp.x, cameraUp.y,
    cameraUp.z
  );
}

static void handleReshape(int w, int h) {
  firstMouse = true;
  windowSize = (Vec2sizei){.x = w, .y = h};
  glViewport(0, 0, windowSize.x, windowSize.y);
  setupCamera();
}

static void moveCamera(bool perpendicular, bool negative) {
  Vec3d directionVec = calcDirectionVec(radians(pitch), radians(yaw));
  directionVec.y = 0;
  directionVec = normalize3d(directionVec);

  if (perpendicular) {
    directionVec = crossProduct3d(directionVec, cameraUp);
    directionVec.y = 0;
    directionVec = normalize3d(directionVec);
  }

  directionVec = scalarMult3d(negative ? -walkSpeed : walkSpeed, directionVec);
  cameraPos = sum3d(cameraPos, directionVec);
}

static void handleKeyboard(unsigned char key, int x, int y) {
  (void)x;
  (void)y;

  switch (key) {
  case '\x1b':
    glutLeaveMainLoop();
    return;
  case 'a':
    moveCamera(true, true);
    break;
  case 'd':
    moveCamera(true, false);
    break;
  case 's':
    moveCamera(false, true);
    break;
  case 'w':
    moveCamera(false, false);
    break;
  case ' ':
    cameraPos.y += walkSpeed;
    break;
  default:
    return;
  }

  setupCamera();
  glutPostRedisplay();
}

static void handleSpecial(int key, int x, int y) {
  (void)x;
  (void)y;

  switch (key) {
  case GLUT_KEY_SHIFT_L:
    goingDown = true;
    break;
  }
}

static void handleSpecialUp(int key, int x, int y) {
  (void)x;
  (void)y;

  switch (key) {
  case GLUT_KEY_SHIFT_L:
    goingDown = false;
    break;
  }
}

static void handleMotion(int x, int y) {
  if (firstMouse) {
    lastMousePos = (Vec2sizei){x, y};
    firstMouse = false;
    return;
  }

  int dx = x - lastMousePos.x;
  int dy = lastMousePos.y - y;

  yaw += dx * mouseSensitivity;
  pitch = clamp(pitch + (dy * mouseSensitivity), 89.9, -89.9);

  // https://gamedev.stackexchange.com/a/98024
  if (x < 100 || x > windowSize.x - 100 || y < 100 || y > windowSize.y - 100) {
    GLsizei newX = windowSize.x / 2, newY = windowSize.y / 2;
    glutWarpPointer(newX, newY);
    lastMousePos = (Vec2sizei){newX, newY};
  } else {
    lastMousePos = (Vec2sizei){x, y};
  }

  setupCamera();
  glutPostRedisplay();
}

static void handleTimer(int value) {
  (void)value;

  if (goingDown) {
    cameraPos.y -= walkSpeed;
    setupCamera();
    glutPostRedisplay();
  }

  glutTimerFunc(1000 / 60, handleTimer, 0);
}

int main(int argc, char *argv[]) {
  glutInit(&argc, argv);

  glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB);
  glutInitWindowSize(800, 600);
  glutCreateWindow("MISA");
  glutSetCursor(GLUT_CURSOR_NONE);

  init();
  glutDisplayFunc(display);
  glutTimerFunc(1000 / 60, handleTimer, 0);
  glutReshapeFunc(handleReshape);
  glutKeyboardFunc(handleKeyboard);
  glutSpecialFunc(handleSpecial);
  glutSpecialUpFunc(handleSpecialUp);
  glutMotionFunc(handleMotion);
  glutPassiveMotionFunc(handleMotion);
  glutMainLoop();

  return EXIT_SUCCESS;
}
