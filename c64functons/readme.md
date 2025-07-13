# C64 functions FNF(x)

In this article we look at _functions_ in Commodore 64 BASIC.

In the context of this article the stabd-alone term "function" 
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
110 DEF FN F(X)=12      <<< only correct one
120 DEF FN F(X,Y)=12
130 DEF FN F(X%)=12
140 DEF FN F$(X)="12"
150 DEF FN F(X$)=12
```

Of the above definitions, only the one on line 110 fits the supported 
signature. All other definitions give an error: `syntax  error` for 
lines 100, 120, 130, and `type mismatch  error` for 140 and 150.

It is surprising to see two different kind of errors, and I would
have expected that 130 gives the same error as 150.


## Naming

The `FN` part in front of the function name is mandatory.
But the name of the function does not have to be `F`.
Similarly the name of the argument does not have to be `X`.
Both can be any name that BASIC allows for a floating point. 

This means that both names are either a single letter, or 
a single letter followed by a letter or a digit. 
The names may have more letters or digits, but only the first two are significant.
Names may not clash with BASIC keywords.

The below program prints 10.

```bas
10 DEF FN FUNC23(ARG)=ARG*2
20 PRINT FN FUNC23(5)
```

Function names are in a different name-space than variable names.
You can have a `DEF FN LG(X)` and at the same time have a float `LG`.
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
  but the function approach is a more robust against overwrites.

- **Simple operators**  
  `DEF FN HEIGHT(SEC)=300-9.82*SEC*SEC/2`  
  `DEF FN SQ(x)=x^2`  
  A function body can use all built-in operators (`+`, `-`, `*`, `/`, `^`) and also 
  the relational operators (`=`, `<`, `>`, `<=`, `>=`, `<>`).

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
  It is counter intuitive (given the restriction of only supporting 
  float-to-float signature), but string functions are allowed in a function 
  body. The only catch, the top-level expression must return a float.
  So a string must be made numeric with e.g. `VAL()`, `LEN()`, or `ASC()`.

- **Built-in system functions**  
  `DEF FN FR(X)=FRE(0)-65535*(FRE(0)<0)`  
  `DEF FN DK(A)=PEEK(A)+256*PEEK(A+1)`  
  `DEF FN DICE(N)=1+INT(RND(1)*N)`  
  Also the non-mathematical functions (`FRE()`, `PEEK()`, `RND()`, `USR()`) 
  are allowed in a function body.
  The function `USR()` could have (programmed) side effects.

- **System variables**   
  `DEF FN TM(X)=TI/60`  
  `DEF FN HMS(X)=VAL(TI$)`  
  The system variables `TI` and `TI$` are allowed in a function body.
  Of course `TI$` would need to be converted (`MID$`, `VAL`) to a float.
  The third system variable, `ST`, is also supported, see below example.
  ```bas
  100 DEF FN S(X)=ST
  110 OPEN 15,8,15
  120 INPUT#15,EN
  130 PRINT ST;FNS(0)
  140 CLOSE 15
  ```

- **Other user functions**  
  A function body may call other user functions.  
  Note that in `DEF FNF(X)= ...FNG(X)...`
  
  - `FNG()` does not need to exist when `FNF()` is _defined_ (function binding is by lookup on name during call).
  - `FNG()` must have been defined when `FNF()` is _called_.
  - The definition shall not be circular: `FNG()` shall not call `FNF()` 
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

- **Global variables**  
  `A=2 : DEF FN F(X)=X+A`  
  A very powerful mechanism is that function bodies have access to 
  global variables. 
  
  Again,
  
  - `A` does not need to exist when `FNF()` is _defined_ (variable binding is by lookup on name during call).
  - `A` must have been defined when `FNF()` is _called_.
  - In a next call to `FNF()`, the value of `A` is again looked-up, so if 
    `A` is changed the new value will be picked up.

  An example, that peeks character codes or color from row `Y` on the screen. 
  
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

Some constructions are _not_ allowed in a function body.

- **Print modifiers**  
  Some built-in functions are not functions but rather modifiers that 
  only work in `PRINT` context: `TAB(0)` and `SPC(0)`. Those can not 
  be used in a function body.
  The `POS(0)` is not bound to `PRINT`, it is allowed in a function body.

- **Statements**  
  The function body must be an _expression_, not a statement. 
  In other words, `IF` or `FOR` is not allowed.
  
  Note that BASIC does have the `IF` expression mechanism: every 
  relation operator returns 0 for false or -1 for true and that can 
  be used is subsequent expressions.
  
  ```bas
  100 DEF FNCLIP0(X)= (X>=0)*X
  110 DEF FNKLIP01(X)= (X>=0)*X-(X>1)*X
  120 :
  130 FOR X=-1 TO +2 STEP 0.25
  140 :PRINT X,FNCLIP0(X),FNKLIP01(X)
  150 NEXT
  READY.
  RUN
  -1         0         0
  -.75       0         0
  -.5        0         0
  -.25       0         0
   0         0         0
   .25      -.25      -.25
   .5       -.5       -.5
   .75      -.75      -.75
   1        -1        -1
   1.25     -1.25      0
   1.5      -1.5       0
   1.75     -1.75      0
   2        -2         0
  ```  
  
- **Self**  
  The body of a function can not include itself.
  Since every operand is always evaluated, this would lead 
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

TODO

as a variable between VARTAB and ARYTAB

dynamic object: can overwrite function



## Execution architecture

TODO

stack frames (x saved)


## Conclusions

- Signature (one float to float) is too restrictive.
  Allowing multiple input parameters would have been great.
  Allowing string output would have been good (making `FNHEX$()`).
  Allowing string input would have been nice.
  
- The function body being just one expression (on one line)
  is very restrictive.
  
- There is no "short-circuit evaluation" in BASIC.
  As a result all sub-expressions are always evaluated,
  so that it is not possible to write a recursive function.

The implementation seems quite elaborate, for example with stack frames
that back-up and restore the value of the function parameter. 
Cost and gain of this feature is out of balance.

I believe most BASIC programmers see functions as a "rarely used feature".

(end)


