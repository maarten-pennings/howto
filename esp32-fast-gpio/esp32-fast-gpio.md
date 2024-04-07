# Fast GPIO on ESP32


## Introduction

The typical way to set a GPIO pin on an ESP32 (in Arduino)
is to use the Arduino API:

```C
#define PIN_TEST2 23
digitalWrite( PIN_TEST2, LOW );
```

The Arduino API might be simple, it is not fast.


## Faster

A faster way is to write directly to the special function register ("SFR")
that controls the pin state.

```C
*(uint32_t*)0x3FF4400C = 0b100000000000000000000000; // 23 zeros
```

This is not very readable and error prone.

Fortunately, the ESP32 header file `gpio_struct.h` is included in every sketch.
It provides a variable `GPIO` which is overlayed on the GPIO SFRs.
This variable is a struct of unions, giving all registers a readable name.

So our final version is

```C
GPIO.out_w1tc = 1UL << PIN_TEST2;
```

The `c` here means clear, there is also a `s` set: `GPIO.out_w1ts = 1UL << PIN_TEST2;`.


## Example

See the Arduino sketch [esp32-fast-gpio.ino](esp32-fast-gpio.ino) as an example.

from the logic analyzer, we see that two consecutive 0-writes to two different ports
now takes 50 ns.

![scope](scope_capture.png)


## Higher pins

[Note](https://esp32.com/viewtopic.php?t=27963) that `GPIO.out_w1ts` and `GPIO.out_w1tc` 
are the set and clear bitmask for the first 32 GPIO pins.
For the pins from 32 and higher you need "out1" instead of "out", but also "val":
`GPIO.out1_w1ts.val` and `GPIO.out1_w1tc.val`.

This also works for ESP32-S3.

(end)

