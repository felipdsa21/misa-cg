#include <GL/gl.h>

typedef struct {
  GLsizei x, y;
} Vec2sizei;

typedef struct {
  GLdouble x, y, z;
} Vec3d;

GLdouble clamp(GLdouble x, GLdouble upper, GLdouble lower);
GLdouble radians(GLdouble degrees);
Vec3d calcDirectionVec(GLdouble pitch, GLdouble yaw);
Vec3d sum3d(Vec3d u, Vec3d v);
Vec3d scalarMult3d(GLdouble a, Vec3d u);
Vec3d normalize3d(Vec3d u);
Vec3d crossProduct3d(Vec3d u, Vec3d v);
