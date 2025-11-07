## Sobre o projeto

Este repositório implementa uma cena 3D usando PyOpenGL (pipeline de função fixa) e FreeGLUT. A cena compõe um edifício com paredes, pisos, janelas (com vidro translúcido), porta, sacada e telhado, além de alguns objetos importados em formato OBJ. Os destaques técnicos são:

- Texturização com imagens (piso de madeira) e textura procedural (reboco das paredes)
- Iluminação por `GL_LIGHT0` com componentes ambiente/difusa/especular
- Normais por face/objeto e `GL_NORMALIZE` para manter a iluminação correta após escalas
- Uso de Stencil Buffer para recortes (vãos de janelas/porta) e Blending para vidros

## Texturas

### Onde ficam e como são carregadas

- Arquivos de textura residem em `textures/` (ex.: `textures/wood.jpg`).
- Texturas de arquivo são carregadas por `misa/primitives.py` (função `load_texture`), que:
  - Converte a imagem para RGBA (Pillow)
  - Cria um `GL_TEXTURE_2D` com `GL_REPEAT` em S/T
  - Usa `GL_LINEAR` para min/mag filter e gera mipmaps
- A textura de reboco das paredes é gerada proceduralmente em `misa/scene/procedural.py`:
  - `create_plaster_texture` cria uma imagem com variações sutis de cor
  - `load_texture_from_image` carrega essa imagem como textura OpenGL e define `GL_TEXTURE_ENV_MODE = GL_MODULATE`

### Mapeamento UV (repetição proporcional)

Os retângulos utilitários (`draw_rect_x`, `draw_rect_y`, `draw_rect_z`) definem coordenadas de textura em função das dimensões reais desenhadas, o que resulta em repetição proporcional da textura em superfícies maiores, sem distorção.

### Onde as texturas são aplicadas na cena

- Pisos: `misa/scene/pisos.py` usa `wood.jpg` e faz bind/unbind ao redor do desenho dos pisos.
- Paredes externas: `misa/scene/paredes.py` faz bind de uma textura de reboco gerada proceduralmente e a aplica nos quads das fachadas.

### Como adicionar uma nova textura

1. Adicione o arquivo em `textures/`.
2. Faça `GL.glBindTexture(GL.GL_TEXTURE_2D, primitives.load_texture("minha-textura.png"))` antes de desenhar quads/retângulos.
3. Desenhe com as funções `draw_rect_*` ou seus próprios quads definindo `glTexCoord2*`.
4. Desfaça o bind com `GL.glBindTexture(GL.GL_TEXTURE_2D, 0)` ao finalizar.

## Iluminação

### Configuração global

A iluminação é configurada em `misa/scene/__init__.py` (função `init`):

- `GL_LIGHTING` e `GL_LIGHT0` habilitados
- `GL_NORMALIZE` para corrigir normais após escalas
- `GL_COLOR_MATERIAL` com `GL_AMBIENT_AND_DIFFUSE` para que a cor corrente defina o material base
- `GL_SMOOTH` para sombreamento suave
- Componentes da luz (valores típicos):
  - Ambiente: `[0.4, 0.4, 0.4, 1.0]`
  - Difusa: `[1.0, 1.0, 1.0, 1.0]`
  - Especular: `[0.1, 0.1, 0.1, 1.0]`

A posição da luz (`GL_POSITION`) é atualizada em `on_setup_camera`, com `w = 0.0` (luz direcional), garantindo que a direção luminosa acompanhe a câmera.

### Normais e materiais

- Para geometria construída via utilitários (paredes, etc.), normais por face são definidas explicitamente antes do desenho.
- Para modelos OBJ, as normais são lidas e enviadas via VBO; a iluminação responde corretamente a essas normais.
- Com `GL_COLOR_MATERIAL`, as chamadas `glColor*` definem a componente ambiente+difusa do material; o realce especular é controlado pela luz especular global.

### Casos especiais e transparência

- A sacada (`misa/scene/sacada.py`) é desenhada sem iluminação (desliga `GL_LIGHTING`) para obter cor branca sólida, pois o modelo é renderizado sem normais nesse trecho, e a iluminação geraria artefatos.
- Vidros das janelas usam Blending (`GL_BLEND`) com `SRC_ALPHA, ONE_MINUS_SRC_ALPHA` para translucidez; funcionam em conjunto com a iluminação ambiente.

## Como executar

```shell
$ python -m misa
```

## Dependências

- Python 3.12 ou superior
- PyOpenGL e PyOpenGL-accelerate
- FreeGLUT

### Instalação das dependências

```shell
$ pip install -r requirements.txt
```

## Estrutura do projeto (resumo)

- `misa/scene/`: montagem da cena (paredes, pisos, janelas, sacada, telhado, etc.)
- `misa/primitives.py`: utilitários de desenho (quads, boxes, UVs, stencil) e carregamento de texturas
- `misa/objImporter.py`: importação e desenho de modelos OBJ com VBOs (vértices, normais, índices)
- `textures/`: imagens usadas nas texturas (ex.: `wood.jpg`)
- `models/`: modelos OBJ usados na cena
