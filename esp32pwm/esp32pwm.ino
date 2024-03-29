// ESP32PWM test

//                 |\  |
//                 | \ |  +-----+
// +---------------|  >|--| 10R |--+
// |     +-----+   | / |  +-----+  |
// |     |     |   |/  |           |
// |     |ESP32| LED 150mA         | +-----+
// |     |     |                    /C     |
// |     |     | (D16)   +-----+   /       |
// |     |     + -RX2----| 10k |---|B BC547|
// |     |     |         +-----+   \       |
// +-VIN-+     + -GND---------------\E     |
//       |     |                     +-----+
//       +-|-|-+
//         +-+
//         USB
//
// At max PWM, the LED, the ESP32 and the builtin LED together consume 70mA


// PWM settings
const int pwmfreq = 5000;
const int pwmchan = 0;
const int pwmbits = 8;
const int pwmgpio = 16; // aka rx2


void setup(){
  Serial.begin(115200); delay(2000);
  Serial.printf("Welcome to ESP32PWM test\n");

  // Signalling LED
  digitalWrite(LED_BUILTIN, LOW);
  pinMode(LED_BUILTIN, OUTPUT);

  // Configure PWM channel
  ledcSetup(pwmchan, pwmfreq, pwmbits);
  // Attach the PWM channel to the GPIO pin
  ledcAttachPin(pwmgpio, pwmchan);
}


// https://electronics.stackexchange.com/questions/1983/correcting-for-non-linear-brightness-in-leds-when-using-pwm
uint8_t pwmduty[] = {0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,2,2,2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5,6,6,6,7,7,7,8,8,8,
  9,9,9,10,10,11,11,11,12,12,13,13,14,14,15,15,16,16,17,17,18,18,19,19,20,20,21,21,22,23,23,24,24,25,26,26,27,
  28,28,29,30,30,31,32,32,33,34,35,35,36,37,38,38,39,40,41,42,42,43,44,45,46,47,47,48,49,50,51,52,53,54,55,
  56,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,73,74,75,76,77,78,79,80,81,82,84,85,86,87,88,89,91,92,
  93,94,95,97,98,99,100,102,103,104,105,107,108,109,111,112,113,115,116,117,119,120,121,123,124,126,127,128,
  130,131,133,134,136,137,139,140,142,143,145,146,148,149,151,152,154,155,157,158,160,162,163,165,166,168,170,
  171,173,175,176,178,180,181,183,185,186,188,190,192,193,195,197,199,200,202,204,206,207,209,211,213,215,217,
  218,220,222,224,226,228,230,232,233,235,237,239,241,243,245,247,249,251,253,255}; 


void loop(){
  digitalWrite(LED_BUILTIN, HIGH);
  Serial.printf("brighter\n");
  for(int level=0; level<=255; level++){   
    ledcWrite(pwmchan, pwmduty[level]);
    delay(100);
  }

  digitalWrite(LED_BUILTIN, LOW);
  Serial.printf("dimmer\n");
  for(int level=255; level>=0; level--){
    ledcWrite(pwmchan, pwmduty[level]);   
    delay(100);
  }
}
