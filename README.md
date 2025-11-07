## Sobre o projeto

Projeto de Computação Gráfica (OpenGL/FreeGLUT com Python) que renderiza um edifício em estilo clássico (um pequeno "museu"), com janelas, portas, telhados, sacada (modelo OBJ), piso texturizado e iluminação noturna. A cena usa iluminação fixa do pipeline (GL_LIGHTx), texturas 2D, transparência para vidros e stencil para recortes precisos (portas/janelas).

Os focos desta documentação são Textura e Iluminação — como estão configuradas, onde o código vive e como ajustar.

## Dependências
- Python 3.12 ou superior
- PyOpenGL e PyOpenGL-accelerate
- FreeGLUT
- Pillow (PIL) para criar/carregar texturas

### Instalação das dependências

```shell
$ pip install -r requirements.txt
```

## Como executar

```shell
$ python -m misa
```

## Organização da cena (arquivos principais)
- `misa/scene/__init__.py`: inicialização de OpenGL (estados, luz ambiente), laço de desenho e callbacks (câmera, input).
- `misa/scene/paredes.py`: paredes externas com recortes por stencil e aplicação de textura de reboco procedural.
- `misa/scene/pisos.py`: pisos com textura de madeira.
- `misa/scene/janelas.py`: geometrias das janelas (retangulares e com arco), incluindo vidro translúcido (blend).
- `misa/scene/lampadas.py`: lâmpadas internas (fontes de luz pontuais) e desenho do bulbo emissivo.
- `misa/scene/sacada.py`: sacada carregada de `models/Sacada.obj` (com normais para iluminação).
- `misa/primitives.py`: primitivas de desenho, mapeamento de textura (UV) e carregamento de texturas de arquivo.
- `misa/scene/procedural.py`: geração e carregamento de textura procedural (reboco).

## Textura

### Visão geral
- **Texturas habilitadas** em `scene/__init__.py` (`GL_TEXTURE_2D`).
- **Paredes** usam uma textura de reboco gerada proceduralmente e aplicada com coordenadas em escala do mundo para telagem natural.
- **Pisos** usam textura de arquivo (`textures/wood.jpg`) com mipmaps.
- **Vidros** usam blend/transparência (não são texturizados), com cor RGBA e `GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA`.

### Onde é feito
- Paredes: `misa/scene/paredes.py`
  - `GL.glBindTexture(GL.GL_TEXTURE_2D, procedural.load_plaster_texture())` antes de desenhar as superfícies.
  - Desenho usando `primitives.draw_rect_*`, que já define coordenadas de textura (UV) proporcionais às dimensões.
- Piso: `misa/scene/pisos.py`
  - `GL.glBindTexture(GL.GL_TEXTURE_2D, primitives.load_texture("wood.jpg"))` e desenho com `draw_rect_y`.
- Carregamento de textura:
  - Arquivo: `misa/primitives.py` ➜ `load_texture(name)` abre `textures/<name>`, configura `GL_REPEAT`, filtros lineares e gera mipmaps (`glGenerateMipmap`).
  - Procedural: `misa/scene/procedural.py` ➜ `create_plaster_texture()` gera imagem (PIL) com variação de cor; `load_texture_from_image()` cria a textura OpenGL, define `GL_REPEAT`, filtros lineares e `GL_TEXTURE_ENV_MODE = GL_MODULATE` para combinar com iluminação/material.

### Mapeamento UV (como as texturas "assentam" nas superfícies)
- As funções `primitives.draw_rect_x|y|z` enviam `glTexCoord2d(...)` com valores derivados das coordenadas do mundo.
- Isso faz a textura repetir proporcionalmente ao tamanho da face (telagem automática). Se uma parede mede 10 unidades no eixo X, o U varia de 0 a 10 e, com `GL_REPEAT`, a textura repete 10 vezes.
- Para ajustar a escala aparente:
  - Reduza/divida as coordenadas usadas nas primitivas (ex.: usar `x/2, y/2`) ou
  - Troque por uma textura com padrão mais denso/menos denso.

### Como adicionar novas texturas
1. Coloque o arquivo em `textures/` (ex.: `minha_textura.png`).
2. No código, carregue com `primitives.load_texture("minha_textura.png")`.
3. Antes de desenhar a geometria alvo, faça `GL.glBindTexture(GL.GL_TEXTURE_2D, texture_id)`.
4. Use `primitives.draw_rect_*` (ou defina UVs manualmente com `glTexCoord2d`).
5. Ao terminar aquele bloco, faça `GL.glBindTexture(GL.GL_TEXTURE_2D, 0)` para limpar o bind local.

Observações:
- Mipmaps já são gerados em `load_texture` (arquivos). No fluxo procedural, se precisar de mipmaps, você pode chamar `glGenerateMipmap(GL_TEXTURE_2D)` após o `glTexImage2D`.
- O modo `GL_MODULATE` garante que a textura seja afetada pela iluminação (mais realista). Evite `GL_REPLACE` se quiser sombreamento.

### Mapa de funções (Textura)
- `misa/scene/__init__.py`
  - `init()`: habilita `GL_TEXTURE_2D` e define estados globais.
- `misa/scene/procedural.py`
  - `create_plaster_texture(...)`: gera imagem da textura de reboco (PIL) com variação.
  - `load_texture_from_image(image)`: cria a textura OpenGL (wrap, filtro, `GL_MODULATE`).
  - `load_plaster_texture()`: memoiza/cria e retorna o texture id do reboco.
- `misa/primitives.py`
  - `load_texture(name)`: carrega `textures/<name>`, configura wrap/filtros e mipmaps.
  - `draw_rect_x|y|z(...)`: desenha retângulos e envia UVs proporcionais ao tamanho da face.
  - `mascarar_retangulo_xy|yz|xz(...)`: desenha máscaras (desabilita textura durante a escrita no stencil).
- `misa/scene/paredes.py`
  - `draw_paredes()`: faz bind de `procedural.load_plaster_texture()` e desenha paredes.
  - `draw_asa()` / `draw_parte_central()`: desenham faces com `primitives.draw_rect_*` (UV implícito).
  - `mascarar_janela_arco(...)` / `mascarar_retangulo(...)`: constroem máscaras para portas/janelas (stencil) sem afetar textura fora dos vãos.
- `misa/scene/pisos.py`
  - `draw_pisos()`: bind de `primitives.load_texture("wood.jpg")`, desenho dos pisos e unbind ao final.
  - `draw_piso_terreo()` / `draw_piso_primeiro_andar()`: organizam stencil e chamadas de piso.
  - `draw_piso(...)`: desenha uma faixa de piso com `primitives.draw_rect_y`.
- `misa/scene/janelas.py`
  - `draw_janela_com_arco(...)` / `draw_janela_retangular(...)`: usam `GL_BLEND` para vidro translúcido (sem textura), molduras com cor sólida.

## Iluminação

### Visão geral
- Pipeline fixo de iluminação do OpenGL: `GL_LIGHT0` como luz ambiente/direcional fraca (noite) e **7 luzes pontuais internas** (`GL_LIGHT1`–`GL_LIGHT7`) para simular lâmpadas quentes no teto.
- `GL_SMOOTH` habilitado para sombreamento suave e `GL_COLOR_MATERIAL` para usar as cores (`glColor*`) como material difuso/ambiente.
- Normais são definidas por face/superfície com `glNormal*` e via dados do modelo OBJ (sacada) — fundamentais para iluminação correta.

### Onde é feito
- Inicialização: `misa/scene/__init__.py`
  - Habilita `GL_LIGHTING`, `GL_LIGHT0`, normalização de normais e materiais por cor.
  - Define a luz ambiente/difusa especular de `GL_LIGHT0` com valores baixos (noite).
  - Posiciona `GL_LIGHT0` a cada atualização de câmera (`on_setup_camera`), com `w = 0.0` (direcional).
- Lâmpadas internas: `misa/scene/lampadas.py`
  - Configura 7 luzes pontuais (`GL_LIGHT1`–`GL_LIGHT7`) com cor quente difusa/especular, baixa componente ambiente e atenuação (`constant`, `linear`, `quadratic`).
  - Atualiza a posição (com `w = 1.0`) após a câmera estar posicionada (`update_lampadas_positions`).
  - Desenha um bulbo emissivo (iluminação desabilitada momentaneamente) para reforçar o efeito visual.

### Ajustes práticos
- Intensidade/Cor global (noite): edite `luz_ambiente`, `luz_difusa` e `luz_especular` de `GL_LIGHT0` em `scene/__init__.py`.
- Direção da luz direcional: ajuste `posicao_luz` em `on_setup_camera` (com `w = 0.0`).
- Lâmpadas internas: ajuste `luz_cor`, `luz_especular` e os coeficientes de atenuação em `scene/lampadas.py`.
- Posição das lâmpadas: mude a lista `lampadas_config` (posições e light IDs).
- Aparência dos materiais: altere cores usadas nos desenhos (`glColor3ub`) ou desabilite `GL_COLOR_MATERIAL` para trabalhar com `glMaterial*` explicitamente.

### Boas práticas usadas
- Normais explícitas por face antes de desenhar (`glNormal3i/d`).
- `GL_NORMALIZE` ativo para manter o comprimento das normais correto após escalas.
- `GL_COLOR_MATERIAL` para reduzir verbosidade e ainda permitir sombreamento coerente com textura (`GL_MODULATE`).

### Mapa de funções (Iluminação)
- `misa/scene/__init__.py`
  - `init()`: habilita `GL_LIGHTING`, `GL_LIGHT0`, `GL_NORMALIZE`, `GL_COLOR_MATERIAL`, `GL_SMOOTH`; define componentes ambiente/difusa/especular de `GL_LIGHT0` e atenuação; chama `lampadas.init_lampadas()`.
  - `on_setup_camera()`: posiciona `GL_LIGHT0` (direcional, `w=0.0`) e atualiza posições das lâmpadas (`lampadas.update_lampadas_positions()`).
- `misa/scene/lampadas.py`
  - `init_lampadas()`: habilita e configura `GL_LIGHT1`–`GL_LIGHT7` (cor difusa/especular quentes, ambiente baixa, atenuação).
  - `update_lampadas_positions()`: posiciona luzes pontuais com `glLightfv(..., GL_POSITION, [x,y,z,1.0])` após a câmera.
  - `draw_lampadas()`: desenha bulbos e suportes (desabilita textura durante desenho visual), chama `draw_lampada(...)`.
  - `draw_lampada(pos)`: desenha bulbo emissivo (desliga `GL_LIGHTING` localmente) e suporte.
- Normais por face
  - `misa/scene/paredes.py`: usa `GL.glNormal3i(...)` antes de cada face nas funções `draw_asa()` e `draw_parte_central()`.
  - `misa/scene/pisos.py`: `draw_piso(...)` define normal para o topo (`0,1,0`).
  - `misa/scene/telhado.py`: define normais (`glNormal3d`) para águas do telhado.
  - `misa/scene/sacada.py`: `objImporter.draw_model_faces(obj)` desenha o OBJ com normais do modelo para iluminação correta.

## Outros recursos gráficos
- **Stencil buffer** para recortar portas e janelas com precisão, evitando "vazamentos" de textura.
- **Transparência (blend)** para os vidros das janelas (RGBA com alpha baixo), desenhados após a moldura.
- **Modelo OBJ** da sacada com normais para iluminação correta.

## Dúvidas comuns
- A textura parece "esticada"? Revise a escala implícita do UV nas primitivas (UV = coordenadas do mundo). Use texturas que telam bem ou ajuste a escala.
- A iluminação ficou muito escura? Aumente `GL_LIGHT0` (difusa) e/ou a componente ambiente das luzes pontuais.
- Artefatos em superfícies coplanares? Pequenos `epsilon` já são usados (ex.: vidros). Se necessário, aumente levemente.

## Licença dos assets
Os arquivos em `textures/` e `models/` devem respeitar suas licenças de origem (inclua créditos/links conforme necessário). Esta base de código é para fins educacionais.

