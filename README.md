# downtidy

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

### Just a stupid Python script to sort my downloads folder based on file extensions   


## To take in consideration:
* <ins>**Not fully developed and tested, might have bugs.**</ins>
* Last tested on Python 3.8.10 and not tested or used since
* One of the objectives is to be compatible with both Windows and Linux
* Tried to use only the Python standard library to avoid adding external dependencies, but will probably add some check for some possibly useful dependencies to add adittional functionality or improve the current one(s)
* It probably isn't very memory or speed performant (will try to improve once I have some more time)
black formatter settings: default
* **Using this script/program might have side effects since I'm pretty sure that the copy/move function used (the one from the module `shutil` from the standard library) isn't truly lossless with respect to file metadata (need to do more investigation regarding this matter to really confirm)**

## TODO

* Comment the code properly
* Maybe add reading config from JSON or similar (from $HOME/.config/downtidy.\<something>)
* Maybe add progress bars (probably unnecessary and will add dependencies ("--progress"? check if tqdm is already installed? or use "\\r"))
* Maybe add color to the error "log" messages and to the exceptions strings (ANSI Escape codes? colorama?)
* Fix bugs and improve performance where needed (Python+I/O are slow,so probably can only optimize memory used, stupidly made for loops or hashing time by just hashing a fixed number of blocks (might cause collisions))
* Change paths from strings to Path types/class (is it better? Probably :thonk:)
* Maybe add "--folder" argument that allows the folder path given to be used as target to be tidied
* Maybe add "--dry-run" or "--dry" to simulate running the script
* Improve the argument reading/parsing probably using the built-in `ArgumentParser` from the module `argparse`
* Maybe add different log level ("--log-level {SILENT,INFO,WARN,ERROR}")
* If logging is added add the possiblity of it going to a file in the root of the folder to be tied (add exception for this file not to be tidied) or to a file in a location chosen by the user "--log-file location"  
* Maybe add total time taken to the log (`timeit` module?)
* After the ones above try to abstract more
* Check if pyxdg is installed and if available use it to get the downloads folder since the library is done by the xdg devs iirc
* [1]Check properly the minimum Python version for the functionality used
* Battle-test the program
* Maybe add sample tests 
* After that all of that reimplement it in a faster language(like C++ or Rust) or in other scripting language (like Bash or POSIX shell), once I learn them enough-ish or as a string manipulation,argument parsing and file I/O handling exercise




