from OpenGL import GL

from .. import objImporter, primitives
from . import constantes


def draw_sacada():
    # Calcular posição da sacada (mesma lógica da versão procedural)
    x_antes_porta = (constantes.parte_central_size.x - constantes.porta_size.x) / 2.0
    largura = constantes.porta_size.x + 4.0
    base_y = constantes.porta_size.y + 1.5
    centro_x = constantes.asa_size.x + x_antes_porta + constantes.porta_size.x / 2.0
    start_x = centro_x - largura / 2.0

    # Carregar modelo OBJ
    obj = objImporter.load_model("models/Sacada.obj")

    with primitives.push_matrix():
        # Posicionar a sacada no local correto (aplicado por último em OpenGL)
        GL.glTranslated(start_x, base_y, 0)

        # Rotacionar -90° no eixo Z
        # Esta rotação: X' = Y, Y' = -X, Z' = Z
        GL.glRotatef(90.0, 0.0, 1.0, 0.0)

        # Calcular escala uniforme para manter proporções
        # Dimensões do modelo: X: ~90.66, Y: ~212.56, Z: ~153.18
        # Dimensões esperadas: largura ~6.8, profundidade ~1.25
        scale_factor = largura / 140  # Escala baseada na largura

        # Aplicar escala uniforme
        GL.glScalef(scale_factor * 0.5, scale_factor * 0.8, scale_factor)

        # Transladar para ajustar origem do modelo (aplicado primeiro em OpenGL)
        # No espaço original do modelo:
        # - Y mínimo em ~17.48, alinhar a base para Y=0
        # - Z máximo em ~-16.29, trazer a face frontal para Z=0
        # Após rotação de -90° em Z, o que era Y vira X, então ajustamos X e Y
        GL.glTranslatef(46.5, -190, 173.5)

        # Desabilitar iluminação temporariamente para cor branca sem sombras
        lighting_was = GL.glIsEnabled(GL.GL_LIGHTING)
        if lighting_was:
            GL.glDisable(GL.GL_LIGHTING)

        # Definir cor branca
        GL.glColor3ub(255, 255, 255)

        # Renderizar o modelo sem normais (desabilitar array de normais)
        _draw_model_without_normals(obj)

        # Reabilitar iluminação se estava ativa
        if lighting_was:
            GL.glEnable(GL.GL_LIGHTING)


def _draw_model_without_normals(obj_model):
    """Desenha o modelo sem usar normais (para cor sólida sem iluminação)."""
    from .. import objImporter

    objImporter._create_vbos(obj_model)

    # Habilitar apenas array de vértices (sem normais)
    GL.glEnableClientState(GL.GL_VERTEX_ARRAY)

    # Bind e configurar VBO de vértices
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, obj_model.vbo_id)
    GL.glVertexPointer(3, GL.GL_FLOAT, 0, None)

    # Bind VBO de índices
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, obj_model.index_buffer_id)

    # Renderizar usando índices
    index_type = GL.GL_UNSIGNED_INT if obj_model.index_array.typecode == "I" else GL.GL_UNSIGNED_LONG
    GL.glDrawElements(GL.GL_TRIANGLES, obj_model.index_count, index_type, None)

    # Limpar estado
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)
    GL.glDisableClientState(GL.GL_VERTEX_ARRAY)
