// esp32-fast-gpio.ino - set ESP32 GPIO pins via direct register access
// see https://github.com/maarten-pennings/howto


// Pick the GPIO pins
#define PIN_TEST1 32
#define PIN_TEST2 23


void setup() {
  Serial.begin(115200);
  delay(1500);
  Serial.printf("\n\nWelcome to esp32-fast-gpio\n\n");

  // Configure pins as outputs
  pinMode(PIN_TEST1, OUTPUT);
  pinMode(PIN_TEST2, OUTPUT);
}


void loop() {
  //digitalWrite( PIN_TEST1, LOW);
  GPIO.out1_w1tc.val = 1UL << (PIN_TEST1-32); // GPIO0~31 output value write 1 to clear

  //digitalWrite( PIN_TEST2, LOW);
  //GPIO.out_w1tc = 1UL << PIN_TEST2;
  *(uint32_t*)0x3FF4400C = 0b100000000000000000000000;

  delay(1);

  //digitalWrite( PIN_TEST1, HIGH);
  GPIO.out1_w1ts.val = 1UL << (PIN_TEST1-32); // GPIO0~31 output value write 1 to set

  //digitalWrite( PIN_TEST2, HIGH);
  GPIO.out_w1ts = 1UL << PIN_TEST2;

  delay(1);
}
