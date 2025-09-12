TARGET := $(shell $(CC) -dumpmachine)
WINDOWS := $(strip $(foreach W,msys w64 windows,$(findstring -$W-,-$(TARGET)-)))
BINEXT := $(if $(WINDOWS),.exe,)
TARGET_LDLIBS := $(if $(WINDOWS),-lglu32 -lopengl32,-lGLU -lOpenGL -lglut)

ERROR_CFLAGS := -Wall -Wc++-compat -Wconversion -Wextra -Wpedantic -Wvla
CFLAGS := $(ERROR_CFLAGS) $(shell pkgconf --cflags freeglut) -Iinclude/ $(CFLAGS)
LDLIBS := -lm $(TARGET_LDLIBS) $(shell pkgconf --libs freeglut)

NAME := misa
SRC := include/*.h src/*.c
OUT_FILE := $(NAME)$(BINEXT)

.PHONY: build

build: build/$(OUT_FILE)

build/:
	mkdir $@

build/$(OUT_FILE): $(SRC) | build/
	$(CC) $(CFLAGS) -o $@ $(filter %.c,$^) $(LDLIBS)
