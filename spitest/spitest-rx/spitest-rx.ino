// spitest-rx.ino - the receiver in the SPI test setup
#include <ESP32SPISlave.h>

// SPIIN

#define SPIIN_SSEL 13
#define SPIIN_SCLK 12
#define SPIIN_MOSI 11
#define SPIIN_MSEL 15

ESP32SPISlave spiin;

volatile uint8_t * volatile mon;
volatile size_t  * volatile len;
void IRAM_ATTR cb(spi_slave_transaction_t *trans, void *arg) {
  mon = (uint8_t*)trans->rx_buffer;
  len = &trans->trans_len;
  *mon = 0x00; // before we begin, init first byte with 0
}

void spiin_init() {
  spiin.setDataMode(SPI_MODE0);
  spiin.begin(FSPI,SPIIN_SCLK,-1,SPIIN_MOSI,SPIIN_SSEL);

  digitalWrite( SPIIN_MSEL, HIGH);
  pinMode( SPIIN_MSEL, OUTPUT );

  spiin.setUserPostSetupCbAndArg(cb, 0);

  Serial.printf("spiin: init\n");
}

uint8_t spiin_buf[4];

// TRIG

#define TRIG_PIN 17

void trig_pulse() {
  digitalWrite( TRIG_PIN, HIGH);
  delayMicroseconds(20);
  digitalWrite( TRIG_PIN, LOW);
}

void trig_init() {
  digitalWrite( TRIG_PIN, LOW);
  pinMode( TRIG_PIN, OUTPUT );
  Serial.printf("trig: init\n");
}



// Main


void setup() {
  Serial.begin(115200);
  Serial.printf("\nwelcome to spitest-rx\n");
  spiin_init();
  trig_init();
}


void loop() {
  // arm spiin
  if( ! spiin.hasTransactionsCompletedAndAllResultsHandled() ) Serial.printf("ERROR not handled\n");
  spiin.queue(NULL, spiin_buf, sizeof spiin_buf);
  spiin.trigger();
  // trigger a send
  trig_pulse();
  // enable reading
  digitalWrite( SPIIN_MSEL, LOW);
  uint32_t start = micros();
  Serial.printf("poll ");
  while( micros()-start < 600 ) {
    Serial.printf("%02X/%02X/%d ", spiin_buf[0], *mon, *len);
  }
  digitalWrite( SPIIN_MSEL, HIGH);
  Serial.printf("\n");
  // check spiin
  if( ! spiin.hasTransactionsCompletedAndAllResultsReady(1) ) Serial.printf("ERROR not ready\n");
  int num = spiin.numBytesReceived();
  Serial.printf("rxed (%d)",num);
  for(int i=0; i<num; i++) Serial.printf(" %02X",spiin_buf[i]);
  Serial.printf("\n");
  delay(2500);
}


