# ARCHIVED

The game still works, and is useful as a validator.
However, a better and faster solver is implemented
[here in Rust](https://github.com/BenWiederhake/solve99game-rs#experimental-results),
and I don't plan to touch this python code anyway.
Also, have fun with my development notes of figuring out
a memory-efficient way to implement A*.

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

## Optimal solutions

### Odd degrees are easy

The top row looks like this: `1 2 3 4 5 6 7 8`

For odd degrees, this means that cells can always be paired up easily: `(1 (2 (3 (4 5) 6) 7) 8)`.
This eliminates the top row.

Furthermore, the "prefix" `1` cells of the second block can be eliminated, leaving something that can again be grouped like `(1 (2 (3 (4 5) 6) 7) 8)`.

Therefore, for odd degree `d = 2k + 1`, the puzzle can be solved trivially in `3 * k` moves.

### Even degrees need expansion

First, note that all non-prefix `1` cells are duplicated, so their overall parity is 0.
Next, note that there are an odd amount of `1` cells, so the all-in-all-parity is 1.

Finally, note that removing cells does not change parity, as either a pair of numbers is removed (`2*x` is even),
or two numbers that sum to our degree, which by assumption is even.

Therefore, a solution must contain at least one expansion step, which always sets parity to 0.

### Experimental results:

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
- INEXACT, iff solution is longer than 30 -
Turn 4: 308 open, 55 closed
Turn 5: 2625 open, 364 closed
Turn 6: 25637 open, 2990 closed
=== Can win after 6 turns! ===
[0,0,v, 2,0,v, 1,1,v, 1,0,>, 'expand', 2,0,>]

$ ./solve.py --base 5
Turn 1: 0 open, 1 closed
Turn 2: 8 open, 2 closed
Turn 3: 54 open, 11 closed
- INEXACT, iff solution is longer than 30 -
Turn 4: 458 open, 66 closed
Turn 5: 4732 open, 525 closed
Turn 6: 56703 open, 5258 closed
=== Can win after 6 turns! ===
[0,0,v, 3,0,>, 1,0,v, 2,1,v, 2,0,>, 0,0,>]

$ ./solve.py --base 6
Turn 1: 0 open, 1 closed
Turn 2: 9 open, 2 closed
- INEXACT, iff solution is longer than 20 -
Turn 3: 58 open, 12 closed
Turn 4: 389 open, 71 closed
Turn 5: 2248 open, 461 closed
Turn 6: 8809 open, 2710 closed
Turn 7: 23214 open, 11520 closed
Turn 8: 49891 open, 34735 closed
Turn 9: 153806 open, 84627 closed
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

$ ./solve.py --base 8
Turn 1: 0 open, 1 closed
Turn 2: 8 open, 2 closed
- INEXACT, iff solution is longer than 20 -
Turn 3: 29 open, 11 closed
Turn 4: 177 open, 41 closed
Turn 5: 1248 open, 219 closed
Turn 6: 5978 open, 1468 closed
Turn 7: 19853 open, 7447 closed
Turn 8: 48141 open, 27301 closed
Turn 9: 88354 open, 75443 closed
Turn 10: 126523 open, 163798 closed
Turn 11: 146290 open, 290322 closed
Turn 12: 142952 open, 436614 closed
Turn 13: 127111 open, 579568 closed
Turn 14: 120179 open, 706680 closed
Turn 15: 195992 open, 826860 closed
=== Can win after 15 turns! ===
[0,0,v, 6,0,v, 1,1,>, 2,0,v, 5,0,>, 1,2,>, 5,2,>, 'expand', 4,2,>, 0,2,>, 5,1,>, 4,1,>, 4,0,v, 3,0,>, 1,0,>]

$ ./solve.py --base 9
Turn 1: 0 open, 1 closed
Turn 2: 11 open, 2 closed
- INEXACT, iff solution is longer than 20 -
Turn 3: 63 open, 14 closed
Turn 4: 204 open, 78 closed
Turn 5: 448 open, 283 closed
Turn 6: 721 open, 732 closed
Turn 7: 5224 open, 1454 closed
Turn 8: 37088 open, 6679 closed
Turn 9: 181914 open, 43768 closed
Turn 10: 647917 open, 225683 closed
Turn 11: 1765278 open, 873601 closed
Turn 12: 3808011 open, 2638880 closed
=== Can win after 12 turns! ===
[3,0,>, 2,0,>, 1,0,>, 0,0,>, 0,0,v, 1,0,>, 4,0,v, 7,0,>, 6,0,>, 5,0,>, 3,0,>, 6,0,>]

$ ./solve.py --base 10
Turn 1: 0 open, 1 closed
Turn 2: 8 open, 2 closed
- INEXACT, iff solution is longer than 30 -
Turn 3: 46 open, 11 closed
Turn 4: 291 open, 58 closed
Turn 5: 1509 open, 350 closed
Turn 6: 5113 open, 1860 closed
Turn 7: 12095 open, 6974 closed
Turn 8: 21674 open, 19070 closed
Turn 9: 31437 open, 40745 closed
Turn 10: 39382 open, 72183 closed
Turn 11: 45238 open, 111566 closed
Turn 12: 49070 open, 156805 closed
Turn 13: 50958 open, 205876 closed
Turn 14: 53560 open, 256835 closed
Turn 15: 61662 open, 310396 closed
Turn 16: 78674 open, 372059 closed
Turn 17: 102197 open, 450734 closed
Turn 18: 123570 open, 552932 closed
Turn 19: 134608 open, 676503 closed
Turn 20: 134339 open, 811112 closed
Turn 21: 127049 open, 945452 closed
Turn 22: 114610 open, 1072502 closed
Turn 23: 93494 open, 1187113 closed
Turn 24: 62974 open, 1280608 closed
Turn 25: 31595 open, 1343583 closed
Turn 26: 10079 open, 1375179 closed
=== Can win after 26 turns! ===
[0,0,v, 8,0,v, 'expand', 1,1,>, 7,0,>, 2,2,v, 1,2,>, 6,2,v, 6,1,v, 5,2,>, 0,3,v, 4,3,v, 7,3,>, 8,2,v, 4,2,>, 4,1,v, 6,0,>, 5,0,>, 4,0,>, 1,2,v, 5,1,>, 3,2,v, 3,1,>, 3,0,>, 2,0,>, 1,0,>]

$ ./solve.py --base 11
Turn 1: 0 open, 1 closed
- INEXACT, iff solution is longer than 20 -
Turn 2: 11 open, 2 closed
Turn 3: 64 open, 14 closed
Turn 4: 214 open, 79 closed
Turn 5: 494 open, 294 closed
Turn 6: 868 open, 789 closed
Turn 7: 1265 open, 1658 closed
Turn 8: 1582 open, 2924 closed
Turn 9: 1669 open, 4507 closed
Turn 10: 1452 open, 6177 closed
Turn 11: 1001 open, 7630 closed
Turn 12: 506 open, 8632 closed
Turn 13: 674 open, 9139 closed
Turn 14: 3573 open, 9814 closed
Turn 15: 11310 open, 13388 closed
=== Can win after 15 turns! ===
[4,0,>, 3,0,>, 2,0,>, 1,0,>, 0,0,>, 0,0,v, 1,0,>, 4,0,v, 5,0,v, 6,0,v, 9,0,>, 8,0,>, 7,0,>, 3,0,>, 8,0,>]

$ ./solve.py --base 12
Turn 1: 0 open, 1 closed
- INEXACT, iff solution is longer than 30 -
Turn 2: 8 open, 2 closed
Turn 3: 29 open, 11 closed
Turn 4: 49 open, 41 closed
Turn 5: 51 open, 91 closed
Turn 6: 86 open, 143 closed
Turn 7: 547 open, 230 closed
Turn 8: 2651 open, 778 closed
Turn 9: 8555 open, 3430 closed
Turn 10: 19944 open, 11986 closed
Turn 11: 35653 open, 31931 closed
Turn 12: 50715 open, 67585 closed
Turn 13: 58789 open, 118301 closed
Turn 14: 56500 open, 177091 closed
Turn 15: 45789 open, 233592 closed
Turn 16: 32129 open, 279382 closed
Turn 17: 20334 open, 311512 closed
Turn 18: 12257 open, 331847 closed
Turn 19: 7134 open, 344105 closed
Turn 20: 3726 open, 351240 closed
Turn 21: 1566 open, 354967 closed
Turn 22: 500 open, 356534 closed
Turn 23: 91 open, 357035 closed
Turn 24: 6 open, 357127 closed
=== FAILED ===
```

Have fun running it with more RAM consumption.

Sadly, the sequence "3,3,6,6,9,9,15,12,26,15" is [not known](https://oeis.org/search?q=3%2C3%2C6%2C6%2C9%2C9%2C15).
What comes next?  Who knows? :D

Since odd degrees are trivial, we might instead want to look at even degrees.
However, there's [only one very unlikely result](https://oeis.org/search?q=3,6,9,15,26) for that.
Known: `3,6,9,15,26,>30`

- `ASSUME_MAX=30` fails (no such solution)
- `ASSUME_MAX=35` needs >6 GiB during Turn 18

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
