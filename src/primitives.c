#include <GL/gl.h>

#include "primitives.h"
#include "util.h"

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

void drawBox(Vec3d pos, Vec3d size) {
  glBegin(GL_QUADS);

  // Frente
  glVertex3d(pos.x, pos.y, pos.z);
  glVertex3d(pos.x + size.x, pos.y, pos.z);
  glVertex3d(pos.x + size.x, pos.y + size.y, pos.z);
  glVertex3d(pos.x, pos.y + size.y, pos.z);

  // Trás
  glVertex3d(pos.x, pos.y, pos.z - size.z);
  glVertex3d(pos.x + size.x, pos.y, pos.z - size.z);
  glVertex3d(pos.x + size.x, pos.y + size.y, pos.z - size.z);
  glVertex3d(pos.x, pos.y + size.y, pos.z - size.z);

  // Esquerda
  glVertex3d(pos.x, pos.y, pos.z);
  glVertex3d(pos.x, pos.y, pos.z - size.z);
  glVertex3d(pos.x, pos.y + size.y, pos.z - size.z);
  glVertex3d(pos.x, pos.y + size.y, pos.z);

  // Direita
  glVertex3d(pos.x + size.x, pos.y, pos.z);
  glVertex3d(pos.x + size.x, pos.y, pos.z - size.z);
  glVertex3d(pos.x + size.x, pos.y + size.y, pos.z - size.z);
  glVertex3d(pos.x + size.x, pos.y + size.y, pos.z);

  // Topo
  glVertex3d(pos.x, pos.y + size.y, pos.z);
  glVertex3d(pos.x + size.x, pos.y + size.y, pos.z);
  glVertex3d(pos.x + size.x, pos.y + size.y, pos.z - size.z);
  glVertex3d(pos.x, pos.y + size.y, pos.z - size.z);

  // Base
  glVertex3d(pos.x, pos.y, pos.z);
  glVertex3d(pos.x + size.x, pos.y, pos.z);
  glVertex3d(pos.x + size.x, pos.y, pos.z - size.z);
  glVertex3d(pos.x, pos.y, pos.z - size.z);

  glEnd();
}
