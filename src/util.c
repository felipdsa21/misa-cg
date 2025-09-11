#include "util.h"

#include <math.h>

GLdouble clamp(GLdouble x, GLdouble lower, GLdouble upper) {
  return x < lower ? lower : (x > upper ? upper : x);
}

GLdouble radians(GLdouble degrees) {
  return degrees * 3.14 / 180.0;
}

Vec3d calcDirectionVec(GLdouble pitch, GLdouble yaw) {
  return (Vec3d){.x = cos(pitch) * cos(yaw), .y = sin(pitch), .z = cos(pitch) * sin(yaw)};
}

Vec3d sum3d(Vec3d u, Vec3d v) {
  return (Vec3d){.x = u.x + v.x, .y = u.y + v.y, .z = u.z + v.z};
}

Vec3d scalarMult3d(GLdouble a, Vec3d u) {
  return (Vec3d){.x = a * u.x, .y = a * u.y, .z = a * u.z};
}

Vec3d normalize3d(Vec3d u) {
  GLdouble norm = sqrt(u.x * u.x + u.y * u.y + u.z * u.z);
  return (Vec3d){.x = u.x / norm, .y = u.y / norm, .z = u.z / norm};
}

Vec3d crossProduct3d(Vec3d u, Vec3d v) {
  return (Vec3d){.x = u.y * v.z - u.z * v.y, .y = u.z * v.x - u.x * v.z, .z = u.x * v.y - u.y * v.x};
}
