#pragma once

#include <GL/gl.h>

// Tipos
typedef struct {
  int x, y;
} Vec2i;

typedef struct {
  double x, y;
} Vec2d;

typedef struct {
  double x, y, z;
} Vec3d;

// Constantes
static const double PI = 3.14159265358979323846;
static const double EPSILON = 0.001; // Para evitar z-fighting

// Funções matemáticas
double clamp(double x, double lower, double upper);
double toRadians(double degrees);
Vec3d withY3d(Vec3d u, int newY);
Vec3d calcDirectionVec(double pitch, double yaw);
Vec3d sum3d(Vec3d u, Vec3d v);
Vec3d scalarMult3d(double a, Vec3d u);
Vec3d normalize3d(Vec3d u);
Vec3d crossProduct3d(Vec3d u, Vec3d v);
