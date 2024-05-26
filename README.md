# How to
Assortment of "How to xxx" I want to remember.

## Iterators and generators

An [article](https://github.com/maarten-pennings/Lego-Mindstorms/tree/main/ms4/multitask/iteratorstudy) about what iterators and generators are, using Python.
An excellent [article](https://btmc.substack.com/p/implementing-generators-yield-in) of how to implement generators in C. I was wondering if setjmp/longjmp would work/help here?


## How to do animations in HTML
A small set of animation demos in html.
See [html-animation](html-animation/readme.md) for soure and demo.


## How to create a Python Virtual environment and use a local package
This [pythonpackage](pythonpackage/readme.md) is an empty 
python application which uses an empty package,
all in a virtual enviroment.


## Using ESP SPI slave without SSEL
I needed to connect an SPI mastering sensor to an ESP32S3.
The sensor does not have an SSEL, which is a no-go for ESP.
I tried various [solutions](spitest), but **failed** - an "how not to".

## SPI modes
SPI communication knows much more variation than e.g. I2C.
This [how to](SPImodes/readme.md) looks at the four modes induced
by CPOL (default clock state) and CPHA (data valid phase).


## Using Windows' symbolic links to manage Arduino Libraries
The Arduino IDE is a bit poor in managing (files of) bigger projects.
The [LinkedLibrary howto](LinkedLibrary/readme.md) explains how you can use Windows' `mklink` to
share libraries but store them in the same repository as the using applications.


## Debugging and ESP32S3 using Arduino IDE
It took many tries, but I have the debugger in the Arduino IDE
running on the ESP32S3-DevKitC-1 board (without any probe).
See [DebuggingESP32S3Arduino](DebuggingESP32S3Arduino/DebuggingESP32S3Arduino.md).


## PWM on ESP32
Project [esp32pwm](esp32pwm/readme.md) shows how to use PWM on an ESP32, 
with an exponential curve and a transistor to drive a high power LED.


## Control an 128x64 LCD screen
I was given an 128x64 LCD module from POWERTIP ("PG12864WRF"). It uses an NT7108 as controller.
Took quite some time to get it [running](NT7108-12864LCD/NT7108-12864LCD.md).


## Drag and drop in HTML
For an example and explanation see [drag-n-drop-html](drag-n-drop-html/readme.md).
Or see it in [action](https://htmlpreview.github.io/?https://github.com/maarten-pennings/howto/blob/main/drag-n-drop-html/drag-n-drop-html.html).


## Wide serial plotter on Arduino 2.0
The Serial Plotter in Arduino 2.0 has a too narrow x-axis. That can be patched wider.
For an example and explanation see [arduino2.0-wideplot](arduino2.0-wideplot/arduino2.0-wideplot.md).


## SNR
Computing the signal to noise ratio [SNR](snr/snr.md) of a series of measurements.


## NodeMCU power architecture
The NodeMCU board (ESP8266, ESP32) have several pins related to power.
See [NodeMCU-power-architecture](NodeMCU-power-architecture/NodeMCU-power-architecture.md) for an explanation of the pins.


## Open drain on an ESP32
Unlike traditional Arduino boards, the ESP32 allows configuring its GPIO pins as open drain. 
For an example and explanation see [esp32-opendrain](esp32-opendrain/esp32-opendrain.md).


## Fast GPIO writes on an ESP32
Set or clear ESP32 GPIO pins via direct register access; this is much faster than via the Arduino API.
For an example and explanation see [esp32-fast-gpio](esp32-fast-gpio/esp32-fast-gpio.md).


## Fast GPIO writes on an ATMEGA
Set or clear ATMEGA GPIO pins via direct register access; this is much faster than via the Arduino API.
For an example and explanation see [atmega-fast-gpio](atmega-fast-gpio/atmega-fast-gpio.md).


(end)
