# downtidy

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Just a stupid Python script to sort my downloads folder based on file extensions.
Tried to use only the Python standard library.

OBS:It should work, but it needs more testing (Not responsible for any files lost to the void 😅).

black formatter settings: default

## TODO

    + Comment the code properly
    + Maybe add reading config from JSON or similar
    + Maybe add progress bars (probably unnecessary and will add dependencies (--progress? check if tqdm is already installed?))
    + Maybe add color to the error "log" messages and to the exceptions strings (ANSI Escape codes?)
    + Fix bugs and improve performance where needed (Python+I/O are slow,so probably can only optimize memory used, stupidly made for loops or hashing time by just hashing a fixed number of blocks (might cause collisions))
    + Change paths from strings to Path types/class (is it better? :thonk:)
    + Maybe add "--folder" argument that allows the folder path given to be used as target to be tidied
    + Maybe add different --log-level that allows to choose from completely silent,log to stdout(default), log to a file in the root of the folder to be tied (add exception for this file not to be tidied)
    + Maybe reimplement in a faster language(like C++ or Rust) or in other scripting language (like Bash or POSIX shell), once I learn them properly (like I even know Python properly :LUL:)
