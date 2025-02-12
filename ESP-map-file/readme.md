# Map file in ESP

When compiling in Arduino, it is not obvious how to get a map file.
For ESP32, it turns out, map files are generated by default, 
but stored in an "obscure" location.


## Intermezzo

How come map files are generated?

Arduino has a `platform.txt` file that governs how builds are performed.
It is also a puzzle to find _that_ file, but on my (current) system I found
it here

```
"C:\Users\maarten\AppData\Local\Arduino15\packages\esp32\hardware\esp32\3.0.2\platform.txt"
```

When we look in that file (around line 155), the important build step is this one (line ends added by me):

```
## Combine gc-sections, archives, and objects
recipe.c.combine.pattern="{compiler.path}{compiler.c.elf.cmd}" 
  {compiler.c.elf.flags} 
  {compiler.c.elf.extra_flags} 
  -Wl,--start-group {object_files} 
  "{archive_file_path}" 
  {build.extra_libs} 
  {build.zigbee_libs} 
  {compiler.c.elf.libs} 
  {compiler.libraries.ldflags} 
  -Wl,--end-group 
  -Wl,-EL -o "{build.path}/{build.project_name}.elf"
```

The interesting part is `{compiler.c.elf.extra_flags}`.

Normally, we would create a file `platform.local.txt` in the same directory
as `platform.txt` and override `{compiler.c.elf.extra_flags}` to include 
generation of a map file.

But what do we see in `platform.txt`?
Around line 70 (abridged by me) there is a definition of `compiler.c.elf.extra_flags` 
with map-file generation.


```
# These can be overridden in platform.local.txt
compiler.c.extra_flags=-MMD -c
compiler.c.elf.extra_flags="-Wl,--Map={build.path}/{build.project_name}.map" 
compiler.ar.extra_flags=
```


## Where is the map file

So every build, we get a map file. But where is it?
It is in the temp directory where Arduino builds our project.
And that temp directory varies from project to project (and from IDE restart to restart).

The only way I know to find it, is to go to File > Preferences ... > tab Settings > Show verbose output during > check compile.

When we compile, we get an enormous amount of log lines in Output.
These are the last lines.

```
Linking everything together...
"C:\\Users\\maarten\\AppData\\Local\\Arduino15\\packages\\esp32\\tools\\esp-x32\\2302/bin/xtensa-esp32-elf-g++" "@C:\\Users\\maarten\\AppData\\Local\\Arduino15\\packages\\esp32\\tools\\esp32-arduino-libs\\idf-release_v5.1-bd2b9390ef\\esp32/flags/ld_flags" "@C:\\Users\\maarten\\AppData\\Local\\Arduino15\\packages\\esp32\\tools\\esp32-arduino-libs\\idf-release_v5.1-bd2b9390ef\\esp32/flags/ld_scripts" "-Wl,--Map=C:\\Users\\maarten\\AppData\\Local\\Temp\\arduino\\sketches\\4AEB01FA0AAE08D43AC944F3B502E71D/esp32-fast-gpio-in.ino.map" "-LC:\\Users\\maarten\\AppData\\Local\\Arduino15\\packages\\esp32\\tools\\esp32-arduino-libs\\idf-release_v5.1-bd2b9390ef\\esp32/lib" "-LC:\\Users\\maarten\\AppData\\Local\\Arduino15\\packages\\esp32\\tools\\esp32-arduino-libs\\idf-release_v5.1-bd2b9390ef\\esp32/ld" "-LC:\\Users\\maarten\\AppData\\Local\\Arduino15\\packages\\esp32\\tools\\esp32-arduino-libs\\idf-release_v5.1-bd2b9390ef\\esp32/dio_qspi" -Wl,--wrap=esp_panic_handler -Wl,--start-group "C:\\Users\\maarten\\AppData\\Local\\Temp\\arduino\\sketches\\4AEB01FA0AAE08D43AC944F3B502E71D\\sketch\\esp32-fast-gpio-in.ino.cpp.o" "C:\\Users\\maarten\\AppData\\Local\\Temp\\arduino\\cores\\a5c673556e6ce5af1bc5d61cbb823a08\\core.a" "@C:\\Users\\maarten\\AppData\\Local\\Arduino15\\packages\\esp32\\tools\\esp32-arduino-libs\\idf-release_v5.1-bd2b9390ef\\esp32/flags/ld_libs" -Wl,--end-group -Wl,-EL -o "C:\\Users\\maarten\\AppData\\Local\\Temp\\arduino\\sketches\\4AEB01FA0AAE08D43AC944F3B502E71D/esp32-fast-gpio-in.ino.elf"
"C:\\Users\\maarten\\AppData\\Local\\Arduino15\\packages\\esp32\\tools\\esptool_py\\4.6/esptool.exe" --chip esp32 elf2image --flash_mode dio --flash_freq 80m --flash_size 4MB --elf-sha256-offset 0xb0 -o "C:\\Users\\maarten\\AppData\\Local\\Temp\\arduino\\sketches\\4AEB01FA0AAE08D43AC944F3B502E71D/esp32-fast-gpio-in.ino.bin" "C:\\Users\\maarten\\AppData\\Local\\Temp\\arduino\\sketches\\4AEB01FA0AAE08D43AC944F3B502E71D/esp32-fast-gpio-in.ino.elf"
esptool.py v4.6
...
...
"C:\\Users\\maarten\\AppData\\Local\\Arduino15\\packages\\esp32\\tools\\esp-x32\\2302/bin/xtensa-esp32-elf-size" -A "C:\\Users\\maarten\\AppData\\Local\\Temp\\arduino\\sketches\\4AEB01FA0AAE08D43AC944F3B502E71D/esp32-fast-gpio-in.ino.elf"
Sketch uses 280941 bytes (21%) of program storage space. Maximum is 1310720 bytes.
Global variables use 20192 bytes (6%) of dynamic memory, leaving 307488 bytes for local variables. Maximum is 327680 bytes.
```

The crucial section is `Linking everything together...`.
There we see our map file.

```
C:\\Users\\maarten\\AppData\\Local\\Temp\\arduino\\sketches\\
  4AEB01FA0AAE08D43AC944F3B502E71D/esp32-fast-gpio-in.ino.map"
```

The good news is that the third but last line already discloses the build directory.

```
"C:\\Users\\maarten\\AppData\\Local\\Arduino15\\packages\\esp32\\tools\\esp-x32\\2302/bin/xtensa-esp32-elf-size" 
  -A "C:\\Users\\maarten\\AppData\\Local\\Temp\\arduino\\sketches\\4AEB01FA0AAE08D43AC944F3B502E71D/esp32-fast-gpio-in.ino.elf"
```

Once we have `4AEB01FA0AAE08D43AC944F3B502E71D`,
We can open the explorer there

```
C:\Users\maarten\AppData\Local\Temp\arduino\sketches\4AEB01FA0AAE08D43AC944F3B502E71D
```

And there we find the map file

```
esp32-fast-gpio-in.ino.map
```

The `esp32-fast-gpio-in.ino` is the name of the sketch.


## New directory

We could also create a file `platform.local.txt` next to `platform.txt` with just one line.
In the below fragment we defined that the map file goes to the desktop.

```
compiler.c.elf.extra_flags="-Wl,--Map=C:\Users\maarten\Desktop\{build.project_name}.map" 
  "-L{compiler.sdk.path}/lib" "-L{compiler.sdk.path}/ld" 
  "-L{compiler.sdk.path}/{build.memory_type}" "-Wl,--wrap=esp_panic_handler"
```

## Understanding the map file

That is a different howto :-(

(end)
