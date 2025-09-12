#pragma once

#include <stdbool.h>

/* Somente as funções da cena */
void init(void);
void draw(void);

/* Tecla para alternar as portas (chamada pelo main) */
void onKey(unsigned char key, int x, int y);

/* Atualiza animações da cena; retorna true se requer redesenho */
bool updateSceneAnimation(void);
