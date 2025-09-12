#include <stdbool.h>

#include <GL/gl.h>

#include "draw.h"
#include "primitives.h"
#include "util.h"

static const Vec3d portaSize = {2.8, 3.2, 0.0};

/* ---------- ANIMAÇÃO DAS PORTAS ---------- */
static double doorAngle = 0.0;
static double doorTarget = 0.0; /* 0 fechada, 90 aberta */
static const double doorMax = 90.0;
static const double doorSpeed = 180.0 / 60.0; /* ~3°/frame @60Hz */

static bool stepDoor(void) {
  double before = doorAngle;
  if (doorAngle < doorTarget) {
    doorAngle += doorSpeed;
    if (doorAngle > doorTarget) {
      doorAngle = doorTarget;
    }
  } else if (doorAngle > doorTarget) {
    doorAngle -= doorSpeed;
    if (doorAngle < doorTarget) {
      doorAngle = doorTarget;
    }
  }
  return before != doorAngle;
}
bool updateSceneAnimation(void) {
  return stepDoor();
}

void onKey(unsigned char key, int x, int y) {
  (void)x;
  (void)y;
  if (key == 'r' || key == 'R') {
    doorTarget = (doorTarget > 0.0) ? 0.0 : doorMax;
  }
}

/* ---------- helpers ---------- */
static void colorWoodBase() {
  colorRgb(120, 78, 48);
} /* marrom base */
static void colorWoodHighlight() {
  colorRgb(139, 94, 62);
} /* partes salientes */
static void colorWoodInset() {
  colorRgb(97, 67, 42);
} /* painéis rebaixados */
static void colorWoodFrame() {
  colorRgb(150, 108, 72);
} /* moldura dos painéis */
static void colorWoodJamb() {
  colorRgb(90, 60, 40);
} /* junta central */
static void colorMetal() {
  colorRgb(80, 80, 80);
} /* maçaneta */

static void drawBox(double w, double h, double t) {
  glNormal3i(0, 0, -1);
  glRectd(0, 0, w, h); /* frente z=0 */
  glNormal3i(0, 0, 1);
  drawRectZ(0, 0, w, h, t); /* trás  z=t   */

  glPushMatrix();
  glRotated(-90, 0, 1, 0);
  glNormal3i(-1, 0, 0);
  glRectd(0, 0, t, h);
  glPopMatrix(); /* lado esq */

  glPushMatrix();
  glTranslated(w, 0, 0);
  glRotated(-90, 0, 1, 0);
  glNormal3i(-1, 0, 0);
  glRectd(0, 0, t, h);
  glPopMatrix(); /* lado dir */

  glPushMatrix();
  glRotated(90, 1, 0, 0);
  glNormal3i(0, 1, 0);
  glRectd(0, 0, w, t);
  glPopMatrix(); /* base */

  glPushMatrix();
  glTranslated(0, h, 0);
  glRotated(90, 1, 0, 0);
  glNormal3i(0, 1, 0);
  glRectd(0, 0, w, t);
  glPopMatrix(); /* topo */
}

/* moldura + painel rebaixado (com offsets para evitar z-fighting) */
static void
drawFramedInset(double x, double y, double w, double h, double t, double moldura, double rebaixo) {
  const double zLift = -0.003; /* saliência à frente da face */

  /* moldura plana saliente */
  glPushMatrix();
  glTranslated(0, 0, zLift);
  glNormal3i(0, 0, -1);
  colorWoodFrame();
  glBegin(GL_QUADS);
  /* esquerda */ glVertex3d(x, y, 0);
  glVertex3d(x + moldura, y, 0);
  glVertex3d(x + moldura, y + h, 0);
  glVertex3d(x, y + h, 0);
  /* direita  */ glVertex3d(x + w - moldura, y, 0);
  glVertex3d(x + w, y, 0);
  glVertex3d(x + w, y + h, 0);
  glVertex3d(x + w - moldura, y + h, 0);
  /* topo     */ glVertex3d(x + moldura, y + h - moldura, 0);
  glVertex3d(x + w - moldura, y + h - moldura, 0);
  glVertex3d(x + w - moldura, y + h, 0);
  glVertex3d(x + moldura, y + h, 0);
  /* base     */ glVertex3d(x + moldura, y, 0);
  glVertex3d(x + w - moldura, y, 0);
  glVertex3d(x + w - moldura, y + moldura, 0);
  glVertex3d(x + moldura, y + moldura, 0);
  glEnd();
  glPopMatrix();

  /* painel rebaixado (entra no volume) */
  glPushMatrix();
  glTranslated(x + moldura, y + moldura, t * rebaixo);
  colorWoodInset();
  drawBox(w - 2 * moldura, h - 2 * moldura, t * 0.12);
  glPopMatrix();
}

/* folha com stiles/rails + painéis (abrir para dentro será controlado no caller) */
static void drawDoorLeaf(double folhaW, double folhaH, double t, bool isRightLeaf) {
  const double zLift = -0.003; /* saliências à frente */

  /* corpo */
  colorWoodBase();
  drawBox(folhaW, folhaH, t);

  /* stiles/rails */
  const double stile = 0.18;
  const double railTop = 0.16;
  const double railMid = 0.22;
  const double railBot = 0.16;

  const double yMid0 = (folhaH - railMid) * 0.5;

  glPushMatrix();
  glTranslated(0, 0, zLift);
  glNormal3i(0, 0, -1);
  colorWoodHighlight();
  glBegin(GL_QUADS);
  /* stiles */
  glVertex3d(0, 0, 0);
  glVertex3d(stile, 0, 0);
  glVertex3d(stile, folhaH, 0);
  glVertex3d(0, folhaH, 0);
  glVertex3d(folhaW - stile, 0, 0);
  glVertex3d(folhaW, 0, 0);
  glVertex3d(folhaW, folhaH, 0);
  glVertex3d(folhaW - stile, folhaH, 0);
  /* rails topo/meio/base */
  glVertex3d(stile, folhaH - railTop, 0);
  glVertex3d(folhaW - stile, folhaH - railTop, 0);
  glVertex3d(folhaW - stile, folhaH, 0);
  glVertex3d(stile, folhaH, 0);

  glVertex3d(stile, yMid0, 0);
  glVertex3d(folhaW - stile, yMid0, 0);
  glVertex3d(folhaW - stile, yMid0 + railMid, 0);
  glVertex3d(stile, yMid0 + railMid, 0);

  glVertex3d(stile, 0, 0);
  glVertex3d(folhaW - stile, 0, 0);
  glVertex3d(folhaW - stile, railBot, 0);
  glVertex3d(stile, railBot, 0);
  glEnd();
  glPopMatrix();

  /* painéis rebaixados */
  const double mold = 0.08;
  const double rel = 0.35;

  double topH = folhaH - railTop - (yMid0 + railMid);
  drawFramedInset(stile, yMid0 + railMid, folhaW - 2 * stile, topH, t, mold, rel);

  double baseRegionH = yMid0;
  double lower1H = baseRegionH * 0.55;
  double lower2H = baseRegionH * 0.35;
  double gapV = baseRegionH - (lower1H + lower2H);

  drawFramedInset(stile, gapV + lower2H, folhaW - 2 * stile, lower1H, t, mold, rel);
  drawFramedInset(stile, 0.02 + mold * 0.25, folhaW - 2 * stile, lower2H - 0.02, t, mold, rel);

  /* junta central e maçaneta na folha direita */
  if (isRightLeaf) {
    const double jamb = 0.025;
    glPushMatrix();
    glTranslated(0, 0, zLift);
    glNormal3i(0, 0, -1);
    colorWoodJamb();
    glBegin(GL_QUADS);
    glVertex3d(folhaW - jamb, 0, 0);
    glVertex3d(folhaW, 0, 0);
    glVertex3d(folhaW, folhaH, 0);
    glVertex3d(folhaW - jamb, folhaH, 0);
    glEnd();
    glPopMatrix();

    colorMetal();
    double knobW = 0.06, knobH = 0.06, knobT = 0.04;
    glPushMatrix();
    glTranslated(folhaW - 0.12 - knobW, yMid0 + railMid * 0.5 - knobH * 0.5, knobT * 0.5);
    drawBox(knobW, knobH, knobT);
    glPopMatrix();
  }
}

/* portas – AGORA ABREM PARA DENTRO (rotação ajustada) */
static void drawPortasFrente(double xAntesPorta) {
  const double leafW = portaSize.x * 0.5;
  const double leafH = portaSize.y;
  const double thickness = 0.06;
  const double zGap = 0.004;

  /* Folha esquerda: rotação NEGATIVA → entra para +Z */
  glPushMatrix();
  glTranslated(xAntesPorta, 0, zGap);
  glRotated(-doorAngle, 0, 1, 0);
  drawDoorLeaf(leafW, leafH, thickness, false);
  glPopMatrix();

  /* Folha direita: rotação POSITIVA (após levar pivô à borda direita) */
  glPushMatrix();
  glTranslated(xAntesPorta + portaSize.x, 0, zGap);
  glRotated(+doorAngle, 0, 1, 0);
  glTranslated(-leafW, 0, 0);
  drawDoorLeaf(leafW, leafH, thickness, true);
  glPopMatrix();
}

void drawPorta(double xAntesPorta) {
  /* batente do vão (leve saliência) */
  const double zLift = -0.002;
  colorRgb(210, 170, 170);
  glPushMatrix();
  glTranslated(0, 0, zLift);
  glNormal3i(0, 0, -1);
  double b = 0.08;
  glBegin(GL_QUADS);
  /* esq */ glVertex3d(xAntesPorta - b, 0, 0);
  glVertex3d(xAntesPorta, 0, 0);
  glVertex3d(xAntesPorta, portaSize.y, 0);
  glVertex3d(xAntesPorta - b, portaSize.y, 0);
  /* dir */ glVertex3d(xAntesPorta + portaSize.x, 0, 0);
  glVertex3d(xAntesPorta + portaSize.x + b, 0, 0);
  glVertex3d(xAntesPorta + portaSize.x + b, portaSize.y, 0);
  glVertex3d(xAntesPorta + portaSize.x, portaSize.y, 0);
  /* topo*/ glVertex3d(xAntesPorta - b, portaSize.y, 0);
  glVertex3d(xAntesPorta + portaSize.x + b, portaSize.y, 0);
  glVertex3d(xAntesPorta + portaSize.x + b, portaSize.y + b, 0);
  glVertex3d(xAntesPorta - b, portaSize.y + b, 0);
  glEnd();
  glPopMatrix();

  drawPortasFrente(xAntesPorta);
}
