from OpenGL import GLU

from .. import util

epsilon = 0.001

# Objeto quadric global
q = GLU.gluNewQuadric()
GLU.gluQuadricNormals(q, GLU.GLU_SMOOTH)

# Níveis dos pisos
piso_y = 1.0
segundo_andar_y = 7.0

# Dimensões do edifício
parte_central_size = util.Vec3d(13, 12.5, 20)
asa_size = util.Vec3d(10.5, 7, 15)
asa_z_offset = 1.0

# Dimensões da porta
porta_size = util.Vec3d(2.8, 3.2, 0)

# Dimensões e posições das janelas
janela_com_arco = util.Vec3d(1.2, 2.6, 0.3)
janela_baixo_y_offset = 1.4
janela_cima_y_offset = janela_baixo_y_offset + 1.6 + 3.2
