# Wide Arduino Serial plotter

The Serial Plotter in Arduino 2.0 has a too narrow x-axis. That can be patched wider.


## Introductions

An Arduino sketch can issue `Serial.print` to print numbers, which can than be graphed.

To be more precise, the sketch shall only print numbers, optionally prefixed with a labels, as in below example.

```C
  Serial.printf("min:-10 max:+10 sin:%f\n",9.0*sin(t/180*3.14159));
```

Then Tools > Serial Plotter will output something like

![A (narrow) plot](narrow.png)

In Arduino 1.8, this serial plotter had an x-axis size of 500, but in Arduino 2.0/2.1/2.2 (and maybe up) 
the x-axis is only 50, and can not be configured.


## Making the serial plotter wider

[Someone found out](https://github.com/arduino/arduino-ide/issues/803#issuecomment-1338149431) that the serial plotter is a web application.
The source of that web application (html, css, js) are part of the Arduino intall, otherwise it could not be run.
But that also means we can change that source.

On one PC, I have the source in this directory
`…\AppData\Local\Programs\Arduino IDE 2\resources\app\node_modules\arduino-serial-plotter-webapp\build\static\js`
but on another PC is is in this directory
`C:\Program Files\ArduinoIDE2\Arduino IDE\resources\app\lib\backend\resources\arduino-serial-plotter-webapp\static\js`.
I'm note sure where the difference comes from (install for one user, install for all).

Anyhow, locate the file `main.35ae02cb.chunk.js` in that directory, search for `(50)` and 
change `Object(o.useState)(50)` to `Object(o.useState)(500)`

![A (500 wide) plot](wide.png).

## Demo

I used [arduino2.0-wideplot.ino](arduino2.0-wideplot.ino) as demo app.

(end)
