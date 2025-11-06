import math
from dataclasses import dataclass
from typing import Tuple

# Constants
PI = 3.14159265358979323846
EPSILON = 0.001  # Para evitar z-fighting


@dataclass
class Vec2i:
    x: int
    y: int


@dataclass
class Vec2d:
    x: float
    y: float


@dataclass
class Vec3d:
    x: float
    y: float
    z: float


def clamp(x: float, lower: float, upper: float) -> float:
    return lower if x < lower else (upper if x > upper else x)


def to_radians(degrees: float) -> float:
    return degrees * PI / 180.0


def with_y3d(u: Vec3d, new_y: int) -> Vec3d:
    return Vec3d(x=u.x, y=new_y, z=u.z)


def calc_direction_vec(pitch: float, yaw: float) -> Vec3d:
    return Vec3d(
        x=math.cos(pitch) * math.cos(yaw),
        y=math.sin(pitch),
        z=math.cos(pitch) * math.sin(yaw),
    )


def sum3d(u: Vec3d, v: Vec3d) -> Vec3d:
    return Vec3d(x=u.x + v.x, y=u.y + v.y, z=u.z + v.z)


def scalar_mult3d(a: float, u: Vec3d) -> Vec3d:
    return Vec3d(x=a * u.x, y=a * u.y, z=a * u.z)


def normalize3d(u: Vec3d) -> Vec3d:
    norm = math.sqrt(u.x * u.x + u.y * u.y + u.z * u.z)
    return Vec3d(x=u.x / norm, y=u.y / norm, z=u.z / norm)


def cross_product3d(u: Vec3d, v: Vec3d) -> Vec3d:
    return Vec3d(
        x=u.y * v.z - u.z * v.y, y=u.z * v.x - u.x * v.z, z=u.x * v.y - u.y * v.x
    )
