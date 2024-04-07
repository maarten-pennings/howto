// spitest-tx.ino - the transmitter in the SPI test setup
#include <SPI.h>

uint8_t triggers; // incremented every trigger

// SPIOUT

#define SPIOUT_SSEL 5
#define SPIOUT_SCLK 18
#define SPIOUT_MOSI 23
#define SPIOUT_FREQ (100*1000)

SPIClass spiout(VSPI);

void spiout_init() {
  spiout.begin(SPIOUT_SCLK, -1, SPIOUT_MOSI, SPIOUT_SSEL); 
  digitalWrite(SPIOUT_SSEL, HIGH);
  pinMode(SPIOUT_SSEL, OUTPUT);
  Serial.printf("spiout: init\n");
}

void spiout_tx() {
  uint8_t spiout_buf[]={triggers, (uint8_t)~triggers, triggers };
  spiout.beginTransaction(SPISettings(SPIOUT_FREQ, MSBFIRST, SPI_MODE0));
  digitalWrite(SPIOUT_SSEL, LOW);
  spiout.transfer(spiout_buf, sizeof spiout_buf);
  digitalWrite(SPIOUT_SSEL, HIGH);
  spiout.endTransaction();
}

// TRIG

#define TRIG_PIN 4

int trig_cur;
int trig_prv;

void trig_scan() {
  trig_prv = trig_cur;
  trig_cur = digitalRead(TRIG_PIN);
}

int trig_rises() {
  return (trig_cur!=trig_prv) && trig_prv==0;
}

void trig_init() {
  pinMode( TRIG_PIN, INPUT_PULLDOWN );
  trig_scan();
  trig_scan();
  Serial.printf("trig: init\n");
}

// Main

void setup() {
  Serial.begin(115200);
  Serial.printf("\nwelcome to spitest-tx\n");
  spiout_init();
  trig_init();
}

void loop() {
  trig_scan();
  if( trig_rises() ) {
    Serial.printf("trig: rises %d\n", ++triggers);
    delayMicroseconds(200); // arbitrary
    spiout_tx();
  }
}


