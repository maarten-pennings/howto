// snr-sketch.ino - Arduino sketch to compute SNR from samples
// see https://github.com/maarten-pennings/howto


uint16_t x[] = {52, 51, 45, 50, 50, 46, 55, 46, 49, 51, 55, 52, 48, 45, 45, 55, 52, 46, 55, 48, 49, 45, 53, 45, 45, 53, 51, 49, 55, 55, 45, 49, 50, 52, 51, 46, 51, 55, 54, 51};

uint16_t _n      = 0;
uint32_t _sum    = 0;
uint64_t _sum_sq = 0; // uint48_t

void add(uint16_t x) {
  _n      += 1;  
  _sum    += x;
  _sum_sq += x * (uint32_t)x;
}

float snr_in_dB() {
  Serial.printf("_n %u _sum %lu _sum_sq %llu\n",_n,_sum,_sum_sq);
  uint64_t _numer = _n * _sum_sq  -  _sum * (uint64_t)_sum;
  float    _var   = _numer / (float)_n / ( _n - 1 );
  float    _sd    = sqrt(_var);
  float    _mu    = (float)_sum / _n;
  Serial.printf("_numer %llu _var %f _sd %f _mu %f\n",_numer,_var,_sd,_mu);
  float    _snr   = _mu / _sd;
  float    _db    = 20 * log( _snr ) / log(10);
  Serial.printf("_snr %f _db\n",_snr,_db);
  return   _db;
}

void setup() {
  Serial.begin(115200);
  delay(1500);
  Serial.printf("\n\nWelcome to SNR\n\n");

  for( int i=0; i<sizeof(x)/sizeof(uint16_t); i++ )
    add(x[i]);
  
  Serial.printf("snr = %f dB\n", snr_in_dB() );
}

void loop() {
  Serial.printf(".");
  delay(10*1000);
}
