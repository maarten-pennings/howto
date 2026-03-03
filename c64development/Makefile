all: build/border-dsk.d64

build/border-dsk.d64: build/border.prg build/border-sub.prg Makefile
	c1541 -format "border-dsk,bd" d64 build/border-dsk.d64 \
        -write build/border.prg      "border" \
        -write build/border-sub.prg  "border-sub"

build/border-sub.prg: src/border-sub.asm Makefile
	mkdir -p build
	64tass  src/border-sub.asm  -o build/border-sub.prg

build/border.prg: src/border.bas Makefile
	mkdir -p build
	petcat  -w2  -o build/border.prg  --  src/border.bas

clean:
	rm -rf build