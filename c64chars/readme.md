# Commodore 64 characters

Font ROM of the C64.


## Introduction

The character management in the C64 is a bit complex.

- There are two character sets: the default (standard, graphics or upper case) and alternate (text or lower case) set.
- In one character set (of 256 characters), the upper 128 are the reverse video of the lower 128 characters (all pixels flipped).
- There is a difference between ASCII codes (or PETSCII if you want) and screen pokecodes.
- Several glyphs ("the specific shape, design, or representation of a character", i.e. the character bitmaps) are duplicated.

This project was an attempt to clarify for myself how the standard set looks like,
how characters can work together to form bigger "ACSII art",
and how the mapping from pokecodes to ASCII works out.


## Process

I started with a font ROM [dump](c64fontromhi.pbm).
This is only the default character set.
The repo also stores the [lower case text set](c64fontromhilo.pbm) if you want to examine it.

I wrote a [Python script](app.py) to convert this to overview tables.
The script separates the pixels of the characters so that I could clearly see which characters connect.
When you run the script (open `cmd` shell, execute `setup.bat`, execute `run.bat`) it generates the tables
in this repo.


## Standard

The first table that is generated just shows all glyphs in a matrix organized according to their pokecodes.

![Standard table](c64fontromhi-1plain.png)

The ASCII code that produces a glyph is printed in small (black) font to the right of it.
For example the glyph with pokecode 0x5E (π) is associated to 3 ASCII codes

![ASCII](ascii.png)

In general, the mapping from ASCII to pokecodes (glyphs) is in chunks of 32 (two columns).
But the ASCII mapping still confuses me. 
For example, I cannot get ASCII codes 0x80-0x9F to do/print anything.


## Duplicates

One of the things that puzzled me is why there are duplicate glyphs.
My Python script finds them all.
There quite some, see the red encircled ones below (with in red the pokecode of the duplicate).

![Duplicate glyphs](c64fontromhi-2dups.png)

One case is the space (0x20) which is also present at 0x60.
I see that as a space that looks like a space but that is not treated by the kernel
as a separator. It was already present in the VIC-20 character set, see
the diagram below with the C64 (left, blue) and VIC-20 (right, grey) character sets.

![C64 vs VIC-20](c64-vs-vic20.png)

The VIC-20 table also hints for easons of the other duplicates.
The rumor goes that when Commodore moved from the 22-column VIC-20 to
the 40-column C64, there was color distortion at pixel boundaries.
To mitigate this Commodore made the characters fat: in horizontal
direction there are always at least two similar colored pixels.
This "double pixel policy" is very clear when comparing the C64 and VIC-20 tables above. 

It also meant that the vertical line character with pokecode 0x42,
a single line in the VIC-20 had to doubled. But so had 0x5D, and 
the result is that they are identical on the C64.

In the above duplicates overview, the pixels added by Commodore 
for the doubling are dotted by the Python script.

Since now all glyphs with vertical lines are double-width, Commodore decided to also 
double the horizontal line glyphs, which resulted in 0x40 and 0x43 to become duplicates.

If you are still not convinced, have a look at the keyboard.
The G and H can be used with the Commodore shift key to give a thin (1 pixel) or thicker (2 pixel)
vertical bar as shown on the key caps. In practice, the G gives glyph 0x65 and H gives glyph 0x74.
On VIC-20 these are indeed 1 and 2 pixels wide but on the C64 both are 2 pixels wide.

![cbm-G and cbm-H](cbm-G-H.jpg)

Similarly, the N and M can be used with the Commodore shift key to give a thick (2 pixel) or thin (1 pixel)
vertical bar. Also this is depicted on the key caps. 
In practice, the N gives glyph 0x6A and M gives glyph 0x67.
On VIC-20 these are 2 and 1 pixels wide but on the C64 both are 2 pixels wide.

![cbm-N and cbm-M](cbm-N-M.jpg)

It is harder to see on the key caps, but similar situation for shift-star and shift-C
respectively shift-minus and shift-B

![shift star, C, minus, and B](shift_star_C_min_B.jpg)

Conclusion: the C64 duplicate glyphs are a result of the "double pixel policy".


## Reverse video errors

My Python script also checks if each glyph is a flip of its reverse video counter part.
To my big surprise, there was one mismatch: for character 0x00 (@), see the pixel in the 6th row of the 6th column (dotted in 0x80 in the table below).

![Wrong RVS](c64fontromhi-3wrongrvs.png)


## Grouping glyphs

This section partitions all glyphs in categories.


### Coarse block graphics

When using character mode, it is possible to plot 80×50 pixels using the block glyphs.

![Block graphics](c64fontromhi-4blocks.png)


### Vertical fill

Use these glyphs for a pixel accurate vertical fill gauge (e.g. battery level).

![Vertical fill](c64fontromhi-5verfill.png)


### Horizontal fill

There is also a set of glyphs for a horizontal fill gauge, but, due to the pixel doubling, 
there are some duplicates.

![Horizontal fill](c64fontromhi-6horfill.png)


### Vertical wave

Use these glyphs for a vertical tick gauge, but, due to the pixel doubling, there are some duplicates.

![Vertical wave](c64fontromhi-7verwave.png)


### Horizontal wave

Use these glyphs for a pixel accurate horizontal tick gauge (e.g. stereo speaker balance).

![Horizontal wave](c64fontromhi-8horwave.png)


### Mid frames

Draw frames with these "mid-cell" line glyphs; corners in red, connectors in orange.

![Mid frame](c64fontromhi-9midframe.png)


### Outside frames

Draw a different style of frames with these glyphs.

![Outer frame](c64fontromhi-10outerframe.png)


### Various symbols

There is an assortment of symbols, including card suits.

![Symbols](c64fontromhi-11symbols.png)


### Diagonal

There are some diagonal glyphs.

![Diagonal](c64fontromhi-12diagonal.png)


### Dithering

For me the least useful glyphs do a sort of gray scaling via dithering.

![Dithering](c64fontromhi-13dither.png)



## Links

This [site](https://sta.c64.org/cbm64petkey.html) maps ASCII codes to key strokes.

The VIC-20 char set is from [kreativekorp](https://www.kreativekorp.com/software/fonts/c64/).



(end)

