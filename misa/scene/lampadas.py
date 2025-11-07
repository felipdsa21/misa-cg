"""Lâmpadas com iluminação pontual para o interior do museu."""
from OpenGL import GL, GLU

from .. import primitives, util
from . import constantes


# Posições das lâmpadas no museu (relativas ao sistema de coordenadas do edifício)
# OpenGL suporta no máximo 8 luzes (GL_LIGHT0 a GL_LIGHT7)
# GL_LIGHT0 já está em uso, então usamos GL_LIGHT1 a GL_LIGHT7 (7 lâmpadas)
lampadas_config = [
    # Asa direita - 2 lâmpadas (coladas no teto da asa)
    {"pos": util.Vec3d(5.0, 0.0, constantes.asa_z_offset + 7.5), "light_id": GL.GL_LIGHT1, "ceiling": "asa"},
    {"pos": util.Vec3d(5.0, 0.0, constantes.asa_z_offset + 3.0), "light_id": GL.GL_LIGHT2, "ceiling": "asa"},
    
    # Parte central (andar inferior) - 2 lâmpadas (coladas no forro do 1º andar)
    {"pos": util.Vec3d(constantes.asa_size.x + 3.5, 0.0, 10.0), "light_id": GL.GL_LIGHT3, "ceiling": "central_low"},
    {"pos": util.Vec3d(constantes.asa_size.x + 9.5, 0.0, 10.0), "light_id": GL.GL_LIGHT4, "ceiling": "central_low"},
    
    # Parte central (andar superior) - 1 lâmpada (colada no teto superior)
    {"pos": util.Vec3d(constantes.asa_size.x + 6.5, 0.0, 10.0), "light_id": GL.GL_LIGHT5, "ceiling": "central_high"},
    
    # Asa esquerda - 2 lâmpadas (espelhadas)
    {"pos": util.Vec3d(constantes.asa_size.x + constantes.parte_central_size.x + 5.0, 0.0, constantes.asa_z_offset + 7.5), "light_id": GL.GL_LIGHT6, "ceiling": "asa"},
    {"pos": util.Vec3d(constantes.asa_size.x + constantes.parte_central_size.x + 5.0, 0.0, constantes.asa_z_offset + 3.0), "light_id": GL.GL_LIGHT7, "ceiling": "asa"},
]


def _ceiling_y(label: str) -> float:
    """Retorna a altura do teto para o rótulo informado."""
    if label == "asa":
        return constantes.asa_size.y
    if label == "central_low":
        return constantes.segundo_andar_y
    if label == "central_high":
        return constantes.parte_central_size.y
    return constantes.asa_size.y


def init_lampadas():
    """Inicializa as configurações das luzes pontuais."""
    # Cor da luz das lâmpadas (amarelo quente, mais suave)
    luz_cor = [0.6, 0.5, 0.3, 1.0]
    luz_especular = [0.4, 0.4, 0.2, 1.0]
    
    # Configurar cada luz
    for lamp in lampadas_config:
        light_id = lamp["light_id"]
        GL.glEnable(light_id)
        GL.glLightfv(light_id, GL.GL_DIFFUSE, luz_cor)
        GL.glLightfv(light_id, GL.GL_SPECULAR, luz_especular)
        GL.glLightfv(light_id, GL.GL_AMBIENT, [0.05, 0.05, 0.02, 1.0])
        
        # Atenuação maior para luz mais localizada
        GL.glLightf(light_id, GL.GL_CONSTANT_ATTENUATION, 1.0)
        GL.glLightf(light_id, GL.GL_LINEAR_ATTENUATION, 0.15)
        GL.glLightf(light_id, GL.GL_QUADRATIC_ATTENUATION, 0.08)


def draw_lampada(pos: util.Vec3d):
    """Desenha o objeto visual de uma lâmpada no teto."""
    with primitives.push_matrix():
        GL.glTranslated(pos.x, pos.y, pos.z)
        
        # Desabilitar iluminação para o bulbo (emissivo)
        GL.glDisable(GL.GL_LIGHTING)
        
        bulbo_raio = 0.2
        
        # Suporte pequeno no teto (metal escuro)
        GL.glColor3ub(80, 80, 70)
        with primitives.push_matrix():
            GL.glTranslated(0, 0, 0)
            GL.glRotatef(-90, 1, 0, 0)
            GLU.gluCylinder(constantes.q, 0.12, 0.1, 0.1, 16, 1)
        
        # Bulbo emissor (amarelo brilhante) - diretamente abaixo do suporte
        GL.glColor3ub(255, 240, 180)
        with primitives.push_matrix():
            GL.glTranslated(0, -0.1 - bulbo_raio, 0)
            GLU.gluSphere(constantes.q, bulbo_raio, 16, 16)
        
        GL.glEnable(GL.GL_LIGHTING)


def update_lampadas_positions():
    """Atualiza as posições das luzes pontuais (PRECISA ser chamado após configurar câmera)."""
    bulbo_raio = 0.2
    for lamp in lampadas_config:
        base = lamp["pos"]
        y_teto = _ceiling_y(lamp.get("ceiling", "asa")) - constantes.epsilon
        light_id = lamp["light_id"]
        # Posição da luz no centro do bulbo (logo abaixo do suporte)
        light_pos = [base.x, y_teto - 0.1 - bulbo_raio, base.z, 1.0]
        GL.glLightfv(light_id, GL.GL_POSITION, light_pos)


def draw_lampadas():
    """Desenha todas as lâmpadas visualmente."""
    # Desabilitar textura para desenhar as lâmpadas
    texture_was_enabled = GL.glIsEnabled(GL.GL_TEXTURE_2D)
    if texture_was_enabled:
        GL.glDisable(GL.GL_TEXTURE_2D)
    
    for lamp in lampadas_config:
        base = lamp["pos"]
        y_teto = _ceiling_y(lamp.get("ceiling", "asa")) - constantes.epsilon
        draw_lampada(util.Vec3d(base.x, y_teto, base.z))
    
    if texture_was_enabled:
        GL.glEnable(GL.GL_TEXTURE_2D)

