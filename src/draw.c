#include <math.h>

#include <GL/gl.h>

#include "draw.h"
#include "objImporter.h"
#include "util.h"

static Model obj;

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

// funções auxiliares para a janela
static void drawBox(Vec3d p, GLdouble w, GLdouble h, GLdouble d) {
  glBegin(GL_QUADS);
  // frente
  glVertex3d(p.x, p.y, p.z);
  glVertex3d(p.x + w, p.y, p.z);
  glVertex3d(p.x + w, p.y + h, p.z);
  glVertex3d(p.x, p.y + h, p.z);
  // trás
  glVertex3d(p.x, p.y, p.z - d);
  glVertex3d(p.x + w, p.y, p.z - d);
  glVertex3d(p.x + w, p.y + h, p.z - d);
  glVertex3d(p.x, p.y + h, p.z - d);
  // esquerda
  glVertex3d(p.x, p.y, p.z);
  glVertex3d(p.x, p.y, p.z - d);
  glVertex3d(p.x, p.y + h, p.z - d);
  glVertex3d(p.x, p.y + h, p.z);
  // direita
  glVertex3d(p.x + w, p.y, p.z);
  glVertex3d(p.x + w, p.y, p.z - d);
  glVertex3d(p.x + w, p.y + h, p.z - d);
  glVertex3d(p.x + w, p.y + h, p.z);
  // topo
  glVertex3d(p.x, p.y + h, p.z);
  glVertex3d(p.x + w, p.y + h, p.z);
  glVertex3d(p.x + w, p.y + h, p.z - d);
  glVertex3d(p.x, p.y + h, p.z - d);
  // base
  glVertex3d(p.x, p.y, p.z);
  glVertex3d(p.x + w, p.y, p.z);
  glVertex3d(p.x + w, p.y, p.z - d);
  glVertex3d(p.x, p.y, p.z - d);
  glEnd();
}

static void drawArchRing(
  GLdouble cx, GLdouble cy, GLdouble outerR, GLdouble innerR, GLdouble zFront, GLdouble depth, int segments
) {
  GLdouble zBack = zFront - depth;

  // anel frontal
  glBegin(GL_TRIANGLE_STRIP);
  for (int i = 0; i <= segments; ++i) {
    GLdouble a = PI * (GLdouble)i / (GLdouble)segments; // 0..pi
    GLdouble xo = cos(a) * outerR, yo = sin(a) * outerR;
    GLdouble xi = cos(a) * innerR, yi = sin(a) * innerR;
    glVertex3d(cx + xo, cy + yo, zFront);
    glVertex3d(cx + xi, cy + yi, zFront);
  }
  glEnd();

  // anel traseiro
  glBegin(GL_TRIANGLE_STRIP);
  for (int i = 0; i <= segments; ++i) {
    GLdouble a = PI * (GLdouble)i / (GLdouble)segments;
    GLdouble xo = cos(a) * outerR, yo = sin(a) * outerR;
    GLdouble xi = cos(a) * innerR, yi = sin(a) * innerR;
    glVertex3d(cx + xo, cy + yo, zBack);
    glVertex3d(cx + xi, cy + yi, zBack);
  }
  glEnd();

  // lateral externa
  glBegin(GL_QUAD_STRIP);
  for (int i = 0; i <= segments; ++i) {
    GLdouble a = PI * (GLdouble)i / (GLdouble)segments;
    GLdouble xo = cos(a) * outerR, yo = sin(a) * outerR;
    glVertex3d(cx + xo, cy + yo, zFront);
    glVertex3d(cx + xo, cy + yo, zBack);
  }
  glEnd();

  // lateral interna
  glBegin(GL_QUAD_STRIP);
  for (int i = 0; i <= segments; ++i) {
    GLdouble a = PI * (GLdouble)i / (GLdouble)segments;
    GLdouble xi = cos(a) * innerR, yi = sin(a) * innerR;
    glVertex3d(cx + xi, cy + yi, zBack);
    glVertex3d(cx + xi, cy + yi, zFront);
  }
  glEnd();
}

// função para a janela
static void drawMuseumWindow(
  Vec3d pos,
  GLdouble width, // largura total
  GLdouble height, // altura total (reta + arco)
  GLdouble frame, // espessura da moldura
  GLdouble depth
) { // quanto "entra" na parede
  if (frame > width * 0.45) {
    frame = width * 0.45;
  }

  GLdouble radius = width / 2.0; // arco semicircular
  if (height <= radius) {
    height = radius + 0.01;
  }
  GLdouble rectH = height - radius; // parte reta
  const int seg = 48;
  const GLdouble eps = 0.002; // evita z-fighting
  GLdouble zFront = pos.z;

  // --- Moldura (tom rosado) ---
  colorRgb(191, 124, 124);
  // ombreiras (laterais) e peitoril (base)
  drawBox((Vec3d){pos.x, pos.y, zFront}, frame, rectH, depth);
  drawBox((Vec3d){pos.x + width - frame, pos.y, zFront}, frame, rectH, depth);
  drawBox((Vec3d){pos.x, pos.y, zFront}, width, frame, depth);

  // arco superior (anel extrudado)
  GLdouble cx = pos.x + radius;
  GLdouble cy = pos.y + rectH;
  drawArchRing(cx, cy, radius, radius - frame, zFront, depth, seg);

  // --- Vidro translúcido ---
  glEnable(GL_BLEND);
  glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
  glColor4d(0.78, 0.87, 0.96, 0.25); // azul claro com alpha

  // retângulo de vidro (parte reta)
  glBegin(GL_QUADS);
  glVertex3d(pos.x + frame, pos.y + frame, zFront - eps);
  glVertex3d(pos.x + width - frame, pos.y + frame, zFront - eps);
  glVertex3d(pos.x + width - frame, pos.y + rectH - frame, zFront - eps);
  glVertex3d(pos.x + frame, pos.y + rectH - frame, zFront - eps);
  glEnd();

  // vidro do arco
  glBegin(GL_TRIANGLE_FAN);
  glVertex3d(cx, cy, zFront - eps);
  for (int i = 0; i <= seg; ++i) {
    GLdouble a = PI * (GLdouble)i / (GLdouble)seg;
    GLdouble xi = cos(a) * (radius - frame);
    GLdouble yi = sin(a) * (radius - frame);
    glVertex3d(cx + xi, cy + yi, zFront - eps);
  }
  glEnd();

  glDisable(GL_BLEND);

  // --- Travessas internas (caixilhos) ---
  colorRgb(191, 124, 124);
  GLdouble bar = frame * 0.45;
  GLdouble innerW = width - 2.0 * frame;
  GLdouble glassBottom = pos.y + frame;
  GLdouble glassTopRect = pos.y + rectH - frame;

  // montante vertical central
  drawBox(
    (Vec3d){pos.x + width / 2.0 - bar / 2.0, glassBottom, zFront - eps}, bar, (glassTopRect - glassBottom),
    eps * 2.0
  );

  // travessa horizontal central (forma o "+")
  GLdouble centerY = (glassBottom + glassTopRect) / 2.0 - bar / 2.0;
  drawBox((Vec3d){pos.x + frame, centerY, zFront - eps}, innerW, bar, eps * 2.0);

  // travessa horizontal próxima ao arco (mantida)
  drawBox((Vec3d){pos.x + frame, pos.y + rectH - frame - bar / 2.0, zFront - eps}, innerW, bar, eps * 2.0);
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

void draw() {
  drawGround();
  drawGroundGrid();

  glPushMatrix();
  glTranslated(-(parteCentralSize.x / 2 + asaSize.x), 0, 0);

  drawParteExterna();
  drawChao();

  glPopMatrix();

  // pos = (x=40, y=0, z=0)  | largura=3.0 | altura=6.0 | moldura=0.22 | profundidade=0.30
  drawMuseumWindow((Vec3d){40.0, 0.0, 0.0}, 3.0, 6.0, 0.22, 0.30);

  drawObjetos();
}
