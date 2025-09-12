#pragma once

#include <GL/gl.h>

typedef struct {
  int x, y;
} Vec2i;

typedef struct {
  double x, y;
} Vec2d;

typedef struct {
  double x, y, z;
} Vec3d;

static const double PI = 3.14159265358979323846;

double clamp(double x, double upper, double lower);
double radians(double degrees);
Vec3d copyY3d(Vec3d u, Vec3d v);
Vec3d calcDirectionVec(double pitch, double yaw);
Vec3d sum3d(Vec3d u, Vec3d v);
Vec3d scalarMult3d(double a, Vec3d u);
Vec3d normalize3d(Vec3d u);
Vec3d crossProduct3d(Vec3d u, Vec3d v);
