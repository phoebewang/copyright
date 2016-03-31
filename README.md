## Overview
Add or replace license/copyright boilerplate in source code files.

All contiguous comment blocks (bounded by empty or code lines) that contain a copyright message are stripped before injecting the new message.

You should commit all your code into a repo before running this program and check the results with a diff utility.

## Features
* Autodetect language from extension or shebang or header.
* Force programming language to use if files cannot be autodetected.
* Specify list of files to process.
* Recursive or non-recursive processing from current or specific path.
* Custom templates loadable from a JSON file.
* Specify author(s), year(s), program and short description.
* Include or exclude files or directories with wildcards or regex.
* Append to file or insert after any contiguous header comment block.
* Control left-hand margin padding and newline spacing.
* JSON config file ingestion for repeated or automated use, overridden by command-line options.
* Multi or single line comment style, such as /* */ vs. //.
* Languages currently supported: C/C++, Java, HTML, Shell/Bash/Csh/Ksh/Tcsh/Zsh, Perl, Python, SQL, XML
* Python 2 and 3.

## Examples

Process current directory recursively and autodetect files.

    $ copyright -c config.json

Process files matching wildcards, appending to end of file.

    $ copyright -a 'Joe Smith' -p MyApp -l mit -i '*.py,foo*.h,script?' --back

Use custom template.

    $ copyright -c config.json -t my_templates.json --license my-license-2.0

## Installation

With PyPI.

    $ pip install copyright

With tarball.

    $ python setup.py install

## Testing

    $ make test

## FAQ
Q1. How can you keep multiple licenses in a file?
A1. One strategy is to create a custom templates file that has all the licenses merged into one key/value pair, and then process your specific list of files.

## License
copyright Copyright (C) 2016 Remik Ziemlinski

This program comes with ABSOLUTELY NO WARRANTY. This is free software, and you are welcome to redistribute it under the conditions of the GPLv3 license.

