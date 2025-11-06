"""
OBJ Model Importer
Developed by: Cristiano Ramos
E-mail: cdgramos@live.com.pt
Web site: www.cdgramos.com
This library is licensed by: CC BY-SA

This library allows you to import OBJ
models to your OpenGL project in Python.
"""

from dataclasses import dataclass
from typing import List
from OpenGL import GL


@dataclass
class Vertex:
    x: float
    y: float
    z: float


@dataclass
class Face:
    v_number: int
    faces: List[int]


@dataclass
class Model:
    tot_v: int
    tot_f: int
    v: List[Vertex]
    f: List[Face]


def load_model(file_name: str) -> Model:
    with open(file_name, "r") as p_file:
        lines = p_file.readlines()

    # Count vertices
    tot_v = sum(1 for line in lines if line.strip().startswith("v "))

    # Count faces
    tot_f = sum(1 for line in lines if line.strip().startswith("f "))

    # Parse vertices
    vertices = []
    for line in lines:
        parts = line.strip().split()
        if len(parts) >= 4 and parts[0] == "v":
            vertices.append(
                Vertex(x=float(parts[1]), y=float(parts[2]), z=float(parts[3]))
            )

    # Parse faces
    faces = []
    for line in lines:
        parts = line.strip().split()
        if len(parts) >= 2 and parts[0] == "f":
            # Count spaces to determine face type
            space_count = len(parts) - 1
            face_indices = []

            for i in range(1, len(parts)):
                # Handle "v" or "v/vt/vn" format
                vertex_index = int(parts[i].split("/")[0])
                face_indices.append(vertex_index)

            faces.append(Face(v_number=len(face_indices), faces=face_indices))

    return Model(tot_v=tot_v, tot_f=tot_f, v=vertices, f=faces)


def draw_model_vertex(point_size: float, obj_model: Model):
    GL.glPointSize(point_size)
    GL.glBegin(GL.GL_POINTS)
    for vertex in obj_model.v:
        GL.glVertex3f(vertex.x, vertex.y, vertex.z)
    GL.glEnd()


def draw_model_faces(obj_model: Model):
    for face in obj_model.f:
        if face.v_number == 3:
            GL.glBegin(GL.GL_TRIANGLES)
            v1 = face.faces[0] - 1
            v2 = face.faces[1] - 1
            v3 = face.faces[2] - 1
            GL.glVertex3f(obj_model.v[v1].x, obj_model.v[v1].y, obj_model.v[v1].z)
            GL.glVertex3f(obj_model.v[v2].x, obj_model.v[v2].y, obj_model.v[v2].z)
            GL.glVertex3f(obj_model.v[v3].x, obj_model.v[v3].y, obj_model.v[v3].z)
            GL.glEnd()
        elif face.v_number == 4:
            GL.glBegin(GL.GL_QUADS)
            v1 = face.faces[0] - 1
            v2 = face.faces[1] - 1
            v3 = face.faces[2] - 1
            v4 = face.faces[3] - 1
            GL.glVertex3f(obj_model.v[v1].x, obj_model.v[v1].y, obj_model.v[v1].z)
            GL.glVertex3f(obj_model.v[v2].x, obj_model.v[v2].y, obj_model.v[v2].z)
            GL.glVertex3f(obj_model.v[v3].x, obj_model.v[v3].y, obj_model.v[v3].z)
            GL.glVertex3f(obj_model.v[v4].x, obj_model.v[v4].y, obj_model.v[v4].z)
            GL.glEnd()
