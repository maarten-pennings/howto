#include <SPI.h>

#define SPI_MISO   12
#define SPI_MOSI   13
#define SPI_SCLK   14
#define SPI_SSEL   15


#define SPI_FREQ   1000000


SPIClass * spi;


void setup() {
  spi = new SPIClass(HSPI);
  spi->begin(SPI_SCLK, SPI_MISO, SPI_MOSI, SPI_SSEL);
}


void loop() {
  spi->beginTransaction(SPISettings(SPI_FREQ, MSBFIRST, SPI_MODE3));
  spi->transfer(0xAD);
  spi->endTransaction();
}
