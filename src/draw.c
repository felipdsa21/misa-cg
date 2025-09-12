#include <math.h> /* cos / sin usados nas máscaras de arco */
#include <stddef.h>

#include <GL/gl.h>
#include <GL/glu.h>

/*
  Definições de controle de compilação:
  - ENABLE_STENCIL_WINDOWS: quando definido (default aqui), usa stencil buffer para recortar
    exatamente o formato das janelas (incluindo arco). Se desabilitado, cai no modo de
    segmentação simples que apenas abre retângulos envolventes (mais rápido, menos preciso).

  Para desativar stencil ao compilar:
    gcc -UENABLE_STENCIL_WINDOWS ...
*/
#ifndef DISABLE_STENCIL_WINDOWS
#ifndef ENABLE_STENCIL_WINDOWS
#define ENABLE_STENCIL_WINDOWS 1
#endif
#endif

#include "draw.h"
#include "obj.h"
#include "objImporter.h"
#include "porta.h"
#include "primitives.h"
#include "util.h"

GLUquadric *q = NULL;

static const int groundSize = 50;
static const float luzAmbiente[] = {0.15f, 0.15f, 0.15f, 1};
static const float luzDifusa[] = {0.8f, 0.8f, 0.8f, 1};
static const float luzEspecular[] = {0.1f, 0.1f, 0.1f, 1};
static const float posicaoLuz[] = {0.0f, 1.7f, -5.0f, 0.0f};

static const double pisoY = 1;
static const double segundoAndarY = 7;
static const Vec2d aberturaEscadaSize = {1, 3};

static const Vec3d parteCentralSize = {13, 12.5, 20};
static const Vec3d asaSize = {10.5, 7, 15};
static const double asaZOffset = 1;

static const Vec3d portaSize = {2.8, 3.2, 0};
static const Vec2d espacoPortaSize = {3, 3};

static const Vec3d janelaComArco = {1.2, 2.6, 0.3};
static const Vec3d janelaRetangularSize = {1.2, 2, 0.3};
#define JANELA_BAIXO_Y_OFFSET 1.4
#define JANELA_CIMA_Y_OFFSET (JANELA_BAIXO_Y_OFFSET + 1.6 + 3.2)
static const double janelaBaixoYOffset = JANELA_BAIXO_Y_OFFSET;
static const double janelaCimaYOffset = JANELA_CIMA_Y_OFFSET;
/* ---------------------------- Pilastras Internas ----------------------------
   Usa a função existente drawPilastra(x,y,z,alturaFuste) definida em obj.c. A altura
   passada corresponde apenas ao fuste cilíndrico; a função adiciona base/anel/prato.
*/
static void drawPilastrasInternas() {
  const double alturaFuste = (segundoAndarY - pisoY) - 1.07; /* compensa base+anel+prato */
  const double offsetLateral = 2.0; /* distância da parede interna lateral */
  const double primeiraZ = 3.8; /* posição ao longo do eixo Z dentro da parte central (frente=0) */
  const double distanciaEntrePares = 6.0; /* separar par frontal do traseiro */

  double xEsq = asaSize.x + offsetLateral;
  double xDir = asaSize.x + (parteCentralSize.x - offsetLateral);

  for (int i = 0; i < 2; i++) {
    double z = primeiraZ + i * distanciaEntrePares - asaZOffset; /* compensar deslocamento asa */
    drawPilastra(xEsq, pisoY, z, alturaFuste);
    drawPilastra(xDir, pisoY, z, alturaFuste);
  }
}

/* ------------------------------- Sacada frontal ------------------------------ */
static void drawSacada() {
  double xAntesPorta = (parteCentralSize.x - portaSize.x) / 2.0;
  double largura = portaSize.x + 4.0;
  double profundidade = 1.25;
  double espessura = 0.18;
  double guardaAltura = 0.80;
  double balaLarg = 0.15;
  double balaEsp = 0.15;
  double balaGap = 0.25;

  /* Altura: colocar a sacada mais alta (~ entre topo porta 3.2 e base janela superior 4.6) */
  double baseY = portaSize.y + 1.5;
  if (baseY + guardaAltura + espessura > janelaCimaYOffset - 0.5) {
    guardaAltura = (janelaCimaYOffset - 0.5) - (baseY + espessura);
    if (guardaAltura < 0.55) {
      guardaAltura = 0.55;
    }
  }

  double centroX = asaSize.x + xAntesPorta + portaSize.x / 2.0;
  double startX = centroX - largura / 2.0;

  glPushMatrix();
  glTranslated(startX, baseY, 0);

  /* Branco total da sacada */
  colorRgb(245, 245, 245); // laje
  drawBox((Vec3d){0, 0, 0}, (Vec3d){largura, espessura, profundidade});
  colorRgb(235, 235, 235); // moldura inferior
  drawBox((Vec3d){0, -0.10, 0}, (Vec3d){largura, 0.10, profundidade * 0.95});

  double railBaseY = espessura;
  double railTopY = railBaseY + guardaAltura;

  colorRgb(250, 250, 250); // Top rail
  drawBox((Vec3d){0, railTopY - 0.07, -0.14}, (Vec3d){largura, 0.07, 0.26});

  colorRgb(250, 250, 250); // Balaústres
  double usable = largura;
  int count = (int)(usable / (balaLarg + balaGap));
  if (count < 3) {
    count = 3;
  }
  double spacing = (usable - count * balaLarg) / (count - 1);
  for (int i = 0; i < count; i++) {
    double x = i * (balaLarg + spacing);
    drawBox((Vec3d){x, railBaseY, -0.07}, (Vec3d){balaLarg, guardaAltura - 0.12, balaEsp * 0.5});
  }

  colorRgb(240, 240, 240); // Rodapé guarda
  drawBox((Vec3d){0, railBaseY, -0.12}, (Vec3d){largura, 0.11, 0.22});

  glPopMatrix();
}

/* ------------------------------- Telhado + frontão --------------------------- */
static void drawTelhado() {
  double yBase = asaSize.y + 0.05;
  double beiral = 0.25;
  double ridgeAlt = 0.9;
  double zFront = asaZOffset - beiral;
  double zBack = asaZOffset + asaSize.z + beiral;
  double zRidge = (zFront + zBack) / 2.0;

  colorRgb(120, 50, 45);
  glBegin(GL_QUADS);
  double xA = 0;
  double xB = asaSize.x;
  double ridgeY = yBase + ridgeAlt;
  glNormal3d(0, ridgeAlt, (zRidge - zFront));
  glVertex3d(xA, yBase, zFront);
  glVertex3d(xB, yBase, zFront);
  glVertex3d(xB, ridgeY, zRidge);
  glVertex3d(xA, ridgeY, zRidge);
  glNormal3d(0, ridgeAlt, (zBack - zRidge) * -1);
  glVertex3d(xA, ridgeY, zRidge);
  glVertex3d(xB, ridgeY, zRidge);
  glVertex3d(xB, yBase, zBack);
  glVertex3d(xA, yBase, zBack);
  xA = asaSize.x + parteCentralSize.x;
  xB = xA + asaSize.x;
  glNormal3d(0, ridgeAlt, (zRidge - zFront));
  glVertex3d(xA, yBase, zFront);
  glVertex3d(xB, yBase, zFront);
  glVertex3d(xB, ridgeY, zRidge);
  glVertex3d(xA, ridgeY, zRidge);
  glNormal3d(0, ridgeAlt, (zBack - zRidge) * -1);
  glVertex3d(xA, ridgeY, zRidge);
  glVertex3d(xB, ridgeY, zRidge);
  glVertex3d(xB, yBase, zBack);
  glVertex3d(xA, yBase, zBack);
  glEnd();

  /* Telhado central (duas águas mais alto que asas) */
  double centroBaseY = parteCentralSize.y + 0.05; /* topo bloco central */
  double centroRidgeAlt = 2.4; /* altura extra */
  double centroBeiral = 0.35;
  double cFront = -centroBeiral;
  double cBack = parteCentralSize.z + centroBeiral;
  double cRidgeZ = (cFront + cBack) / 2.0;
  double cRidgeY = centroBaseY + centroRidgeAlt;
  double cStartX = asaSize.x - centroBeiral;
  double cEndX = asaSize.x + parteCentralSize.x + centroBeiral;
  colorRgb(110, 40, 38);
  glBegin(GL_QUADS);
  glNormal3d(0, centroRidgeAlt, (cRidgeZ - cFront));
  glVertex3d(cStartX, centroBaseY, cFront);
  glVertex3d(cEndX, centroBaseY, cFront);
  glVertex3d(cEndX, cRidgeY, cRidgeZ);
  glVertex3d(cStartX, cRidgeY, cRidgeZ);
  glNormal3d(0, centroRidgeAlt, (cBack - cRidgeZ) * -1);
  glVertex3d(cStartX, cRidgeY, cRidgeZ);
  glVertex3d(cEndX, cRidgeY, cRidgeZ);
  glVertex3d(cEndX, centroBaseY, cBack);
  glVertex3d(cStartX, centroBaseY, cBack);
  glEnd();

  /* Friso (linha branca) acima das janelas superiores – percorre largura parte central */
  colorRgb(245, 240, 235);
  double frisoAlt = 0.30;
  double frisoY = janelaCimaYOffset + janelaComArco.y + 0.25; /* base do friso */
  if (frisoY > parteCentralSize.y - 0.4) {
    frisoY = parteCentralSize.y - 0.4; /* não invadir telhado central */
  }
  drawBox((Vec3d){asaSize.x, frisoY, 0.02}, (Vec3d){parteCentralSize.x, frisoAlt, 0.18});

  /* Frontão curvo mais baixo (mantido) */
  double frontaoLarg = parteCentralSize.x * 0.65;
  double frontaoAlt = 1.8;
  double frontaoEsp = 0.16;
  double frontaoBaseX = asaSize.x + (parteCentralSize.x - frontaoLarg) / 2.0;
  double frontaoBaseY = frisoY + frisoAlt * 0.15;
  double frontaoBaseZ = 0.05;
  int seg = 32;
  double raio = frontaoLarg / 2.0;
  double arcoH = frontaoAlt * 0.65;
  double arcoBaseY = frontaoBaseY + frontaoAlt * 0.35;
  double cx = frontaoBaseX + raio;
  colorRgb(235, 222, 210);
  drawBox(
    (Vec3d){frontaoBaseX, frontaoBaseY, frontaoBaseZ}, (Vec3d){frontaoLarg, frontaoAlt * 0.35, frontaoEsp}
  );
  glBegin(GL_QUADS);
  for (int i = 0; i < seg; i++) {
    double a1 = PI * i / seg, a2 = PI * (i + 1) / seg;
    double x1 = cx + cos(a1) * raio, y1 = arcoBaseY + sin(a1) * arcoH;
    double x2 = cx + cos(a2) * raio, y2 = arcoBaseY + sin(a2) * arcoH;
    glVertex3d(x1, y1, frontaoBaseZ);
    glVertex3d(x2, y2, frontaoBaseZ);
    glVertex3d(x2, y2, frontaoBaseZ + frontaoEsp);
    glVertex3d(x1, y1, frontaoBaseZ + frontaoEsp);
  }
  glEnd();
  glBegin(GL_TRIANGLE_FAN);
  glVertex3d(cx, arcoBaseY, frontaoBaseZ);
  for (int i = 0; i <= seg; i++) {
    double a = PI * i / seg;
    glVertex3d(cx + cos(a) * raio, arcoBaseY + sin(a) * arcoH, frontaoBaseZ);
  }
  glEnd();
  glBegin(GL_TRIANGLE_FAN);
  glVertex3d(cx, arcoBaseY, frontaoBaseZ + frontaoEsp);
  for (int i = 0; i <= seg; i++) {
    double a = PI * i / seg;
    glVertex3d(cx + cos(a) * raio, arcoBaseY + sin(a) * arcoH, frontaoBaseZ + frontaoEsp);
  }
  glEnd();
}

void init(void) {
  glClearColor(0.53f, 0.81f, 0.98f, 1);

  glEnable(GL_LIGHTING);
  glEnable(GL_LIGHT0);
  glEnable(GL_NORMALIZE);
  glShadeModel(GL_SMOOTH);

  glEnable(GL_COLOR_MATERIAL);
  glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE);
  glLightfv(GL_LIGHT0, GL_AMBIENT, luzAmbiente);
  glLightfv(GL_LIGHT0, GL_DIFFUSE, luzDifusa);
  glLightfv(GL_LIGHT0, GL_SPECULAR, luzEspecular);

  q = gluNewQuadric();
  gluQuadricNormals(q, GLU_SMOOTH);

#if ENABLE_STENCIL_WINDOWS
  glClearStencil(0);
  glEnable(GL_STENCIL_TEST);
#endif
}

void onSetupCamera(void) {
  glLightfv(GL_LIGHT0, GL_POSITION, posicaoLuz);
}

static void drawGrass(void) {
  colorRgb(65, 152, 10);
  glNormal3i(0, 1, 0);
  drawRectY(-groundSize, -groundSize, groundSize, groundSize, 0);
}

static void drawChao(void) {
  Vec2d tamanho = {parteCentralSize.x + asaSize.x * 2, parteCentralSize.z + asaSize.z * 2};

  colorRgb(156, 146, 143);
  glNormal3i(0, 1, 0);
  drawRectY(-2, -2, tamanho.x + 2, tamanho.y + 2, EPSILON);
}

static void drawPiso(double x1, double z1, double x2, double z2, double y) {
  colorRgb(150, 108, 72);
  drawRectY(x1, z1, x2, z2, y);

  colorRgb(97, 67, 42);
  GLdouble spacing = 0.45;

  glBegin(GL_LINES);
  for (GLdouble x = x1 + spacing; x < x2; x += spacing) {
    glVertex3d(x, y + EPSILON, z1);
    glVertex3d(x, y + EPSILON, z2);
  }
  glEnd();
}

static void drawPisos(void) {
  glNormal3i(0, 1, 0);
  glPushMatrix();

  // Asa direita
  glTranslated(0, 0, asaZOffset);
  drawPiso(0, 0, asaSize.x, asaSize.z, pisoY);

  // Parte central
  glTranslated(asaSize.x, 0, -asaZOffset);

  GLdouble espacoPortaXStart = (parteCentralSize.x - espacoPortaSize.x) / 2;
  GLdouble espacoPortaXEnd = (parteCentralSize.x + espacoPortaSize.x) / 2;
  // Espaço para porta
  drawPiso(0, espacoPortaSize.y, parteCentralSize.x, parteCentralSize.z, pisoY);
  drawPiso(0, 0, espacoPortaXStart, espacoPortaSize.y, pisoY);
  drawPiso(espacoPortaXEnd, 0, parteCentralSize.x, espacoPortaSize.y, pisoY);
  drawPiso(espacoPortaXStart, 0, espacoPortaXEnd, espacoPortaSize.y, EPSILON * 2);

  // Segundo andar
  GLdouble limiteX = parteCentralSize.x - aberturaEscadaSize.x;
  GLdouble limiteZ = parteCentralSize.z / 2;
  GLdouble fimAberturaZ = limiteZ + aberturaEscadaSize.y;

  drawPiso(0, 0, limiteX, parteCentralSize.z, segundoAndarY);
  drawPiso(limiteX, 0, parteCentralSize.x, limiteZ, segundoAndarY);
  drawPiso(limiteX, fimAberturaZ, parteCentralSize.x, parteCentralSize.z, segundoAndarY);
  drawPiso(parteCentralSize.x - 0.1, limiteZ, parteCentralSize.x, fimAberturaZ, segundoAndarY);

  // Asa esquerda
  glTranslated(parteCentralSize.x, 0, asaZOffset);
  drawPiso(0, 0, asaSize.x, asaSize.z, pisoY);

  glPopMatrix();
}

/* --------------------------------------------------------------------------
   Helpers para stencil
*/
#if ENABLE_STENCIL_WINDOWS
/* Desenha um retângulo cheio no plano Z=0 para máscara */
static inline void maskRect(double x1, double y1, double w, double h) {
  glBegin(GL_QUADS);
  glVertex3d(x1, y1, 0);
  glVertex3d(x1 + w, y1, 0);
  glVertex3d(x1 + w, y1 + h, 0);
  glVertex3d(x1, y1 + h, 0);
  glEnd();
}

/* Desenha retângulo + semicirculo topo (janela arco) para máscara */
static void maskJanelaArco(double x, double yBase, double totalW, double totalH, int seg) {
  double radius = totalW * 0.5; // raio = metade da largura
  double rectH = totalH - radius; // altura da parte reta
  maskRect(x, yBase, totalW, rectH); // parte reta
  double cx = x + radius, cy = yBase + rectH;
  glBegin(GL_TRIANGLE_FAN);
  glVertex3d(cx, cy, 0);
  for (int i = 0; i <= seg; i++) {
    double a = PI * (double)i / (double)seg;
    glVertex3d(cx + cos(a) * radius, cy + sin(a) * radius, 0);
  }
  glEnd();
}
#endif

static void drawAsa(void) {
  // Calcula posições das 3 janelas retangulares na asa (distribuição uniforme pelo distBase)
  double winW = janelaRetangularSize.x;
  double winH = janelaRetangularSize.y;
  double baseY = janelaBaixoYOffset;
  double topY = baseY + winH;
  int distBase = 3; // distância progressiva usada já no desenho das janelas
  double winX[3];
  double cursor = -winW;
  for (int i = 0; i < 3; i++) {
    cursor += distBase;
    winX[i] = cursor;
  }

#if ENABLE_STENCIL_WINDOWS
  // Modo preciso: usa stencil para recortar exatamente os retângulos das janelas
  glNormal3i(0, 0, -1);
  // Preparar stencil: marcamos 1 onde haverá janela
  glColorMask(GL_FALSE, GL_FALSE, GL_FALSE, GL_FALSE);
  glDepthMask(GL_FALSE);
  glStencilMask(0xFF);
  glClear(GL_STENCIL_BUFFER_BIT);
  glStencilFunc(GL_ALWAYS, 1, 0xFF);
  glStencilOp(GL_KEEP, GL_KEEP, GL_REPLACE);
  glBegin(GL_QUADS);
  for (int i = 0; i < 3; i++) { // máscara cada janela
    glVertex3d(winX[i], baseY, 0);
    glVertex3d(winX[i] + winW, baseY, 0);
    glVertex3d(winX[i] + winW, topY, 0);
    glVertex3d(winX[i], topY, 0);
  }
  glEnd();
  // Desenha parede exceto onde stencil == 1
  glColorMask(GL_TRUE, GL_TRUE, GL_TRUE, GL_TRUE);
  glDepthMask(GL_TRUE);
  glStencilFunc(GL_EQUAL, 0, 0xFF);
  glStencilOp(GL_KEEP, GL_KEEP, GL_KEEP);
  glRectd(0, 0, asaSize.x, asaSize.y);
  glStencilFunc(GL_ALWAYS, 0, 0xFF); // libera
#else
  // Modo simples: subtrai retângulos manualmente (menos preciso, mas rápido e sem stencil)
  glNormal3i(0, 0, -1);
  glRectd(0, 0, asaSize.x, baseY); // faixa inferior
  glRectd(0, topY, asaSize.x, asaSize.y); // faixa superior
  double segStart[] = {0, winX[0] + winW, winX[1] + winW, winX[2] + winW};
  double segEnd[] = {winX[0], winX[1], winX[2], asaSize.x};
  for (int i = 0; i < 4; i++) {
    if (segEnd[i] - segStart[i] > EPSILON) {
      glRectd(segStart[i], baseY, segEnd[i], topY);
    }
  }
#endif

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
  double xAntesPorta = (parteCentralSize.x - portaSize.x) / 2.0; // início da porta na fachada frontal
  // Parâmetros das janelas com arco
  double jw = janelaComArco.x; // largura total
  double jh = janelaComArco.y; // altura total (reta + arco)
  double yLow = janelaBaixoYOffset; // base das janelas inferiores
  double yTopBase = janelaCimaYOffset; // base das janelas superiores
  double distLado = (xAntesPorta - jw) / 2.0; // deslocamento lateral entre borda e primeira janela
  double distCentro = xAntesPorta + (portaSize.x - jw) / 2.0; // janela central superior
  double rightStart = xAntesPorta + portaSize.x + distLado; // primeira janela lado direito

#if ENABLE_STENCIL_WINDOWS
  // --- STENCIL (modo preciso) ---
  glNormal3i(0, 0, -1);
  glColorMask(GL_FALSE, GL_FALSE, GL_FALSE, GL_FALSE);
  glDepthMask(GL_FALSE);
  glStencilMask(0xFF);
  glClear(GL_STENCIL_BUFFER_BIT);
  glStencilFunc(GL_ALWAYS, 1, 0xFF);
  glStencilOp(GL_KEEP, GL_KEEP, GL_REPLACE);
  // Porta (retângulo)
  maskRect(xAntesPorta, 0, portaSize.x, portaSize.y);
  // Janelas arco (5): esquerda baixa/alta, central alta, direita baixa/alta
  int seg = 48;
  maskJanelaArco(distLado, yLow, jw, jh, seg);
  maskJanelaArco(distLado, yTopBase, jw, jh, seg);
  maskJanelaArco(distCentro, yTopBase, jw, jh, seg);
  maskJanelaArco(rightStart, yLow, jw, jh, seg);
  maskJanelaArco(rightStart, yTopBase, jw, jh, seg);

  // Desenha parede exceto onde máscara = 1
  glColorMask(GL_TRUE, GL_TRUE, GL_TRUE, GL_TRUE);
  glDepthMask(GL_TRUE);
  glStencilFunc(GL_EQUAL, 0, 0xFF);
  glStencilOp(GL_KEEP, GL_KEEP, GL_KEEP);
  glRectd(0, 0, parteCentralSize.x, parteCentralSize.y);
  glStencilFunc(GL_ALWAYS, 0, 0xFF);
#else
  // --- SEGMENTAÇÃO (modo simples) ---
  glNormal3i(0, 0, -1);
  double jh2Low = yLow + jh; // topo janela inferior
  double jh2Top = yTopBase + jh; // topo janela superior
  struct Open {
    double x1, y1, x2, y2;
  } opens[] = {
    {xAntesPorta, 0, xAntesPorta + portaSize.x, portaSize.y},
    {distLado, yLow, distLado + jw, jh2Low},
    {distLado, yTopBase, distLado + jw, jh2Top},
    {distCentro, yTopBase, distCentro + jw, jh2Top},
    {rightStart, yLow, rightStart + jw, jh2Low},
    {rightStart, yTopBase, rightStart + jw, jh2Top}
  };
  double yMarks[] = {0, portaSize.y, yLow, jh2Low, yTopBase, jh2Top, parteCentralSize.y};
  int yCount = (int)(sizeof(yMarks) / sizeof(yMarks[0]));
  for (int i = 1; i < yCount; i++) {
    double v = yMarks[i];
    int j = i - 1;
    while (j >= 0 && yMarks[j] > v) {
      yMarks[j + 1] = yMarks[j];
      j--;
    }
    yMarks[j + 1] = v;
  }
  for (int yi = 0; yi < yCount - 1; yi++) {
    double ya = yMarks[yi], yb = yMarks[yi + 1];
    if (yb - ya <= EPSILON) {
      continue;
    }
    struct Seg {
      double a, b;
    } segs[8];
    int sc = 0;
    for (unsigned o = 0; o < sizeof(opens) / sizeof(opens[0]); o++) {
      if (opens[o].y1 <= ya + EPSILON && opens[o].y2 >= yb - EPSILON) {
        segs[sc++] = (struct Seg){opens[o].x1, opens[o].x2};
      }
    }
    for (int i = 1; i < sc; i++) {
      struct Seg v = segs[i];
      int j = i - 1;
      while (j >= 0 && segs[j].a > v.a) {
        segs[j + 1] = segs[j];
        j--;
      }
      segs[j + 1] = v;
    }
    int m = 0;
    for (int i = 0; i < sc; i++) {
      if (m == 0 || segs[i].a > segs[m - 1].b + EPSILON) {
        segs[m++] = segs[i];
      } else if (segs[i].b > segs[m - 1].b) {
        segs[m - 1].b = segs[i].b;
      }
    }
    double cursor = 0;
    for (int i = 0; i < m; i++) {
      if (segs[i].a - cursor > EPSILON) {
        glRectd(cursor, ya, segs[i].a, yb);
      }
      cursor = segs[i].b;
    }
    if (parteCentralSize.x - cursor > EPSILON) {
      glRectd(cursor, ya, parteCentralSize.x, yb);
    }
  }
#endif

  // Porta (folhas) desenhada depois da parede para aparecer no vão
  glPushAttrib(GL_CURRENT_BIT);
  drawPorta(xAntesPorta);
  glPopAttrib();

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
  int distBase = 3;

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
  drawGrass();

  glPushMatrix();
  glTranslated(-(parteCentralSize.x / 2 + asaSize.x), 0, 0);

  drawChao();
  drawPisos();
  drawParteExterna(drawAsa, drawParteCentral);
  drawParteExterna(drawJanelasAsa, drawJanelasParteCentral);
  drawPilastrasInternas();
  drawSacada();
  drawTelhado();
  // drawObjetos();

  glPopMatrix();
  drawBotao();
}
