# C64 Memory partitioning

Can we partition the C64 memory, storing two programs simultaneously?
A multi-app setup?

No multitasking, we activate one, run it, stop it, activate another and run it.


## Introduction

I was browsing "Mapping the Commodore 64" from Sheldon Leemon. I still have an original, falling apart.
It is a [classic](https://archive.org/details/Compute_s_Mapping_the_64_and_64C) for programmers, 
describing the memory map of the C64 ([webversion](https://www.pagetable.com/c64ref/c64mem/)).

The entry `TXTTAB` caught my attention.
It is the "Pointer to the Start of BASIC Program Text" at $002B-$002C (43-44 decimal).
The book explains

> This two-byte pointer lets BASIC know where program text is stored. 
> Ordinarily, such text is located beginning at 2049 ($0801). 
> Using this pointer, it is possible to change the program text area. 
> Typical reasons for doing this include:

> (3) Keeping two or more programs in memory simultaneously. 
> By changing this pointer, you can keep more than one BASIC program in memory at one time, 
> and switch back and forth between them. 

Then came a reference to [COMPUTE!'s First Book of PET/CBM, pages 66 and 163](https://archive.org/details/COMPUTEs_First_Book_of_PET-CBM_1981_Small_Systems_Services)
an article showcasing a multi-app implementation. The book predates the C64. 
It describes the [Commodore PET](https://en.wikipedia.org/wiki/Commodore_PET), 
but since the PET also had Microsoft BASIC, it was a usable start. 
The administration of BASIC interpreter (pointer names, pointer locations) on the PET 
differs from the C64, so it did take me some time to 
get going on my [C64](https://en.wikipedia.org/wiki/Commodore_64).

I did miss one reason for changing `TXTTAB`/`MEMSIZ`, namely to set aside a 
part of the memory for an assembly routine. We will utilize this later in the
[advanced partition manager](#advanced-partition-manager) for a central 
switching routine.


## BASIC memory map

The above mentioned _COMPUTES!'s First Book_ contains the article 
"Memory Partition of BASIC Workspace" by Harvey B. Herman on pages 64-67.
It explains a system with four programs, all four in the memory of the PET. 
Program 1, 2 and 3 are the actual programs between which we want to switch.
The 4th program is the manager; it lets the user pick the one to switch to.
Once program 1, 2, or 3 is done, it switches back to the manager, where we
can dispatch again one of 1, 2, or 3.

The four programs implement the switching by manipulating pointers.
Herman's article describes and uses pointers on the PET.
In the meantime I found the corresponding pointers for the C64.
The table below comes from the book, with the right-most column ("C64 ROM") added by me.

![Pointer table](pointers.jpg)

What are all these pointers? The diagram below shows the C64 memory map with focus on BASIC.
The gray parts (zero page, stack, OS data, screen buffer, BASIC, I/O and Kernal) are ignored;
we look at the colored parts.

![C64 memory map with focus on BASIC](basicmemorymap.drawio.png)

By default, a BASIC program starts at $0800. With a zero byte, which _must_ be there (or even `NEW` won't work).
Then comes the BASIC program "text" (the entered lines). Program text starts at a location known
as `TXTTAB` ($0801) and grows pushing up `VARTAB`. 
The image below shows a simple example (of a two-line program `10 A$="ABC"`/`20 B=0`) in more detail.

![10 REM A](10REM_A.drawio.png)

If a program uses _plain_ variables (scalars, i.e. not arrays), they are stored from location `VARTAB` 
to location `ARYTAB`. Every new variable pushes up `ARYTAB`. Every variable takes a fixed 
amount of 7 bytes, two for the name and 5 for the data. For strings, the data part is actually 
the size and a _pointer_ to the characters, the characters themselves are on the heap at top of the BASIC memory
(when constructed dynamically), or part of the program text (string literals).

If a program uses _array_ variables, they are stored from location `ARYTAB` to location `STREND`.
Every new array (explicit or implicit `DIM`) pushes up `STREND`. 
This name is a bit confusing (I expected `ARYEND`). As mentioned before, string 
characters are stored in the heap. The heap grows _down_ from `MEMSIZ` to `FRETOP`, until the 
latter hits `STREND`. Hence the name.

This explains all six pointers relevant for managing a BASIC program.
I call this set of six BASIC/Kernal maintained zero-page locations the **layout pointers**.
The table below lists them. Although pointer `FRESPC` is interspersed, it does not 
contribute to describing the layout of a BASIC program.

  | addr (dec)| addr (hex)|   name   |life cycle|
  |:---------:|:---------:|:--------:|:--------:|
  | **43/44** |**$2B/$2C**|**TXTTAB**| progtime |
  | **45/46** |**$2D/$2E**|**VARTAB**| progtime |
  | **47/48** |**$2F/$30**|**ARYTAB**| runtime  |
  | **49/50** |**$31/$32**|**STREND**| runtime  |
  | **51/52** |**$33/$34**|**FRETOP**| runtime  |
  |   53/54   |  $35/$36  |  FRESPC  |          |
  | **55/56** |**$37/$38**|**MEMSIZ**| progtime |

The layout pointers tagged _progtime_ in the life cycle column are established during the programming phase. 
The layout pointers tagged _runtime_ are updated during the program execution. 
By calling `CLR`, the runtime pointers are initialized by emptying the
variables block, the array block, and the heap block.
  

## Simple partition manager

My first trial is to replicate Herman's article, but then on the C64.

- I create one partition manager (app "A0").
- I create two apps ("A1" and "A2", instead of three as Herman does).
- Each app gets a block of 2k RAM (yes, that is small), the first one starting at $0800.
- All three apps are BASIC programs.

The figure below shows how I've partitioned the 38k BASIC RAM (leaving 32k unused).
The numbers on the right are the partition boundaries as selected in the bullets above.
They are shown in hex (`$0801`) followed by an equals sign, and then the 
high byte and low byte in decimal (`8/1`), because that is what we need
for pokes in BASIC.

![Partitioning the BASIC RAM](A0A1A2.drawio.png)

The partition manager A0 can be loaded from e.g. a disk (but you can also type it in).
It will be loaded at the standard `TXTTAB` ($0801), and the 
loader will set `VARTAB` once the whole program is loaded and the end is known 
(or the editor maintains `VARTAB` while editing).

When ran, one of the first things the partition manager does, is to lower 
its own `MEMSIZ`. With that the three progtime layout pointers for its partition are set.
The partition manager then calls `CLR`, which updates `ARYTAB`, `STREND` and `FRETOP`;
all six layout pointers are then set correctly for A0.
For debugging (and as we will see later, for configuring A1 and A2),
A0 does print the three progtime layout pointers (`TXTTAB`, `VARTAB`, and `MEMSIZ`) to the screen.

The partition manager A0, does need to know the addresses of the partitions
that will contain applications A1 and A2, because activating an application 
means changing the six layout pointers. 

However, at this moment, we do not yet know `VARTAB` of A1 and A2, because we don't know
which (how big) those programs will be. Fortunately that doesn't hamper use.
At first we will uses dummy values for `VARTAB` in A0, then run A0 
(write down its `TXTTAB`, `VARTAB`, and `MEMSIZ`), let it switch to A1, and there call `NEW`. 
This initializes `VARTAB` of A1 (and the dependent layout pointers).

Then we type in the program for A1. At the end of the A1 program, we add lines
that set `TXTTAB`, `VARTAB`, and `MEMSIZ` to the values written down for A0.
Once A1 is done, we can inspect its length by peeking `VARTAB` 
(`TXTTAB` and `MEMSIZ` should not have changed). In my experimental apps, part 
of the code of A1 is to actually print the three progtime layout pointers 
`TXTTAB`, `VARTAB`, and `MEMSIZ`.

In other words, from the table below, the layout pointers with no marking come for free, 
the layout pointers with the single < marking come by design (it is the partitions we want),
and the layout pointers with the double << marking come once we have written those apps.

  |  App |TXTTAB (43/44)| |VARTAB (45/46)|  |MEMSIZ (55/56)| |
  |:----:|:------------:|-|:------------:|--|:------------:|-|
  |  A0  | $0801 =  8/1 | |$0A13 = 10/19 |  | $1000 = 16/0 |<|
  |  A1  | $1001 = 16/1 |<|$110D = 17/50 |<<| $1800 = 24/0 |<|
  |  A2  | $1801 = 24/1 |<|$190D = 25/50 |<<| $2000 = 32/0 |<|


### Application A0 (partition manager)

The screenshot below shows the complete listing for a simple partition manager A0.

Before or after running it (but don't press `1` or `2` yet), the listing can be saved e.g. to disk. 
BASIC's SAVE will look at `TXTTAB` and `VARTAB` (but not `MEMSIZ`) to determine what to save.
`TXTTAB` is even saved as header of the `PRG` file (see hex dump [below](#intermezzo-on-file-loading)).
This way BASIC knows where to load a `PRG` back. 

![A0 listing](A0listing.png)

Note
- Line 100, identifies this program as the simple partition manager A0.
- Line 110, sets own the partition size by poking `MEMSIZ`
- Line 120 updates the runtime layout pointers via the BASIC `CLR` command.
- Lines 130 and 140 set the leading 0 for the other two partitions.
- Lines 150-170 print the progtime layout pointers (to write down, needed when editing A1 or A2).
- Lines 180-220 let the user enter `1` or `2` or something else, and activate A1 or A2, or just end A0 (to be rerun, edited, saved).
- Lines 300-330 active A0.
- Lines 400-430 active A1.
- The activation sets `TXTTAB`, `VARTAB`, and `MEMSIZ` (then `CLR` for the other 3). 
  At first `VARTAB` at lines 310 and 410 are set to dummy values. 
  They need to be updated with the actual values once A1 and A2 are known (programmed/edited, loaded).
- On purpose we have extra spaces for the poke values, so that there is room for 3 digits (0..255)
  without changing the size of the program (and thus without changing A0's `VARTAB`).
- If you enter the programs yourself make sure to _copy the lines exactly_.
  If there is any size change you need to correct the layout pointer values in A1 and A2.

The screen below is what we see after running.
We need to write down the values of the three layout pointers.

![A0 output](A0output.png)

Go ahead and press `1` now.


### Application A1 (user program)

After pressing `1` in the partition manager A0, it activated the partition for A1.

> Remember, the first time we activate a partition, we need to call `NEW` to set `VARTAB`.

We can now load or enter a program. We start with the latter.

![A1 listing](A1listing.png)

Note
- Lines 100-110 identify this program as user program A1. One could argue these are the only two real lines of app A1, the rest is to support switching.
- Lines 120-140 print the progtime layout pointers (to write down - we need to update A0 for that).
- Lines 200-220 let the user enter `0` or something else, and return to A0, or just end A1 (to be rerun, edited, saved).
- Lines 230-260 active A0. These are the numbers we wrote down while running A0.

The screen below is what we see after running A1.
Again, we need to write down the values of the three layout pointers of A1 to patch A0.

![A1 output](A1output.png)

Press e.g. space to exit. Save this user program. For fun, do a `PRINT FRE(0)`. Rerun it and press `0`. 
After pressing `0` in A1, it activates (the partition for) A0 again.

Update the A1's `VARTAB` in A0 and save A0.


### Application A2 (user program)

When we now run A0, we can press `1` and got to A1. List it. Run it and press `0`. We are back in A0.

Run A0 and now press `2`. We are now in partition A2, which was unused until now.

We can write a program for A2. In that case we should start with `NEW`.

However, we can also `LOAD "A1",8`.
**Do not `LOAD "A1",8,1`**.
When loading without the `,1` BASIC will load at `TXTTAB` (which is $1801 for A2) and 
automagically fix the linked list of BASIC line numbers (of A1 which was saved for $1001).
See [LOAD behavior](#load-behavior)

> I have the KCS power cartridge. I features a `DLOAD`. That seems to do a "FAST-LOAD,8,1" so do not use it.

After A1 is loaded, fix e.g. line 1 to identify it as user program 2.
Run it. Write down the layout pointers. 

![A2 listing and output](A2listingoutput.png)

Hit `0` to switch to A0. Update A0, to have the correct pointers for A2.


### After thoughts

While a program like A0 (or A1) is changing the layout pointers - by 
poking in 43/44, 45/46, 55/56 - it is changing its own "world". 
Would it still be able to use its variables? 
Probably not, because `VARTAB` is broken.
Would it be able to use `GOTO`? 
I believe that a `NN GOTO MM` starts looking from the current line (`NN`) 
downwards when `MM>NN`. But it starts looking from the start (from `TXTTAB`) 
when `MM<NN`. So that will probably not work either. 
But apparently just going to the next line is fine.

Note that A0 needs to know the layout pointers of apps A1 and A2, 
otherwise it can not activate those apps. Note also that A1 and A2 
need to know the layout pointers of A0, otherwise they cannot switch back.
If you are editing A1, this dependency is painful.


## Intermezzo on file loading

We dump the content of file `A1`, to check its load address and line links.
With that info, we check the behavior of BASIC's `LOAD`.


### Hex dump

The image below shows the hex dump of app A1.

> A hex dump utility is included in the [disk image](#files). 
> You could load it in the second partition, and run it, to see how A1 was saved to disk.

What is special about this file is that it is saved with BASIC's `SAVE`,
but the `TXTTAB` address was not $0800 but $1000.
BASIC's `SAVE` uses `TXTTAB` as start of program and `VARTAB` as end.

![A1 hexdump](A1hexdump.png)

To analyze the dumped file, we tabulate the first 12 bytes, see table below.
The first row (header) is offset in the file, the second row the contents.
All numbers are in hex.


|offset in file `A1`   | 0000 | 0001 | 0002 | 0003 | 0004 | 0005 | 0006 | 0007 | 0008 | 0009 | 000A | 000B |
|:--------------------:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|
|byte at file offset   |  01  |  10  |  09  |  10  |  64  |  00  |  4E  |  B2  |  31  |  00  |  25  |  10  |
|`LOAD` in partition 1 |      |      |[1001]| 1002 | 1003 | 1004 | 1005 | 1006 | 1007 | 1008 |[1009]| 100A |
|byte at memory address|      |      |  09  |  10  |  64  |  00  |  4E  |  B2  |  31  |  00  |  25  |  10  |


- The first two bytes (low byte, high byte order) of the file form $1001, 
  the original _load address_ of the program (`TXTTAB`). The rest of the 
  file is the _content_ of the program. That is stored in memory at the 
  load address.

- If the program is indeed loaded at $1001, we get the memory content as
  shown in rows 2 and 3 of the table.

- Bytes at file offset 2 and 3 (again: low byte, high byte) form $1009, 
  the link to the next line (start-of-lines are marked with square brackets)

- Bytes at file offset 4 and 5 form $0064, which is the line number, 100.

- Bytes at offset 6-8 are E4 B2 31, which represents the BASIC fragment `N=1`.

- Byte at offset 9 is the terminating 0 for line 100.

- We see that the next line indeed starts at address $1009, 
  just as the first link indicated. The next line is at $1025.


### LOAD behavior

What is more surprising than the support for a non-standard load address,
Is that the loader relocates!
When `LOAD`ing a program with load address $1001 in a partition 
that does not start at $1001, BASIC patches the line links. 

That is a neat feature, illustrated by these experiments:

- Try `LOAD "A1",8` in partition 1. As expected (A1 was written for/in partition 1) it loads, lists, and runs fine. 
  "Reduce" A1 by deleting all of its lines except the code to switch to A0. 
  Switch to A0 and from there to partition 2.

- Try `LOAD "A1",8` in partition 2. Also here, it loads, lists, and runs fine. 
  This shows that (1) BASIC's `LOAD` loads at `TXTTAB`, ignoring the load 
  address in the file, and (2) BASIC's `LOAD` patches the line links.

  The table below shows the file (`A1`) being loaded in partition 2, which 
  starts at $1809. Note that the line links (bold) are patched by the loader.

  |offset in file `A1`   | 0000 | 0001 | 0002 | 0003 | 0004 | 0005 | 0006 | 0007 | 0008 | 0009 | 000A | 000B |
  |:--------------------:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|
  |byte at file offset   |  01  |  10  |  09  |  10  |  64  |  00  |  4E  |  B2  |  31  |  00  |  25  |  10  |
  |`LOAD` in partition 2 |      |      |[1801]| 1802 | 1803 | 1804 | 1805 | 1806 | 1807 | 1808 |[1809]| 180A |
  |byte at memory address|      |      |  09  |**18**|  64  |  00  |  4E  |  B2  |  31  |  00  |  25  |**18**|

  This table is generated with `FORI=$1801TOI+10:?HEX$(PEEK(I))" ";:NEXT` 
  (using the KCS power cartridge).
  
- Switch to 0 and from there to 1 to check A1 app is still the "reduced" one.
  Switch back to 0 and from there to 2. "Reduce" A2 by deleting all of its 
  lines except the code to switch to A0. Partition 1 and 2 now both have a 
  "reduced" version of program `A1`.
  
  Try `LOAD "A1",8,1` in partition 2. Note the `,1` to force LOAD to use
  the load address in the file. Recall that the load address in the file is 
  $1001, the start of partition 1. Check with `LIST` that after the `LOAD` 
  partition 2 still has the "reduced" A2 code, so nothing is loaded 
  (in partition 2). 
  
  Switch to 0 and then to 1 and check with `LIST` that the "reduced" A1
  is now replaced by the loaded A1.
  
  This shows that (1) `LOAD "XXX",8` loads in the activate partition, and 
  (2) `LOAD "XXX",8,1` loads absolute, that could be in another partition.


## Advanced partition manager 

In the second part of this document we try to make an **advanced** partition 
manager, which mitigates the shortcomings of the simple partition manager.
Let's first have a look at those shortcomings.

### Analysis of the simple partition manager

The first drawback of the simple partition manager is that the actual apps 
(A1, A2,...) need to include switching code (eg lines 150-180 of A1). Of course 
the developer of the partition manager A0 needs to understand partitions and 
layout pointers, but the user apps (A1, A2, ...) should be plain BASIC, free of 
partition knowledge. 

The second drawback is that while developing a user app (say A1), its layout 
pointers (most notably `VARTAB`) change. Therefore, each time a switch is made 
from app A1 to the partition manager A0, the layout pointers of A1 need to be 
recorded, so that they can be updated in A0. Failing to do so, would block us 
from switching back to A1 at a later stage. This is a maintenance burden and 
it is easy to forget.

A related drawback is that when changing A0 (to update the layout pointers 
of one of the apps A1, A2, ...) there is a risk that the layout of A0 itself 
changes (typically pointer VARTAB). That would require an update of the 
switching code of all apps (A1, A2, ...) otherwise they could no longer 
switch to A0.

A small nuisance is also that the switching code only restores the progtime 
pointers (begin of partition, end of BASIC program text, and end of partition), 
not the runtime pointers (variables, arrays, strings) - it clears them. 
Adding the runtime pointers in the switching code would aggravate the 
maintenance burden (more pointers to record and update, and more often).

A final drawback is that the apps (A1, A2, ...) only have switching code to go 
back to partition manager A0, and not to another app. Of course we could 
expand the switching code in each app to allow switching to all other apps, 
but this would make the previous drawbacks only more painful. 

There is a solution to all this; it is presented in the next section.


### Sketch of the advanced partition manager

Why would the programmer of app A1 need to write down the values of A1's 
layout pointers when switching to A0? We have a computer, we could store 
those pointers in variables, can't we? No. Not really. The problem is that while we 
are changing the layout pointers of an app we lose access to our variables 
(`VARTAB` indicates where they are). So that doesn't work. 

Unless we do not use _BASIC_ variables to record the layout pointers, but 
some fixed memory locations. And then we do not use BASIC but some assembly 
routine to update those locations.

The idea is that the partition manager A0 sets aside a piece of memory, the 
_layout table_, that records the layout pointers of all its apps. If 
there are 8 apps (partitions), that would be 8 sets of 7 pointers of 2 bytes, 
nearly 128 bytes for the layout table. The partition manager also records 
which partition is active. Finally, there would be one assembly routine, 
the _switcher_, with one input parameter: the partition to make active. 

When the switcher gets called, it first copies the actual layout pointers 
(43..56) to the layout table (a "backup"). The switcher knows which slot in the 
layout table to use, because it knows which partition is currently active. 
Then the switcher updates the location that records the active partition with 
the passed parameter. Finally, it copies (it "restores") the layout pointers 
from the layout table (using the slot of the new active partition) to the 
actual layout pointers (43..56).

The advanced partition manager thus consists of three parts
- the _layout table_ with layout pointers of all partitions,
- the _switcher_, an assembly routine that implements the switching using 
  the layout table,
- a BASIC program that packages all this; it
   - has some easy way to define partition boundaries,
   - creates the partitions (pokes the leading zeros),
   - initializes the layout table with pointers for all partitions,  
   - pokes the switcher assembly routine into memory, and
   - maps `USR()` to the switcher. This makes it easy pass a parameter 
     (new partition to become active) to the switcher. 
     It also makes the switcher easily accessible in all partitions.


### Todo

...


## Files

This document comes with a [d64](partmngr.d64) disk image, with these files
- `A0`, the simple partition manager.
- `A1`, a simple app that prints its name, progtime addresses and returns to A0.
- `HEXDUMP` a basic program that prints a hex dump (e.g. of file `A1`).


(end)
