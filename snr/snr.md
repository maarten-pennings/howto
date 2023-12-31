# Signal to Noise Ration (SNR)

Computing the signal to noise ratio (SNR) from a series of measurements.


## Definition of variance

We assume that we have $N$ measurement results $x_i$ (for $i=1..N$).
The average $\bar{x}$ of these measurements is
```math
  \bar{x} = \frac{1}{N} \sum_{i=1}^{N} x_{i}
```

If these $N$ samples are the _entire_ population, the variance is defined as

```math
  V = \frac{1}{N} \sum_{i=1}^{N} (x_{i} - \bar{x})^2
```

However, if the $N$ samples are a _subset_, the variance is computed using 
Bessel's correction (eq 1)

```math
  V = \frac{1}{N-1} \sum_{i=1}^{N} (x_{i} - \bar{x})^2
```


## Optimize computation of variance

To compute the variance using this formula requires storing all $x_{i}$ samples,
so that we can compute the differences once the average is known.
Fortunately there is an alternative.
 
We rewrite the sum in the definition of variance.

```math
  \sum_{i=1}^{N} \left( x_{i} - \bar{x} \right)^2
```

= { expand square }

```math
  \sum_{i=1}^{N} \left( x_{i}^2 - 2\cdot x_{i}\cdot\bar{x} + \bar{x}^2 \right)
```

= { associate sum over - and + }

```math
  \sum_{i=1}^{N} x_{i}^2 - \sum_{i=1}^{N} 2\cdot x_{i}\cdot\bar{x} + \sum_{i=1}^{N} \bar{x}^2
```

= { distribute constants out }

```math
  \sum_{i=1}^{N} x_{i}^2 - 2\cdot\bar{x}\sum_{i=1}^{N} x_{i} + \bar{x}^2 \sum_{i=1}^{N} 1
```

= { sum of $N$ terms 1 }

```math
  \sum_{i=1}^{N} x_{i}^2 - 2\cdot\bar{x}\sum_{i=1}^{N} x_{i} + \bar{x}^2\cdot N
```

= { $\sum x_{i} = N\cdot \bar{x}$ }

```math
  \sum_{i=1}^{N} x_{i}^2 - 2\cdot\bar{x}\cdot N \cdot\bar{x} + N \cdot \bar{x}^2
```

= { calculus }

```math
  \sum_{i=1}^{N} x_{i}^2 - N \cdot \bar{x}^2
```

= { $\bar{x} = \frac{1}{N} \sum x_{i}$ }

```math
  \sum_{i=1}^{N} x_{i}^2 - N \cdot \left( \frac{1}{N} \sum_{i=1}^{N} x_{i} \right)^2
```

= { calculus }

```math
  \sum_{i=1}^{N} x_{i}^2 - \frac{1}{N} \left( \sum_{i=1}^{N} x_{i} \right)^2
```

= { introduce two constants }

```math
  \mbox{\_sum\_sq} - \frac{1}{N} \mbox{\_sum}^2
```

= { calculus }

```math
  \left( N\cdot\mbox{\_sum\_sq} - \mbox{\_sum}^2 \right) / N
```


## Formula for variance

This results in a new formula for variance.

```math
  \mbox{\_var} = \left( N\cdot\mbox{\_sum\_sq} - \mbox{\_sum}^2 \right) / N / (N-1)
```


## Implementation in C

We will now give an implementation in C.
We pay special attention to overflow and floating point inaccuracy.

We assume the samples $x_{i}$ are measurements from a sensor that 
reports 16 bits unsigned integer measurements.
The function `add(uint16_t x)` accumulates measurement data.

```c
  uint16_t _n      = 0;
  uint32_t _sum    = 0;
  uint64_t _sum_sq = 0; // uint48_t

  void add(uint16_t x) {
    _n      += 1;  
    _sum    += x;
    _sum_sq += x * (uint32_t)x;
  }
```

Note that data samples are 16 bit.
We restrict the number of samples (`_n`) to 65535, or 16 bits too.
This means that the maximum value of `_sum` fits in 32 bits.
Since a data sample is 16 bits, its square is 32 bits, and summing 16 bits of those
leads to a maximum size for `_sum_sq` of 48 bits.
So, by limiting `_n` to 65535, `_n`, `_sum`, and `_sum_sq` fit in the assigned data types
(and the data type for `_sum_sq` is even 16 bits too large).
Also note the last expression `x * (uint32_t)x` has a typecast.
This is needed because `x` is 16 bit, and this code might be compiled on a 16 bit platform:
we need to widen the expression to 32 bits to ensure the result of the multiplication is 32 bits.

To compute the variance, we start by computing its numerator `_n * _sum_sq  -  _sum * _sum`.
Observe that the first term is 16 bits times 48 bits, so 64 bits, and the
second term is 32 bits time 32 bits so also 64 bits. 
Both terms are positive, and the second is subtracted from the first so there can be no overflow at MAX_UNIT64.
Also note that the variance is never negative so there can be no underflow at 0. 
Finally note the since we compute the numerator as integer, we do not have floating point accuracy errors.

Next, we compute the _variance_ (numerator divided by denominator), but this
requires we switch to float (again a typecast). The _standard deviation_ is the square root
of the variance. The _signal to noise ratio_ is defined as the average (`_mu`)
divided by the standard deviation (`_sd`). As a last step, we express that in decibel (dB).

```c
  float snr_in_dB() {
    uint64_t _numer = _n * _sum_sq  -  _sum * (uint64_t)_sum;
    float    _var   = _numer / (float)_n / ( _n - 1 );
    float    _sd    = sqrt(_var);
    float    _mu    = (float)_sum / _n;
    float    _snr   = _mu / _sd;
    float    _db    = 20 * log( _snr ) / log(10);
    return   _db;
  }
```

## Arduino

An implementation of the C-code is given in this [Arduino sketch](snr-sketch).

This is the output of the example

```text
Welcome to SNR

_n 40 _sum 2000 _sum_sq 100482
_numer 19280 _var 12.358974 _sd 3.515533 _mu 50.000000
_snr 14.222593 _db
snr = 23.059576 dB
```

Compare that with this [spreadsheet](snr.xlsx).
Observe that the spreadsheet has three implementations:
- yellow, using the math formula (eq 1)
- green, using excel's built-in formula's
- blue, the c-code from this howto (but then in excel).

(end)
