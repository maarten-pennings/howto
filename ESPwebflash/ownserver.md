# Cloning esptool

This is a log of my experiment cloning Espressif's esptool.
Clone here means getting their sources run on my webserver.


## Overview

- Download and install nodejs with npm - _this implements the typescript compiler_
- Download and unzip esptool-js - _the actual typescript sources of the webflasher_
- Compile esptool typescript to javascript - _compile and test_
- Activate with IIS - _get it running in a real web server_


## Steps

- Downloaded standalone binary from [nodejs](https://nodejs.org/en/download/)
  and unpacked it to `C:\programs\node-v22.15.1-win-x64`
  
- Added PATH to that dir.

- Downloaded and unzipped [esptool-js](https://github.com/espressif/esptool-js)
  to desktop `C:\Users\mpen\Desktop\esptool-js`.

- Started `cmd` and ran `npm install` from the example, that is in 
  `C:\Users\mpen\Desktop\esptool-js\esptool-js-main\examples\typescript`.

  ```
  npm warn deprecated inflight@1.0.6: This module is not supported, and leaks memory. Do not use it. Check out lru-cache if you want a good and tested way to coalesce async requests by a key value, which is much more comprehensive and powerful.
  npm warn deprecated glob@7.2.3: Glob versions prior to v9 are no longer supported

  added 303 packages, and audited 304 packages in 15s

  147 packages are looking for funding
    run `npm fund` for details

  found 0 vulnerabilities
  ```
  
  Hmm two warnings.
  
- Ran `npm run dev` in same cmd and dir.

  ```
  > typescript@1.0.0 dev
  > npm-run-all clean genDocs parcel:dev


  > typescript@1.0.0 clean
  > shx rm -rf dist .parcel-cache


  > typescript@1.0.0 genDocs
  > npm run genDocs:root && shx mkdir -p dist && shx cp -r ../../docs dist


  > typescript@1.0.0 genDocs:root
  > cd ../.. && npm run genDocs


  > esptool-js@0.5.4 genDocs
  > rimraf docs && typedoc

  [warning] ResetStrategy, defined in ./src/reset.ts, is referenced by ClassicReset but not included in the documentation.
  [warning] FlashReadCallback, defined in ./src/esploader.ts, is referenced by ESPLoader.readFlash.readFlash.onPacketReceived but not included in the documentation.
  [info] Documentation generated at ./docs

  > typescript@1.0.0 parcel:dev
  > cross-env PARCEL_WORKERS=0 parcel src/index.html

  - Building index.html...
  Server running at http://localhost:1234
  √ Built in 628ms
  ```

  Then tried `http://localhost:1234` in chrome.
  
  **It seemed to work**
  
  Pressed control-C in cmd to stop the webserver.

- Then, again in same cmd and dir, ran `npm run build`

  ```
  > typescript@1.0.0 build
  > npm-run-all clean genDocs parcel:build


  > typescript@1.0.0 clean
  > shx rm -rf dist .parcel-cache


  > typescript@1.0.0 genDocs
  > npm run genDocs:root && shx mkdir -p dist && shx cp -r ../../docs dist


  > typescript@1.0.0 genDocs:root
  > cd ../.. && npm run genDocs


  > esptool-js@0.5.4 genDocs
  > rimraf docs && typedoc

  [warning] ResetStrategy, defined in ./src/reset.ts, is referenced by ClassicReset but not included in the documentation.
  [warning] FlashReadCallback, defined in ./src/esploader.ts, is referenced by ESPLoader.readFlash.readFlash.onPacketReceived but not included in the documentation.
  [info] Documentation generated at ./docs

  > typescript@1.0.0 parcel:build
  > cross-env PARCEL_WORKERS=0 parcel build src/index.html --no-optimize --public-url ./

  \ Building index.html...
  √ Built in 795ms

  dist\index.html                          6.07 kB    110ms
  dist\favicon.ee2246ac.ico               15.41 kB     79ms
  dist\esp-logo.e558125a.png              18.98 kB     84ms
  dist\typescript.8928628d.js            372.72 kB    112ms
  dist\stub_flasher_32.3d9ab3ed.js         5.34 kB    112ms
  dist\stub_flasher_32c2.e43b19ff.js       5.14 kB    112ms
  dist\stub_flasher_32c3.c5d433d8.js        5.8 kB    112ms
  dist\stub_flasher_32c5.1287eb63.js       5.69 kB    112ms
  dist\stub_flasher_32c6.b0cbc065.js       5.69 kB    112ms
  dist\stub_flasher_32c61.c24dbc8b.js      5.69 kB    112ms
  dist\stub_flasher_32h2.d77b4ab0.js       5.69 kB    112ms
  dist\stub_flasher_32p4.e49e5065.js       5.54 kB    112ms
  dist\stub_flasher_32s2.af25aa38.js       6.56 kB    112ms
  dist\stub_flasher_32s3.64c2ffa5.js       7.81 kB    112ms
  dist\stub_flasher_8266.2c4bd201.js      12.44 kB    112ms
  dist\esp32.d9c897f5.js                   6.08 kB    112ms
  dist\esp32c2.4315955a.js                 3.92 kB    112ms
  dist\esp32c3.70b29e70.js                 4.65 kB    111ms
  dist\esp32c6.52a7233b.js                 3.34 kB    111ms
  dist\esp32c61.d3570c8f.js                 5.8 kB    111ms
  dist\esp32c5.c0b86a3d.js                 6.13 kB    111ms
  dist\esp32h2.d34a7ee2.js                 2.89 kB    111ms
  dist\esp32s3.f3144e52.js                 7.56 kB    111ms
  dist\esp32s2.78102e0a.js                10.94 kB    111ms
  dist\esp8266.4c08e62b.js                 4.13 kB    111ms
  dist\esp32p4.e74d7c20.js                 8.57 kB    111ms
  ```

- Activated IIS (web server) on windows, see e.g. 
  [supportyourtech](https://www.supportyourtech.com/tech/how-to-enable-iis-on-windows-11-a-step-by-step-installation-guide/)
  for instructions.

- Copied all dist files 
  from `C:\Users\mpen\Desktop\esptool-js\esptool-js-main\examples\typescript\dist`
  to `C:\inetpub\wwwroot\dist`.
  
- Tested `http://localhost/dist/` in the browser.

(end)
