# How to implement USR() on the C64

This document explains how to implement a `USR()` function on the C64.

It also shows a trick from Robin "8-Bit Show And Tell" how to easily return to Turbo Macro Pro.


## Introduction

Commodore BASIC has two ways to mix machine language subroutines with BASIC: `SYS <address>` and `USR(<argument>)`.


### SYS

The first one is relatively straightforward. The `SYS` command is passed address, and then execution is transferred to
the machine code at that address, until an `RTS`. That transfers execution back to basic. There is no official
way to pass an argument, nor is there an official way to get a return value. 

The following example calls the routine at 49152 (a free region of memory). 
Make sure to first place a routine there (e.g. by `POKE`ing or via `LOAD "XXX",8,1`).
At minimum `POKE 49152,96` to get a one-instruction routine `RTS`.

```basic
  SYS 49152
```


### USR

The second method allows passing an argument to the routine, and getting a result back.
We can pass _one_ argument, and we get one result back; both must be floating point).
That is a bit limited, but for the rest, this function behaves like any BASIC function;
it can appear in any place where say `SIN` can occur.

The following example is a bit contrived, but it shows the possibilities.

```basic 
  PRINT USR(785)+USR(780+5)
```

You might wonder which routine gets called. The answer is the vector at location 785 ($311).
By default this vector points to a routine that prints `?ILLEGAL QUANTITY  ERROR`.
You would poke the vector with your routines address before calling `USR()`.


### Expression

It is good to realize that Commodore BASIC has three _types_: float, string and integer.
A variable (function) ending in `$` is (returns) a string, a variable ending in `%` is an integer,
all other variables and function are float. Floats are stored in 5 bytes, strings use
variable width blocks on a heap and integers are _signed_ and 16 bit. 

You might be thinking that it would generally be better to use integers, but the answer is a firm _no_.
First of all you do not save memory: every variable uses 7 bytes: 2 for the name and 5 for the value
(float, size and pointer, respectively lo byte and high byte and padding). Secondly, you do not
save cycles. On the contrary: integers are first converted to float, then the computation is performed
in the float domain, and the result is converted back to integer. This has been done to keep
the BASIC interpreter simple; there is only one "ALU", a float one.

Why are there integers? They help in one place: when you make an array of them. Then to occupy only 2 bytes.


### ALU

Commodore BASIC has an "ALU" (arithmetic and logic unit) in the float domain.
It has a "FAC" (a Floating point ACcumulator), and a second accumulator, "FAC2" or "ARG".
It also implements several operation; see [c64.org](https://sta.c64.org/cbm64basconv.html)
or [codebase64.org](https://codebase64.org/doku.php?id=base:kernal_floating_point_mathematics#the_floating_point_routines).

Example are "FAC:=ARG+FAC" or "FAC:=const*FAC".



## Turbo Macro Pro

To write the `USR` function, we will use TMP or [Turbo Macro Pro](https://turbo.style64.org/).
This is an assembler that runs on the C64 itself, but also on [VICE](https://vice-emu.sourceforge.io/), the emulator.

TMP consists of an editor with some commands.
One command is assemble, another command is to run it, or go to basic (and there start it).
Typically in the development cycle, you test and want to go back to TMP.

Robin from [8-Bit Show And Tell](https://www.youtube.com/c/8BitShowAndTell) has a clever trick for that.
I first saw it in a [video](https://www.youtube.com/watch?v=05vlobA3JeU) but when I needed it, I couldn't find it back.
Fortunately, somebody else documented it in wa way that was easier to [find](https://old-crank.neocities.org/examples/easy.return.to.tmp).

The trick is to add this to your assembler program.

```asm
tmpentry  = $8000
          sei ; make vector swap atomic
          lda #<tmpentry
          sta $0318
          lda #>tmpentry
          sta $0319
          cli
```

What it does is vector the interrupt (caused by pressing the RESTORE key) to the start of TMP.
**One key press, and your back.**


## Implementing `USR()` 

We write an assembly program that we locate in the cassette buffer.
The program consists of two parts. The second part implements the
function `USR`. The first part sets up the vector to the second part.


### Program header

The program header explains shortly what to program does.
More importantly is specifies the location for the program.
We selected the cassette buffer ar (decimal) 828.

```basic 
         ; implements usr(addr)
         ; returns vector at <addr>
         ; also known as deek(addr)
         ; Maarten Pennings 2025 04 23
         *= 828 ; cassette buffer
```

### Setup vector

The first part of the program sets the vector of the `USR`
function to point to the second part of our program.
The vector is located at (decimal) 785 (vectors take two bytes).

This is just two stores and a return.
Observe that `<` and `>` are TMP functions that take the
low byte and high byte respectively of a word (an address).

```basic 
         ; set usr() vector
usradd   = 785; $0311
         lda #<main
         sta usradd+0
         lda #>main
         sta usradd+1
         rts
```

### Some constants

The second parts needs some constants.
It uses three subroutines and two buffers (`poker` and `fac`).

```basic
getadr   = $b7f7; int(fac) to mem[poker]
givayf   = $b391; a/y to fac
addmem   = $b867; fac+=mem[a/y]
poker    = $14  ; aka linnum
fac      = $61  ; floating point accu
```

### DEEK() implementation

We are making DEEK or double PEEK.

```basic
  DEEK(A) := PEEK(A)+256*PEEK(A+1)
```

When calling `USR(expr)`, BASIC first evaluates `expr` and puts the
resulting value in the floating point accumulator (`FAC`).

We use the function `getadr` which converts the FAC to an integer.
This routine assumes the integer is an address and even gives an
error when out of range. If the number is ok, the routine returns
with address in location known as `poker` (address $14).

When we would enter `USR(2039)` to inspect location $0801, after 
this call, `poker` would store the low byte $01 and `poker+1` would 
store the high byte $08.

We now want to peek at location $0801 and $0802, this is where the two
`lda (addr),y` comes to the rescue. After that, `x` has the high byte
mem[$0802] and `y` has the low byte mem[$0801].

Finally we call the routine givayf which converts the integer
in `y` and `a` to a float in FAC.


```basic 
main     ; fac parsed as int in poker
         jsr getadr
         
         ; deref to get hi byte in x
         ldy #1
         lda (poker),y
         tax
         ; deref to get lo byte in y
         dey
         lda (poker),y
         tay
         
         ; lo in y, hi in a, to fac
         txa
         jsr givayf
```

You might believe we are done now.
But we are not.
The problem is integer overflow.
If the value in y/a exceeds 32767, the FAC becomes negative.

If the is new to you, try `FRE()` is suffers from this.

```basic 

    **** COMMODORE 64 BASIC V2 ****

 64K RAM SYSTEM  38911 BASIC BYTES FREE

READY.
?FRE(0)
-26627

READY.
?65536+FRE(0)
 38909

READY.
```

The final piece of the puzzle comes now.
When the FAC is negative, we add 65536.
We use `addmem` which adds a float constant
pointed to bt a/y to FAC.

The constant is located a `n65536` at the
end of the program. This is in floating
point representation.


```basic 
         ; problem: if y/a>32767 the
         ; fac is now negative
         ; same problem not fixed for
         ; the fre() function

         ; if fac>=0 then done
         lda fac+5 ; sign
         beq done

         ; fac<0 so add 65536,as fre()
         lda #<n65536
         ldy #>n65536
         jsr addmem

done     ; return fac
         rts

         ; 65536 encoded as float
n65536   .byte 145,0,0,0,0,0
```

## Running

Let's try it.
First some illegal addresses.
Next the vector of USR iteself.
And finally BRK vector at 65534, which maps to 65352.

```basic
SYS 828

READY.
?USR(-2)

?ILLEGAL QUANTITY  ERROR
READY.

?USR(65536)

?ILLEGAL QUANTITY  ERROR
READY.

?USR(785)
 839

READY.
?USR(65534)
 65352

READY.
```


## Files

Unpacked with [d64viewer](https://github.com/maarten-pennings/d64viewer) to get the files.

- [`usr13@828.d64`](usr13@828.d64) the disk image with the following files.
- [`usr13@828.tmp`](usr13@828.tmp) the turbo macro pro source (binary).
- [`usr13@828.txt`](usr13@828.txt) the turbo macro pro source (text).
- [`usr13@828.prg`](usr13@828.prg) the generated executable which will be loaded at address 828.


(end)







