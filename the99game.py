#!/usr/bin/env python3

import argparse
import enum


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
    def __init__(self, base=None, state=None, turn=None):
        self.base = base or 10
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
        if not self.can_combine(self.state[base_index], self.state[next_index]):
            return False
        self.state[base_index] = None
        self.state[next_index] = None
        return True

    def expand(self):
        old_len = len(self.state)
        for i in range(old_len):
            val = self.state[i]
            if val is not None:
                self.state.append(val)


def build_parser():
    parser = argparse.ArgumentParser()
    # TODO: Support other bases than just 10
    # parser.add_argument("--base", type=int, help="dase of the game (defaults to 10)")
    parser.add_argument("--hide-board", action="store_true", help="do not show the board while playing")
    return parser    


def main():
    args = build_parser().parse_args()
    raise NotImplementedError()


if __name__ == '__main__':
    main()
