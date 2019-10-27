#!/usr/bin/env python3

import argparse


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
                    line_parts.append('_' * self.celllen)
                else:
                    line_parts.append(self.cellformat.format(self.state[index]))
            line_parts.append('({})'.format(row))
            lines.append(' ' + ' '.join(line_parts))
        return '\n'.join(lines)


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
