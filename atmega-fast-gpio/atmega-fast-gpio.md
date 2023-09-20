# Fast GPIO on ATMEGA

The classic Arduino use an MCU of the ATMEGA series.


## Introduction

The typical way to set a GPIO pin in Arduino
is to use the Arduino API:

```C
#define PIN_TEST2 23
digitalWrite( PIN_TEST2, LOW );
```

The Arduino API might be simple, it is not fast.


## Faster

A faster way is to write directly to the special function register ("SFR")
that controls the pin state.

The ATMEGAs have 8 GPIO pins grouped in a so-called port.
The ports get letters (A, B, ...).
For each port `x` there are two registers.
The 8 bits in these registers map to the 8 gpio pins.
For example, the ATMEGA256 has GPIO pins 22,23,24,25,26,27,28,29 mapped to port A.


 - `DDRx` data direction register x  
   When a bit is 0 that GPIO is an input, when the bit is 1, the GPIO is an output.
   
 - `PORTx` is the value at the pins of port x  
   When a bit is 0 the pin is low, when a bit is 1 the pin is high.


## Example

Output example of 8 pins in one go.

```C
  // Port A: 22,23,24,25,26,27,28,29        DATA (7=MD7..0=MD0)
  // DATA pins: instruction NOP
  DDRA  = 0xFF; // all pins output
  PORTA = 0xEA; // NOP
```


Input example of a single pin
```C
  // Port J: 15                             POW (0=MVCC)
  // POW pin: output and on
  DDRJ = 0x01;
  PORTJ = 0x00; // low active
```

These example are taken from an [ATMEGA that feeds a 6502](https://github.com/maarten-pennings/6502/blob/master/2emulation/2560shield-hwtest/2560shield-hwtest.ino).

(end)
