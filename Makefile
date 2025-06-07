SOURCE_FILE ?= generator/tree1.c
DIST_FILE ?= dist/tree1

build: generator/tree1.c
	gcc `xml2-config --cflags --libs` -o $(DIST_FILE) $(SOURCE_FILE)
