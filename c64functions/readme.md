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

As _Mapping the Commodore 64_ [explains](https://archive.org/details/Compute_s_Mapping_the_Commodore_64/page/n27/mode/2up?page=15) 

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
120 I%=34*256+17
130 DEF FNF(X)=789+X
140 :
200 T$(0)="FLOAT":T$(1)="FN()"
210 T$(2)="STRING":T$(3)="INT"
220 B=0:FOR A=PEEK(45)+256*PEEK(46) TO P
EEK(47)+256*PEEK(48)-1 STEP 7
230 PRINT CHR$(PEEK(A)AND127);
240 PRINT CHR$(PEEK(A+1)AND127);TAB(3);
250 PRINT T$(INT(PEEK(A)/128)+2*INT(PEEK(A+1)/128));TAB(9);
260 FOR B=A+2 TO A+6:PRINTPEEK(B);:NEXT
270 PRINT:NEXT A
```

This is the output, which matches nicely the description 
in _Mapping the Commodore 64_. 

```bas
FL FLOAT  145  0  0  0  0
S  STRING 3  22  8  0  0
I  INT    34  17  0  0  0
F  FN()   56  8  118  9  55
X  FLOAT  0  0  0  0  0
B  FLOAT  140  23  240  0  0
A  FLOAT  140  24  32  0  0
```

- For the five content bytes of `FL` see 
  [c64usr](https://github.com/maarten-pennings/howto/tree/main/c64usr#comparison).
- For the five content bytes of `S` note that the string is indeed 3 
  characters long (`"123"`), and that it is a literal in the BASIC program. 
  BASIC starts at $0800, so address 8/22 for `123` makes sense. 
- The integer `I` was assigned `34*256+17`, the dump shows both 34 and 17 
  (in the unusual high-byte/low-byte order). 
- Finally we see `FNF()`. Again, the body is in the BASIC text, so address 
  8/56 seems plausible, and 9/118 referring to `X` seems also plausible.
  We do a quick test to disclose the function body. Note that 170 is the 
  [token](https://sta.c64.org/cbm64basins2.html) for `+`.
  ```
  FOR A=8*256+56 TO A+4:PRINT CHR$(PEEK(A));:NEXT
  789JX
  FOR A=8*256+56 TO A+4:PRINT PEEK(A);:NEXT
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

Although the `FNF()` mechanism is kept simple, the implementation seems 
quite elaborate, for example with stack frames that back-up and restore 
the value of the function parameter. 
For me, cost and gain of this feature is out of balance.

I believe most BASIC programmers see functions as a "rarely used feature".

(end)


