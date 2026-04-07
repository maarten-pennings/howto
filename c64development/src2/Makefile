test: build/result.log

all: build/bord2scrn.d64

build/bord2scrn.d64: build/bord2scrn.prg build/testprog-vals.prg build/testprog-dflt.prg Makefile
	c1541 -format "bord2scrn,bd" d64 build/bord2scrn.d64 \
        -write build/bord2scrn.prg      bord2scrn      \
        -write build/testprog-vals.prg  testprog-vals  \
        -write build/testprog-dflt.prg  testprog-dflt

build/bord2scrn.prg: bord2scrn.asm Makefile
	mkdir -p build
	64tass  bord2scrn.asm  -o build/bord2scrn.prg

build/testprog-vals.prg: testprog-vals.bas Makefile
	mkdir -p build
	petcat  -w2  -o build/testprog-vals.prg  --  testprog-vals.bas

build/testprog-dflt.prg: testprog-dflt.bas Makefile
	mkdir -p build
	petcat  -w2  -o build/testprog-dflt.prg  --  testprog-dflt.bas

clean:
	rm -rf build



PRINTER4 = -pr4txtdev 0  -pr4output text  -pr4drv ascii  -device4  1  -virtualdev4
DISK8 = -drive8type 1542  
OTHER = -warp  
ARGS = $(DISK8) $(PRINTER4) $(OTHER)

build/result.log: build/result-vals.log build/result-dflt.log Makefile
	rm -f build/result.log
	date +%Y%m%d.%H%M%S > build/result.log
	grep RESULT build/result-vals.log >> build/result.log
	grep RESULT build/result-dflt.log >> build/result.log
	echo SUMMARY `grep PASS build/result.log | wc -l`  `grep FAIL build/result.log | wc -l` >> build/result.log

build/result-vals.log: build/bord2scrn.d64 build/testprog-vals.prg Makefile
	rm -f build/result-vals.log
	x64sc  $(ARGS)  -prtxtdev1 build/result-vals.log  -autostart build/bord2scrn.d64:testprog-vals  -limitcycles 40999000

build/result-dflt.log: build/bord2scrn.d64 build/testprog-dflt.prg Makefile
	rm -f build/result-dflt.log
	x64sc  $(ARGS)  -prtxtdev1 build/result-dflt.log  -autostart build/bord2scrn.d64:testprog-dflt  -limitcycles 40999000

