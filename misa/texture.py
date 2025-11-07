"""Módulo para carregar e gerenciar texturas OpenGL."""
import random
from typing import Optional

from OpenGL import GL
from PIL import Image


def load_texture_from_image(image: Image.Image) -> int:
    """
    Carrega uma textura OpenGL a partir de uma imagem PIL.
    
    Args:
        image: Imagem PIL em qualquer formato
        
    Returns:
        ID da textura OpenGL
    """
    # Converter para RGBA se necessário
    image = image.convert("RGBA")
    img_data = image.tobytes()
    width, height = image.size
    
    # Gerar ID de textura
    texture_id = GL.glGenTextures(1)
    GL.glBindTexture(GL.GL_TEXTURE_2D, texture_id)
    
    # Configurar parâmetros da textura
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_REPEAT)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_REPEAT)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
    
    # Carregar dados da textura
    GL.glTexImage2D(
        GL.GL_TEXTURE_2D,
        0,
        GL.GL_RGBA,
        width,
        height,
        0,
        GL.GL_RGBA,
        GL.GL_UNSIGNED_BYTE,
        img_data,
    )
    
    return texture_id


def create_plaster_texture(width: int = 512, height: int = 512, seed: Optional[int] = None) -> Image.Image:
    """
    Cria uma textura procedural de reboco usando ruído aleatório.
    
    Args:
        width: Largura da textura
        height: Altura da textura
        seed: Semente para geração aleatória (para reprodutibilidade)
        
    Returns:
        Imagem PIL com textura de reboco
    """
    if seed is not None:
        random.seed(seed)
    
    # Cor base do reboco (bege/creme claro)
    base_r, base_g, base_b = 228, 206, 211
    
    # Criar imagem
    image = Image.new("RGB", (width, height))
    pixels = []
    
    for y in range(height):
        for x in range(width):
            # Adicionar variação aleatória para simular textura de reboco
            variation = random.randint(-15, 15)
            
            r = max(0, min(255, base_r + variation))
            g = max(0, min(255, base_g + variation))
            b = max(0, min(255, base_b + variation))
            
            pixels.append((r, g, b))
    
    image.putdata(pixels)
    
    # Aplicar um leve blur para suavizar (simula reboco mais realista)
    # Blur muito leve para manter a textura granulada
    from PIL import ImageFilter
    image = image.filter(ImageFilter.GaussianBlur(radius=0.5))
    
    return image


def load_plaster_texture() -> int:
    """
    Cria e carrega uma textura de reboco procedural.
    
    Returns:
        ID da textura OpenGL
    """
    image = create_plaster_texture(512, 512, seed=42)
    return load_texture_from_image(image)


def bind_texture(texture_id: int) -> None:
    """Ativa uma textura."""
    GL.glBindTexture(GL.GL_TEXTURE_2D, texture_id)


def unbind_texture() -> None:
    """Desativa a textura atual."""
    GL.glBindTexture(GL.GL_TEXTURE_2D, 0)

