// esp32-opendrain.ino - test open drain in ESP32
// see https://github.com/maarten-pennings/howto

// Tested on DOIT ESP32  DEVKIT V1


// === Open Drain =============================================


// The pin we control as open drain
#define OD_PIN      23 


// Pull the pin to ground
void od_pulldown() {
  digitalWrite(OD_PIN, LOW);
}


// Release the pin to floating (since we engaged a weak pull-up the pin goes high)
void od_release() {
  digitalWrite(OD_PIN, HIGH);
}


// Configures GPIO pin as open drain
// This works on ESP32, probably not on plain Arduinos
void od_init() {
  Serial.printf("od  : pin %d can output %d\n",OD_PIN ,digitalPinCanOutput(OD_PIN) );
  Serial.printf("od  : feel free to ground pin (eg during release)\n");
  // I added INPUT, this allows read-back From esp32 2.0.12 onwards this is merged into OUTPUT_OPEN_DRAIN
  // pinMode(OD_PIN, INPUT | OUTPUT_OPEN_DRAIN ); // no internal pull-up
  pinMode(OD_PIN, INPUT | OUTPUT_OPEN_DRAIN | PULLUP ); // engage built-in pull-up
  od_release();
  Serial.printf("od  : init\n");
}


// === Main application =========================================


int pulldown_activated;
uint32_t last;


void setup() {
  Serial.begin(115200);
  delay(1500);
  Serial.printf("\n\nWelcome to esp32-opendrain\n");

  od_init();
  pulldown_activated = 0;
  last = millis() - 10*1000;
}


void loop() {
  if( millis()-last >= 5*1000 ) {
    // time to toggle pin
    Serial.printf("\n");
    if( pulldown_activated )  { 
      od_release(); 
      pulldown_activated=0; 
      Serial.printf("od  : engaged release (typically 1, except when externally grounded\n");
    } else {
      od_pulldown(); 
      pulldown_activated=1; 
      Serial.printf("od  : engaged pulldown (always 0)\n");
    }
    Serial.printf("od  : reading ");
    last = millis();
  }

  Serial.printf("%d",digitalRead(OD_PIN) );
  delay(50);
}
