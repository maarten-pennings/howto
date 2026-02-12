# C64 disk drive commands

The Commodore 64 (C64) comes with disk drives with built-in DOS (disk operating system).
This means the C64 itself does not contain DOS commands.
Instead, the C64 must send command _strings_ (like "file delete") to the drive 
and the drive executes those commands.

This "how to" explains the syntax of those command strings.
For a more generic discussion of the C64 drives see a related 
[howto](https://github.com/maarten-pennings/howto/tree/main/c64drive).


## Directory 

The C64 drive doesn't model "asking for a directory" as a command,
instead it models it as "loading a file"; or to be more precise as 
"loading a program", which can be `LIST`ed.


### Plain directory

```basic
LOAD "$",8
SEARCHING FOR $
LOADING
READY.

LIST
0 "DOS-TEST        " 01 2A
1    "DUMMY-1"          SEQ
1    "DUMMY-2"          SEQ
1    "DUMMY-3"          PRG
1    "DUMMY-4"          PRG
3    "BASIC-1"          PRG
1    "BASIC-2"          PRG
1    "BOARD-1"          PRG
655 BLOCKS FREE.
```

The `$` is the "file name" for the directory; 
a C64 drive only has one directory, the root directory.
There are no sub directories.

Naturally, we could add the drive number.
  
```basic
LOAD "$0",8
```

The directory - the `LIST`ing - contains these details.
- The initial `0` on the first line means this is the directory for drive number 0.
- Between quotes (and in reverse video) we see the 16 characters that
  make up the _diskname_ (`DOS-TEST`).
- After the name we see the two characters of the disk _id_ (`01`),
  which was passed in the format command.
- The final `2A` is tells that the drive (or the disk?) uses DOS version `2` and format `A`.
- This disk contains 7 files, 2 sequential files, and 4 (BASIC) program files.
  For example the file with name `BASIC-1` takes `3` disk blocks (all others only `1`)
  and its file type is `PRG`. Other file types are `SEQ` (sequential), 
  `REL` (relative, i.e. records), `USR` (?), and maybe `DEL`.
- The last line shows the number of free blocks. A block is ¼k bytes (256 bytes).
  A disk is said to have 170 kbytes, but some blocks are reserved for the BAM 
  (block allocation map) or the root directory.
  An empty disk has 644 blocks free, which is 166 kbyte.
  This disk has 1+1+1+1+3+1+1 = 9 blocks in use, so indeed 644-9 = 655 free.

It is possible to read the directory programmatically; since we 
load a program we use secondary channel 0.

```basic
OPEN 3,8,0,"$" : REM SECONDARY CHANEL IS 0 
GET#3, ...
CLOSE 3
```

### Splat files

Sometimes there is a directory entry with a `*` in front of the file type.

```basic
1    "BOARD-3"         *SEQ
```

The `*` tags the file as a _splat_ file. You create a splat file by opening 
a file, writing to the file, but not closing the file, and then resetting the 
C64. A splat file is a file under construction, the disk administration 
is _inconsistent_. Run the [Validate](#validate) 
command to fix the  inconsistencies, do not delete the file as that might 
free blocks that belong to properly closed (other) files.



### Locked files

Sometimes there is a directory entry with a `<` in front of the file type.

```basic
1    "BOARD-3"         <SEQ
```

The `<` tags the file as a _locked_ file. Locked files can not be deleted with 
the scratch command, you need a disk tool for that.


### Directory filter with `*`

We can also add a `*` wildcard matching any sequence of characters.

```basic
LOAD "$0:DUM*",8
...
0 "DOS-TEST        " 01 2A
1    "DUMMY-1"          SEQ
1    "DUMMY-2"          SEQ
1    "DUMMY-3"          PRG
1    "DUMMY-4"          PRG
655 BLOCKS FREE.
```

Note that `LOAD "$0:",8` matches no file.

Note also that the number of free blocks is not influenced by the filter.


### Directory filter with `?`

We can use the `?` wildcard matching precisely one characters.

```basic
LOAD "$0:B????-1",8
...
0 "DOS-TEST        " 01 2A
3    "BASIC-1"          PRG
1    "BOARD-1"          PRG
```


### Directory filter with `=`

C64 DOS even has a file type filter `=`.

```basic
LOAD "$0:D*=PRG",8
...
0 "DOS-TEST        " 01 2A
1    "DUMMY-3"          PRG
1    "DUMMY-4"          PRG
```


## Commands


### Sending commands

To send a command `mycommand` to a drive there are several options.
The various flavors for `mycommand` itself will be discussed later,
here we explain _how_ to send `mycommand` to the drive.

- **Classical**

  ```basic
  OPEN 3,8,15
  PRINT#3, "mycommand"
  CLOSE 3
  ```
  
- **Abridged**

  ```basic
  OPEN 3,8,15, "mycommand" : CLOSE 3
  ```
  
- **Wedge**

  ```basic
  DISK "mycommand"
  ```

In all variants the same string `mycommand` is passed.

Syntactically, the wedge variant is the bare minimum, but it requires 
some software to be loaded beforehand. The BASIC command ("`DISK`") to send 
the string depends on this pre-loaded software. I often use the 
"KCS power cartridge", and there the BASIC command to send a disk 
command is `DISK`. The [original wedge](https://en.wikipedia.org/wiki/DOS-Wedge) 
was made by Bob Fairbairn. It uses `@` instead of `DISK`. JiffyDOS also uses `@`.

The only difference between the classical and abridged variants is that in the 
abridged variant, the command is passed using the optional argument of `OPEN`.
In both cases, the file must be closed.

Another thing to note is that the classical and abridged variants have an 
_explicit_ device number, in the above examples the center `8`. The first 
disk drive typically has device number 8, a second typically 9, but 10 and 11 
are also used. How to send the command to a different device than 8 in case of 
the wedge depends on the wedge software. In case of the KCS power software 
I believe it is _not_ possible to send a command to a different device than 8.
But please prove me wrong by submitting an issue with the method.

In the classical and abridged variants we see that `15` is used as secondary 
channel. That is a _must have_. Commands must be send to secondary channel 15.
The wedge command rightfully hides that.

In the examples above we see that the classical and abridged variants use 
`3` as file number. This can be any free file number (1..255) on the C64 side.
Lot of developers chose `15` as file number, to remind them that file 15 is 
coupled to the secondary channel for commands (15): `OPEN 15,8,15,...`. But 
this is just a convention, not a necessity.


### Drive number

One of the older disk drive devices (the "box") has two drive units 
("disk slots") in them, known as units 0 and 1. All commands therefore 
require to pass the drive unit. It is allowed to leave that out, and then 
the drive unit defaults  to 0. In this document we will mostly include 
the drive number for clarity.

Example:

```basic
OPEN 3,8,15, "I0" : CLOSE 3
OPEN 3,8,15, "I"  : CLOSE 3 : REM Implicit drive number 0
```

It seems it is even allowed to put a space between the command and the drive number `"I 0"`.


### Drive status

When a command results in an error condition, the drive LED will flicker. 
To get the error details, we must read from secondary channel 15.
There is a problem: `INPUT#` does not work in direct mode, only in a program.

Make sure you have the following code fragment in memory before 
giving a command whose status we want to check
(here I used the favorite file number 15):

```basic
55555 REM ERROR NUMBER, MESSAGE, TRACK, SECTOR
55556 INPUT#15,EN,EM$,ET,ES
55555 REM REAL ERROR WHEN EN>=20
55558 PRINT EN;EM$;ET;ES
55558 RETURN
```

After a command (now using file number 15), do not close.

```basic
OPEN 15,8,15, "I0"
```

Instead `GOSUB 55555` to get the drive status.


### List of commands


#### New (Format)

A disk must be newed or formatted before it can be used. 
An example of this command is

```basic
OPEN 3,8,15, "NEW0:DOS-TEST,01" : CLOSE 3
```

```basic
OPEN 3,8,15, "N0:DOS-TEST,01" : CLOSE 3
OPEN 3,8,15, "N:DOS-TEST,01" : CLOSE 3
OPEN 3,8,15, "N:DOS-TEST" : CLOSE 3 : REM WITHOUT ID FOR REFORMAT
```

- For the _file number_,  _device number_ and _secondary address_ (`3,8,15`) see [Sending commands](#sending-commands).
- The _command_ is `NEW`.
  It may be shortened to e.g. `N`.
- The _drive number_ is `0`, and may be omitted.
- The _disk name_ is `DOS-TEST` in the example.
  It can be any name up to 16 characters.
  It is recommended not to use "funny" characters in _disk name_.
  Don't use `,`, `:`, `?`, `*`, or `=` (and probably some others).
  Spaces (` `) or graphical characters (`◆`) are allowed.
- The _id_ is `01` in this example; this is a two-character disk ID. 
  It will be added to every dlock ("sector"), that's why the formatting 
  takes about 70 seconds. The _id_ helps preventing overwrites when swapping disks. 
  It is suggested to use `00` to `99`, or even `AA`..`ZZ`.
- A brand new disk must be formatted before use.
- A previously formatted disk may be formatted again. It will erase all files,
  change the _diskname_ and the _id_ (in all disk blocks).
- The _id_ is optional when _reformatting_. This will erase all files, 
  change the _diskname_, but not the _id_'s (in all blocks). 
  As a result, reformat is much faster than a full format (with _id_).
- See Section [Plain directory](#plain-directory) for an example.


#### Scratch (Delete)

There is a command to scratch (delete) a file on the disk.
An example of this command is

```basic
OPEN 3,8,15, "SCRATCH0:DUMMY-1" : CLOSE 3
```

```basic
OPEN 3,8,15, "S0:DUMMY-1" : CLOSE 3
OPEN 3,8,15, "S:DUMMY-1" : CLOSE 3
```

- For the _file number_,  _device number_ and _secondary address_ (`3,8,15`) see [Sending commands](#sending-commands).
- The _command_ is `SCRATCH`.
  It may be shortened to e.g. `S`.
- The _drive number_ is `0`, and may be omitted.
- The _file name_ is `DUMMY-1` in the example.
  It shall be an existing file name, but it may contain wild cards.
  See the Subsections of Section [Plain directory](#plain-directory) for wildcards.
  Tip: test the wildcards first in the directory command, before using them in the 
  scratch command.
- The wildcard support means you have a means to delete files with rogue characters in them (like a `,`).
- Remember, do not use scratch when there are [splat files](#splat-files).
  Use the [Validate](#validate) instead.

Example, following the wildcard tip, and using the routine at lines 5555 from 
Section [Drive status](#drive-status) to get the amount of deleted files.

```basic
LOAD "$0:BASIC*",8
SEARCHING FOR $0:BASIC*
LOADING
READY.

LIST
0 "DOS-TEST        " 01 2A
3    "BASIC-1"          PRG
1    "BASIC-2"          PRG
655 BLOCKS FREE.

OPEN 15,8,15, "S0:BASIC*"

GOSUB 55555
 1 FILES SCRATCHED 2  0
```


#### Rename

There is a command to rename a file on the disk.
An example of this command is

```basic
OPEN 3,8,15, "RENAME0:NEWNAME=OLDNAME" : CLOSE 3
```

```basic
OPEN 3,8,15, "R0:NEWNAME=OLDNAME" : CLOSE 3
OPEN 3,8,15, "R:NEWNAME=OLDNAME" : CLOSE 3
```

- For the _file number_,  _device number_ and _secondary address_ (`3,8,15`) see [Sending commands](#sending-commands).
- The _command_ is `RENAME`.
  It may be shortened to e.g. `R`.
- The _drive number_ is `0`, and may be omitted.
- The _file name_ of the file to be renamed is `OLDNAME` in the example. It comes second.
- The _file name_ of the file will be changed to `NEWNAME` in this example. It comes first.
- The rename command does not seem to support wildcards.


#### Copy

There is a command to copy a file on the disk.
An example of this command is

```basic
OPEN 3,8,15, "COPY0:NEWFILE=0:OLDFILE" : CLOSE 3
```

```basic
OPEN 3,8,15, "COPY0:NEWFILE=OLDFILE" : CLOSE 3
OPEN 3,8,15, "C0:NEWFILE=OLDFILE" : CLOSE 3
OPEN 3,8,15, "C:NEWFILE=OLDFILE" : CLOSE 3
```

- For the _file number_,  _device number_ and _secondary address_ (`3,8,15`) see [Sending commands](#sending-commands).
- The _command_ is `COPY`.
  It may be shortened to e.g. `C`.
- The _drive number_ is `0`, and may be omitted, also for the old file.
- It is not possible to copy from disk to disk, unless you have a dual drive device.
  On a single drive unit device, to copy from disk to disk, you need an external utility.
- The _file name_ of the file to be copied is `OLDFILE` in the example. It comes second.
- The _file name_ of the new file will be `NEWFILE` in this example. It comes first.
- The copy command does not seem to support wildcards.
- Copy creates new file; this means it searches for a free slot in the directory. 
  If you delete the old file afterwards (freeing that directory slot), you have 
  effectively moved the file entry in the directory list. 


#### Concatenate

The copy command can be used to concatenate files.
The comma is used to separate the constituent files.

```basic
OPEN 3,8,15, "COPY0:NEWFILE=0:OLDFILEA,0:OLDFILEB,0:OLDFILEC" : CLOSE 3
OPEN 3,8,15, "C:NEWFILE=OLDFILEA,OLDFILEB,OLDFILEC" : CLOSE 3
```

- All files on the same disk.
- The concatenate copies all bytes in all files.
  As a result, concatenate of PRG files like BASIC files results in a file that can not be executed.
  Program files have a header (the load address) and those will be copied to 
  offsetting the second (and later) files.


#### Validate

When a file is opened for write, and bytes are being written, the DOS allocates 
disk blocks ("sectors") to write those files to. Each disk block has a link 
to the next block. This chain is made consistent when the file is `CLOSE`d, 
but while writing the links might be dangling.
If the disk is removed from the drive, the drive is re-initialized, 
reset, power cycled, etc, the chain for that file is broken, and the file 
is called a ["splat file"](#splat-files).

Do not delete a splat file, rather perform a Validate operation 
on the disk.

An example of this command is

```basic
OPEN 3,8,15, "VALIDATE0" : CLOSE 3
```

```basic
OPEN 3,8,15, "V0" : CLOSE 3
OPEN 3,8,15, "V" : CLOSE 3
```

- For the _file number_,  _device number_ and _secondary address_ (`3,8,15`) see [Sending commands](#sending-commands).
- The _command_ is `VALIDATE`.
  It may be shortened to e.g. `V`.
- The _drive number_ is `0`, and may be omitted.
- Use this to delete splat files.


#### Initialize

There is a command to initialize a disk.
This causes a re-read of the BAM or Block Availability Map.
The initialize function is performed automatically when a disk is inserted,
using the optical write-protect sensor, so there is no need in practice
to issue this command.

An example of this command is

```basic
OPEN 3,8,15, "INITIALIZE0" : CLOSE 3
```

```basic
OPEN 3,8,15, "I0" : CLOSE 3
OPEN 3,8,15, "I" : CLOSE 3
```

- For the _file number_,  _device number_ and _secondary address_ (`3,8,15`) see [Sending commands](#sending-commands).
- The _command_ is `INITIALIZE`.
  It may be shortened to e.g. `I`.
- The _drive number_ is `0`, and may be omitted.
- Do not issue this commands when there are open files.
- Do not confuse Initialize with [Reset](#reset-and-version).


#### Reset and Version

There is a command to reset the drive.
After a cold boot or a reset, a read of the disk status returns the DOS version
("error" 73), so an explicit reset offers a means to get the DOS version 
at any time.

An example of this command is

```basic
OPEN 3,8,15, "UJ" : CLOSE 3
```

- For the _file number_,  _device number_ and _secondary address_ (`3,8,15`) see [Sending commands](#sending-commands).
- The _command_ is `UJ`.
  The `U` stands for `USER`, it has sub commands, and sub command `J` causes the reset.
- In this command the long name (`USER`) does not seem to work.
- Executing the reset takes time: wait 2 seconds before giving a next command.
- Do not confuse Reset with [Initialize](#initialize).

```basic
100 OPEN 3,8,15, "UJ"
110 FOR I=0 TO 1500:NEXT I
120 INPUT#3,EN,EM$,ET,ES
130 PRINT EM$
140 CLOSE 3

Run
CBM DOS V2.6 1541
```


## Files

### Files via OPEN

The C64 does not have a "touch" command to create an empty file.
But we can use a file-write for that.

```basic
OPEN 3,8,6, "0:DUMMY-1,SEQUENTIAL,WRITE" : CLOSE 3
```

- The C64 _file number_ is `3`. 
  Any number between 1 and 255 will do, if that file number is not yet OPENed.
  Note, file numbers from 128 onward will get a linefeed after every carriage 
  return, good for printers, not for disk files.
- The (disk) _device number_ is `8`.
  Any number between 0 and 31 will do, but disk drives are typically 8, 9, 10 or 11.
- The _secondary address_ is `6`.
  For drives the allowed secondary addresses are 0..15, but 
  0 is reserved for LOADs, 1 for SAVEs, and 15 for commands.
- The _drive number_ is `0`.
  The `0:` part may be omitted.
- The _file name_ is `DUMMY-1`, up to 16 characters, spaces allowed but be careful
  with "funny" chars like  `,`, `:`, `?`, `*`, or `=` (and probably some others).
- The _file type_ is `SEQUENTIAL`, `PROGRAM`, `USER`, `L`# for relative files.
  The _file type_ may be shortened to e.g. `SEQ` or even `S`.
- The _file direction_ is `WRITE`; alternative are `READ` and `MODIFY`.
  `MODIFY` is unclear to me.
  The _file direction_ may be shortened to e.g. `WRI` or even `W`.
  The _file type_ or _file direction_ may be swapped 
  `"0:DUMMY-1,S,W"` versus `"0:DUMMY-1,W,S"`.


### Files via SAVE

```basic
SAVE "0:DUMMY"
SAVE "DUMMY"
SAVE "@DUMMY"
```

todo: save may use @

todo: with load address (basic)

todo: with load address (in monitor)

todo: verify


### Files via LOAD

todo

(end)
