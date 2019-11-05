#!/usr/bin/env python3

import argparse
import enum
import hashlib
import random
from the99game import Board


ASSUME_MAX = 11


def stringify_board(board):
    #assert board.base <= 10
    base_str = ','.join(str(e or 0) for e in board.state)
    return hashlib.md5(base_str.encode()).digest()


def try_solve(board):
    if board.has_won():
        return []
    seen = dict()
    reseen = 0
    queue_head = []
    queue_tail = []
    seen[stringify_board(board)] = '.'
    queue_head.append(board)
    turn = 0
    inexact = False
    step = 0
    while queue_head or queue_tail:
        if step % 10000 == 0:
            num_open = len(queue_head) + len(queue_tail)
            num_total = len(seen)
            print('\t{:6} steps, {:6} open, {:6} closed, {:6} reseen'.format(
                step, num_open, num_total - num_open, reseen))
        step += 1
        if not queue_head:
            queue_head = queue_tail[::-1]
            queue_tail = []
        board = queue_head.pop()
        if board.turn != turn:
            turn = board.turn
            num_open = len(queue_head) + len(queue_tail)
            num_total = len(seen)
            print('Turn {}: {:6} steps, {:6} open, {:6} closed, {:6} reseen'.format(
                turn, step, num_open, num_total - num_open, reseen))
        base_moves = seen[stringify_board(board)]
        for move in board.compute_legal_moves() + ['expand']:
            board_copy = Board(board.base, state=board.state, turn=board.turn)
            if move == 'expand':
                board_copy.expand()
            else:
                board_copy.make_move(move)
            if sum(e is not None for e in board_copy.state) > 2 * (ASSUME_MAX - board_copy.turn + 1):
                if not inexact:
                    inexact = True
                    print('- INEXACT, iff solution is longer than {} -'.format(ASSUME_MAX))
                continue
            next_string = stringify_board(board_copy)
            if next_string in seen:
                reseen += 1
                continue
            next_moves = ' '.join([base_moves, str(move)])
            seen[next_string] = next_moves
            queue_tail.append(board_copy)
            if board_copy.has_won():
                return board.turn, next_moves
    print('=== FAILED ===')
    exit(1)


def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", type=int, default=10, help="base of the game (defaults to 10)")
    return parser


def main():
    args = build_parser().parse_args()
    if args.base < 2:
        print('base must be at least 2')
        exit(1)
    board = Board(args.base)
    turns, winning_moves = try_solve(board)
    print('=== Can win after {} turns! ==='.format(turns))
    print(winning_moves)


if __name__ == '__main__':
    main()
