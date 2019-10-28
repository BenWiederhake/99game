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

### Optimal solutions

Here are the optimal solutions for various bases, as far as I know:

```
$ ./solve.py --base 2
Turn 1: 0 open, 1 closed
Turn 2: 1 open, 2 closed
Turn 3: 2 open, 4 closed
=== Can win after 3 turns! ===
[0,0,v, 'expand', 0,0,v]

$ ./solve.py --base 3
Turn 1: 0 open, 1 closed
Turn 2: 7 open, 2 closed
Turn 3: 29 open, 10 closed
=== Can win after 3 turns! ===
[0,0,v, 1,0,v, 0,0,>]

$ ./solve.py --base 4
Turn 1: 0 open, 1 closed
Turn 2: 8 open, 2 closed
Turn 3: 43 open, 11 closed
Turn 4: 309 open, 55 closed
- INEXACT, iff solution is longer than 20 -
Turn 5: 2689 open, 365 closed
Turn 6: 27204 open, 3055 closed
=== Can win after 6 turns! ===
[0,0,v, 2,0,v, 1,1,v, 1,0,>, 'expand', 2,0,>]

$ ./solve.py --base 5
Turn 1: 0 open, 1 closed
Turn 2: 8 open, 2 closed
Turn 3: 54 open, 11 closed
- INEXACT, iff solution is longer than 20 -
Turn 4: 414 open, 66 closed
Turn 5: 2710 open, 481 closed
Turn 6: 17499 open, 3192 closed
=== Can win after 6 turns! ===
[0,0,v, 3,0,>, 1,0,v, 2,1,v, 2,0,>, 0,0,>]

$ ./solve.py --base 6
Turn 1: 0 open, 1 closed
Turn 2: 9 open, 2 closed
Turn 3: 59 open, 12 closed
- INEXACT, iff solution is longer than 20 -
Turn 4: 418 open, 72 closed
Turn 5: 2591 open, 491 closed
Turn 6: 11024 open, 3083 closed
Turn 7: 31550 open, 14108 closed
Turn 8: 71143 open, 45659 closed
Turn 9: 188219 open, 116803 closed
=== Can win after 9 turns! ===
[0,0,v, 3,0,v, 1,1,v, 4,0,>, 4,0,v, 2,0,>, 1,0,>, 'expand', 3,0,>]

$ ./solve.py --base 7
Turn 1: 0 open, 1 closed
Turn 2: 10 open, 2 closed
Turn 3: 77 open, 13 closed
- INEXACT, iff solution is longer than 20 -
Turn 4: 644 open, 91 closed
Turn 5: 5258 open, 736 closed
Turn 6: 33624 open, 5995 closed
Turn 7: 161310 open, 39620 closed
Turn 8: 585618 open, 200931 closed
Turn 9: 1640943 open, 786550 closed
=== Can win after 9 turns! ===
[2,0,>, 1,0,>, 0,0,>, 0,0,v, 1,0,>, 3,0,v, 4,0,v, 5,0,>, 2,0,>]
```

Have fun running it with more RAM consumption.

Sadly, the sequence "3,3,6,6,9,9" is [not unique](https://oeis.org/search?q=3%2C3%2C6%2C6%2C9%2C9+-tabl+-cons).
Some are [plausible](https://oeis.org/A213332), some [less](https://oeis.org/A110261).


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
