#include <math.h>

#include <GL/gl.h>
#include <GL/glu.h>

#include "obj.h"
#include "primitives.h"
#include "util.h"

extern GLUquadric *q;

static void
drawArchRing(double cx, double cy, double outerR, double innerR, double zFront, double depth, int segments) {
  double zBack = zFront - depth;

  // Anel frontal
  glBegin(GL_TRIANGLE_STRIP);
  for (int i = 0; i <= segments; ++i) {
    double a = PI * (double)i / (double)segments;
    double xo = cos(a) * outerR, yo = sin(a) * outerR;
    double xi = cos(a) * innerR, yi = sin(a) * innerR;
    glVertex3d(cx + xo, cy + yo, zFront);
    glVertex3d(cx + xi, cy + yi, zFront);
  }
  glEnd();

  // Anel traseiro
  glBegin(GL_TRIANGLE_STRIP);
  for (int i = 0; i <= segments; ++i) {
    double a = PI * (double)i / (double)segments;
    double xo = cos(a) * outerR, yo = sin(a) * outerR;
    double xi = cos(a) * innerR, yi = sin(a) * innerR;
    glVertex3d(cx + xo, cy + yo, zBack);
    glVertex3d(cx + xi, cy + yi, zBack);
  }
  glEnd();

  // Lateral externa
  glBegin(GL_QUAD_STRIP);
  for (int i = 0; i <= segments; ++i) {
    double a = PI * (double)i / (double)segments;
    double xo = cos(a) * outerR, yo = sin(a) * outerR;
    glVertex3d(cx + xo, cy + yo, zFront);
    glVertex3d(cx + xo, cy + yo, zBack);
  }
  glEnd();

  // Lateral interna
  glBegin(GL_QUAD_STRIP);
  for (int i = 0; i <= segments; ++i) {
    double a = PI * (double)i / (double)segments;
    double xi = cos(a) * innerR, yi = sin(a) * innerR;
    glVertex3d(cx + xi, cy + yi, zBack);
    glVertex3d(cx + xi, cy + yi, zFront);
  }
  glEnd();
}

void drawJanelaComArco(
  double width, // Largura total
  double height, // Altura total (reta + arco)
  double depth
) {
  double frame = 0.22;
  double radius = width / 2.0; // Arco semicircular

  if (height <= radius) {
    height = radius + 0.01;
  }

  double rectH = height - radius; // Parte reta
  int seg = 48;
  double epsilon = 0.002; // evita z-fighting
  double zFront = 0;

  // Moldura (tom rosado)
  colorRgb(191, 124, 124);
  // ombreiras (laterais) e peitoril (base)
  drawBox((Vec3d){0, 0, zFront}, (Vec3d){frame, rectH, depth});
  drawBox((Vec3d){width - frame, 0, zFront}, (Vec3d){frame, rectH, depth});
  drawBox((Vec3d){0, 0, zFront}, (Vec3d){width, frame, depth});

  // Arco superior
  double cx = radius;
  double cy = rectH;
  drawArchRing(cx, cy, radius, radius - frame, zFront, depth, seg);

  // Vidro translúcido
  glEnable(GL_BLEND);
  glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
  glColor4d(0.78, 0.87, 0.96, 0.25); // azul claro com alpha

  // Retângulo de vidro (parte reta)
  glBegin(GL_QUADS);
  glVertex3d(frame, frame, zFront - epsilon);
  glVertex3d(width - frame, frame, zFront - epsilon);
  glVertex3d(width - frame, rectH - frame, zFront - epsilon);
  glVertex3d(frame, rectH - frame, zFront - epsilon);
  glEnd();

  // Vidro do arco
  glBegin(GL_TRIANGLE_FAN);
  glVertex3d(cx, cy, zFront - epsilon);
  for (int i = 0; i <= seg; ++i) {
    double a = PI * (double)i / (double)seg;
    double xi = cos(a) * (radius - frame);
    double yi = sin(a) * (radius - frame);
    glVertex3d(cx + xi, cy + yi, zFront - epsilon);
  }
  glEnd();

  glDisable(GL_BLEND);

  // Travessas internas (caixilhos)
  colorRgb(191, 124, 124);
  double bar = frame * 0.45;
  double innerW = width - 2.0 * frame;
  double glassBottom = frame;
  double glassTopRect = rectH - frame;

  // Montante vertical central
  drawBox(
    (Vec3d){width / 2.0 - bar / 2.0, glassBottom, zFront - epsilon},
    (Vec3d){bar, (glassTopRect - glassBottom), epsilon * 2.0}
  );

  // Travessa horizontal central (forma o "+")
  double centerY = (glassBottom + glassTopRect) / 2.0 - bar / 2.0;
  drawBox((Vec3d){frame, centerY, zFront - epsilon}, (Vec3d){innerW, bar, epsilon * 2.0});

  // Travessa horizontal próxima ao arco (mantida)
  drawBox((Vec3d){frame, rectH - frame - bar / 2.0, zFront - epsilon}, (Vec3d){innerW, bar, epsilon * 2.0});
}

void drawJanelaRetangular(
  double width, // Largura total
  double height, // Altura total (reta + arco)
  double depth
) {
  double frame = 0.22;
  double epsilon = 0.002; // evita z-fighting

  // Moldura
  colorRgb(191, 124, 124);
  drawBox((Vec3d){0, 0, 0}, (Vec3d){frame, height, depth});
  drawBox((Vec3d){width - frame, 0, 0}, (Vec3d){frame, height, depth});
  drawBox((Vec3d){0, 0, 0}, (Vec3d){width, frame, depth});
  drawBox((Vec3d){0, height - frame, 0}, (Vec3d){width, frame, depth});

  // Vidro
  colorRgb(199, 222, 245);
  glBegin(GL_QUADS);
  glVertex3d(frame, frame, -epsilon);
  glVertex3d(width - frame, frame, -epsilon);
  glVertex3d(width - frame, height - frame, -epsilon);
  glVertex3d(frame, height - frame, -epsilon);
  glEnd();

  // Travessas internas (caixilhos)
  colorRgb(191, 124, 124);
  double bar = frame * 0.5;
  double innerW = width - 2.0 * frame;
  double glassTopRect = height - frame;

  // Montante vertical central
  Vec3d montantePos = {width / 2 - bar / 2, frame, -epsilon};
  Vec3d montanteSize = {bar, (glassTopRect - frame), epsilon * 2};
  drawBox(montantePos, montanteSize);

  // Travessa horizontal central (forma o "+")
  double centerY = (frame + glassTopRect) / 2 - bar / 2;
  drawBox((Vec3d){frame, centerY, -epsilon}, (Vec3d){innerW, bar, epsilon * 2});
}

/* helper C para paralelepípedo alinhado aos eixos:
   desenha w x h x t a partir da origem local (0,0,0), avançando em -Z */
static void drawBoxLocal(double w, double h, double t) {
  glNormal3i(0, 0, -1);
  glRectd(0, 0, w, h); /* frente z=0 */
  glNormal3i(0, 0, 1);
  drawRectZ(0, 0, w, h, t); /* trás  z=t   */

  glPushMatrix();
  glRotatef(-90, 0, 1, 0);
  glNormal3i(-1, 0, 0);
  glRectd(0, 0, t, h);
  glPopMatrix(); /* lado esq    */

  glPushMatrix();
  glTranslated(w, 0, 0);
  glRotatef(-90, 0, 1, 0);
  glNormal3i(-1, 0, 0);
  glRectd(0, 0, t, h);
  glPopMatrix(); /* lado dir    */

  glPushMatrix();
  glRotatef(90, 1, 0, 0);
  glNormal3i(0, 1, 0);
  glRectd(0, 0, w, t);
  glPopMatrix(); /* base        */

  glPushMatrix();
  glTranslated(0, h, 0);
  glRotatef(90, 1, 0, 0);
  glNormal3i(0, 1, 0);
  glRectd(0, 0, w, t);
  glPopMatrix(); /* topo        */
}

/* desenha a pilastra conforme as fotos – VERSÃO C */
void drawPilastra(double x, double y, double z, double alturaFuste) {
  /* proporções (m) */
  const double baseW = 0.85, baseH = 0.12; /* base madeira escura */
  const double pedestalW = 0.70, pedestalH = 0.75; /* bloco amarelo */
  const double moldW = 0.90, moldH = 0.10; /* moldura branca */
  const double fusteR = 0.20; /* coluna cilíndrica */
  const double anelR = 0.30, anelH = 0.06; /* anel branco */
  const double pratoR = 0.45, pratoH = 0.04; /* prato verde (teto) */

  glPushMatrix();
  glTranslated(x, y, z);

  /* base madeira escura */
  colorRgb(70, 42, 25);
  drawBoxLocal(baseW, baseH, baseW);

  /* pedestal amarelo */
  glTranslated((baseW - pedestalW) / 2.0, baseH, (baseW - pedestalW) / 2.0);
  colorRgb(225, 197, 126);
  drawBoxLocal(pedestalW, pedestalH, pedestalW);

  /* moldura branca */
  glTranslated(-(moldW - pedestalW) / 2.0, pedestalH, -(moldW - pedestalW) / 2.0);
  colorRgb(240, 240, 240);
  drawBoxLocal(moldW, moldH, moldW);

  /* fuste (cilindro fechado, alinhado ao eixo Y) */
  glTranslated(moldW / 2.0, moldH, moldW / 2.0);
  colorRgb(225, 197, 126);
  glPushMatrix();
  glRotatef(-90, 1, 0, 0); /* GLU usa +Z → vira para +Y */
  gluCylinder(q, fusteR, fusteR, alturaFuste, 32, 1);
  gluDisk(q, 0.0, fusteR, 32, 1); /* tampa inferior */
  glTranslatef(0, 0, (GLfloat)alturaFuste);
  gluDisk(q, 0.0, fusteR, 32, 1); /* tampa superior */
  glPopMatrix();

  /* anel branco no topo do fuste */
  glPushMatrix();
  glTranslated(0, alturaFuste, 0);
  colorRgb(240, 240, 240);
  glRotatef(-90, 1, 0, 0);
  gluCylinder(q, anelR, anelR, anelH, 32, 1);
  gluDisk(q, 0.0, anelR, 32, 1);
  glTranslatef(0, 0, (GLfloat)anelH);
  gluDisk(q, 0.0, anelR, 32, 1);
  glPopMatrix();

  /* prato verde que toca o teto */
  glPushMatrix();
  glTranslated(0, alturaFuste + anelH, 0);
  colorRgb(126, 168, 146);
  glRotatef(-90, 1, 0, 0);
  gluCylinder(q, pratoR, pratoR, pratoH, 32, 1);
  gluDisk(q, 0.0, pratoR, 32, 1);
  glTranslatef(0, 0, (GLfloat)pratoH);
  gluDisk(q, 0.0, pratoR, 32, 1);
  glPopMatrix();

  glPopMatrix();
}