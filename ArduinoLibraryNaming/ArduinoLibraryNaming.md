# Naming in Arduio libraries

An registered Arduino library needs a name, and several aspects play a role.
These aspects are described in this document.


## GitHub

A registered library must be stored on a public server.
A typical candidate for that is GitHub.

On GitHub there are an `<account>` pages (don't know the official name
for that), which can be for a personal account or for a company account.

On those account pages there are repositories `<repo>`. The URL of 
such a repo is then `https://github.com/<account>/<repo>`.

The `<repo>` name is only used at this location.
You are free to pick whatever you like - as long as GitHub accepts it.
This name will not be used anywhere else in Arduino.

Inside this repo, we have to follow the Arduino conventions.

```text
<repo>
+-- examples\
+-- extras\
+-- src\
+-- library.properties
+-- license.txt
```

## Library name

The file `library.properties` contains the meta information on the 
library. The one that is of interrest to us is `name` which is typically
on the first line of that file.

This is the official [specification](https://arduino.github.io/arduino-cli/0.19/library-specification/) 
of `name`:

> Library names must contain only basic letters (A-Z or a-z) and numbers (0-9), spaces ( ), underscores (_), dots (.) and dashes (-). They must start with a letter or number. They must contain at least one letter. Note that libraries with a name value starting with `Arduino` will no longer be allowed addition to the Library Manager index as these names are now reserved for official Arduino libraries.

However, if you try to register a library you might stumble of "soft" requirements.

> WARNING: library.properties name value xxx is longer than the recommended length of 16 characters.
> WARNING: library.properties name xxx contains spaces. Although supported, best practices is to not use  spaces.

The `name` is defined in `library.properties`, where is it used?


### `name` usage in `library.properties`

The first place where a `name` is used is in the `library.properties` file
nmely in the `depends` section. The line has the form

```text
depends=name1,name2,name3
```

that is, a coma separated list of names, just as they occur in the `name` definition (with spaces if they occur in the name).


### `name` usage in examples

In the Arduino IDE, when opening File > Examples, the examples are grouped by library.
Each group shows the library `name`, as before, the name is used as definited (with spaces if they occur in the `name`).


### `name` usage in library manager

In the Arduino IDE, when opening the Library Manager, libraries are listed with their `name`.
As before, they are used as they occur in the `name` definition (with spaces if they occur in the `name`).


### `name` usage in file system

When a library is installed (via the Arduino Library manager), the IDE creates
a directory for that library in `C:\users\<user>\Documents\Arduino\libraries`.

The directory is a mangeled version of `name`: all spaces are replaced with underscores.

By the way, the name of the directory that stores a library is not relevant; it can be changed to whatever.
The Arduino build system finds libraries - I believe - via a header file that is included in an (ino) file.


## Advise

How to name your library.

I would suggest to pick a "brand" name and a "descriptive" name.
Both without spaces.
Use that as name

```text
name=Brand ShortLibDescription
```

Then in the examples and library manager we the user sees a readable but branded name Brand `ShortLibDescription`.
The library will stored in a directory with an acceptable name `Brand_ShortLibDescription`.
You could even consider to call the header file `Brand_ShortLibDescription.h`, to prevent an "INFO" while
registering.

> INFO: No header file found matching library name (Brand ShortLibDescription). Best practices are for primary header filename to match library name.

(end)

