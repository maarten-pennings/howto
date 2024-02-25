# SPI modes

SPI communication knows much more variation than e.g. I2C.
This "how to" looks at the four modes induced
by CPOL (default clock state) and CPHA (data valid phase).

Arduino has the [following table](https://docs.arduino.cc/learn/communication/spi) giving an overview of the modes.

![SPI Modes table](SPImodesTable.png)

The [sketch](SPImodes.ino) is available.
The traces are made with [Saleae](https://www.saleae.com/).


## Mode 0

![SPI mode0 trace](SPImode0trace.png)

![SPI mode0 settings](SPImode0settings.png)


## Mode 1

![SPI mode1 trace](SPImode1trace.png)

![SPI mode1 settings](SPImode1settings.png)


## Mode 2

![SPI mode2 trace](SPImode2trace.png)

![SPI mode2 settings](SPImode2settings.png)


## Mode 3

![SPI mode3 trace](SPImode3trace.png)

![SPI mode3 settings](SPImode3settings.png)

(end)
