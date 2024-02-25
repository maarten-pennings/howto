#include "mylib.h"

void setup() {
  Serial.begin(115200); 
  Serial.printf("\n\nlinked\n");
}

void loop() {
  int x = random(100);
  int y = mylib_succ(x);
  Serial.printf("linked(%d)=%d",x,y);
  delay(2000);
}
