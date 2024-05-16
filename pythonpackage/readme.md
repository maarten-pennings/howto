# Python package

Empty example of a python package with one module, used in 
an application - which runs in a virtual environment.

## Introduction

We have an application `app.py` that uses a function `myfunc` in a package `mypkg`.

```text
root
+-- app
|   +-- app.py
+-- mypkg
    +.. mymod.py // implements myfunc()
```

We want to use a virtual environment to run `app.py`, and we want to
install `mypkg` in that virtual environment.

## mypkg

Suppose we have a module `mymod.py` with the function `myfunc()`
that we want to use in `app.py`:

```python
def myfunc() :
  print("myfunc")
```

In order to make this into a package `mypkg`, we need to create a directory
with that name, put the module file there, and add an empty `__init__.py`.
A file named `__init__.py` marks a directory as a Python package;
typically it is empty, but when a package is imported, `__init__.py` is executed.

```text
mypkg
+-- __init__.py
+-- mymod.py
```

In order to convert this into an _installable_  package, we need to create 
a container directory with - again - the package name, store some meta files, and
store the above create package directory there.

```text
mypkg
+-- mypkg
|   +-- __init__.py
|   +-- mymod.py
+-- license.txt  // optional
+-- readme.md    // optional
+-- setup.py   
```

The `setup.py` is mandatory. It contains something like the below.

```python
from setuptools import setup

setup( 
  name='mypkg',
  version='0.1',
  description='a test for packaging modules',
  author='Maarten Pennings',
  packages=['mypkg']
)
```


## app

The application code `app.py` just calls `myfunc()`.
Do note that we import that function first.

```python
from mypkg.mymod import myfunc

def main() :
  print("myapp")
  myfunc()

if __name__ == "__main__":
  main()
```

I like to develop python projects in a virtual environment.
This allows different versions of package to be used by
different projects. Maybe even more important, environments
allow installing packages in those environments, instead of
in the global space. This means the global space is not 
"polluted" by packages, so each project _has_ to install
them explicitly.

To protect myself, I do not even have python in my `path`.
This way I _must_ create a virtual enviroment.

To create an environment I have a standard script `setup.bat`.
You will probably have to change `LOCATION` (eg keep it empty
if Python is in your path).

```bat
SET LOCATION=C:\Users\maarten\AppData\Local\Programs\Python\Python39\

%LOCATION%python.exe -m venv env
CALL env\Scripts\activate.bat
env\Scripts\python -m pip install --upgrade pip setuptools wheel
IF EXIST requirements.txt (
   pip install -r requirements.txt
)
```

What does differ per project is the `requirements.txt` file.
Normally it has lines like `numpy` and `matplotlib`.
In this simple project it has only a ref to `mypkg`.

```text
../mypkg
```

Finally, I typically have a `run.bat`.

```bat
@ECHO off
IF "(env) " neq "%PROMPT:~0,6%" ECHO Please run setup.bat first && EXIT /b

python app.py
```

## Running setup.bat

The files we store in the repo are as follows.

```text
root
+-- app
|   +-- app.py
|   +-- requirements.txt
|   +-- run.bat
|   +-- setup.bat
+--mypkg
|  +-- license.txt
|  +-- readme.md
|  +-- setup.py
|  +-- mypkg
|      +-- mymod.py
|      +-- __init__.py
+-- clean.bat
```

We open `cmd` in the `app` directory and run `setup.bat`.
This is the output.

```text
root> setup
root> SET LOCATION=C:\Users\maarten\AppData\Local\Programs\Python\Python39\
root> C:\Users\maarten\AppData\Local\Programs\Python\Python39\python.exe -m venv env
root> CALL env\Scripts\activate.bat
Collecting pip
  Using cached pip-24.0-py3-none-any.whl (2.1 MB)
Collecting setuptools
  Using cached setuptools-69.5.1-py3-none-any.whl (894 kB)
Collecting wheel
  Using cached wheel-0.43.0-py3-none-any.whl (65 kB)
Installing collected packages: pip, setuptools, wheel
  Attempting uninstall: pip
    Found existing installation: pip 20.2.3
    Uninstalling pip-20.2.3:
      Successfully uninstalled pip-20.2.3
  Attempting uninstall: setuptools
    Found existing installation: setuptools 49.2.1
    Uninstalling setuptools-49.2.1:
      Successfully uninstalled setuptools-49.2.1
Successfully installed pip-24.0 setuptools-69.5.1 wheel-0.43.0
Processing c:\users\maarten\desktop\pythonpackage\mypkg
  Preparing metadata (setup.py) ... done
Building wheels for collected packages: mypkg
  Building wheel for mypkg (setup.py) ... done
  Created wheel for mypkg: filename=mypkg-0.1-py3-none-any.whl size=1520 sha256=03ae38ab17f1f5cd9590f407cf5842dbe2070650166f2282c753324d1eb68ea8
  Stored in directory: C:\Users\maarten\AppData\Local\Temp\pip-ephem-wheel-cache-mebwrils\wheels\f1\43\54\fe5b636ba825d845520f054e0e72b3d2dd5e47ecab4f620c8b
Successfully built mypkg
Installing collected packages: mypkg
Successfully installed mypkg-0.1
(env) root> 
```

The `setup` creates a virtual environment in directory `app\env`.
The `(env)` in the prompt indicates that the virtual environment has been
activated; basically, this means that `root\app\env` has been prepended
to the system search `path`.
 
The `setup` also creates and two directories in `mypkg`. 
These and `env` do not have to be stored in the repo.

```text
+-- readme.md
+-- app
|   +-- app.py
|   +-- requirements.txt
|   +-- run.bat
|   +-- setup.bat
|   +-- env              <=== lots of generated stuff
+-- mypkg
|   +-- license.txt
|   +-- readme.md
|   +-- setup.py
|   +-- build            <=== lots of generated stuff
|   +-- mypk
|   |   +-- mymod.py
|   |   +-- __init__.py
|   +-- mypkg.egg-info   <=== lots of generated stuff
+-- clean.bat
```

You may use `clean.bat` to remove the generated files.


## Running run.bat

We can now run the `app`. We use the helper `run.bat` for that.

```bat
(env) root> run
myapp
myfunc
```

(end)
