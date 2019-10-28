#!/usr/bin/env python3

import argparse
import enum
import random
from the99game import Board


def stringify_board(board):
    return ''.join(str(e or 0) for e in board.state)


def try_solve(board):
    if board.has_won():
        return []
    seen = dict()
    queue_head = []
    queue_tail = []
    seen[stringify_board(board)] = []
    queue_head.append(board)
    turn = 0
    inexact = False
    while queue_head or queue_tail:
        if not queue_head:
            queue_head = queue_tail[::-1]
            queue_tail = []
        board = queue_head.pop()
        if len(board.state) > 100:
            if not inexact:
                inexact = True
                print('- INEXACT, possibly -')
            continue
        if board.turn != turn:
            turn = board.turn
            num_open = len(queue_head) + len(queue_tail)
            num_total = len(seen)
            print('Turn {}: {} open, {} closed'.format(
                turn, num_open, num_total - num_open))
        base_moves = seen[stringify_board(board)]
        for move in board.compute_legal_moves() + ['expand']:
            board_copy = Board(board.base, state=board.state, turn=board.turn)
            if move == 'expand':
                board_copy.expand()
            else:
                board_copy.make_move(move)
            next_string = stringify_board(board_copy)
            if next_string in seen:
                continue
            seen[next_string] = base_moves + [move]
            queue_tail.append(board_copy)
            if board_copy.has_won():
                return base_moves + [move]


def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", type=int, default=10, help="dase of the game (defaults to 10)")
    return parser


def main():
    args = build_parser().parse_args()
    if args.base < 2:
        print('base must be at least 2')
        exit(1)
    board = Board(args.base)
    winning_moves = try_solve(board)
    print('=== Can win after {} turns! ==='.format(len(winning_moves)))
    print(winning_moves)


if __name__ == '__main__':
    main()
