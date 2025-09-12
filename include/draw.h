#pragma once

#include <stdbool.h>

void init(void);
void draw(void);
bool updateAnimation(void);
void onSetupCamera(void);
void onKey(unsigned char key, int x, int y);
bool onMousePress(int button, int state, int x, int y);
