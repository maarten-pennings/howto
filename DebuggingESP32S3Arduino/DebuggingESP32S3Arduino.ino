int n;

void setup() {
  Serial.begin(115200);
  delay(2000);
  Serial.printf("\nSerial : ESP32-S3 test\n");
  n=3000;
}

void loop() {
  n= n+1;
  digitalWrite(LED_BUILTIN, n%2 );
  Serial.printf("Serial : %d\n",n);
  delay(1000);
}
