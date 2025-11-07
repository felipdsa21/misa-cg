"""
OBJ Model Importer (Otimizado)
Desenvolvido por: Cristiano Ramos (original)
Otimizado para usar VBOs e parsing eficiente

Esta biblioteca permite importar modelos OBJ
para seu projeto OpenGL em Python usando VBOs.
"""

from dataclasses import dataclass
import functools
from typing import List, Optional
import array

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
    # Cache de VBOs para renderização otimizada
    vbo_id: Optional[int] = None
    index_buffer_id: Optional[int] = None
    index_count: int = 0
    # Arrays intercalados para renderização eficiente
    vertex_array: Optional[array.array] = None
    index_array: Optional[array.array] = None


@functools.cache
def load_model(file_name: str) -> Model:
    """Carrega um modelo OBJ de forma otimizada (parsing em uma única passada)."""
    vertices = []
    faces = []

    with open(file_name, "r", encoding="utf-8") as p_file:
        for line in p_file:
            line = line.strip()
            if not line:
                continue

            parts = line.split()
            if not parts:
                continue

            if parts[0] == "v" and len(parts) >= 4:
                # Parse vértice
                vertices.append(Vertex(x=float(parts[1]), y=float(parts[2]), z=float(parts[3])))
            elif parts[0] == "f" and len(parts) >= 2:
                # Parse face
                face_indices = []
                for i in range(1, len(parts)):
                    # Handle "v" or "v/vt/vn" format
                    vertex_index = int(parts[i].split("/")[0])
                    face_indices.append(vertex_index)

                if len(face_indices) >= 3:
                    faces.append(Face(v_number=len(face_indices), faces=face_indices))

    tot_v = len(vertices)
    tot_f = len(faces)

    model = Model(tot_v=tot_v, tot_f=tot_f, v=vertices, f=faces)

    # Preparar arrays para VBOs
    _prepare_vbo_data(model)

    return model


def _prepare_vbo_data(model: Model) -> None:
    """Prepara arrays de vértices e índices para uso com VBOs."""
    # Criar array de vértices (x, y, z para cada vértice)
    vertex_data = array.array("f")
    for vertex in model.v:
        vertex_data.append(vertex.x)
        vertex_data.append(vertex.y)
        vertex_data.append(vertex.z)

    # Criar array de índices
    # Usar 'I' (unsigned int) se disponível, senão 'L' (unsigned long)
    try:
        index_data = array.array("I")  # Unsigned int (32-bit)
    except (ValueError, OverflowError):
        index_data = array.array("L")  # Unsigned long (fallback)

    for face in model.f:
        # Converter índices OBJ (1-based) para índices Python (0-based)
        indices = [idx - 1 for idx in face.faces]

        # Triangulação de quads (se necessário)
        if face.v_number == 3:
            index_data.extend(indices)
        elif face.v_number == 4:
            # Dividir quad em dois triângulos
            index_data.append(indices[0])
            index_data.append(indices[1])
            index_data.append(indices[2])
            index_data.append(indices[0])
            index_data.append(indices[2])
            index_data.append(indices[3])

    model.vertex_array = vertex_data
    model.index_array = index_data
    model.index_count = len(index_data)


def _create_vbos(model: Model) -> None:
    """Cria VBOs na GPU para renderização eficiente."""
    if model.vbo_id is not None:
        return  # Já criado

    if model.vertex_array is None or model.index_array is None:
        _prepare_vbo_data(model)

    # Criar VBO para vértices (glGenBuffers retorna lista no PyOpenGL)
    vbo_ids = GL.glGenBuffers(2)
    model.vbo_id = vbo_ids[0]
    model.index_buffer_id = vbo_ids[1]

    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, model.vbo_id)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, model.vertex_array.tobytes(), GL.GL_STATIC_DRAW)

    # Criar VBO para índices
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, model.index_buffer_id)
    GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, model.index_array.tobytes(), GL.GL_STATIC_DRAW)

    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)


def draw_model_faces(obj_model: Model) -> None:
    """Desenha o modelo usando VBOs para máxima performance."""
    # Criar VBOs se ainda não foram criados
    _create_vbos(obj_model)

    # Habilitar arrays de vértices
    GL.glEnableClientState(GL.GL_VERTEX_ARRAY)

    # Bind e configurar VBO de vértices
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, obj_model.vbo_id)
    GL.glVertexPointer(3, GL.GL_FLOAT, 0, None)

    # Bind VBO de índices
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, obj_model.index_buffer_id)

    # Renderizar usando índices
    # Determinar tipo de índice baseado no tipo do array
    index_type = GL.GL_UNSIGNED_INT if obj_model.index_array.typecode == "I" else GL.GL_UNSIGNED_LONG
    GL.glDrawElements(GL.GL_TRIANGLES, obj_model.index_count, index_type, None)

    # Limpar estado
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)
    GL.glDisableClientState(GL.GL_VERTEX_ARRAY)


def draw_model_vertex(point_size: float, obj_model: Model) -> None:
    """Desenha apenas os vértices como pontos (modo de debug)."""
    GL.glPointSize(point_size)

    # Criar VBOs se necessário
    _create_vbos(obj_model)

    GL.glEnableClientState(GL.GL_VERTEX_ARRAY)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, obj_model.vbo_id)
    GL.glVertexPointer(3, GL.GL_FLOAT, 0, None)

    GL.glDrawArrays(GL.GL_POINTS, 0, obj_model.tot_v)

    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    GL.glDisableClientState(GL.GL_VERTEX_ARRAY)


def cleanup_model(obj_model: Model) -> None:
    """Libera recursos de VBOs do modelo."""
    if obj_model.vbo_id is not None and obj_model.index_buffer_id is not None:
        GL.glDeleteBuffers([obj_model.vbo_id, obj_model.index_buffer_id])
        obj_model.vbo_id = None
        obj_model.index_buffer_id = None
