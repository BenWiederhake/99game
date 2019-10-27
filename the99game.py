#!/usr/bin/env python3

import argparse
import enum
import random


class Direction(enum.Enum):
    RIGHT = '>'
    DOWN = 'v'


class Move:
    def __init__(self, col, row, direction):
        self.col = int(col)
        self.row = int(row)
        self.direction = Direction(direction)

    def __str__(self):
        return '{},{},{}'.format(self.col, self.row, self.direction.value)

    __repr__ = __str__

    @staticmethod
    def parse(string):
        parts = string.split(',')
        try:
            return Move(*parts)
        except (TypeError, ValueError):
            return None


class Board:
    def __init__(self, base, state=None, turn=None):
        self.base = base
        self.celllen = len(str(self.base - 1))
        self.cellformat = '{{:{}}}'.format(self.celllen)
        if state:
            self.state = list(state)
        else:
            self.state = Board.build_state(self.base)
        self.turn = turn or 1
        self.cols = self.base - 1

    @staticmethod
    def build_state(base):
        board = []
        for i in range(1, base):
            board.append(i)
        for i in range(1, base):
            board.append(1)
            board.append(i)
        return board

    def can_combine(self, number_a, number_b):
        if number_a is None or number_b is None:
            return False
        return number_a == number_b or number_a + number_b == self.base

    def colrow_to_index(self, col, row):
        return col + row * self.cols

    def index_to_colrow(self, index):
        return index % self.cols, index // self.cols

    @property
    def rows(self):
        return (len(self.state) + (self.cols - 1)) // self.cols

    def __str__(self):
        lines = []
        lines.append('(' + ' '.join(self.cellformat.format(i) for i in range(self.cols)) + ')')
        for row in range(self.rows):
            line_parts = []
            for col in range(self.cols):
                index = self.colrow_to_index(col, row)
                if index >= len(self.state):
                    line_parts.append(' ' * self.celllen)
                elif self.state[index] is None:
                    line_parts.append('x' * self.celllen)
                else:
                    line_parts.append(self.cellformat.format(self.state[index]))
            line_parts.append('({})'.format(row))
            lines.append(' ' + ' '.join(line_parts))
        return '\n'.join(lines)

    def compute_legal_moves(self):
        legal_moves = []
        base_index = 0
        while base_index is not None:
            next_index = self.find_down(base_index)
            if next_index is not None and self.can_combine(self.state[base_index], self.state[next_index]):
                legal_moves.append(Move(*self.index_to_colrow(base_index), Direction.DOWN))
            next_index = self.find_right(base_index)
            if next_index is not None and self.can_combine(self.state[base_index], self.state[next_index]):
                legal_moves.append(Move(*self.index_to_colrow(base_index), Direction.RIGHT))
            # It would be simpler to just "+1" here.  However, if there are many consecutive
            # empty cells, we might run into quadratic behavior.  Thus, we have to skip the
            # known-empty cells immediately.
            base_index = next_index
        return legal_moves

    def find_down(self, index):
        index += self.cols
        while index < len(self.state):
            if self.state[index] is not None:
                return index
            index += self.cols
        return None

    def find_right(self, index):
        index += 1
        while index < len(self.state):
            if self.state[index] is not None:
                return index
            index += 1
        return None

    def find_next(self, index, direction):
        if direction == Direction.DOWN:
            return self.find_down(index)
        elif direction == Direction.RIGHT:
            return self.find_right(index)
        else:
            raise ValueError(direction, 'is not a Direction?!')

    def make_move(self, move):
        base_index = self.colrow_to_index(move.col, move.row)
        next_index = self.find_next(base_index, move.direction)
        if next_index is None or not self.can_combine(self.state[base_index], self.state[next_index]):
            return False
        self.state[base_index] = None
        self.state[next_index] = None
        self.turn += 1
        return True

    def expand(self):
        old_len = len(self.state)
        for i in range(old_len):
            val = self.state[i]
            if val is not None:
                self.state.append(val)
        self.turn += 1

    def has_won(self):
        return all(e is None for e in self.state)


class Game:
    def __init__(self, base=None):
        self.base = base
        self.moves = []
        self.board = Board(base)

    def rebuild_board(self):
        self.board = Board(self.base)
        oldmoves = self.moves
        self.moves = []
        for m in oldmoves:
            assert m != 'back'
            self.make_move(m)

    def make_move(self, move_str):
        if move_str == 'back':
            self.moves = self.moves[:-1]
            self.rebuild_board()
            return True, ''
        if move_str == 'expand':
            self.moves.append(move_str)
            self.board.expand()
            return True, ''
        move = Move.parse(move_str)
        if move is None:
            return False, 'parse'
        res = self.board.make_move(move)
        if res:
            self.moves.append(move_str)
            return True, ''
        else:
            return False, 'make'


def build_parser():
    parser = argparse.ArgumentParser()
    # TODO: Support other bases than just 10
    parser.add_argument("--base", type=int, default=10, help="dase of the game (defaults to 10)")
    parser.add_argument("--hide-board", action="store_true", help="do not show the board while playing")
    parser.add_argument("--hints", action="store_true", help="show legal moves at each step")
    return parser    


def main():
    args = build_parser().parse_args()
    if args.base < 2:
        print('base must be at least 2')
        exit(1)
    game = Game(base=args.base)
    moves = []
    while not game.board.has_won():
        print('=== Turn {} ==='.format(game.board.turn))
        if not args.hide_board:
            print(game.moves)
            print(game.board)
        if args.hints:
            moves = game.board.compute_legal_moves()
            if not moves:
                print('There are no legal moves.')
                print([])
                print('You could "expand" the board, or go "back".')
            else:
                print('Legal moves are:')
                print(moves)
                print('You can also "expand" the board, or go one step "back".')
        print('Please enter a move in the "col,row,dir" format, or "back" or "expand":')
        try:
            move = input('? ')
        except (EOFError, KeyboardInterrupt):
            print('Exiting')
            exit(1)
        if args.hints:
            if move.startswith('m'):
                move = str(moves[int(move[1:])])
                print('→{}'.format(move))
            elif not move:
                if moves:
                    move = str(random.choice(moves + ['back', 'expand']))
                else:
                    if random.random() < 0.6:
                        move = 'back'
                    else:
                        move = 'expand'
                print('→{}'.format(move))
        res, error = game.make_move(move)
        if not res:
            print('Cannot {} that move.'.format(error))  # Dirty hack
        print()
    print('=== You won after {} turns! ==='.format(game.board.turn - 1))
    if not args.hide_board:
        print(game.moves)
        print(game.board)


if __name__ == '__main__':
    main()
