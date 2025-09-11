#include "draw.h"

#include <GL/gl.h>

#include "util.h"

static const Vec3d origin = {};
static const int groundSize = 50;

void init(void) {
  glClearColor(0.53f, 0.81f, 0.98f, 1);
}

static void colorRgb(int r, int g, int b) {
  glColor3d((GLdouble)r / 255, (GLdouble)g / 255, (GLdouble)b / 255);
}

static void drawGround(void) {
  colorRgb(65, 152, 10);
  glBegin(GL_QUADS);
  glVertex3d(-groundSize, 0, -groundSize);
  glVertex3d(-groundSize, 0, groundSize);
  glVertex3d(groundSize, 0, groundSize);
  glVertex3d(groundSize, 0, -groundSize);
  glEnd();
}

static void drawGroundGrid(void) {
  const GLdouble groundGridY = 0.001;

  colorRgb(153, 153, 153);
  glBegin(GL_LINES);
  for (int i = -groundSize; i <= groundSize; i++) {
    glVertex3d(i, groundGridY, -groundSize);
    glVertex3d(i, groundGridY, groundSize);
    glVertex3d(-groundSize, groundGridY, i);
    glVertex3d(groundSize, groundGridY, i);
  }
  glEnd();
}

static void drawFloor(void) {
  const int floorWidth = 48, floorDepth = 40;
  const GLdouble floorY = 0.001;

  colorRgb(123, 107, 99);
  glBegin(GL_QUADS);
  glVertex3d(0, floorY, 0);
  glVertex3d(0, floorY, floorDepth);
  glVertex3d(floorWidth, floorY, floorDepth);
  glVertex3d(floorWidth, floorY, 0);
  glEnd();
}

static void drawRect(Vec3d startPos, Vec3d endPos) {
  glRectd(startPos.x, startPos.y, endPos.x, endPos.y);
}

static void drawFachada(void) {
  colorRgb(228, 206, 211);

  Vec3d asaSize = {10.5, 4.5, 0};
  Vec3d parteCentralSize = {13, 9.5, 0};

  Vec3d asaEsquerdaStart = origin;
  Vec3d asaEsquerdaEnd = asaSize;
  drawRect(asaEsquerdaStart, asaSize);

  Vec3d parteCentralStart = copyY3d(asaEsquerdaEnd, asaEsquerdaStart);
  Vec3d parteCentralEnd = sum3d(parteCentralStart, parteCentralSize);
  drawRect(parteCentralStart, parteCentralEnd);

  Vec3d asaDireitaStart = copyY3d(parteCentralEnd, parteCentralStart);
  Vec3d asaDireitaEnd = sum3d(asaDireitaStart, asaSize);
  drawRect(asaDireitaStart, asaDireitaEnd);
}

void draw(void) {
  drawGround();
  drawGroundGrid();
  drawFloor();
  drawFachada();
}
