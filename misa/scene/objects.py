"""3D Objects drawing functions - Furniture and decorative objects loaded from OBJ files."""

from OpenGL.GL import *
from ..objImporter import load_model, draw_model_faces


def draw_objetos():
    """Draw all 3D objects (furniture, decorations) in the scene."""
    obj = load_model("models/Mesa.obj")
    glPushMatrix()
    glTranslatef(10.0, 1.0, 7.0)  # movendo o objeto
    glRotatef(90.0, 0.0, 1.0, 0.0)
    glColor3ub(0, 0, 0)
    draw_model_faces(obj)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(10.0, 1.0, 12.0)  # movendo o objeto
    glRotatef(90.0, 0.0, 1.0, 0.0)
    glColor3ub(0, 0, 0)
    draw_model_faces(obj)
    glPopMatrix()

    obj = load_model("models/Flores.obj")
    glPushMatrix()
    glTranslatef(9.5, 2.0, 6.5)  # movendo o objeto
    glRotatef(0.0, 0.0, 1.0, 0.0)
    glScalef(0.2, 0.2, 0.2)  # reduzindo a escala
    glColor3ub(245, 245, 220)
    draw_model_faces(obj)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(9.5, 2.0, 7.5)  # movendo o objeto
    glRotatef(0.0, 0.0, 1.0, 0.0)
    glScalef(0.2, 0.2, 0.2)  # reduzindo a escala
    glColor3ub(245, 245, 220)
    draw_model_faces(obj)
    glPopMatrix()

    obj = load_model("models/Tv.obj")
    glPushMatrix()
    glTranslatef(9.5, 2.2, 12.5)  # movendo o objeto
    glRotatef(0.0, 0.0, 1.0, 0.0)
    glScalef(0.2, 0.2, 0.2)  # reduzindo a escala
    glColor3ub(0, 245, 220)
    draw_model_faces(obj)
    glPopMatrix()

    obj = load_model("models/Telefone.obj")
    glPushMatrix()
    glTranslatef(9.5, 2.1, 11.5)  # movendo o objeto
    glRotatef(180.0, 0.0, 1.0, 0.0)
    glScalef(0.1, 0.1, 0.1)  # reduzindo a escala
    glColor3ub(0, 0, 255)
    draw_model_faces(obj)
    glPopMatrix()
