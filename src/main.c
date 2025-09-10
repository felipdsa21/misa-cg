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

// https://learnopengl.com/Getting-started/Camera
static Vec3d cameraPos = {.x = 0, .y = 0, .z = 5};
static const Vec3d cameraUp = {.x = 0, .y = 1, .z = 0};
static GLdouble pitch = 0, yaw = -90;

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
  gluPerspective(60, (GLdouble)windowSize.x / (GLdouble)windowSize.y, 1, 20);

  Vec3d centerPos = sum3d(cameraPos, calcDirectionVec(radians(pitch), radians(yaw)));

  gluLookAt(
    cameraPos.x, cameraPos.y, cameraPos.z, centerPos.x, centerPos.y, centerPos.z, cameraUp.x, cameraUp.y,
    cameraUp.z
  );
}

static void handleReshape(int w, int h) {
  windowSize = (Vec2sizei){.x = w, .y = h};
  firstMouse = true;
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

  directionVec = scalarMult3d(negative ? -0.05 : 0.05, directionVec);
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
  default:
    return;
  }

  setupCamera();
  glutPostRedisplay();
}

static void handleMotion(int x, int y) {
  if (firstMouse) {
    lastMousePos = (Vec2sizei){x, y};
    firstMouse = false;
    return;
  }

  yaw += x - lastMousePos.x;
  pitch = clamp(pitch + (lastMousePos.y - y), 89.9, -89.9);
  lastMousePos = (Vec2sizei){x, y};

  // https://gamedev.stackexchange.com/a/98024
  if (x < 100 || x > windowSize.x - 100 || y < 100 || y > windowSize.y - 100) {
    glutWarpPointer(windowSize.x / 2, windowSize.y / 2);
  }

  setupCamera();
  glutPostRedisplay();
}

int main(int argc, char *argv[]) {
  glutInit(&argc, argv);

  glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB);
  glutInitWindowSize(500, 500);
  glutInitWindowPosition(100, 100);
  glutCreateWindow("MISA");
  glutSetCursor(GLUT_CURSOR_NONE);

  init();
  glutDisplayFunc(display);
  glutReshapeFunc(handleReshape);
  glutKeyboardFunc(handleKeyboard);
  glutMotionFunc(handleMotion);
  glutPassiveMotionFunc(handleMotion);
  glutMainLoop();

  return EXIT_SUCCESS;
}
