from OpenGL import GL

from .. import objImporter


def draw_objetos():
    obj = objImporter.load_model("models/Mesa.obj")
    GL.glPushMatrix()
    GL.glTranslatef(10.0, 1.0, 7.0)  # movendo o objeto
    GL.glRotatef(90.0, 0.0, 1.0, 0.0)
    GL.glColor3ub(0, 0, 0)
    objImporter.draw_model_faces(obj)
    GL.glPopMatrix()

    GL.glPushMatrix()
    GL.glTranslatef(10.0, 1.0, 12.0)  # movendo o objeto
    GL.glRotatef(90.0, 0.0, 1.0, 0.0)
    GL.glColor3ub(0, 0, 0)
    objImporter.draw_model_faces(obj)
    GL.glPopMatrix()

    obj = objImporter.load_model("models/Flores.obj")
    GL.glPushMatrix()
    GL.glTranslatef(9.5, 2.0, 6.5)  # movendo o objeto
    GL.glRotatef(0.0, 0.0, 1.0, 0.0)
    GL.glScalef(0.2, 0.2, 0.2)  # reduzindo a escala
    GL.glColor3ub(245, 245, 220)
    objImporter.draw_model_faces(obj)
    GL.glPopMatrix()

    GL.glPushMatrix()
    GL.glTranslatef(9.5, 2.0, 7.5)  # movendo o objeto
    GL.glRotatef(0.0, 0.0, 1.0, 0.0)
    GL.glScalef(0.2, 0.2, 0.2)  # reduzindo a escala
    GL.glColor3ub(245, 245, 220)
    objImporter.draw_model_faces(obj)
    GL.glPopMatrix()

    obj = objImporter.load_model("models/Tv.obj")
    GL.glPushMatrix()
    GL.glTranslatef(9.5, 2.2, 12.5)  # movendo o objeto
    GL.glRotatef(0.0, 0.0, 1.0, 0.0)
    GL.glScalef(0.2, 0.2, 0.2)  # reduzindo a escala
    GL.glColor3ub(0, 245, 220)
    objImporter.draw_model_faces(obj)
    GL.glPopMatrix()

    obj = objImporter.load_model("models/Telefone.obj")
    GL.glPushMatrix()
    GL.glTranslatef(9.5, 2.1, 11.5)  # movendo o objeto
    GL.glRotatef(180.0, 0.0, 1.0, 0.0)
    GL.glScalef(0.1, 0.1, 0.1)  # reduzindo a escala
    GL.glColor3ub(0, 0, 255)
    objImporter.draw_model_faces(obj)
    GL.glPopMatrix()
