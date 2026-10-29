[![MCC](https://github.com/maarten-pennings/C64howto/blob/main/MCC/mcc240x160.png)](https://github.com/maarten-pennings/C64howto/tree/main/MCC#overview)

Maarten Pennings MCC#07


# Functions in BASIC

In dit artikel bekijken we _functies_ in Commodore 64 BASIC.

Met _functie_ bedoelen we hier `FN F(X)`, niet subroutines (`GOSUB`), 
en ook niet de ingebouwde functies (zoals `SIN(X)`).


## Introduction

Functies in C64 BASIC gebruiken het keywoord `FN`.

Om een functie `F` _aan te roepen_ met argument `3`, schrijven we `FN F(3)`.

Voor we een functie kunnen aanroepen moet hij _gedefinieerd_ zijn.
Daarvoor hebben we een tweede keywoord nodig `DEF`.
Een functie definitie zou er zo uit kunnen zien `DEF FN F(X)= X*2`.

Functie definities moeten in een programma staan.
Zonder regel nummer krijgen we de foutmelding `?ILLEGAL DIRECT  ERROR`.
Dat is logisch omdat de code ("_body_") van de functie (in ons voorbeeld `X*2`) 
persistent bewaard moet worden, zodat hij uitgevoerd kan worden.
Eenmaal gedefinieerd zijn aanroepen in directe mode toegestaan.

Zoals altijd zijn spaties rond keywoorden optioneel.
De volgende twee fragmenten zijn dus gelijk.
De eerste is leesbaarder, de tweede wat korter en iets sneller.

```basic 
100 DEF FN F(X)= X*2
110 PRINT FN F(3)
```

```basic
100 DEFFNF(X)=X*2
110 PRINTFNF(3)
```


## Signatuur

Een van de grootste beperkingen van functies in BASIC is dat er maar één signatuur 
wordt ondersteund. De signatuur van een functie bepaalt de invoer en uitvoer van een functie;
het omvat het aantal, type en volgorde van de functie argumenten als ook het type van de uitvoer. 

De enige functie signatuur in C64 BASIC is float naar float 
("float" staat voor gebroken getallen, het type van een variabele zoals `A`).

```basic
100 DEF FN F()= 12       | geen argument
110 DEF FN F(X)= 12      | ENIGE GOEDE SIGNATUUR IN HET LIJSTJE
120 DEF FN F(X,Y)= 12    | meer dan één argument
130 DEF FN F(X%)= 12     | argument verkeerd type (integer)
140 DEF FN F$(X)= "12"   | uitvoer verkeerd type (string)
150 DEF FN F(X$)= 12     | argument verkeerd type (string)
```

Van de functie definities hierboven heeft er maar een de goede signatuur, die op regel 110.
Alle andere geven een foutmelding `syntax  error` (for regels 100, 120, 130), 
of `type mismatch  error` (voor regels 140 en 150). Opmerkelijk dat er verschillende 
foutmelding komen, helemaal voor 130 en 150.


## Naamgeving

De `FN` voor de functie naam is verplicht.
Maar de functienaam zelf hoeft niet `F` te zijn.
Ook de het functie argument hoeft niet `X` te zijn.
Beide kunnen een naam hebben die is toegestaan voor een variabele in BASIC.

Beide namen bestaan dus uit een losse letter, of een letter gevolgd 
door een letter of een cijfer. Namen mogen langer zijn, 
maar alleen de eerste twee karakters tellen.
Namen mogen geen BASIC keywoord bevatten (zoals `ST`).

Hieronder een voorbeeld met lange namen.

```basic
10 DEF FN MY1FUNC(ARG)= ARG*2
20 PRINT FN MY1FUNC(5)
```

Functie namen zitten in een andere _name-space_ dan variabele namen.
Het is toegestaan om een functie `DEF FN LG(X)` te hebben naast een  float variabele `LG`.
Dit is hetzelfde mechanisme dat strings (`LG$`) en integers (`LG%`) een 
eigen _name space_ hebben naast floats. 



## Voorbeelden

De float-naar-float signatuur is een zware beperking.
Toch zijn er nog best wat interessante mogelijkheden voor functies
Hieronder staan voorbeelden uitgesplitst in categorieën.

- **Constanten**  
  `DEF FN E(X)= 2.71828183`  
  Een functie moet een argument hebben, maar die hoeft niet gebruikt te worden in de _body_.
  Het voorbeeld had natuurlijk ook `E=2.71828183` kunnen zijn,
  maar de functie is iets moeilijker van waarde te veranderen.

- **Rekenkundige operatoren**  
  `DEF FN HEIGHT(SEC)= 300-9.82*SEC*SEC/2`  
  `DEF FN SQ(X)= X↑2`  
  Een functie _body_ mag alle BASIC operatoren gebruiken (`+`, `-`, `*`, `/`, `↑`).

- **Ingebouwde rekenkundige functies**  
  `DEF FN SN(A)= SIN(Π*A/180)`  
  `DEF FN LG(X)= LOG(X)/LOG(10)`  
  `DEF FN HI(B)= INT(B/16)`  
  `DEF FN LO(B)= B AND 15`  
  Een functie _body_ mag de ingebouwde functies gebruiken, zelfs meerdere keren in een body.
  Voorbeelden zijn `ABS()`, `ATN()`, `COS()`, `EXP()`, `INT()`, `LOG()`, `SGN()`, `SIN()`, `SQR()`, en `TAN()`.
  Andere voorbeelden zijn de logische operatoren (`AND`, `OR`, `NOT`) en de constante pi (`π`).
  Merk op dat de logische operatoren werken op twee floats en een float opleveren.

- **Relationele operatoren**  
  `DEF FN EVEN(X)= (X AND 1)=0`  
  `DEF FN RANGE(X)= (0<=X) AND (X<10)`  
  Er zijn verschillende relationele operatoren (`=`, `<`, `>`, `<=`, `>=`, `<>`).
  Die leveren ook een float op (0 voor _false_, en  `-1` voor _true_).

- **Ingebouwde string functies**  
  `DEF FN NUMDIG(X)= LEN(STR$(X))-1`  
  Het is onverwacht, gegeven de verplichte float-naar-float signatuur,
  maar string functies zijn toegestaan in een functie _body_.
  Maar, het return type moet nog steeds float zijn.
  We moeten de string dus nog numeriek maken, bijvoorbeeld met `VAL()`, `LEN()`, or `ASC()`.

- **Ingebouwde systeem functies**  
  `DEF FN FR(X)= FRE(0)-65535*(FRE(0)<0)`  
  `DEF FN DK(A)= PEEK(A)+256*PEEK(A+1)`  
  `DEF FN DICE(N)= 1+INT(RND(1)*N)`  
  Ook de niet wiskundige functies (`FRE()`, `PEEK()`, `RND()`, `POS()`, `USR()`) 
  zijn toegestaan in een functie _body_.
  De functie `USR()` kan zelfs zij-effecten hebben.

- **Systeem variablen**   
  `DEF FN TM(X)= TI/60`  
  `DEF FN HMS(X)= VAL(TI$)`  
  De systeem variabelen `TI` en `TI$` zijn toegestaan in een functie _body_.
  Natuurlijk moet `TI$` geconverteerd worden (`MID$`, `VAL`) naar float.
  De derde systeem variabele, `ST` (I/O status), is ook toegstaan, zie voorbeeld.
  
  ```basic
  100 DEF FN S(X)= ST
  110 OPEN 15,8,15
  120 INPUT#15,EN
  130 PRINT ST;FNS(0)
  140 CLOSE 15
  ```

- **Andere `FN` functies**  
  Een functie mag andere functies aanroepen.
  Dit zijn de regels voor `DEF FNF(X)= ...FNG(X)...`:
  
  - `FNG()` hoeft niet te bestaan als `FNF()` gedefinieerd wordt 
    (de functie wordt opgezocht bij aanroep).
  - `FNG()` moet bestaan als `FNF()` aangeroepen wordt.
  - De definitie mag niet circulair zijn:
    `FNG()` mag `FNF()` niet aanroepen (direct of indirect)
    want dit zou tot oneindige recursie leiden.
    
  Het volgende voorbeeld converteert bytes naar hex, gebruik 
  makend van geneste functies.
  `H(B)` levert de hoge nibble van `B` op en `L(B)` de lage nibble;
  beide roepen daarna `A(D)` aan. Die converteert een hexadecimaal 
  cijfer (0..15) naar ASCII. Helaas mogen we geen `A$(D)` maken.
  
  ```bas
  100 DEF FN H(B)= FNA(INT(B/16))
  110 DEF FN L(B)= FNA(B AND 15)
  120 DEF FN A(D)= 48+D-7*(D>9):REM CONVERT 0..15 TO ASCII
  130 FOR X=13 TO 19
  140 :PRINT X;"=$";CHR$(FNH(X));CHR$(FNL(X))
  150 NEXT
  
   13 =$0D
   14 =$0E
   15 =$0F
   16 =$10
   17 =$11
   18 =$12
   19 =$13
  ```  

  Niet alleen functie definities mogen genest worden, ook functie aanroepen. 
  De ASCII waarde van "cijfer" 10 (hex `A`) is 65.
  De low byte van 65 ($41) is 1, en de ASCII waarde daarvan is 49.
  
  ```bas
  PRINT FNA(10);FNL(FNA(10))
   65  49
  ```

- **Globale variabelen**  
  `A=2 : DEF FN F(X)= X+A`  
  Een erg krachtig mechanisme is dat een functie _body_ toegang heeft tot 
  alle globale variabelen. De regels zijn
  
  - `A` hoeft niet te bestaan als `FNF()` gedefinieerd wordt
    (de variabele wordt opgezocht bij aanroep).
  - `A` moet bestaan als `FNF()` aangeroepen wordt.

  Het voorbeeld hieronder `PEEK`-t de karakter code of de karakter kleur
  van het karakter op scherm positie `X`,`Y`. Hierbij is `X` het argument
  van de functie en `Y` een globale variabele.
  
  ```basic
  100 A0= 1024:REM ADDRESS FOR CHAR  MEM
  110 A1=55296:REM ADDRESS FOR COLOR MEM
  120 :
  130 FOR I=0 TO 3*40-1
  140 :POKE A0+I,I:POKE A1+I,14
  150 NEXT I
  160 :
  170 DEF FN CHR(X)= PEEK(A0+Y*40+X)
  180 DEF FN COL(X)= PEEK(A1+Y*40+X)AND15
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


## Verboden functie _ body_

Er zijn ook constructies niet toegstaan in een functie _body_ die we daar 
wel zouden kunnen verwachten.

- **Print helpers**  
  Sommige ingebouwde functies zijn eigenlijk geen functies 
  ze werken alleen in de context van `PRINT`; we hebben het over 
  `TAB()` en `SPC()`. De functie `POS(0)` staat los van `PRINT`, 
  die is wel toegestaan.

- **Statements**  
  Een functie _body_ moet een _expressie_ zijn, geen _statement_.
  Dus `IF` en `FOR` zijn niet toegestaan.

  Maar BASIC heeft wel een `IF` expressie mechansime:
  elke relationele operator levert 0 of -1 op, en dat gebruikt worden
  in de omliggende expressie.

  In het onderstaande voorbeeld, clipt `FNA3()` waardes kleiner dan 3, 
  en `FNB6()` clipt waardes groter dan 6.
  
  ```bas
  100 DEF FNA3(X)= -(X>=3)*X-3*(X<3)
  110 DEF FNB6(X)= -(X<=6)*X-6*(X>6)
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
  
- **Zelf**  
  Een functie _body_ mag niet naar zichzelf verwijzen.
  In C64 BASIC wordt elke functie altijd uitgevoerd - in sommige 
  talen wordt `F(3)` niet uitgevoerd in een expressie zoals `0*F(3)`.
  In C64 BASIC wel. Daarom leiden zulke expressie tot oneindige recursie 
  en dus een run-time error (stack overflow).

  ```BASIC
  100 DEF FN FAC(N)= N*FNFAC(N-1)
  110 PRINT FNFAC(5)
  RUN
  ?OUT OF MEMORY  ERROR IN 110
  ```
  

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
My suspicion is that when later computing `FNF(444)`, the BASIC interpreter 
wants to assign `444` to `X`, and then calls the evaluator on the body,
here `789+X`. Variable `X` must exist for this scheme to work.


## Dynamic behavior

Functions are relatively dynamic; they are stored like variables. 
This means it is easy to change them on the fly.
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

The next example of the dynamic behavior is a program that dynamically 
modifies itself ("self modifying code"). It defines function `F` on the 
first line (which we know starts at address 2048). 
Lines 200 to 250 increase address `A` by checking all tokens; when `A` 
hits the the `=` it is incremented one more time, pointing the the `4` of 
the body `42*x`.

The next two block modify that `4`, first in a `1`, then in a `3`, each time 
calling `F`.

```bas
LIST

100 DEF FN F(X)=42*X
110 :
200 A=2048+1+2+2:REM START+0+LINK+LINE
210 READ D:IF PEEK(A)<>D THEN STOP
220 IF D<>178 THEN A=A+1:GOTO 210
230 A=A+1:REM SKIP "="
240 REM  DEF SPC FN SPC F (  X  )  =
250 DATA 150,32,165,32,70,40,88,41,178
260 :
270 POKE A,ASC("1")
300 PRINT "12*2=";FN F(2)
310 POKE A,ASC("3")
320 PRINT "32*2=";FN F(2)
READY.

RUN
12*2= 24
32*2= 64

READY.
```


## Execution architecture

How are functions evaluated?


### High level

Assume we have a function definition for `F` using argument `X`,

```txt
  DEF FN F(X) = <expression in X>
```

and assume a function call of `F`.

```txt
  ... FN F( <other expression> ) ...
```

My guess of what is actually executed by the BASIC interpreter is

```txt
  X= <other expression>
  ... <expression in X> ...
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

We see that `(2+3)*2` is correctly computed,
but we also see that `X` is still `123` after evaluating `F`.

My new guess therefore is 

```bas
  PUSH(X)
  X= <other expression>
  ... <expression in X> ...
  POP(X)
```

This time _Mapping the Commodore 64_ seems [wrong](https://archive.org/details/Compute_s_Mapping_the_Commodore_64/page/n61/mode/2up).
It seems to describe a stack frame for `DEF`, not for a call, and it suggests a frame of 5 bytes.
We will make a snapshot of the stack and we will see the C64-wiki is much closer with its 16 byte stack frame.
How to make a snapshot is described in the next section.


### Making a stack snapshot 

How do we snapshot the stack in the middle of calling a function?

I decided to misuse the `USR()` function for that.
Recall, when calling `USR( <expr> )` in BASIC, this is what happens.

- `<expr>` is evaluated, and resulting value stored in the so-called floating point accumulator 
  [FAC1](https://archive.org/details/Compute_s_Mapping_the_Commodore_64/page/n35/mode/2up)
  at addresses 97-102.

- The BASIC interpreter then calls a user defined machine language routine, vectored through 
  [USRADD](https://archive.org/details/Compute_s_Mapping_the_Commodore_64/page/n85/mode/2up)
  at address 785,786
  
- That routine is "supposed" to use FAC1, compute something, leave the floating point result again in FAC1,
  and `RTS` back to the BASIC interpreter.
  
- The BASIC interpreter picks up the value returned by `USR()` in FAC1 and continues with that in the BASIC expression it was evaluating.

I have written a machine language routine that receives a value in FAC1, does not 
look at it, makes a snapshot of the entire stack (all 256 bytes), then returns.
BASIC sees the same value come out as was passed in.

I decided to store the machine language routine at $C000 (49152) 
and to store the stack snapshot (all 256 bytes) at $C100 .. $C200.

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

Converted to decimal gives this.

```BAS
FOR A=49152 TO A+11:PRINT PEEK(A);:NEXT
 162  0  189  0  1  157  0  193  202  208  247  96
```

The following BASIC program then makes a snapshot.

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
Line 130 writes the vector for `USR()` to point to the just poked implementation.
Lines 150-170 contain 3 nested functions. Function `P2(X)` computes 
a simple polynomial of degree 2 (x²+x+1). It uses function `SQ(X)` computes 
the square if `X`, but also calls the identity function, which is implemented
by calling our stack snapshot routine.

When we run this program we get the expected outcome (2*2+2+1=7).

```bas
run
 7
```

As a side effect of such a call, a snapshot of the stack is made.
In the next sections, we analyze the BASIC program and variables 
and then the stack snapshot.


### Hex dump BASIC program

For analysis, we print three pointers: start of BASIC program (2049 or $0801),
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
The below hex numbers are annotated with `*` to denote the begin and end 
of the two areas (BASIC program and variables), see lines 0800, 08B8 and 08E0. 
The symbol `/` separates BASIC lines respectively variables.

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
So I chunked the bytes per line and per variable and I added 
annotation below the bytes (their meaning) and 
above the bytes (flagged some addresses).
I skipped the first half of the program.

```txt
:0863 69 08 8C 00 3A 00
      LINK  140   :
                                          |0875      
:0869 7A 08 96 00 96 A5 49 44 28 58 29 B2 B7 28 58 29 00
      LINK  150   DEFFN I  D  (  X  )  =  USR(  X  )       
                                          |0886                   |088E
:087A 8F 08 A0 00 96 A5 53 51 28 58 29 B2 A5 49 44 28 58 AC 58 29 00
      LINK  160   DEFFN S  Q  (  X  )  =  FN I  D  (  X  *  X  )
                                          |089B             |08A1
:088F A6 08 AA 00 96 A5 50 32 28 58 29 B2 A5 53 51 28 58 29 AA 58 AA 31 00
      LINK  170   DEFFN P  2  (  X  )  =  FN S  Q  (  X  )  +  X  +  1
                                                   |08B5
:08A6 B8 08 B4 00 58 B2 31 3A 99 A5 50 32 28 32 29 3A 80 00
      LINK  180   X  =  1  :  PR FN P  2  (  2  )  :  END
      
:08B8 00 00
      LINK
      
:08B8 41 00 90 40 0C 00 00
      A  _ 
      
:08C1 44 00 87 40 00 00 00
      D  _
      
:08C8 C9 44 75 08 D1 08 B7
      I  D
            |08D1
:08CF 58 00 81 00 00 00 00
      X
      
:08D6 D3 51 86 08 D1 08 A5
      S  Q
      
:08DD D0 32 9B 08 D1 08 A5
      P  2
```

Note the following address(es), the start of a variable's value.

- In the line starting at $08CF, storing float variable `X` (the 58 00 encodes the name), at **$08D1** we see 81 00 00 00 00, the value in floating point format.

Note the following addresses, each the start of a _function body_.

- In the line starting at $0869, the body of `FNID(X)` starts at **$0875**.  
  At line $08C8 the first two bytes encode function name `ID`, the next two hold the start address $0875, 
  and the next two point to the value of `X` $08D1. The 7th byte B7 has no meaning.

- In the line starting at $087A, the body of `FNSQ(X)` starts at **$0886**.  
  At line $08D6 the first two bytes encode function name `SQ`, the next two hold the start address $0886, 
  and the next two point to the value of `X` $08D1. The 7th byte A5 has no meaning.

- In the line starting at $088F, the body of `FNP2(X)` starts at **$089B**.
  At line $08DD the first two bytes encode function name `P2`, the next two hold the start address $089B, 
  and the next two point to the value of `X` $08D1. The 7th byte A5 has no meaning.

Note the following addresses, each the token just after a _function call_. 
Those will be found on the stack (see next section).

- At the end of the line starting at $087A, at **$088E**, we see $00, which terminates the call to `FNID(X)`.

- Near the end of the line starting at $088F, at **$08A1**, we see $AA or `+`, which terminates the call to `FNSQ(X)`.

- Near the end of the line starting at $08A6, at **$08B5**, we see $3A or `:` just before `END`, which terminates the call to `FNP2(2)`.


> For the floating point storage format, recall that a number like 2 is first 
> written in binary with a binary point: 10.00000000 00000000 00000000 000000.
> Then it is normalized (binary point moved to the left just after the first 1), 
> adding a binary exponent (E) to register the shift: 
> 1.00000000 00000000 00000000 0000000 E 00000001.
> In the storage format, the leading 1 is dropped, and the exponent gets $81 added 
> (to handle negative exponents): 00000000 00000000 00000000 00000000 E 10000010.
> Finally, the exponent moves to the front: 10000010 00000000 00000000 00000000 00000000.
> In other words, 2 is encoded as 82 00 00 00 00.
> Likewise 1 is encoded as 81 00 00 00 00. 

The value 81 00 00 00 00 is indeed the value of `X` as it was assigned on line 180 and stored at $08D1.

### Hex dump of the stack 

Next step is to use POWERMON to dump the snapshot of the stack.
We dumped the top half only ($0180..$01FF); the bottom half ($0100..$017F) was empty.

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
Since the memory dump is low to high, the stack in the dump visually grows up.

We can not explain the first 12 bytes that got pushed (B3 AD 00 B7 AA E9 A7 A4 01 01 B4 00).
Leaving those out, and then reordering to get frames of 16 bytes gives this.

```txt
   ret  | 00 |  ret  |  ret  | @ arg | basic | saved arg
  B3 AD | 00 | 8C AD | 3A B4 | D1 08 | 8E 08 | 82 00 00 00 00
  B3 AD | 00 | 8C AD | 3A B4 | D1 08 | A1 08 | 82 00 00 00 00
  B3 AD | 00 | 8C AD | 3A B4 | D1 08 | B5 08 | 81 00 00 00 00
```

Why 16 bytes; that is what the [C64-wiki](https://www.c64-wiki.com/wiki/FN) explains.

> Calling a FN function consumes 16 bytes on the BASIC stack. These consists of
> - float value (in variable encoding) of the argument (5 bytes) (in order mantissa bytes 4, 3, 2, 1 followed by the exponent byte)
> - address of the position pointing to BASIC text ("EXEC_CURSOR") right after the bracket (2 bytes)
> - pointer to the value of the of the argument variable (2 bytes)
> - return address $B43A=(180, 58) from call JSR $AD8A - Confirm Result (2 bytes)
> - return address $AD8C=(173, 140) from call JSR $AD9E - Evaluate Expression in Text (2 bytes)
> - zero byte from $ADAB (1 byte)
> - return address $ADB1=(173, 177) from all JSR $AE83 Evaluate Single Term (2 bytes)

There is only one mismatch, C64 wiki says that the last push is ADB1, 
and that appears to be ADB3 in out case (slightly different ROM version)?

We see
- all the constants as C64 wiki explains;
- the ref to the value of `X` at $08D1;
- the EXEC_CURSORs at respectively $08B5, $08A1, $088E;
- and the pushed value of X, namely 1, 2, and 2 in floating point format (as explained above).

See the next section for more details.


### Execution model

We study the stack generated while evaluating `FNP2(2)`.

The following program fragment (`//` are comments from this article)

```bas
180 X=1:PRINTFNP2(2):END // EXEC_CURSOR at ":" is $08B5
```

leads to the following steps of the BASIC interpreter.

```txt
X=1
PUSH(X) // 1 in float is 81 00 00 00 00
PUSH(EXEC_CURSOR) // $08B5
  X=2
  EVALBODY FNP2()
POP(EXEC_CURSOR)
POP(X)
```

To evaluate the body of `FNP2()`, BASIC jumps to it.
This is the reason the EXEC_CURSOR was pushed: so that the interpreter can resume 
execution at the right point in line 180.

```
170 DEFFNP2(X)=FNSQ(X)+X+1 // EXEC_CURSOR at first "+" is $08A1
```

The first expression of tye body of `FNP2()` is a function call to `FNSQ()`, which 
means we see the same 6 steps being repeated.

```txt
X=1
PUSH(X) // 1 in float is 81 00 00 00 00
PUSH(EXEC_CURSOR) // $08B5
  X=2
  
  PUSH(X) // 2 in float is 82 00 00 00 00
  PUSH(EXEC_CURSOR) // $08A1
    X=2
    EVALBODY FNSQ()
  POP(EXEC_CURSOR)
  POP(X)
  
POP(EXEC_CURSOR)
POP(X)
```

This is the function definition (with body) of `FNSQ()`.

```bas
160 DEFFNSQ(X)=FNID(X*X) // EXEC_CURSOR after ")" is $088E
```

The body of `FNSQ()` starts with a function call to `FNID()`, which 
means we see again the same 6 steps being repeated.

```txt
X=1
PUSH(X) // 1 in float is 81 00 00 00 00
PUSH(EXEC_CURSOR) // $08B5
  X=2
  
  PUSH(X) // 2 in float is 82 00 00 00 00
  PUSH(EXEC_CURSOR) // $08A1
    X=2

    PUSH(X) // 2 in float is 82 00 00 00 00
    PUSH(EXEC_CURSOR) // $088E
      X=2
      EVALBODY FNID()
    POP(EXEC_CURSOR)
    POP(X)

  POP(EXEC_CURSOR)
  POP(X)
  
POP(EXEC_CURSOR)
POP(X)
```

The body of `FNID()` does not call any (user) functions.
No more stack frame. Just a call to `USR()`, which snapshots the stack.
What should be on the stack at the moment of snapshot?
This is what got pushed.

```txt
PUSH(X)           // 81 00 00 00 00
PUSH(EXEC_CURSOR) // B5 08
PUSH(X)           // 82 00 00 00 00
PUSH(EXEC_CURSOR) // A1 08
PUSH(X)           // 82 00 00 00 00
PUSH(EXEC_CURSOR) // 8E 08
```

This matches what we captured earlier, see the last two columns.
Recall this stack dump visually grows upwards, so earlier pushes are lower.

```txt
   ret  | 00 |  ret  |  ret  | @ arg | basic | saved arg
  B3 AD | 00 | 8C AD | 3A B4 | D1 08 | 8E 08 | 82 00 00 00 00
  B3 AD | 00 | 8C AD | 3A B4 | D1 08 | A1 08 | 82 00 00 00 00
  B3 AD | 00 | 8C AD | 3A B4 | D1 08 | B5 08 | 81 00 00 00 00
```

As we saw on [C64-wiki](https://www.c64-wiki.com/wiki/FN), the other pushes 
belong to the evaluation mechanism.

 
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




## Ten slotte 

Dit artikel is een verkorte Nederlandse versie van een Engels artikel.
Dat bevat meer details en bijvoorbeeld ook de design files om er zelf een te maken.

[https://github.com/maarten-pennings/howto/tree/main/c64functions](https://github.com/maarten-pennings/howto/tree/main/c64functions)

(end)


