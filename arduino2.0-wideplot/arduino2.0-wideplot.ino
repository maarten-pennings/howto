// arduino2.0-wideplot - Configure Arduino plotter for wider x-axis
// see https://github.com/maarten-pennings/howto


void setup() {
  Serial.begin(115200);
}


float t;
void loop() {
  Serial.printf("min:-10 max:+10 sin:%f\n",9.0*sin(t/180*3.14159));
  t = t + 1;
}
