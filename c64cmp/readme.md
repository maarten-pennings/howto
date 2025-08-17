# How to compare (CMP) on C64

How to use the compare instruction of the 6502?


## Introduction

The 6502 instruction set contains three compare instructions: `CMP`, `CPX` and `CPY`,
see [masswerk](https://www.masswerk.at/6502/6502_instruction_set.html#:~:text=set%20interrupt%20disable-,Comparisons,-Generally%2C%20comparison%20instructions).
They behave all the same, but compare the `A`, `X`, or `Y` register respectively.

The compare instructions subtract the operand from the register, but discard
the resulting value. However, the flags in the status register are set as 
with a real subtraction.

So, to implement `A < $E0` I was tempted to write

```
    LDA #??
    CMP #$E0
    BMI yes
    RTS
yes:
```

But, as suggested by the "tempted" this does not work.

Why not? The `BMI` instruction branches when the `N` flag is set, and as masswerk writes
[cryptically](https://www.masswerk.at/6502/6502_instruction_set.html#:~:text=0-,sign%20bit%20of%20result,-Register%20%3D%20Operand),
the value of `N`, in case `A < $E0` is "sign bit of result".

What does that mean?

The `CMP #$E0` instruction computes `A-$E0`. 
If `A` was `E0`, the result is 0 so the `Z` flag will be set.
If `A` is greater than `E0` the result is positive so the `N` flag will be cleared.
If `A` is less than `E0` the result of the subtract is negative so the `N` flag will be set.

Sounds good. However, we have an 8 bit CPU, so when using the 8 bits in the 
signed interpretation, which is what we do when using `N`, exactly _half_ of 
the range is considered negative, and this might not be what you want. 
Let's check that with an experiment.


## Programming the experiment

I understand the theory, but let's verify that practically.
The fun thing of an 8 bit CPU is that it is so small that we can check all cases.

The following BASIC program loads the accumulator with values $00 to $FF, 
executes a `CMP #$E0` and prints the status register. In more detail

- `POKE 780,AC` loads the accumulator AC for use in the upcoming `SYS`; see 
  [map](https://www.zimmers.net/anonftp/pub/cbm/c64/manuals/mapping-c64.txt#:~:text=783%20(%2430C%2D%2430F)-,Register%20Storage%20Area,-The%20BASIC%20SYS).
- `SYS AD` runs the `CMP #$E0; RTS` stored at address `AD` (49152)
- `P=PEEK(783)` loads the program status register from the last `SYS` into `P`.
- `P` is analyzed for 3 flags: `N`, `Z` and `C`; 
  [note](https://www.masswerk.at/6502/6502_instruction_set.html#CMP) the `CMP` does not affect the other flags.
- Finally `AC` is printed (in hex) followed by the three flags and a space.

Please note that I use the [KCS cartridge](https://nl.wikipedia.org/wiki/KCS_Power_Cartridge) because
it supports hex expressions.

By the way, the program runs the described (sub) routine three times,
once with operand $E0 (`CMP #$E0`) but before that with $20, and with $80.

```BASIC
100 AD=49152:REM ADDRESS OF ASM ROUTINE
110 OP=$20:GOSUB 150
120 OP=$80:GOSUB 150
130 OP=$E0:GOSUB 150
140 END
150 PRINT "LDA #?;CMP #$"HEX$(OP)";RTS"
160 POKE AD,$C9:POKE AD+1,OP:REM CMP#OP
170 POKE AD+2,$60:REM RTS
180 FOR AC=0TO255
190 :POKE 780,AC:SYS AD:P=PEEK(783)
200 :N$="-":IFPAND128THENN$="N"
220 :Z$="-":IFPAND  2THENZ$="Z"
230 :C$="-":IFPAND  1THENC$="C"
240 :PRINT HEX$(AC)":"N$Z$C$" ";
250 :IF AC-4*INT(AC/4)=3 THEN PRINT
260 NEXT:RETURN
```

## Results of the experiment

The above program prints the following results. 
I have manually placed the three outputs side by side for this article.

```
LDA #?;CMP #$20;RTS            LDA #?;CMP #$80;RTS            LDA #?;CMP #$E0;RTS
00:N-- 01:N-- 02:N-- 03:N--    00:N-- 01:N-- 02:N-- 03:N--    00:--- 01:--- 02:--- 03:---
04:N-- 05:N-- 06:N-- 07:N--    04:N-- 05:N-- 06:N-- 07:N--    04:--- 05:--- 06:--- 07:---
08:N-- 09:N-- 0A:N-- 0B:N--    08:N-- 09:N-- 0A:N-- 0B:N--    08:--- 09:--- 0A:--- 0B:---
0C:N-- 0D:N-- 0E:N-- 0F:N--    0C:N-- 0D:N-- 0E:N-- 0F:N--    0C:--- 0D:--- 0E:--- 0F:---
10:N-- 11:N-- 12:N-- 13:N--    10:N-- 11:N-- 12:N-- 13:N--    10:--- 11:--- 12:--- 13:---
14:N-- 15:N-- 16:N-- 17:N--    14:N-- 15:N-- 16:N-- 17:N--    14:--- 15:--- 16:--- 17:---
18:N-- 19:N-- 1A:N-- 1B:N--    18:N-- 19:N-- 1A:N-- 1B:N--    18:--- 19:--- 1A:--- 1B:---
1C:N-- 1D:N-- 1E:N-- 1F:N--    1C:N-- 1D:N-- 1E:N-- 1F:N--    1C:--- 1D:--- 1E:--- 1F:---
20:-ZC 21:--C 22:--C 23:--C    20:N-- 21:N-- 22:N-- 23:N--    20:--- 21:--- 22:--- 23:---
24:--C 25:--C 26:--C 27:--C    24:N-- 25:N-- 26:N-- 27:N--    24:--- 25:--- 26:--- 27:---
28:--C 29:--C 2A:--C 2B:--C    28:N-- 29:N-- 2A:N-- 2B:N--    28:--- 29:--- 2A:--- 2B:---
2C:--C 2D:--C 2E:--C 2F:--C    2C:N-- 2D:N-- 2E:N-- 2F:N--    2C:--- 2D:--- 2E:--- 2F:---
30:--C 31:--C 32:--C 33:--C    30:N-- 31:N-- 32:N-- 33:N--    30:--- 31:--- 32:--- 33:---
34:--C 35:--C 36:--C 37:--C    34:N-- 35:N-- 36:N-- 37:N--    34:--- 35:--- 36:--- 37:---
38:--C 39:--C 3A:--C 3B:--C    38:N-- 39:N-- 3A:N-- 3B:N--    38:--- 39:--- 3A:--- 3B:---
3C:--C 3D:--C 3E:--C 3F:--C    3C:N-- 3D:N-- 3E:N-- 3F:N--    3C:--- 3D:--- 3E:--- 3F:---
40:--C 41:--C 42:--C 43:--C    40:N-- 41:N-- 42:N-- 43:N--    40:--- 41:--- 42:--- 43:---
44:--C 45:--C 46:--C 47:--C    44:N-- 45:N-- 46:N-- 47:N--    44:--- 45:--- 46:--- 47:---
48:--C 49:--C 4A:--C 4B:--C    48:N-- 49:N-- 4A:N-- 4B:N--    48:--- 49:--- 4A:--- 4B:---
4C:--C 4D:--C 4E:--C 4F:--C    4C:N-- 4D:N-- 4E:N-- 4F:N--    4C:--- 4D:--- 4E:--- 4F:---
50:--C 51:--C 52:--C 53:--C    50:N-- 51:N-- 52:N-- 53:N--    50:--- 51:--- 52:--- 53:---
54:--C 55:--C 56:--C 57:--C    54:N-- 55:N-- 56:N-- 57:N--    54:--- 55:--- 56:--- 57:---
58:--C 59:--C 5A:--C 5B:--C    58:N-- 59:N-- 5A:N-- 5B:N--    58:--- 59:--- 5A:--- 5B:---
5C:--C 5D:--C 5E:--C 5F:--C    5C:N-- 5D:N-- 5E:N-- 5F:N--    5C:--- 5D:--- 5E:--- 5F:---
60:--C 61:--C 62:--C 63:--C    60:N-- 61:N-- 62:N-- 63:N--    60:N-- 61:N-- 62:N-- 63:N--
64:--C 65:--C 66:--C 67:--C    64:N-- 65:N-- 66:N-- 67:N--    64:N-- 65:N-- 66:N-- 67:N--
68:--C 69:--C 6A:--C 6B:--C    68:N-- 69:N-- 6A:N-- 6B:N--    68:N-- 69:N-- 6A:N-- 6B:N--
6C:--C 6D:--C 6E:--C 6F:--C    6C:N-- 6D:N-- 6E:N-- 6F:N--    6C:N-- 6D:N-- 6E:N-- 6F:N--
70:--C 71:--C 72:--C 73:--C    70:N-- 71:N-- 72:N-- 73:N--    70:N-- 71:N-- 72:N-- 73:N--
74:--C 75:--C 76:--C 77:--C    74:N-- 75:N-- 76:N-- 77:N--    74:N-- 75:N-- 76:N-- 77:N--
78:--C 79:--C 7A:--C 7B:--C    78:N-- 79:N-- 7A:N-- 7B:N--    78:N-- 79:N-- 7A:N-- 7B:N--
7C:--C 7D:--C 7E:--C 7F:--C    7C:N-- 7D:N-- 7E:N-- 7F:N--    7C:N-- 7D:N-- 7E:N-- 7F:N--
80:--C 81:--C 82:--C 83:--C    80:-ZC 81:--C 82:--C 83:--C    80:N-- 81:N-- 82:N-- 83:N--
84:--C 85:--C 86:--C 87:--C    84:--C 85:--C 86:--C 87:--C    84:N-- 85:N-- 86:N-- 87:N--
88:--C 89:--C 8A:--C 8B:--C    88:--C 89:--C 8A:--C 8B:--C    88:N-- 89:N-- 8A:N-- 8B:N--
8C:--C 8D:--C 8E:--C 8F:--C    8C:--C 8D:--C 8E:--C 8F:--C    8C:N-- 8D:N-- 8E:N-- 8F:N--
90:--C 91:--C 92:--C 93:--C    90:--C 91:--C 92:--C 93:--C    90:N-- 91:N-- 92:N-- 93:N--
94:--C 95:--C 96:--C 97:--C    94:--C 95:--C 96:--C 97:--C    94:N-- 95:N-- 96:N-- 97:N--
98:--C 99:--C 9A:--C 9B:--C    98:--C 99:--C 9A:--C 9B:--C    98:N-- 99:N-- 9A:N-- 9B:N--
9C:--C 9D:--C 9E:--C 9F:--C    9C:--C 9D:--C 9E:--C 9F:--C    9C:N-- 9D:N-- 9E:N-- 9F:N--
A0:N-C A1:N-C A2:N-C A3:N-C    A0:--C A1:--C A2:--C A3:--C    A0:N-- A1:N-- A2:N-- A3:N--
A4:N-C A5:N-C A6:N-C A7:N-C    A4:--C A5:--C A6:--C A7:--C    A4:N-- A5:N-- A6:N-- A7:N--
A8:N-C A9:N-C AA:N-C AB:N-C    A8:--C A9:--C AA:--C AB:--C    A8:N-- A9:N-- AA:N-- AB:N--
AC:N-C AD:N-C AE:N-C AF:N-C    AC:--C AD:--C AE:--C AF:--C    AC:N-- AD:N-- AE:N-- AF:N--
B0:N-C B1:N-C B2:N-C B3:N-C    B0:--C B1:--C B2:--C B3:--C    B0:N-- B1:N-- B2:N-- B3:N--
B4:N-C B5:N-C B6:N-C B7:N-C    B4:--C B5:--C B6:--C B7:--C    B4:N-- B5:N-- B6:N-- B7:N--
B8:N-C B9:N-C BA:N-C BB:N-C    B8:--C B9:--C BA:--C BB:--C    B8:N-- B9:N-- BA:N-- BB:N--
BC:N-C BD:N-C BE:N-C BF:N-C    BC:--C BD:--C BE:--C BF:--C    BC:N-- BD:N-- BE:N-- BF:N--
C0:N-C C1:N-C C2:N-C C3:N-C    C0:--C C1:--C C2:--C C3:--C    C0:N-- C1:N-- C2:N-- C3:N--
C4:N-C C5:N-C C6:N-C C7:N-C    C4:--C C5:--C C6:--C C7:--C    C4:N-- C5:N-- C6:N-- C7:N--
C8:N-C C9:N-C CA:N-C CB:N-C    C8:--C C9:--C CA:--C CB:--C    C8:N-- C9:N-- CA:N-- CB:N--
CC:N-C CD:N-C CE:N-C CF:N-C    CC:--C CD:--C CE:--C CF:--C    CC:N-- CD:N-- CE:N-- CF:N--
D0:N-C D1:N-C D2:N-C D3:N-C    D0:--C D1:--C D2:--C D3:--C    D0:N-- D1:N-- D2:N-- D3:N--
D4:N-C D5:N-C D6:N-C D7:N-C    D4:--C D5:--C D6:--C D7:--C    D4:N-- D5:N-- D6:N-- D7:N--
D8:N-C D9:N-C DA:N-C DB:N-C    D8:--C D9:--C DA:--C DB:--C    D8:N-- D9:N-- DA:N-- DB:N--
DC:N-C DD:N-C DE:N-C DF:N-C    DC:--C DD:--C DE:--C DF:--C    DC:N-- DD:N-- DE:N-- DF:N--
E0:N-C E1:N-C E2:N-C E3:N-C    E0:--C E1:--C E2:--C E3:--C    E0:-ZC E1:--C E2:--C E3:--C
E4:N-C E5:N-C E6:N-C E7:N-C    E4:--C E5:--C E6:--C E7:--C    E4:--C E5:--C E6:--C E7:--C
E8:N-C E9:N-C EA:N-C EB:N-C    E8:--C E9:--C EA:--C EB:--C    E8:--C E9:--C EA:--C EB:--C
EC:N-C ED:N-C EE:N-C EF:N-C    EC:--C ED:--C EE:--C EF:--C    EC:--C ED:--C EE:--C EF:--C
F0:N-C F1:N-C F2:N-C F3:N-C    F0:--C F1:--C F2:--C F3:--C    F0:--C F1:--C F2:--C F3:--C
F4:N-C F5:N-C F6:N-C F7:N-C    F4:--C F5:--C F6:--C F7:--C    F4:--C F5:--C F6:--C F7:--C
F8:N-C F9:N-C FA:N-C FB:N-C    F8:--C F9:--C FA:--C FB:--C    F8:--C F9:--C FA:--C FB:--C
FC:N-C FD:N-C FE:N-C FF:N-C    FC:--C FD:--C FE:--C FF:--C    FC:--C FD:--C FE:--C FF:--C
```

## Discussion

Let's start by looking at case $E0.

### CMP #$E0

Note that in the third test, `CMP #$E0`, the `Z` flag is indeed set once,
namely when the accumulator was E0, see `E0:-ZC`. 
As expected the `N` flag is not set; 0 is not negative.
All following numbers also have the `N` flag clear.
If we look at all predecessors, that starts as expected:
DF, DE, DD, DC all have the `N` flag set (`DC:N-- DD:N-- DE:N-- DF:N--`).
But after exactly $80 predecessors, the `N` flag stops being set:

```
5C:--- 5D:--- 5E:--- 5F:---
60:N-- 61:N-- 62:N-- 63:N--
```

So we can not use the `N` flag for testing if the accumulator is less than E0,
if we want to go all the way down to $00.

### CMP #$80

The second test, `CMP #$80` happens to be ok.
When the accumulator is $80 the `Z` is set.
For all numbers $80 and higher `N` is clear and below $80 `N` is set.
But this is sheer luck, because we compare to $80.
As we mentioned before, the `N` flag is set for the $80 numbers below the 
compare value, which here is precisely the whole range when we compare to $80.

### CMP #$20

In the first test, `CMP #$20` we see the same thing go wrong, but now with 
different results. Where in the case `CMP #$E0`, we got false positives
for the lowest numbers (from $00 to $5F).
In the case `CMP #$20` we get false false negatives for the highest numbers 
(from $A0 to $FF).

### What now?

The `N` flag doesn't work, but as we can see from the table, 
the `C` flag is precisely what we need!
That is, when we want to treat the accumulator as unsigned.


## Conclusion

After compare, use the `C` flag when the accumulator is treated as unsigned.
Do not use the `N` flag.

The `V` flag is not affected by the compare instructions.
See [6502.org](http://www.6502.org/tutorials/vflag.html) for details on the `V` flag.

(end)
