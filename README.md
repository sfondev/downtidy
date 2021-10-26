# downtidy

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Just a stupid Python script to sort my downloads folder based on file extensions.  
Tried to use only the Python standard library to avoid adding dependencies.

OBS #1:It should work, but it needs more testing.  
OBS #2:The tests I performed were on Python3.8.10 (I think some Python features used on the script are only available to versions 3.3+,3.5+ or 3.7+)  
OBS #2.5: Maybe obvious, but there is very high chance that the script will not run with Python2

black formatter settings: default

## TODO

* Comment the code properly
* Maybe add reading config from JSON or similar
* Maybe add progress bars (probably unnecessary and will add dependencies ("--progress"? check if tqdm is already installed?))
* Maybe add color to the error "log" messages and to the exceptions strings (ANSI Escape codes?)
* Fix bugs and improve performance where needed (Python+I/O are slow,so probably can only optimize memory used, stupidly made for loops or hashing time by just hashing a fixed number of blocks (might cause collisions))
* Change paths from strings to Path types/class (is it better? :thonk:)
* Maybe add "--folder" argument that allows the folder path given to be used as target to be tidied
* Maybe add "--dry-run" or "--dry" to simulate running the script on the downloads folder (or in the folder given to "--folder" if I end up implementing that)
* Maybe add different "--log-level" that allows to choose from completely silent,log to stdout(default), log to a file in the root of the folder to be tied (add exception for this file not to be tidied)
* Maybe add total time taken to the log
* Maybe reimplement in a faster language(like C++ or Rust) or in other scripting language (like Bash or POSIX shell), once I learn them properly (like I even know Python properly :LUL:)
* Check if pyxdg is installed and if available use it to get the downloads folder since the library is done by the xdg devs iirc
