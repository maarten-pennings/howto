// ExampleShort.ino - blinky with short pulses and serial prints

void setup() {
  Serial.begin(115200);
  Serial.printf("Welcome to ExampleShort\n");
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  digitalWrite(LED_BUILTIN, HIGH);
  delay(100);
  digitalWrite(LED_BUILTIN, LOW);
  delay(900);
  Serial.printf("short\n");
}
