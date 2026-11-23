[![MCC](https://github.com/maarten-pennings/C64howto/blob/main/MCC/mcc240x160.png)](https://github.com/maarten-pennings/C64howto/tree/main/MCC#overview)

Maarten Pennings MCC#08


# USR(X)

In dit artikel gaan we `USR(X)` gebruiken om `DEEK()` te implementeren.
De functie `DEEK()` is een "Double Peek":
`DEEK(ADDR)` levert `PEEK(ADDR)+256*PEEK(ADDR+1)`. 

Maar het doel is niet `DEEK()`, het doel is om `USR()` te begrijpen.


## Introductie

Commodore BASIC heeft twee manieren om vanuit BASIC een 
machine code sub-routine aan te roepen: `SYS <adres>` en `USR( <argument> )`.


### SYS

De eerste manier om een machine code sub-routine 
aan te roepen, `SYS`, is een soort `GOTO`.

De uitvoering van het commando `SYS <adres>` betekent dat de BASIC 
interpreter stopt met uitvoering van het BASIC programma.
In plaats daarvan verplaatst executie naar de machine code routine
op `adres`. De CPU (6510) voert die instructie na instructie uit,
totdat er een `RTS` uitgevoerd wordt. Die zorgt ervoor dat 
de BASIC interpreter weer opstart waar hij gebleven was:
het statement na de `SYS <adres>`.

Ik ben er pas heel laat achter gekomen (het staat niet in de gebruikers handleiding)
dat er een eenvoudige manier is om argumenten mee te geven en resultaten terug te krijgen.
Het gebied $030C-$030F (780-783) wordt door `SYS` gebruikt om de CPU registers 
op te slaan: de accumulator A (op 780), index registers X (op 781) en Y (op 782), 
en het program status register P (op 783). Voor elk SYS-commando worden de CPU 
registers geladen met de waardes op die adressen. Nadat de machine code is uitgevoerd, 
worden de nieuwe waarden van de CPU registers weer opgeslagen op diezelfde adressen.

```BASIC 11
100 POKE  49152,232:REM INX
110 POKE  49153, 96:REM RTS
200 POKE  781,45
210 SYS   49152
220 PRINT PEEK(781)
RUN
 46
```

Dit eenvoudige programma hoogt CPU register X met 1 op. 
De initiële waarde (45, op schaduw adres 781, regel 200),
is na de machine code aanroep (regel 210) verhoogd tot 46, 
en dat controleren we door op regel 220 de schaduw weer te printen.


### USR()

De tweede manier om een machine code sub-routine 
aan te roepen, `USR()`, is een functie aanroep.

We kunnen een argument meegeven (een float) en we krijgen een 
waarde terug (ook een float). Dit is een beetje beperkt qua signatuur, 
maar voor de rest gedraagt deze functie zich als iedere BASIC functie.

Het volgende voorbeeld is gekunsteld, maar laat wel zien wat er 
technisch mogelijk is: `PRINT USR(1)+USR(2+USR(3))`.

Je vraagt ​​je wellicht af welke machine code routine wordt aangeroepen; 
naar welk adres er gesprongen wordt. Het antwoord is: het adres op locatie 
785 en 786 ($311 en $312). Deze vector heeft de (interne) naam `USRADD`, 
voor "USR() address".

Standaard wijst deze vector naar een routine die de melding 
`?ILLEGAL QUANTITY  ERROR` afdrukt. We moeten het adres van onze eigen 
routine in deze vector `POKE`-n voordat we `USR()` aanroepen.

  | adres (hex) | adres (dec) | inhoud    |
  |:------------|:------------|:----------|
  | $030C       | 780         | A         |
  | $030D       | 781         | X         |
  | $030E       | 782         | Y         |
  | $030F       | 783         | P         |
  | $0310       | 784         | $4C (JMP) |
  | $0311       | 785         | lo(addr)  |
  | $0312       | 786         | hi(addr)  |


### Expressies

Het is goed om te weten dat Commodore BASIC drie _types_ kent: 
_float_ (kommagetal), _string_ (tekenreeks) en _integer_ (geheel getal).
Een variabele zoals `A$` (of een functie zoals `MID$`) die eindigt op een `$`, is een string.
Een variabele zoals `XX%` die eindigt op een `%`, is een integer.
Alle overige variabelen en functies zijn van het type float. 

Wellicht denk je dat het verstandig is om integers te gebruiken, 
maar het antwoord is een eenduidig _nee_. Ten eerste bespaar je er 
geen geheugen mee: elke variabele neemt 7 bytes in beslag — 
2 bytes voor de naam en 5 bytes voor de waarde (bij float is dit de waarde zelf; 
bij strings betreft het de lengte, een pointer naar de data, en een dummy; 
bij integers gaat het om de waarde, opgeslagen in twee bytes, 
aangevuld met drie dummies). 
Ten tweede bespaar je er geen rekentijd (_cycles_) mee. 
Integendeel: een integer worden eerst omgezet naar een float, 
waarna de berekening in het float-domein wordt uitgevoerd, 
om vervolgens weer te worden geconverteerd naar een integer. 
Dit is waarschijnlijk zo ontworpen om de BASIC-interpreter eenvoudig 
te houden; er is namelijk slechts één "ALU" (rekeneenheid) aanwezig, 
en die is alleen ingericht voor floats.

Waarom bestaan ​​integers dan? 
Ze zijn nuttig in één specifiek geval: 
wanneer je er een array van maakt. 
In dat geval nemen ze namelijk slechts 2 bytes per element in beslag.


## Ten slotte 

Dit artikel is een verkorte Nederlandse versie van een Engels artikel.
Dat bevat meer details, source files en bijvoorbeeld een klein uitstapje naar Turbo Macro Pro, een assembler op de C64 zelf.

[https://github.com/maarten-pennings/howto/tree/main/c64usr](https://github.com/maarten-pennings/howto/tree/main/c64usr)

(end)

