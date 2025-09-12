#include <GL/gl.h>

#include "primitives.h"

void colorRgb(int r, int g, int b) {
  glColor3d((double)r / 255, (double)g / 255, (double)b / 255);
}

void drawRectY(double x1, double z1, double x2, double z2, double y) {
  glBegin(GL_QUADS);
  glVertex3d(x1, y, z1);
  glVertex3d(x2, y, z1);
  glVertex3d(x2, y, z2);
  glVertex3d(x1, y, z2);
  glEnd();
}

void drawRectZ(double x1, double y1, double x2, double y2, double z) {
  glBegin(GL_QUADS);
  glVertex3d(x1, y1, z);
  glVertex3d(x2, y1, z);
  glVertex3d(x2, y2, z);
  glVertex3d(x1, y2, z);
  glEnd();
}
