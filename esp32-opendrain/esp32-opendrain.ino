// esp32-opendrain.ino - test open drain in ESP32
// see https://github.com/maarten-pennings/howto


#define OD_PIN      23 


void od_pulldown() {
  digitalWrite(OD_PIN, LOW);
}


void od_release() {
  digitalWrite(OD_PIN, HIGH);
}


// Configures GPIO pin as open drain
// This works on ESP32, also on plain Arduinos?
void od_init() {
  Serial.printf("od  : pin %d can output %d\n",OD_PIN ,digitalPinCanOutput(OD_PIN) );
  // pinMode(OD_PIN, OUTPUT_OPEN_DRAIN ); 
  pinMode(OD_PIN, OUTPUT_OPEN_DRAIN | PULLUP ); // engage built-in pull-up
  od_release();
  Serial.printf("od  : init\n");
}


int pulldown_activated;
uint32_t last;

void setup() {
  Serial.begin(115200);
  delay(1500);
  Serial.printf("\n\nWelcome to esp32-opendrain\n");
  Serial.printf("\n\nFeel free to ground the pin\n");

  od_init();
  pulldown_activated = 0;
  last = millis() - 10*1000;
}


void loop() {
  if( millis()-last >= 10*1000 ) {
    // time to toggle pin
    Serial.printf("\n");
    if( pulldown_activated )  { 
      od_release(); 
      pulldown_activated=0; 
      Serial.printf("od  : release\n");
    } else {
      od_pulldown(); 
      pulldown_activated=1; 
      Serial.printf("od  : pulldown\n");
    }
    last = millis();
  }

  Serial.printf("%d",digitalRead(OD_PIN) );
  delay(50);
}
