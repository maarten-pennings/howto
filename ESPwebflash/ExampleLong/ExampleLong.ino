// ExampleLong.ino - blinky with long pulses and serial prints

void setup() {
  Serial.begin(115200);
  Serial.printf("Welcome to ExampleLong\n");
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  digitalWrite(LED_BUILTIN, HIGH);
  delay(900);
  digitalWrite(LED_BUILTIN, LOW);
  delay(100);
  Serial.printf("long\n");
}
