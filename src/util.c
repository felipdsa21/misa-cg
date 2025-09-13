#include <math.h>

#include "util.h"

double clamp(double x, double lower, double upper) {
  return x < lower ? lower : (x > upper ? upper : x);
}

double toRadians(double degrees) {
  return degrees * PI / 180.0;
}

Vec3d withY3d(Vec3d u, int newY) {
  return (Vec3d){.x = u.x, .y = newY, .z = u.z};
}

Vec3d calcDirectionVec(double pitch, double yaw) {
  return (Vec3d){.x = cos(pitch) * cos(yaw), .y = sin(pitch), .z = cos(pitch) * sin(yaw)};
}

Vec3d sum3d(Vec3d u, Vec3d v) {
  return (Vec3d){.x = u.x + v.x, .y = u.y + v.y, .z = u.z + v.z};
}

Vec3d scalarMult3d(double a, Vec3d u) {
  return (Vec3d){.x = a * u.x, .y = a * u.y, .z = a * u.z};
}

Vec3d normalize3d(Vec3d u) {
  double norm = sqrt(u.x * u.x + u.y * u.y + u.z * u.z);
  return (Vec3d){.x = u.x / norm, .y = u.y / norm, .z = u.z / norm};
}

Vec3d crossProduct3d(Vec3d u, Vec3d v) {
  return (Vec3d){.x = u.y * v.z - u.z * v.y, .y = u.z * v.x - u.x * v.z, .z = u.x * v.y - u.y * v.x};
}
