# C64 drive

The drives (like the 1541) that come with the Commodore 64 (C64) are called _smart_.
This naming refers to the fact that the disk operating system is implemented in the drive, not in the computer (C64).
The computer sends a command (a string) to the drive, and the drive interprets the command and executes it.


## Communication

Drive devices are connected to a serial bus.
The C64 has _one_ serial port. Typically, a serial cable is plugged into that port and the other end is plugged into a drive device.
A drive device has _two_ serial port; they are identical. The other port can be used to plug in another cable to run to a second drive device (or a printer or a ...).
In other words, devices are _daisy chained_ on the serial bus. Every device on the bus has a hardwired (typically with dip switches on that device) _device number_.
Disk drive device numbers range from 8 up to 15.

Within a drive _device_ - a physical enclosure with an incoming serial port, an outgoing serial port and a set of 
dip switches that configure a device number, there could be two drive _units_ - a spindle and head and an opening to insert a disk. 
When sending a command to a drive device, the command string includes a drive unit id (e.g. 0 or 1).
If the drive unit id is absent, it usually defaults to 0.

![Serial bus](drives.drawio.png)

In the past maybe there were drive devices with two drive units. But those no longer appear to exist 
- or [do they](https://bitbinders.com/products/commodore-1581dv).
Therefore, in the remainder of this document, we will no longer use the term "drive device" but simply "drive" or "device".

Since a program might have more then one file open on a drive (remember that the disk operating system is in the drive),
the drive needs to differentiate between them. This is done with so-called _secondary addresses_. 
One aspects of a secondary address is that it has a 256 byte buffer on the drive; other aspects 
associtaed with a secomdary address are pointers to the current track, sector and (byte) offset.

To [open](https://www.c64-wiki.com/wiki/OPEN) a file the following command is given.

```
open <logical_file_number> , <device_number> , <secondary_address> , <command_string>
```

This allocates a file handle on the C64 (e.g. a buffer) identified by `<logical_file_number>`.
The handle is associated with a file on device `<device_number>`, but since there could be more,
specifically using handle `<secondary_address>` on the drive. 

For example, this opens two sequential files on device 8. The have handles 2 and 3 on the C64 and 5 and 6 on the drive.

```
OPEN 2, 8, 5, "FILENAME,SEQ,READ" 
OPEN 3, 8, 6, "FILENAME,SEQ,WRITE" 
```

Yes that is confusing, so you see a lot of programs keeping the two handles equal (`open 15,8,15`).

Three secondary addresses are special:
- secondary address 0 is dedicated for LOAD; the file type is implicitly PRG and the mode is implicitly READ.
- secondary address 1 is dedicated for SAVE; the file type is implicitly PRG and the mode is implicitly WRITE.
- secondary address 15 is not for managing files, rather it allows to give _commands_ to the device.

Device commands are the way the disk operating system is used. As an example, see the following "new" command,
which formats a disk. It assigns name `DISKNAME` (disk names have a maximum length of 16 characters) and 
identifier `ID` (disk identifiers are exactly 2 characters) to the disk.

```
OPEN 1, 8, 15, "N0:DISKNAME,ID" 
```

For other examples see [c64-wiki](https://www.c64-wiki.com/wiki/Commodore_1541), or [manual](https://www.mocagh.org/cbm/c1541II-manual.pdf).


An example of a complex administrative command is the following: it seems to change the [device number](https://www.c64-wiki.com/wiki/Device_number).

```
OPEN 2,8,15:PRINT#2,"M-W";CHR$(119);CHR$(0);CHR$(2);CHR$(devnum+32);CHR$(devnum+64):CLOSE 2
```

## Example basic programs

### filedump

This basic program prints a hex dump of a file.

Lines 100-130 records in `DK` the device number of the disk and inputs in `NM$` the name of the file to dump.
Line 200 opens the file on (unit 0 in device 8) using 3 as file handle on the C64 and on the drive.

![filedump](filedump.png)

Statement `GET#3,B$` gets exactly one byte from the file (handle 3) and assigns that to `B$`.
`B$` has therefore always a length of 1 except when the read byte is 0x00, that doesn't match with basic strings.
If that happens, `B$` is empty. This special case is repaired on line 300: 
`B` is the read byte (`B$` or 0x00) after the line is executed.

Line 320 prints the address (in hex) of the row (if address is nr 0 of a block of 8).
Line 330 prints the read byte (8in hex).
Line 360 converts byte `B` to printable character `C` or to `.` (char 46) when not printable.
Those characters are accumulated in `C$` on line 370, which is printed by routine 995, 
for each complete line (at 380), and for the remaining characters of the last incomplete line (400).

On line 310 `GET` updates `ST`, if it is non-zero in line 390, lines 400 and 410 terminate the program.

The subroutine at line 900 prints (numeric) variable `D` to a _two_ character string 
with the hex representation of `D`. It uses `DH` and `DL` as scratch variables.
The subroutine at line 800 prints (numeric) variable `DD` to a _four_ character string 
with the hex representation of `DD`. It calls 800 twice, so uses `D`, `DH` and `DL` as scratch variables.

The following shows filedump dumping itself.

![filedump](filedump-run.png)

The first two bytes (white: 01 08) is the address where to load this program (0x0801).

The next two bytes (red: 15 08) store the link, the address of the next basic line (0x0815).
The next two line (green: 64 00) give the line number of the line (0x0064 or 100 dec).
The line ends at 0814 (file offset 0015, black: 00).

The the next lines starts. Two bytes for the link (red: 0832), two bytes for the line 
number (green: 006E or 110 dec) the several bytes terminated by a 00 (black, at offset 0032).
And so on.

The last link (at offset 0222) 00 00, prefixed by the terminating 00 of the last 
basic line (at offset 0221).

ST is printed on line 410. It prints 64, bit 6 of `ST` indicates 
[end of file has been reached](https://www.c64-wiki.com/wiki/STATUS).
I'm a bit puzzled when to check ST, this feels a bit late (we processes the read `B$`), 
but this way the dump has the correct amount of bytes.


### filecopy

This basic program copies a file from device 8 to 9.

![filecopy](filecopy.png)


### sectordump

This basic program prints one "raw" sector of a disk.
Note that it uses the command address (secondary address 15) to send the block-read command `U1`,
and a plain secondary address 5 to get the block bytes.

![sectordump](sectordump.png)

(end)

