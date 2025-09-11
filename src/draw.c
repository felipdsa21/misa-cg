#include "draw.h"

#include <GL/freeglut_std.h>
#include <GL/gl.h>

static const int groundSize = 50;
static const GLdouble groundGridY = 0.001;

void init(void) {
  glClearColor(0.53f, 0.81f, 0.98f, 1);
}

static void drawGround(void) {
  glColor3d(0.25, 0.59, 0.03);
  glBegin(GL_QUADS);
  glVertex3d(-groundSize, 0, -groundSize);
  glVertex3d(-groundSize, 0, groundSize);
  glVertex3d(groundSize, 0, groundSize);
  glVertex3d(groundSize, 0, -groundSize);
  glEnd();
}

static void drawGroundGrid(void) {
  glColor3d(0.6, 0.6, 0.6);
  glBegin(GL_LINES);
  for (int i = -groundSize; i <= groundSize; i++) {
    glVertex3d(i, groundGridY, -groundSize);
    glVertex3d(i, groundGridY, groundSize);
    glVertex3d(-groundSize, groundGridY, i);
    glVertex3d(groundSize, groundGridY, i);
  }
  glEnd();
}

static void drawStar(void) {
  glColor3d(1, 1, 0);
  glPushMatrix();
  glTranslatef(0.5, 0, 0.5);
  glRotatef(90, 1, 0, 0);
  glutWireSphere(0.5, 20, 16);
  glPopMatrix();
}

void draw(void) {
  drawGround();
  drawGroundGrid();
  drawStar();
}
