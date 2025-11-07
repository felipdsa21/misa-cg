from __future__ import annotations

import math
from dataclasses import dataclass

# Constantes
EPSILON = 0.001  # Para evitar z-fighting


@dataclass(frozen=True, slots=True)
class Vec2i:
    x: int
    y: int

    def __add__(self, other: Vec2i) -> Vec2i:
        return Vec2i(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vec2i) -> Vec2i:
        return Vec2i(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: int) -> Vec2i:
        return Vec2i(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: int) -> Vec2i:
        return self.__mul__(scalar)


@dataclass(frozen=True, slots=True)
class Vec2d:
    x: float
    y: float

    def __add__(self, other: Vec2d) -> Vec2d:
        return Vec2d(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vec2d) -> Vec2d:
        return Vec2d(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> Vec2d:
        return Vec2d(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: float) -> Vec2d:
        return self.__mul__(scalar)

    def __truediv__(self, scalar: float) -> Vec2d:
        return Vec2d(self.x / scalar, self.y / scalar)

    @property
    def magnitude(self) -> float:
        return math.hypot(self.x, self.y)

    def normalized(self) -> Vec2d:
        mag = self.magnitude
        if mag == 0.0:
            return Vec2d(0.0, 0.0)
        return Vec2d(self.x / mag, self.y / mag)


@dataclass(frozen=True, slots=True)
class Vec3d:
    x: float
    y: float
    z: float

    def __add__(self, other: Vec3d) -> Vec3d:
        return Vec3d(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Vec3d) -> Vec3d:
        return Vec3d(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar: float) -> Vec3d:
        return Vec3d(self.x * scalar, self.y * scalar, self.z * scalar)

    def __rmul__(self, scalar: float) -> Vec3d:
        return self.__mul__(scalar)

    def __truediv__(self, scalar: float) -> Vec3d:
        return Vec3d(self.x / scalar, self.y / scalar, self.z / scalar)

    @property
    def magnitude(self) -> float:
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def normalized(self) -> Vec3d:
        mag = self.magnitude
        if mag == 0.0:
            return Vec3d(0.0, 0.0, 0.0)
        return Vec3d(self.x / mag, self.y / mag, self.z / mag)

    def dot(self, other: Vec3d) -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other: Vec3d) -> Vec3d:
        return Vec3d(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )

    def with_y(self, new_y: float) -> Vec3d:
        return Vec3d(self.x, new_y, self.z)


def clamp(value: float, min_value: float, max_value: float) -> float:
    return max(min_value, min(value, max_value))


def direction_vector(pitch: float, yaw: float) -> Vec3d:
    return Vec3d(x=math.cos(pitch) * math.cos(yaw), y=math.sin(pitch), z=math.cos(pitch) * math.sin(yaw))
