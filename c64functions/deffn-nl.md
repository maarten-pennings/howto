[![MCC](https://github.com/maarten-pennings/C64howto/blob/main/MCC/mcc240x160.png)](https://github.com/maarten-pennings/C64howto/tree/main/MCC#overview)

Maarten Pennings MCC#07


# Functies in BASIC

In dit artikel bekijken we _gebruikers functies_ in Commodore 64 BASIC.

Met _gebruikers functie_ bedoelen we hier `FN F(X)`, niet subroutines (`GOSUB`), 
en ook niet de ingebouwde functies (zoals `SIN(X)` of `USR(X)`).

We zullen in dit artikel vaak "functie" schijven als we "gebruikers functie" bedoelen.


## Introduction

Gebruikers functies in C64 BASIC gebruiken het keywoord `FN`.

Om een functie `F` _aan te roepen_ met argument `3`, schrijven we `FN F(3)`.

Voor we een gebruikers functie kunnen aanroepen moet hij _gedefinieerd_ zijn.
Daarvoor hebben we een tweede keywoord nodig `DEF`.
Een gebruikers functie definitie zou er zo uit kunnen zien `DEF FN F(X)= X*2`.

Functie definities moeten in een programma staan.
Zonder regel nummer krijgen we de foutmelding `?ILLEGAL DIRECT  ERROR`.
Dat is logisch omdat de code ("_body_") van de gebruikers functie 
(in ons voorbeeld `X*2`) 
persistent bewaard moet worden, zodat hij uitgevoerd kan worden.
Eenmaal gedefinieerd zijn aanroepen in directe mode wel toegestaan.

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

Een van de grootste beperkingen van gebruikers functies in BASIC is dat er maar één signatuur 
wordt ondersteund. De signatuur van een functie bepaalt de invoer en uitvoer van een functie;
het omvat het aantal, type en volgorde van de functie argumenten als ook het type van de
uitvoer (return). 

De enige functie signatuur in C64 BASIC is float naar float 
("float" staat voor gebroken getallen, het type van een variabele zoals `A`).

```basic
100 DEF FN F()= 12       | fout: geen argument
110 DEF FN F(X)= 12      | goed: ENIGE GOEDE SIGNATUUR IN HET LIJSTJE
120 DEF FN F(X,Y)= 12    | fout: meer dan één argument
130 DEF FN F(X%)= 12     | fout: argument verkeerd type (integer)
140 DEF FN F$(X)= "12"   | fout: uitvoer verkeerd type (string)
150 DEF FN F(X$)= 12     | fout: argument verkeerd type (string)
```

Van de functie definities hierboven heeft er maar een de goede signatuur, die op regel 110.
Alle andere geven een foutmelding `syntax  error` (voor regels 100, 120, 130), 
of `type mismatch  error` (voor regels 140 en 150). Opmerkelijk dat er verschillende 
foutmelding komen, helemaal voor 130 en 150.


## Naamgeving

De `FN` voor de functie naam is verplicht.
Maar de functienaam zelf hoeft niet `F` te zijn.
Ook de het functie argument hoeft niet `X` te zijn.
Beide kunnen een naam hebben zoals die is toegestaan voor een variabele in BASIC.

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
Dit is hetzelfde mechanisme als waarbij strings (`LG$`) en integers (`LG%`) een 
eigen _name space_ hebben naast floats. 


## Voorbeelden

De float-naar-float signatuur is een zware beperking.
Toch zijn er nog best wat interessante mogelijkheden voor gebruikers functies
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

- **Rekenkundige functies**  
  `DEF FN SN(A)= SIN(Π*A/180)`  
  `DEF FN LG(X)= LOG(X)/LOG(10)`  
  `DEF FN HI(B)= INT(B/16)`  
  `DEF FN LO(B)= B AND 15`  
  Een functie _body_ mag de ingebouwde functies gebruiken, zelfs meerdere keren in een body.
  Voorbeelden zijn `ABS()`, `ATN()`, `COS()`, `EXP()`, `INT()`, `LOG()`, `SGN()`, `SIN()`, `SQR()`, en `TAN()`.
  Andere voorbeelden zijn de logische operatoren (`AND`, `OR`, `NOT`) en de constante pi (`π`).
  Merk op dat de logische operatoren werken op twee floats/integers en een float opleveren.

- **Relationele operatoren**  
  `DEF FN EVEN(X)= (X AND 1)=0`  
  `DEF FN RANGE(X)= (0<=X) AND (X<10)`  
  Er zijn verschillende relationele operatoren (`=`, `<`, `>`, `<=`, `>=`, `<>`).
  Die leveren ook een float maar alleen `0` voor _false_, en  `-1` voor _true_.

- **String functies**  
  `DEF FN NUMDIG(X)= LEN(STR$(X))-1`  
  Het is onverwacht, gegeven de verplichte float-naar-float signatuur,
  maar string functies zijn toegestaan in een functie _body_.
  Let wel, het return type moet nog steeds float zijn.
  We moeten de string dus nog numeriek maken, bijvoorbeeld met `VAL()`, `LEN()`, of `ASC()`.

- **Systeem functies**  
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
  De derde systeem variabele, `ST` (I/O status), is ook toegstaan.
  
- **Andere gebruikers functies**  
  Een gebruikers functie mag andere gebruikers functies aanroepen.
  Dit zijn de regels voor `DEF FNF(X)= ...FNG(X)...`:
  
  - `FNG()` hoeft niet te bestaan als `FNF()` gedefinieerd wordt 
    (de functie wordt opgezocht bij aanroep).
  - `FNG()` moet bestaan als `FNF()` aangeroepen wordt.
  - De definitie mag niet circulair zijn:
    `FNG()` mag `FNF()` niet aanroepen (direct of indirect)
    want dit zou tot oneindige recursie leiden.
    
  Het volgende voorbeeld converteert bytes naar hex, gebruikmakend 
  van extra gebruikers functie.
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
  De ASCII waarde van het "cijfer" 10 (hex `A`) is 65.
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

  Het voorbeeld hieronder `PEEK`-t de karakter code en de karakter kleur
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


## Verboden functie _body_

Er zijn ook constructies niet toegstaan in een functie _body_ die we daar mogelijk 
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
  elke relationele operator levert 0 of -1 op, en dat kan gebruikt 
  worden in de omliggende expressie.

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
  

## De definitie

Als we de C64 opstarten is er ongeveer 38 kB RAM vrij.
Als we daarna een programma intypen (of laden), gaat dat ten koste van die 38 kB.
Als we daarna het programma runnen, wordt er achter het programma, in de vrije RAM
een tabel aangemaakt van (scalaire) variabelen (arrays komen daar weer achter).

De variabelen tabel bevat _records_ van 7 bytes: 
2 bytes voor de naam van de variabele en 5 bytes vooor de waarde.
De 2 bytes voor de naam zijn eigenlijk 7 bits voor de eerste letter en 7 bits 
voor de tweede letter (of 0 als die er niet is) plus 2 bits voor het type.

Er zijn vier types: float, string, integer, ... en gebruikers functie.
Voor een gebruikers functie zijn de 5 bytes voor de waarde als volgt:
2 bytes zijn een pointer naar de _body_ in de BASIC code, en 2 bytes zijn
een pointer naar de argument variabele. Het vijfde byte wordt niet gebuikt.

Met andere woorden, een gebruikers functie deelt een aantal eigenschappen 
met gewone variabelen (eigen namespace, opzoeken bij gebruik, kunnen overschreven worden).


## De aanroep

Hoe worden gebruikers functies berekend?

Laten we aannemen dat we een definitie hebben voor `F` met argument `X`:

```txt
  DEF FN F(X) = <expressie_in_X>
```

Verder hebben we een aanroep van `F`.

```txt
  R= ... FN F( <arg_expressie> ) ...
```

De eerste gok is dat de BASIC interpreter deze stappen maakt voor de aanroep

```txt
  X= <arg_expressie>
  R= ... <expressie_in_X> ...
```

Maar het volgende voorbeeld laat zien dat het subtieler is

```basic
110 X=123
100 DEF FN F(X)=X*2
120 PRINT FN F(2+3)
130 PRINT X
RUN
 10
 123
```

We zien dat `(2+3)*2` correct berekend is,
maar we zien ook dat `X` nog steeds `123` is na het berekenen van `F`.

De nieuwe gok is dat de BASIC interpreter deze stappen maakt voor de aanroep

```basic
  PUSH(X)
  X= <arg_expressie>
  R= ... <expressie_in_X> ...
  POP(X)
```

Op C64-wiki blijkt de echte implementatie nog ingewikkelder.
Om `<expressie_in_X>` uit te rekenen moet de BASIC programma wijzer 
verschoven worden van de aanroep naar (de _body_ van) de definitie. 
Na het uitrekenen van de _body_ moet de BASIC programma wijzer 
weer terug gezet worden naar de aanroep. 
Aangezien de ene gebruikers functie een andere gebruikers functie 
kan aanroepen moet de programma wijzer manipulatie ook via de stack.
C64-wiki legt uit dat een gebruikers functie aanroep een 16-byte
stackframe plaatst.


## Conclusies

- De signatuur (één float naar één float) is erg beperkend.
  Meer dan één argument toestaan zou een verbetering zijn (`FNLOG(X,B)`).
  Strings als uitvoer toestaan zou een verbetering zijn (`FNHEX$()`).
  
- Er is geen "short-circuit evaluation" in BASIC.
  Elke subexpressie wordt altijd berekend en dus is er geen recursie mogelijk.

- Dat de hele _body_ op één regel moet staan is een behoorlijke beperking.
  Ook dat statements niet zijn toegestaan is jammer.
  
Hoewel het `FNF()` mechanisme erg beperkt is lijkt de implementatie 
behoorlijk ingewikkeld, kijk bijvoorbeeld naar het 16-byte stackframe.

Mijn conclusie is dat voor dit feature de opbrengst voor de 
BASIC-programmeur niet in balans is met de (kernal) implementatie 
kosten. Ik denk dat de meeste BASIC-programmeurs _gebruikers functies_ 
beschouwen als een "zelden gebruikte feature".


## Ten slotte 

Dit artikel is een verkorte Nederlandse versie van een Engels artikel.
Dat bevat meer details en bijvoorbeeld een uitgebreide stack analyze.

[https://github.com/maarten-pennings/howto/tree/main/c64functions](https://github.com/maarten-pennings/howto/tree/main/c64functions)

(end)

