# 99game

> A CLI version of a nameless game that I dubbed "99game".

The game is completely deterministic, so this program can also be used to
quickly check whether a sequence of moves is valid.

Hopefully this is implemented modular enough to also be used as a
kind of search library.

The file is named `the99game.py` because `99game.py` would cause all kinds of
trouble in python.

## Table of Contents

- [Install](#install)
- [Usage](#usage)
- [TODOs](#todos)
- [NOTDOs](#notdos)
- [Contribute](#contribute)

## Install

No installation required.

## Usage

Just use it!  No dependencies, but you need to run it in a console.

```
$ ./the99game.py --help
usage: the99game.py [-h] [--hide-board]

optional arguments:
  -h, --help    show this help message and exit
  --hide-board  do not show the board while playing
```

## TODOs

* Computing legal moves
* Executing moves
* Console interaction

## NOTDOs

Here are some things this project will not support:
* GUI.
* Advanced AI.
* Anything networking.

These are highly unlikely, but if you actually need them and can tell me
how to elegantly implement it, I might look into it:
* More efficient.
* Stupid AI.
* Nicer representation.
* Nicer terminal control. (Stay in "one window"?)

## Contribute

Feel free to dive in! [Open an issue](https://github.com/BenWiederhake/99game/issues/new) or submit PRs.
