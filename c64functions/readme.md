# C64 functions FNF(x)

In this article we look at _functions_ in Commodore 64 BASIC.

In the context of this article the stand-alone term "function" 
refers to `FN F(X)`, not subroutines (`GOSUB`), nor built-in functions.


## Introduction

Functions in C64 BASIC use the keyword `FN`.

To _call_ a function `F` with argument 3, we write `FN F(3)`.

Before calling `F`, function `F` must be defined. 
To _define_ a function we need a second keyword: `DEF`.
A function definition could look like this `DEF FN F(X)=X*2`.

Function definitions must be done in a BASIC program context.
If typed directly, the response is `?ILLEGAL DIRECT  ERROR`.
The reason is that the function _body_ (in our example `X*2`) must
be stored "persistently", in the BASIC program text. Once defined,
calls are allowed in direct mode.

As usual, spaces around BASIC keywords are optional.
The two fragments below are the same.
The former is more readable, the latter smaller and slightly faster 
(less characters for the interpreter).

```bas 
100 DEF FN F(X)=X*2
110 PRINT FN F(3)
```

```bas
100 DEFFNF(X)=X*2
110 PRINTFNF(3)
```


## Signature

One of the downsides of BASIC functions is that only one _signature_ is supported.

Liberally quoting [wikipedia](https://en.wikipedia.org/wiki/Type_signature):
a signature defines the inputs and outputs of a function;
it includes the number, types, and order of the function's arguments as 
well as the type it returns.

The one signature supported in C64 BASIC is "float to float".

```bas
100 DEF FN F()=12
110 DEF FN F(X)=12      <<< only supported one
120 DEF FN F(X,Y)=12
130 DEF FN F(X%)=12
140 DEF FN F$(X)="12"
150 DEF FN F(X$)=12
```

Of the above definitions, only the one on line 110 fits the supported 
signature. All other definitions give an error: `syntax  error` (for 
lines 100, 120, 130), or `type mismatch  error` (for lines 140 and 150).

It is surprising to see two different kind of errors, and I would
have expected that 130 gives the same error as 150.


## Naming

The `FN` part in front of the function name is mandatory.
But the name of the function does not have to be `F`.
Similarly the name of the argument does not have to be `X`.
Both can be any name that BASIC allows for a variable. 

This means that both names are either a single letter, or 
a single letter followed by a letter or a digit. 
The names may have more than two letters or digits, 
but only the first two are significant.
Names may not clash with BASIC keywords (like `SIN` or `ST`).

The below program with long names prints 10.

```bas
10 DEF FN FUNC23(ARG)=ARG*2
20 PRINT FN FUNC23(5)
```

Function names are in a different name-space than variable names.
It is allowed to have a `DEF FN LG(X)` and at the same time have a float `LG`.
This is analogues to strings (`LG$`) and integers (`LG%`) having their 
own name space, distinct from floats. 
See also [Implementation](#implementation).


## Examples

The single [signature](#signature) is a severe restriction.
Still, there are several possibilities to make interesting functions.
We have tried to categorize the possibilities and to
list useful function definitions for each category.

- **Constant**  
  `DEF FN E(X)=2.71828183`  
  A function must have an argument, but the body does not need to use it.
  The example could also be done as variable `E=2.71828183`, 
  but the function approach is a bit more robust against overwrites.

- **Simple operators**  
  `DEF FN HEIGHT(SEC)=300-9.82*SEC*SEC/2`  
  `DEF FN SQ(x)=x↑2`  
  `DEF FN EVEN(X)=(X AND 1)=0`  
  A function body can use all built-in operators (`+`, `-`, `*`, `/`, `↑`) and 
  also the relational operators (`=`, `<`, `>`, `<=`, `>=`, `<>`).
  For the latter, see example `EVEN()`. 
  Note that relational operators return a number (0 for false, and -1 for true) 
  so that fits with the mandatory float-to-float signature.

- **Built-in numeric functions**  
  `DEF FN SN(A)=SIN(Π*A/180)`  
  `DEF FN LG(X)=LOG(X)/LOG(10)`  
  `DEF FN HI(B)=INT(B/16)`  
  `DEF FN LO(B)=B AND 15`  
  A function body can use the built-in functions (even multiple in one body) 
  like `ABS()`, `ATN()`, `COS()`, `EXP()`, `INT()`, `LOG()`, 
  `SGN()`, `SIN()`, `SQR()`, and `TAN()`; 
  and also logical operators (`AND`, `OR`, `NOT`) and the constant pi.

- **Built-in string functions**  
  `DEF FN NUMDIG(X)=LEN(STR(X)-1)`  
  It is counter intuitive, given the restriction of only supporting 
  float-to-float signature, but string functions are allowed in a function 
  body. The only catch, the top-level expression must return a float.
  So a string must be made numeric with e.g. `VAL()`, `LEN()`, or `ASC()`.

- **Built-in system functions**  
  `DEF FN FR(X)=FRE(0)-65535*(FRE(0)<0)`  
  `DEF FN DK(A)=PEEK(A)+256*PEEK(A+1)`  
  `DEF FN DICE(N)=1+INT(RND(1)*N)`  
  Also the non-mathematical functions (`FRE()`, `PEEK()`, `RND()`, `USR()`) 
  are allowed in a function body.
  The function `USR()` could even have (programmed) side effects.

- **System variables**   
  `DEF FN TM(X)=TI/60`  
  `DEF FN HMS(X)=VAL(TI$)`  
  The system variables `TI` and `TI$` are allowed in a function body.
  Of course `TI$` would need to be converted (`MID$`, `VAL`) to a float.
  The third system variable, `ST` (I/O status), is also supported, 
  see below example.
  
  ```bas
  100 DEF FN S(X)=ST
  110 OPEN 15,8,15
  120 INPUT#15,EN
  130 PRINT ST;FNS(0)
  140 CLOSE 15
  ```

- **Other user functions**  
  A function body may also call other user functions.  
  Note that in `DEF FNF(X)= ...FNG(X)...`
  
  - `FNG()` does not need to exist when `FNF()` is _defined_ (function binding is by lookup on name during call).
  - `FNG()` must have been defined when `FNF()` is _called_.
  - The definition shall not be circular: `FNG()` shall not call 
    (directly or indirectly) function `FNF()` 
    because this leads to infinite recursion.
    
  An example, which converts bytes to hex, using nested functions 
  (`H(B)` and `L(B)` both call `A(D)`):
  
  ```bas
  100 DEF FN H(B)=FNA(INT(B/16))
  110 DEF FN L(B)=FNA(B AND 15)
  120 DEF FN A(D)=48+D-7*(D>9):REM CONVERT 0..15 TO ASCII
  130 FOR X=12 TO 20
  140 :PRINT X;"=$";CHR$(FNH(X));CHR$(FNL(X))
  150 NEXT
  
  RUN
   12 =$0C
   13 =$0D
   14 =$0E
   15 =$0F
   16 =$10
   17 =$11
   18 =$12
   19 =$13
   20 =$14
  ```  

  It is not only allowed to nest function definitions, it is also allowed to 
  nest function calls; see third expression below.
  
  ```bas
  PRINT FNA(0);FNA(10);FNL(FNA(10))
   48  65  49
  ```

  `FNA(D)` returns the ASCII code of the hex number passed as argument.
  Number 0 has ASCII code 48. Number 10 ($A) has ASCII code 65.
  `FNL(B)` returns the ASCII code of the low nibble of its argument. 
  For argument 65 ($41), the low nibble is 1, which has ASCII code 49.
  
- **Global variables**  
  `A=2 : DEF FN F(X)=X+A`  
  A very powerful mechanism is that function bodies have access to 
  global variables. 
  
  Again,
  
  - `A` does not need to exist when `FNF()` is _defined_ (variable binding is by lookup on name during call).
  - `A` must have been defined when `FNF()` is _called_.
  - In a next call to `FNF()`, the value of `A` is again looked-up, so if 
    `A` is changed the new value will be picked up.

  Find below an example, which peeks character codes or color indices 
  from row `Y` on the screen, `Y` being a global variable. The column 
  `X` is passed as argument.
  
  ```bas
  100 A0= 1024:REM ADDRESS FOR CHAR MEM
  110 A1=55296:REM ADDRESS FOR COLOR MEM
  120 :
  130 FOR I=0 TO 3*40-1
  140 :POKE A0+I,I:POKE A1+I,14
  150 NEXT I
  160 :
  170 DEF FN CHR(X)=PEEK(A0+Y*40+X)
  180 DEF FN COL(X)=PEEK(A1+Y*40+X)AND15
  190 :
  200 Y=2:FOR X=5 TO 9
  210 :PRINT X;FNCHR(X);FNCOL(X)
  220 NEXT X
  RUN
   5  85  14
   6  86  14
   7  87  14
   8  88  14
   9  89  14
  ```

Now that we have seen that there are several possibilities to make 
interesting functions, let's turn to constructions that are _not_ 
allowed in a function body.

- **Print modifiers**  
  Some built-in functions are not functions but rather modifiers that 
  only work in `PRINT` context: `TAB()` and `SPC()`. Those can not 
  be used in a function body.
  The `POS(0)` is not bound to `PRINT`, it is allowed in a function body.

- **Statements**  
  The function body must be an _expression_, not a statement. 
  In other words, `IF` or `FOR` is not allowed.
  
  Note that BASIC does have the `IF` expression mechanism: every 
  relational operator returns 0 for false or -1 for true and that can 
  be used in subsequent expressions.
  
  In below example function `FNA3()` clips values smaller than 3, and
  `FNB6()` clips values greater than 6. This does require a bit of 
  expression magic.
  
  ```bas
  100 DEF FNA3(X)=-(X>=3)*X-3*(X<3)
  110 DEF FNB6(X)=-(X<=6)*X-6*(X>6)
  120 :
  130 FOR X=0 TO 9
  140 :PRINT X,FNA3(X),FNB6(X)
  150 NEXT
  RUN
   0         3         0
   1         3         1
   2         3         2
   3         3         3
   4         4         4
   5         5         5
   6         6         6
   7         7         6
   8         8         6
   9         9         6
  ```  
  
- **Self**  
  The body of a function can not include itself.
  Since every operand is always evaluated in BASIC, this would lead 
  to infinite recursion and thus memory overflow.
  ```BAS
  100 DEF FN FAC(N)=N*FNFAC(N-1)
  110 PRINT FNFAC(5)
  RUN
  ?OUT OF MEMORY  ERROR IN 110
  ```
  
  If BASIC would have short circuit evaluation, like skipping evaluation of
  expression `<expr>` in `0*<expr>`, we would have had recursion.


## Implementation

The decision made for BASIC was that functions are stored in the same way 
as variables. All (scalar, i.e. non-array) variables are stored in a 7 byte
block between VARTAB and ARYTAB. These are two pointers, maintained by BASIC,
and stored at 43/44 ($2D/$2E) respectively 45/46 ($2F/$30).

As _Mapping the Commodore 64_ [explains](https://archive.org/details/Compute_s_Mapping_the_Commodore_64/page/n27/mode/2up) 

> Seven bytes of memory are allocated for each variable. The first two bytes are used for the variable name ... 
> The seventh bit of one or both of these bytes can be set ... 
> This indicates the variable type ... floating point ... string ... function (FN) ... integer.
> The use of the other five bytes depends on the type of variable. 

> A floating point variable will use the five bytes to store the value of the variable in floating point format. 

> An integer will have its value stored in the third and fourth bytes, high byte first, and the other three will be unused.

> A string variable will use the third byte for its length, and the fourth and fifth bytes for a pointer to the address of the string text, leaving the last two bytes unused. Note that the actual string text that is pointed to is located either in the part of the BASIC program ... or heap [maarten]

> A function definition will use the third and fourth bytes for a pointer to the address in the BASIC program text where the function definition starts. It uses the fifth and sixth bytes for a pointer to the dependent variable (the X of FN A(X)). The final byte is not used.

Armed with this knowledge, let's make a dump of the variable storage.
For testing, we begin with creating a variable of each of the four types.
Next comes the dump routine.

```bas
100 FL=65536
110 S$="123"
120 I%=34*256+199
130 DEF FNF3(X)=789+X
140 :
200 T$(0)="FLOAT":T$(1)="FN()"
210 T$(2)="STRING":T$(3)="INT"
220 B=0:FOR A=PEEK(45)+256*PEEK(46) TO PEEK(47)+256*PEEK(48)-1 STEP 7
230 PRINT CHR$(PEEK(A) AND 127);
240 PRINT CHR$(PEEK(A+1) AND 127);TAB(3);
250 PRINT T$(INT(PEEK(A)/128)+2*INT(PEEK(A+1)/128));TAB(9);
260 FOR B=A+2 TO A+6:PRINT PEEK(B);:NEXT:PRINT
270 NEXT A
```

This is the output, which matches nicely the description 
in _Mapping the Commodore 64_. 

```bas
FL FLOAT  145  0  0  0  0
S  STRING 3  22  8  0  0
I  INT    34  199  0  0  0
F3 FN()   58  8  84  9  55
X  FLOAT  0  0  0  0  0
B  FLOAT  140  21  208  0  0
A  FLOAT  140  22  0  0  0
```

- For the five content bytes of `FL` see 
  [c64usr](https://github.com/maarten-pennings/howto/tree/main/c64usr#comparison).
- For the five content bytes of `S` note that the string is indeed 3 
  characters long (`"123"`), and that it is a literal in the BASIC program. 
  BASIC starts at $0800, so address 8/22 for `123` makes sense. 
- The integer `I` was assigned `34*256+199`, the dump shows both 34 and 199 
  (in the unusual high-byte/low-byte order). 
- Finally we see `FNF3()`. Again, the body is in the BASIC text, so address 
  8/58 seems plausible, and 9/84 referring to `X` seems also plausible.
  We do a quick test to disclose the function body. Note that 170 is the 
  [token](https://sta.c64.org/cbm64basins2.html) for `+`.
  ```
  FOR A=8*256+58 TO A+4:PRINT CHR$(PEEK(A));:NEXT
  789JX
  FOR A=8*256+58 TO A+4:PRINT PEEK(A);:NEXT
  55  56  57  170  88
  ```

One thing is remarkable: the program is _not_ using the variable `X`.
`X` is only used as parameter of `FNF()`. 
Still `X` occurs in the variable dump.
My suspicion is that when computing `FNF(444)`, the BASIC interpreter 
assigns `444` to `X`, and then simply calls the evaluator on the body,
here `789+X`. Variable `X` must exist for this scheme to work.

What is also worth noting, is that functions are relatively dynamic; they 
are stored like variable. This means it is easy to change them. 
The following is an a-typical (kind wording for ridiculous) implementation 
of [Collatz](https://en.wikipedia.org/wiki/Collatz_conjecture)
using dynamically switching functions.

```bas
100 REM COLLATZ
110 X=30
120 IF X=1 THEN END
130 IF(X AND 1)=0 THEN DEF FNF(X)=X/2
140 IF(X AND 1)=1 THEN DEF FNF(X)=3*X+1
150 X=FNF(X):PRINT X;
160 GOTO 120
RUN
 15  46  23  70  35  106  53  160  80  40  20  10  5  16  8  4  2  1
```


## Execution architecture

Assume we have a function definition for `F` using argument X,

```bas
  DEF FN F(X) = <expression in X>
```

and a function call of `F`.

```bas
  PRINT FN F( <other expression> )
```

My guess of what is actually executed by the BASIC interpreter is

```bas
  X= <other expression>
  PRINT <expression in X>
```

But as the following code shows, it is a bit more subtle.

```
110 X=123
100 DEF FN F(X)=X*2
120 PRINT FN F(2+3)
130 PRINT X
RUN
 10
 123
```

We see that (2+3)*2 is correctly computed,
but we also see that `X` is still `123` after evaluating `F`.

My new guess therefore is 

```bas
  PUSH(X)
  X= <other expression>
  PRINT <expression in X>
  POP(X)
```

This time _Mapping the Commodore 64_ seems [wrong](https://archive.org/details/Compute_s_Mapping_the_Commodore_64/page/n61/mode/2up).
It seems to describe a stack frame for `DEF`, not for a call, and it suggests a frame of 5 bytes.
As we shall see the C64-wiki is much closer with its 16 byte stack frame).

How do we snapshot the stack in the middle of calling a function?

We misused the `USR()` function.
When calling `USR( <expr> )` in basic this is what happens.

- `<expr>` is evaluated, and resulting value stored in the so-called floating point accumulator 
  [FAC1](https://archive.org/details/Compute_s_Mapping_the_Commodore_64/page/n35/mode/2up)
  at addresses 97-102.

- The BASIC interpreter then calls a user defined machine language routine, vectored through 
  [USRADD](https://archive.org/details/Compute_s_Mapping_the_Commodore_64/page/n85/mode/2up)
  at address 785,786
  
- That routine is "supposed" to use FAC1, compute something, leave the result again in FAC1,
  and `RTS` back to the basic interpreter.
  
- The BASIC interpreter picks up the value returned by `USR()` in FAC1 and continues with that.

We have written a machine language routine that receives a value in FAC1, does not 
look at it, makes a snapshot of the entire stack (all 256 bytes), then returns.
BASIC sees the same value come out as was passed in.

We decided to store the machine language routine at $C000 (49152).
We decided to store the stack snapshot (all 256 bytes) at $C100 .. $C200.

This is the routine we wrote, a simple one-page copy loop using POWERMON.

```asm
    *** POWERMON 2.0 ***

  PC  CR NV-BDIZC AC XR YR SP
;90E7 37 10110000 83 04 7A FA
*C000.A2 00    LDX #$00
*C002.BD 00 01 LDA $0100,X
*C005.9D 00 C1 STA $C100,X
*C008.CA       DEX
*C009.D0 F7    BNE $C002
*C00B.60       RTS
```

We converted this to decimal.

```BAS
FOR A=49152 TO A+11:PRINT PEEK(A);:NEXT
 162  0  189  0  1  157  0  193  202  208  247  96
```

And wrote the following BASIC program.

```bas
100 FORA=49152TOA+11:READD:POKEA,D:NEXT
110 DATA162,0,189,0,1,157,0
120 DATA193,202,208,247,96
130 POKE785,0:POKE 786,192
140 :
150 DEFFNID(X)=USR(X)
160 DEFFNSQ(X)=FNID(X*X)
170 DEFFNP2(X)=FNSQ(X)+X+1
180 X=1:PRINTFNP2(2):END
```

Lines 100-120 place the `USR()` implementation at 49152.
Line 130 write the vector for `USR()` to point to the implementation.
Lines 150-170 contain 3 nested functions. Function `P2(X)` computes 
a simple polynomial of degree 2 (x²+x+1). It uses function `SQ(X)` computes 
the square if `X`, but also calls the identity function, which is implemented
by calling our stack snapshot routine.

When we run this program we get the expected outcome.

```bas
run
 7
```

We also print three pointers: start of BASIC program (2049 or $0801),
end of BASIC program and start of variables (2234 or $08BA), and 
end of variables (2276, $08E4).

```bas
PRINT PEEK(43)+256*PEEK(44)
 2049
PRINT PEEK(45)+256*PEEK(46)
 2234
PRINT PEEK(47)+256*PEEK(48)
 2276
```

We used POWERMON to dump the BASIC program and variables.
The below listing is annotated with `*` to denote the begin and end 
of the two areas (BASIC program and variables). The symbol `/` 
separates BASIC lines respectively variables.

```txt
:0800 00*1D 08 64 00 81 41 B2  ...D..aR
:0808 34 39 31 35 32 A4 41 AA  49152DaJ
:0810 31 31 3A 87 44 3A 97 41  11:.d:.a
:0818 2C 44 3A 82/00 36 08 6E  ,d:..6.N
:0820 00 83 31 36 32 2C 30 2C  ..162,0,
:0828 31 38 39 2C 30 2C 31 2C  189,0,1,
:0830 31 35 37 2C 30 00/4E 08  157,0.n.
:0838 78 00 83 31 39 33 2C 32  X..193,2
:0840 30 32 2C 32 30 38 2C 32  02,208,2
:0848 34 37 2C 39 36 00/63 08  47,96.C.
:0850 82 00 97 37 38 35 2C 30  ...785,0
:0858 3A 97 20 37 38 36 2C 31  :. 786,1
:0860 39 32 00/69 08 8C 00 3A  92.I...:
:0868 00/7A 08 96 00 96 A5 49  .Z....Ei
:0870 44 28 58 29 B2 B7 28 58  d(x)RW(x
:0878 29 00/8F 08 A0 00 96 A5  )......E
:0880 53 51 28 58 29 B2 A5 49  sq(x)REi
:0888 44 28 58 AC 58 29 00/A6  d(xLx).F
:0890 08 AA 00 96 A5 50 32 28  .J..Ep2(
:0898 58 29 B2 A5 53 51 28 58  x)REsq(x
:08A0 29 AA 58 AA 31 00/B8 08  )JxJ1.X.
:08A8 B4 00 58 B2 31 3A 99 A5  T.xR1:.E
:08B0 50 32 28 32 29 3A 80 00  p2(2):..
:08B8/00 00*41 00 90 40 0C 00  ..a..@..
:08C0 00/44 00 87 40 00 00 00  .d..@...
:08C8/C9 44 75 08 D1 08 B7/58  IdU.Q.Wx
:08D0 00 81 00 00 00 00/D3 51  ......Sq
:08D8 86 08 D1 08 A5/D0 32 9B  ..Q.EP2.
:08E0 08 D1 08 A5*4D 00 00 00  .Q.Em...
```

Even with the `*` and `/` annotation this is quite hard to read.
So we reordered the data, per line and per variable, and annotated the bytes.
We skipped the first half of the program.

```txt
      LINK  140   :
:0863 69 08 8C 00 3A 00
      LINK  150   DEFFN I  D  (  X  )  =  USR(  X  )       
:0869 7A 08 96 00 96 A5 49 44 28 58 29 B2 B7 28 58 29 00
      LINK  160   DEFFN S  Q  (  X  )  =  FN I  D  (  X  *  X  )
:087A 8F 08 A0 00 96 A5 53 51 28 58 29 B2 A5 49 44 28 58 AC 58 29 00
      LINK  170   DEFFN P  2  (  X  )  =  FN S  Q  (  X  )  +  X  +  1
:088F A6 08 AA 00 96 A5 50 32 28 58 29 B2 A5 53 51 28 58 29 AA 58 AA 31 00
      LINK  180   X  =  1  :  PR FN P  2  (  2  )  :  END
:08A6 B8 08 B4 00 58 B2 31 3A 99 A5 50 32 28 32 29 3A 80 00
      LINK
:08B8 00 00
      A  _ 
:08B8 41 00 90 40 0C 00 00
      D  _
:08C1 44 00 87 40 00 00 00
      I  D
:08C8 C9 44 75 08 D1 08 B7
      X
:08CF 58 00 81 00 00 00 00
      S  Q
:08D6 D3 51 86 08 D1 08 A5
      P  2
:08DD D0 32 9B 08 D1 08 A5
```

Important to Note
- At $08B5, we see $3A or `:`, which terminates the call to `FNP2(2)`.
- At $08A1, we see $AA or `+`, which terminates the call to `FNSQ(X)`.
- At $088E, we see $00 (line terminator), which terminates the call to `FNID(X)`.
- $08D1 is between 58 00, the name of variable `X`, and 81 00 00 00 00, the value of variable `X`, in floating point format.

Recall that a number like 2 is first written in binary: 10.00000000 00000000 00000000 000000.
Then it is normalized (decimal point moved to the left just after the first 1), adding a binary exponent: 1.00000000 00000000 00000000 0000000 E 00000001.
In the storage format, the leading 1 is dropped, and the exponent gets $81 added (to handle negative exponents): 00000000 00000000 00000000 00000000 E 10000010.
Finally, the exponent moves to the front: 10000010 00000000 00000000 00000000 00000000.
In other words, 2 is encoded as 82 00 00 00 00.
Likewise 1 is encoded as 81 00 00 00 00.

Next step is to use POWERMON to dump the snapshot of the stack.
We dumped the top half, we leaft out the bottom half, since it was empty.

```txt
:C180 00 00 FD FF FF FF 00 00  .........
:C188 00 00 FF FF FF FF 00 00  .........
:C190 00 00 FE FF FF FF 00 00  .........
:C198 00 00 FF FF FF FF 00 00  .........
:C1A0 00 00 FF FF FF FF 00 00  .........
:C1A8 00 00 FF FF FF FF 00 00  .........
:C1B0 00 00 7D EA 7D EA 01 58  ....J.J.x
:C1B8 80 A0 BD BB BA AD 00 F6  .....ZM.V
:C1C0 AE D3 E2 AF/B3 AD 00 8C  .NSBOSM..
:C1C8 AD 3A B4 D1 08 8E 08 82  .M:TQ....
:C1D0 00 00 00 00/B3 AD 00 8C  .....SM..
:C1D8 AD 3A B4 D1 08 A1 08 82  .M:TQ.A..
:C1E0 00 00 00 00/B3 AD 00 8C  .....SM..
:C1E8 AD 3A B4 D1 08 B5 08 81  .M:TQ.U..
:C1F0 00 00 00 00/B3 AD 00 B7  .....SM.W
:C1F8 AA E9 A7 A4 01 01 B4 00  .JIGD..T.
```

Note that the stack grows "down" from $200.
In our snapshot it means it grows down from $C200.
Since the memory dump is low to high, the stack in the dump grows up.

We can not explain the top 12 bytes (B3 AD 00 B7 AA E9 A7 A4 01 01 B4 00).
Leaving those out, and then reordering to get frames of 16 bytes gives this.

```txt
   ret  | 00 |  ret  |  ret  | @ arg | basic | 
  B3 AD | 00 | 8C AD | 3A B4 | D1 08 | 8E 08 | 82 00 00 00 00
  B3 AD | 00 | 8C AD | 3A B4 | D1 08 | A1 08 | 82 00 00 00 00
  B3 AD | 00 | 8C AD | 3A B4 | D1 08 | B5 08 | 81 00 00 00 00
```

Why 16 bytes; that is what the [C64-wiki](https://www.c64-wiki.com/wiki/FN) suggests.

> Calling a FN function consumes 16 bytes on the BASIC stack. These consists of
> - float value (in variable encoding) of the argument (5 bytes) (in order mantissa bytes 4, 3, 2, 1 followed by the exponent byte)
> - address of the position pointing to BASIC text right after the bracket (2 bytes)
> - pointer to the value of the of the argument variable (2 bytes)
> - return address $B43A=(180, 58) from call JSR $AD8A - Confirm Result (2 bytes)
> - return address $AD8C=(173, 140) from call JSR $AD9E - Evaluate Expression in Text (2 bytes)
> - zero byte from $ADAB (1 byte)
> - return address $ADB1=(173, 177) from all JSR $AE83 Evaluate Single Term (2 bytes)

There is only one mismatch, C64 wiki says that the last push is ADB1, and that appears to be ADB3 
in out case (slightly different ROM version)?

We see
- all the constants as C64 wiki explains;
- the ref the the value of `X` at $08D1;
- the pointer to after the closing bracket at respectively $08B5, $08A1, $088E;
- and the pushed value of X, namely 1, 2, and 2 in floating point format (as explained above).


## Conclusions

- The signature (one float to float) is too restrictive.
  Allowing multiple input parameters would have been great.
  Allowing string output would have been good (allowing `FNHEX$()`).
  Allowing string input would have been nice.
  
- The function body being just one expression (on one line)
  is very restrictive (no for, no if).
  
- There is no "short-circuit evaluation" in BASIC.
  As a result all sub-expressions are always evaluated,
  so that it is not possible to write a recursive function.

Although the `FNF()` mechanism was kept simple, the implementation seems 
quite elaborate looking at the stack frames. 
For me, cost and gain of this feature is out of balance.

I believe most BASIC programmers see functions as a "rarely used feature".

(end)

