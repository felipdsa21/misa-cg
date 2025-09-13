#pragma once

#include <stdbool.h>

void init(void);
void draw(void);

void onSetupCamera(void);
bool onLoop(void);
bool onMousePress(int button, int state, int x, int y);
