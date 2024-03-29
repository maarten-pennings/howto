# ESP32 PWM
This project shows how to use PWM on an ESP32, 
with an exponential curve and a transistor to drive a high power LED.

## Setup
We use this to drive a high power, low voltage, LED filament light bulb, similar
to [these](https://www.aliexpress.com/item/1005006027765315.html).

![Setup](setup.jpg)

## Sketch
For the sketch see [esp32pwm.ino](esp32pwm.ino).

To compute the mapping from brightness to pwm yourself (replacing the lookup table in the above ino file) see the explanation of the gamma curve at [adafruit](https://learn.adafruit.com/led-tricks-gamma-correction).

(end)
