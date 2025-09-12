#include <GL/gl.h>

#include "draw.h"
#include "obj.h"
#include "objImporter.h"
#include "primitives.h"
#include "util.h"

static const int groundSize = 50;
static const double groundGridY = 0.001;

static const double pisoY = 1;
static const double segundoAndarY = 7;
static const Vec2d aberturaEscadaSize = {1, 3};

static const Vec3d parteCentralSize = {13, 13.5, 20};
static const Vec3d asaSize = {10.5, 7, 15};
static const double asaZOffset = 1;

static const Vec3d portaSize = {2.8, 3.2, 0};

static const Vec3d janelaComArco = {1.2, 2.6, 0.3};
static const Vec3d janelaRetangularSize = {1.2, 2, 0.3};
static const double janelaBaixoYOffset = 1;
static const double janelaCimaYOffset = janelaBaixoYOffset + 1.2 + 3.2;

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

static void drawGround(void) {
  colorRgb(65, 152, 10);
  glNormal3i(0, 1, 0);
  drawRectY(-groundSize, -groundSize, groundSize, groundSize, 0);
}

static void drawGroundGrid(void) {
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

static void drawPisos(void) {
  colorRgb(123, 107, 99);
  glNormal3i(0, 1, 0);
  glPushMatrix();

  // Asa direita
  glTranslated(0, 0, asaZOffset);
  drawRectY(0, 0, asaSize.x, asaSize.z, pisoY);

  // Parte central
  glTranslated(asaSize.x, 0, -asaZOffset);
  drawRectY(0, 0, parteCentralSize.x, parteCentralSize.z, pisoY);

  // Segundo andar
  GLdouble limiteX = parteCentralSize.x - aberturaEscadaSize.x;
  GLdouble limiteZ = parteCentralSize.z / 2;
  GLdouble fimAberturaZ = limiteZ + aberturaEscadaSize.y;

  drawRectY(0, 0, limiteX, parteCentralSize.z, segundoAndarY);
  drawRectY(limiteX, 0, parteCentralSize.x, limiteZ, segundoAndarY);
  drawRectY(limiteX, fimAberturaZ, parteCentralSize.x, parteCentralSize.z, segundoAndarY);
  drawRectY(parteCentralSize.x - 0.1, limiteZ, parteCentralSize.x, fimAberturaZ, segundoAndarY);

  // Asa esquerda
  glTranslated(parteCentralSize.x, 0, asaZOffset);
  drawRectY(0, 0, asaSize.x, asaSize.z, pisoY);

  glPopMatrix();
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
  double zDepoisAsa = asaZOffset + asaSize.z;
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

static void drawParteExterna(void (*asaFunc)(void), void (*parteCentralFunc)(void)) {
  colorRgb(228, 206, 211);
  glPushMatrix();

  // Asa direita
  glTranslated(0, 0, asaZOffset);
  asaFunc();

  // Parte central
  glTranslated(asaSize.x, 0, -asaZOffset);
  parteCentralFunc();

  // Asa esquerda
  glTranslated(parteCentralSize.x, 0, asaZOffset);
  glTranslated(asaSize.x, 0, 0);
  glScalef(-1, 1, 1); // Espelha
  asaFunc();

  glPopMatrix();
}

static void drawObjetos(void) {
  Model obj = loadModel("models/Mesa.obj");
  glPushMatrix();
  glTranslatef(10.0f, 0.0f, 7.0f); // movendo o objeto
  glRotatef(-90.0f, 0.0f, 1.0f, 0.0f);
  glColor3f(0.0f, 0.0f, 0.0f);
  drawModelFaces(obj);
  glPopMatrix();

  obj = loadModel("models/Flores.obj");
  glPushMatrix();
  glTranslatef(10.5f, 1.0f, 6.5f); // movendo o objeto
  glRotatef(180.0f, 0.0f, 1.0f, 0.0f);
  glScalef(0.2f, 0.2f, 0.2f); // reduzindo a escala
  glColor3f(1.0f, 0.0f, 0.0f);
  drawModelFaces(obj);
  glPopMatrix();

  glPushMatrix();
  glTranslatef(10.5f, 1.0f, 7.5f); // movendo o objeto
  glRotatef(180.0f, 0.0f, 1.0f, 0.0f);
  glScalef(0.2f, 0.2f, 0.2f); // reduzindo a escala
  glColor3f(1.0f, 0.0f, 0.0f);
  drawModelFaces(obj);
  glPopMatrix();
}

static void drawJanelaComArcoAjustado(Vec3d pos) {
  glPushMatrix();
  glTranslated(pos.x, pos.y, pos.z);
  drawJanelaComArco(janelaComArco.x, janelaComArco.y, janelaComArco.z);
  glPopMatrix();
}

static void drawJanelaRetangularAjustado(Vec3d pos) {
  glPushMatrix();
  glTranslated(pos.x, pos.y, pos.z);
  drawJanelaRetangular(janelaRetangularSize.x, janelaRetangularSize.y, janelaRetangularSize.z);
  glPopMatrix();
}

static void drawJanelasAsa(void) {
  // Frente
  int distBase = 3;
  int x = 0;

  Vec3d janelaPos = {-janelaRetangularSize.x, janelaBaixoYOffset, 0};

  for (int i = 0; i < 3; i++) {
    janelaPos.x += distBase;
    drawJanelaRetangularAjustado(janelaPos);
  }
}

static void drawJanelasParteCentral(void) {
  // Frente
  double xAntesPorta = (parteCentralSize.x - portaSize.x) / 2;
  glNormal3i(0, 0, -1);

  double distLado = (xAntesPorta - janelaComArco.x) / 2;
  double distCentro = xAntesPorta + (portaSize.x - janelaComArco.x) / 2;

  Vec3d janelaPos = {distLado, janelaBaixoYOffset, 0};
  drawJanelaComArcoAjustado(janelaPos);
  janelaPos.y = janelaCimaYOffset;
  drawJanelaComArcoAjustado(janelaPos);

  janelaPos.x = distCentro;
  drawJanelaComArcoAjustado(janelaPos);

  janelaPos.x = xAntesPorta + portaSize.x + distLado;
  janelaPos.y = janelaBaixoYOffset;
  drawJanelaComArcoAjustado(janelaPos);
  janelaPos.y = janelaCimaYOffset;
  drawJanelaComArcoAjustado(janelaPos);
}

void draw() {
  drawGround();
  drawGroundGrid();

  glPushMatrix();
  glTranslated(-(parteCentralSize.x / 2 + asaSize.x), 0, 0);

  drawPisos();
  drawParteExterna(drawAsa, drawParteCentral);
  drawParteExterna(drawJanelasAsa, drawJanelasParteCentral);

  glPopMatrix();
  drawObjetos();
}
