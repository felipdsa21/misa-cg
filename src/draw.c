#include "draw.h"

#include <GL/gl.h>

#include "util.h"

static const int groundSize = 50;

static const Vec3d parteCentralSize = {13, 9.5, 20};
static const Vec3d portaSize = {2.8, 3.2, 0};
static const Vec3d asaSize = {10.5, 4.5, 10.5};
static const double asaZOffset = 1;

void init(void) {
  glClearColor(0.53f, 0.81f, 0.98f, 1);

  glEnable(GL_LIGHTING);
  glEnable(GL_LIGHT0);
  glEnable(GL_NORMALIZE);
  glShadeModel(GL_SMOOTH);

  glEnable(GL_COLOR_MATERIAL);
  glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE);

  float luzAmbiente[] = {0.15f, 0.15f, 0.15f, 1};
  float luzDifusa[] = {0.8f, 0.8f, 0.8f, 1};
  float luzEspecular[] = {0.1f, 0.1f, 0.1f, 1};
  float posicaoLuz[] = {0, -1, 1, 0};

  glLightfv(GL_LIGHT0, GL_AMBIENT, luzAmbiente);
  glLightfv(GL_LIGHT0, GL_DIFFUSE, luzDifusa);
  glLightfv(GL_LIGHT0, GL_SPECULAR, luzEspecular);
  glLightfv(GL_LIGHT0, GL_POSITION, posicaoLuz);
}

static void colorRgb(int r, int g, int b) {
  glColor3d((double)r / 255, (double)g / 255, (double)b / 255);
}

static void drawRectY(double x1, double z1, double x2, double z2, double y) {
  glBegin(GL_QUADS);
  glVertex3d(x1, y, z1);
  glVertex3d(x2, y, z1);
  glVertex3d(x2, y, z2);
  glVertex3d(x1, y, z2);
  glEnd();
}

static void drawRectZ(double x1, double y1, double x2, double y2, double z) {
  glBegin(GL_QUADS);
  glVertex3d(x1, y1, z);
  glVertex3d(x2, y1, z);
  glVertex3d(x2, y2, z);
  glVertex3d(x1, y2, z);
  glEnd();
}

static void drawGround(void) {
  colorRgb(65, 152, 10);
  glNormal3i(0, 1, 0);
  drawRectY(-groundSize, -groundSize, groundSize, groundSize, 0);
}

static void drawGroundGrid(void) {
  double groundGridY = 0.001;

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

static void drawChao(void) {
  int floorWidth = 48, floorDepth = 40;
  double floorY = 0.001;

  colorRgb(123, 107, 99);
  glNormal3i(0, 1, 0);
  drawRectY(0, 0, floorWidth, floorDepth, floorY);
}

static void drawAsa(void) {
  // Frente
  glNormal3i(0, 0, -1);
  glRectd(0, 0, asaSize.x, asaSize.y);

  // Atrás
  glNormal3i(0, 0, 1);
  drawRectZ(0, 0, asaSize.x, asaSize.y, asaSize.z);

  // Lado
  glPushMatrix();
  glRotatef(-90, 0, 1, 0);
  glNormal3i(-1, 0, 0);
  glRectd(0, 0, asaSize.z, asaSize.y);
  glPopMatrix();

  // Cima
  glNormal3i(0, 1, 0);
  drawRectY(0, 0, asaSize.x, asaSize.z, asaSize.y);
}

static void drawParteCentral() {
  // Frente
  double xAntesPorta = (parteCentralSize.x - portaSize.x) / 2;

  glNormal3i(0, 0, -1);
  glRectd(0, 0, xAntesPorta, parteCentralSize.y);
  glRectd(xAntesPorta, portaSize.y, xAntesPorta + portaSize.x, parteCentralSize.y);
  glRectd(xAntesPorta + portaSize.x, 0, parteCentralSize.x, parteCentralSize.y);

  // Atrás
  glNormal3i(0, 0, 1);
  drawRectZ(0, 0, parteCentralSize.x, parteCentralSize.y, parteCentralSize.z);

  // Cima
  glNormal3i(0, 1, 0);
  drawRectY(0, 0, parteCentralSize.x, parteCentralSize.z, parteCentralSize.y);

  // Lados
  double zDepoisAsa = asaZOffset + asaSize.x;
  glPushMatrix();
  glRotatef(-90, 0, 1, 0);

  glNormal3i(-1, 0, 0);
  glRectd(0, 0, asaZOffset, asaSize.y); // Em frente a asa
  glRectd(0, asaSize.y, zDepoisAsa, parteCentralSize.y); // Cima
  glRectd(zDepoisAsa, 0, parteCentralSize.z, parteCentralSize.y); // Atrás

  glTranslated(0, 0, -parteCentralSize.x);
  glNormal3i(-1, 0, 0);
  glRectd(0, 0, asaZOffset, asaSize.y); // Em frente a asa
  glRectd(0, asaSize.y, zDepoisAsa, parteCentralSize.y); // Cima
  glRectd(zDepoisAsa, 0, parteCentralSize.z, parteCentralSize.y); // Atrás

  glPopMatrix();
}

static void drawParteExterna(void) {
  colorRgb(228, 206, 211);
  glPushMatrix();

  // Asa direita
  glTranslated(0, 0, asaZOffset);
  drawAsa();

  // Parte central
  glTranslated(asaSize.x, 0, -asaZOffset);
  drawParteCentral();

  // Asa esquerda
  glTranslated(parteCentralSize.x, 0, asaZOffset);
  glTranslated(asaSize.x, 0, 0);
  glScalef(-1, 1, 1); // Espelha
  drawAsa();

  glPopMatrix();
}

void draw() {
  drawGround();
  drawGroundGrid();

  glPushMatrix();
  glTranslated(-(parteCentralSize.x / 2 + asaSize.x), 0, 0);

  drawParteExterna();
  drawChao();

  glPopMatrix();
}
