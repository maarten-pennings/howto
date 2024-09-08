# Arduino CLI

First experiments using the Arduino Command Line Interface (CLI).


## Install

No windows images on [GitHub.com](https://github.com/arduino/arduino-cli/releases).

But I did find images on [GitHub.io](https://arduino.github.io/arduino-cli/1.0/installation/#latest-release).

I copied the exe in the zip to `C:\Programs\ArduinoCLI`.

Seems to work:

```
C:\Programs\ArduinoCLI>arduino-cli version
arduino-cli  Version: 1.0.4 Commit: a0d912da Date: 2024-08-12T13:42:36Z
```


## Create config

I was told to execute

```
C:\Programs\ArduinoCLI>arduino-cli config init
Config file written to: C:\Users\maarten\AppData\Local\Arduino15\arduino-cli.yaml
```

But it creates a rather empty file, so I do not know if it is needed.

```
board_manager:
    additional_urls: []
```

It seems I can change this to

```
board_manager:
  additional_urls: [https://arduino.esp8266.com/stable/package_esp8266com_index.json]
```

but I did _not_ do this. For now, I also skipped `arduino-cli core update-index`.



## Create a sketch

```
arduino-cli sketch new MaartenBlinky
```

This creates a boilerplate project.
I believe in the directory where the command is given.

I used an editor to change the sketch

```
int n;
void setup() {
  Serial.begin(115200);
  Serial.println("Maarten Blinky");
  n=1;
}

void loop() {
  Serial.println(n++);
  delay(5000);
}
```


## Installing boards

I did _not_ install a board like so

```
arduino-cli core install esp8266:esp8266
```

I guess this was not needed, because the ESP8266 board was installed via the IDE, and the CLI uses that too.

```
C:\Programs\ArduinoCLI>arduino-cli core list
ID              Installed Latest Name
arduino:avr     1.8.6     1.8.6  Arduino AVR Boards
attiny:avr      1.0.2     1.0.2  ATtiny Microcontrollers
esp32:esp32     3.0.2     3.0.4  esp32
esp8266:esp8266 3.0.2     3.0.2  ESP8266 Boards (3.0.2)
rp2040:rp2040   3.2.0     3.2.0  Raspberry Pi RP2040 Boards(3.2.0)
```


## Installing libraries

I did _not_ install a library like so.

```
arduino-cli lib install ENS210
```

But this library is known.

```
C:\Programs\ArduinoCLI>arduino-cli lib search ENS210
Downloading index: library_index.tar.bz2 downloaded
Name: "ENS210"
  Author: Maarten Pennings
  Maintainer: Maarten Pennings
  Sentence: Arduino library for the ENS210 relative humidity and temperature sensor with I2C interface from ams
  Paragraph: This library controls the ENS210. The main feature of this library is performing a single shot measurement, retrieving the measurement data, and checking the CRC. Other features include reset, power control and obtaining version information. This library has functions to convert to Kelvin, Celsius and Fahrenheit.
  Website: https://github.com/maarten-pennings/ENS210
  Category: Device Control
  Architecture: *
  Types: Contributed
  Versions: [1.0.0]
```


## Compile for ESP8266

The compile command needs the project, but also the target architecture (via the fqbn).

```
arduino-cli compile --fqbn esp8266:esp8266:generic MaartenBlinky
```

The `esp8266:esp8266:generic` is the Fully Qualified Board Name.

You can find them via

```
arduino-cli board listall
```

For example with Windows "grep"

```
C:\Programs\ArduinoCLI>arduino-cli board listall | findstr "esp8266"
4D Systems gen4 IoD Range                          esp8266:esp8266:gen4iod
Adafruit Feather HUZZAH ESP8266                    esp8266:esp8266:huzzah
Amperka WiFi Slot                                  esp8266:esp8266:wifi_slot
Arduino                                            esp8266:esp8266:arduino-esp8266
DOIT ESP-Mx DevKit (ESP8285)                       esp8266:esp8266:espmxdevkit
Digistump Oak                                      esp8266:esp8266:oak
ESPDuino (ESP-13 Module)                           esp8266:esp8266:espduino
ESPectro Core                                      esp8266:esp8266:espectro
ESPino (ESP-12 Module)                             esp8266:esp8266:espino
ESPresso Lite 1.0                                  esp8266:esp8266:espresso_lite_v1
ESPresso Lite 2.0                                  esp8266:esp8266:espresso_lite_v2
Generic ESP8266 Module                             esp8266:esp8266:generic
Generic ESP8285 Module                             esp8266:esp8266:esp8285
ITEAD Sonoff                                       esp8266:esp8266:sonoff
Invent One                                         esp8266:esp8266:inventone
LOLIN(WEMOS) D1 R2 & mini                          esp8266:esp8266:d1_mini
LOLIN(WEMOS) D1 mini (clone)                       esp8266:esp8266:d1_mini_clone
LOLIN(WEMOS) D1 mini Lite                          esp8266:esp8266:d1_mini_lite
LOLIN(WEMOS) D1 mini Pro                           esp8266:esp8266:d1_mini_pro
LOLIN(WeMos) D1 R1                                 esp8266:esp8266:d1
Lifely Agrumino Lemon v4                           esp8266:esp8266:agruminolemon
NodeMCU 0.9 (ESP-12 Module)                        esp8266:esp8266:nodemcu
NodeMCU 1.0 (ESP-12E Module)                       esp8266:esp8266:nodemcuv2
Olimex MOD-WIFI-ESP8266(-DEV)                      esp8266:esp8266:modwifi
Phoenix 1.0                                        esp8266:esp8266:phoenix_v1
Phoenix 2.0                                        esp8266:esp8266:phoenix_v2
Schirmilabs Eduino WiFi                            esp8266:esp8266:eduinowifi
Seeed Wio Link                                     esp8266:esp8266:wiolink
SparkFun Blynk Board                               esp8266:esp8266:blynk
SparkFun ESP8266 Thing                             esp8266:esp8266:thing
SparkFun ESP8266 Thing Dev                         esp8266:esp8266:thingdev
SweetPea ESP-210                                   esp8266:esp8266:esp210
ThaiEasyElec's ESPino                              esp8266:esp8266:espinotee
WiFi Kit 8                                         esp8266:esp8266:wifi_kit_8
WiFiduino                                          esp8266:esp8266:wifiduino
WifInfo                                            esp8266:esp8266:wifinfo
XinaBox CW01                                       esp8266:esp8266:cw01
```



## Upload

Go to to Device manager to find the COM port, or use the `arduino-cli`.

```
C:\Programs\ArduinoCLI>arduino-cli board list
Port Protocol Type              Board Name FQBN Core
COM3 serial   Serial Port (USB) Unknown
```

Very slow, but uploading.

```
C:\Programs\ArduinoCLI>arduino-cli upload MaartenBlinky  -p COM3  -b esp8266:esp8266:generic
esptool.py v3.0
Serial port COM3
Connecting....
Chip is ESP8266EX
Features: WiFi
Crystal is 26MHz
MAC: 5c:cf:7f:f1:df:77
Uploading stub...
Running stub...
Stub running...
Configuring flash size...
Auto-detected Flash size: 4MB
Flash params set to 0x0340
Compressed 269584 bytes to 197921...
Writing at 0x00000000... (7 %)
Writing at 0x00004000... (15 %)
Writing at 0x00008000... (23 %)
Writing at 0x0000c000... (30 %)
Writing at 0x00010000... (38 %)
Writing at 0x00014000... (46 %)
Writing at 0x00018000... (53 %)
Writing at 0x0001c000... (61 %)
Writing at 0x00020000... (69 %)
Writing at 0x00024000... (76 %)
Writing at 0x00028000... (84 %)
Writing at 0x0002c000... (92 %)
Writing at 0x00030000... (100 %)
Wrote 269584 bytes (197921 compressed) at 0x00000000 in 17.5 seconds (effective 123.1 kbit/s)...
Hash of data verified.

Leaving...
Hard resetting via RTS pin...
New upload port: COM3 (serial)
```

For faster upload, use the ` --board-options` parameter.

```
arduino-cli upload MaartenBlinky -b esp8266:esp8266:generic --port COM3 --board-options baud=3000000
```

(end)
