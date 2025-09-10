#include "draw.h"

#include <stdbool.h>

#include <GL/freeglut_std.h>
#include <GL/gl.h>

#include "util.h"

static int year = 0, day = 0;

static void drawStar(void) {
  glPushMatrix();

  glRotated(day, 0, 1, 0);
  glRotatef(90, 1, 0, 0);

  glutWireSphere(1, 20, 16);
  glPopMatrix();
}

static void drawPlanet(Vec3d pos, bool retrograde) {
  glPushMatrix();

  glRotated(retrograde ? -year : year, 0, 1, 0);
  glTranslated(pos.x, pos.y, pos.z);
  glRotated(day, 0, 1, 0);
  glRotatef(90, 1, 0, 0);

  glutWireSphere(0.25, 10, 8);
  glPopMatrix();
}

static void drawMoon(Vec3d primaryPos, bool primaryRetrograde, Vec3d pos, Vec3d tlAxis) {
  glPushMatrix();

  glRotated(primaryRetrograde ? -year : year, 0, 1, 0);
  glTranslated(primaryPos.x, primaryPos.y, primaryPos.z);
  glRotated(primaryRetrograde ? -year : year, tlAxis.x, tlAxis.y, tlAxis.z);
  glTranslated(pos.x, pos.y, pos.z);
  glRotated(day, 0, 1, 0);
  glRotatef(90, 1, 0, 0);

  glutWireSphere(0.08, 10, 8);
  glPopMatrix();
}

void draw(void) {
  glColor3d(1, 1, 0);
  drawStar();

  Vec3d planet1Pos = {.x = 1.8, .y = -0.4, .z = 0};
  glColor3d(0.549, 0.694, 0.871);
  drawPlanet(planet1Pos, false);

  Vec3d planet2Pos = {.x = -1.8, .y = 0.4, .z = 0.5};
  glColor3d(0.757, 0.267, 0.055);
  drawPlanet(planet2Pos, true);

  Vec3d moon1Pos = {.x = 0.4, .y = 0.15, .z = 0};
  Vec3d moon1TlAxis = {.x = 0, .y = 1, .z = 0};
  glColor3d(0.58, 0.565, 0.553);
  drawMoon(planet2Pos, true, moon1Pos, moon1TlAxis);

  Vec3d moon2Pos = {.x = 0.4, .y = -0.1, .z = 0.5};
  Vec3d moon2TlAxis = {.x = 0, .y = 0, .z = 1};
  glColor3d(0.494, 0.353, 0.235);
  drawMoon(planet2Pos, true, moon2Pos, moon2TlAxis);
}
