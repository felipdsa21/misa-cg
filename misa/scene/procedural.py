import functools
import random
from typing import Optional

from PIL import Image

from .. import primitives, util

cor_creme = util.Vec3d(228, 206, 211)


def create_plaster_texture(
    color: util.Vec3d, width: int = 512, height: int = 512, seed: Optional[int] = None
) -> Image.Image:
    if seed is not None:
        random.seed(seed)

    base_r, base_g, base_b = color.x, color.y, color.z

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


@functools.cache
def load_plaster_texture(color: Optional[util.Vec3d] = cor_creme) -> int:
    image = create_plaster_texture(color, 512, 512, seed=42)
    return primitives.load_texture_from_image(image)
