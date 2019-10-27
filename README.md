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

And here's how gameplay looks like:

```
$ ./the99game.py --hints --base 5
=== Turn 1 ===
(0 1 2 3)
 1 2 3 4 (0)
 1 1 1 2 (1)
 1 3 1 4 (2)
Legal moves are:
[0,0,v, 1,0,>, 3,0,>, 0,1,v, 0,1,>, 1,1,>, 2,1,v, 2,2,>]
You can also "expand" the board, or go one step "back".
Please enter a move in the "col,row,dir" format, or "back" or "expand":
?
→0,0,v

=== Turn 2 ===
(0 1 2 3)
 x 2 3 4 (0)
 x 1 1 2 (1)
 1 3 1 4 (2)
Legal moves are:
[1,0,>, 3,0,>, 1,1,>, 2,1,v, 2,2,>]
You can also "expand" the board, or go one step "back".
Please enter a move in the "col,row,dir" format, or "back" or "expand":
?
→1,0,>

=== Turn 3 ===
(0 1 2 3)
 x x x 4 (0)
 x 1 1 2 (1)
 1 3 1 4 (2)
Legal moves are:
[3,0,>, 1,1,>, 2,1,v, 2,2,>]
You can also "expand" the board, or go one step "back".
Please enter a move in the "col,row,dir" format, or "back" or "expand":
? 2,1,v

=== Turn 4 ===
(0 1 2 3)
 x x x 4 (0)
 x 1 x 2 (1)
 1 3 x 4 (2)
Legal moves are:
[3,0,>]
You can also "expand" the board, or go one step "back".
Please enter a move in the "col,row,dir" format, or "back" or "expand":
?
→3,0,>

=== Turn 5 ===
(0 1 2 3)
 x x x x (0)
 x x x 2 (1)
 1 3 x 4 (2)
There are no legal moves.
[]
You could "expand" the board, or go "back".
Please enter a move in the "col,row,dir" format, or "back" or "expand":
?
```

## TODOs

* Make everything nicer
* Solve the world's problems

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
