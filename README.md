# x2y

Convert line ending between DOS, Mac (pre OS X) and Unix

Where:

* DOS = '\\r\\n'
* Mac = '\\r' (OS9)
* Unix = '\\n'

Note: Mac here is OS9 and earlier. OS X line endings are Unix.

## Examples

### Convert From Unix To DOS Line Endings

```shell
$ x2y -f unx -t dos file.txt
```

The above command will convert Unix line ending to DOS line endings. The result is written back in to the source file. 

If you want to write to another file use the -o or -d options (see below).

```shell
$ x2y -o output.txt -f unx -t dos file.txt
```

Will write the converted file to output.txt

```shell
$ x2y -d outputs -f unx -t dos file.txt
```

Will save converted files to the outputs directory.

To back up the source file use the -b option. For example:

```shell
$ x2y -b bak -f unx -t dos file.txt
```

Will rename the source file with a ".bak" extensions before writing the converted file.

## Installation

```shell
pip install x2y
```

## Usage

```shell
usage: x2y [options] --from line-ending --to line-ending File [File ...]

x2y: convert line ending between DOS, Mac (pre OS X) and Unix

positional arguments:
  File                  Files to convert

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  --debug               Turn on debug logging.
  --debug-log FILE      Save debug logging to FILE.
  -b BACKUP EXTENTSION, --backup BACKUP EXTENTSION
                        Save a backup of the input file by renaming with
                        BACKUP EXTENTSION. Ignored if the -o option is given.
                        Default: None.
  -d DIRECTORY, --directory DIRECTORY
                        Save extracted text to DIRECTORY. Ignored if the -o
                        option is given.
  -f {dos,mac,unx}, --from {dos,mac,unx}
                        Line ending to convert from.
  -o FILE, --output FILE
                        Save extracted text to FILE. If not given, the output
                        file is named the same as the input file but with a
                        txt extension. The extension can be changed with the
                        -e option. Files are opened in append mode unless the
                        -X option is given.
  -t {dos,mac,unx}, --to {dos,mac,unx}
                        Line ending to convert to.
  -A, --suppress-file-access-errors
                        Do not print file/directory access errors.
```