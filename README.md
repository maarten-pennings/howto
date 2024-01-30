# How to
Assortment of "How to xxx" I want to remember.


## Fast GPIO writes on an ATMEGA
Set or clear ATMEGA GPIO pins via direct register access; this is much faster than via the Arduino API.
For an example and explanation see [atmega-fast-gpio](atmega-fast-gpio/atmega-fast-gpio.md).


## Fast GPIO writes on an ESP32
Set or clear ESP32 GPIO pins via direct register access; this is much faster than via the Arduino API.
For an example and explanation see [esp32-fast-gpio](esp32-fast-gpio/esp32-fast-gpio.md).


## Open drain on an ESP32
Unlike traditional Arduino boards, the ESP32 allows configuring its GPIO pins as open drain. 
For an example and explanation see [esp32-opendrain](esp32-opendrain/esp32-opendrain.md).


## NodeMCU power architecture
The NodeMCU board (ESP8266, ESP32) have several pins related to power.
See [NodeMCU-power-architecture](NodeMCU-power-architecture/NodeMCU-power-architecture.md) for an explanation of the pins.


## SNR
Computing the signal to noise ratio [SNR](snr/snr.md) of a series of measurements.


## Wide serial plotter on Arduino 2.0
The Serial Plotter in Arduino 2.0 has a too narrow x-axis. That can be patched wider.
For an example and explanation see [arduino2.0-wideplot](arduino2.0-wideplot/arduino2.0-wideplot.md).


## Drag and drop in HTML
For an example and explanation see [drag-n-drop-html](drag-n-drop-html/drag-n-drop-html.html).
Or see it in [action](https://htmlpreview.github.io/?https://github.com/maarten-pennings/howto/blob/main/drag-n-drop-html/drag-n-drop-html.html).


## Control an 128x64 LCD screen
I was given an 128x64 LCD module from POWERTIP ("PG12864WRF"). It uses an NT7108 as controller.
Took quite some time to get it [running](NT7108-12864LCD/NT7108-12864LCD.md).

## PWM on ESP32
Project [esp32pwm](esp32pwm/readme.md) shows how to use PWM on an ESP32, 
with an exponential curve and a transistor to drive a high power LED.

(end)
