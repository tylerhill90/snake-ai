#!/usr/bin/env python3
"""A game of classic snake played by a simple classic AI."""

from math import sqrt

from .Snake import Snake


class Simple_ai_snake(Snake):
    """
    A class to house the snake. This snake uses a simple classical AI that
    calculates the Euclidean distance between the head and food on the board
    and takes the shortest path to the food.
    """

    def __init__(self, width, height):
        super().__init__(width, height)

    def move_snake(self):
        """Move the snake and grow its body after eating food."""

        head = self.body[0]

        # Calculate distance from the head to the food for each possible move
        moves = {
            (0, -1): self.calc_dist(self.food, (head[0], head[1] - 1)),  # Up
            (0, 1): self.calc_dist(self.food, (head[0], head[1] + 1)),  # Down
            (-1, 0): self.calc_dist(self.food, (head[0] - 1, head[1])),  # Left
            (1, 0): self.calc_dist(self.food, (head[0] + 1, head[1]))  # Right
        }

        # Sort the dictionary of moves by distance
        sorted_moves = dict(sorted(moves.items(), key=lambda item: item[1]))

        # Create list of valid moves
        for move in sorted_moves.keys():
            if self.look_ahead(move):
                self.direction = move
                break

        # Just move right if no valid moves
        if not sorted_moves:
            self.direction = (1, 0)

        return

    @staticmethod
    def calc_dist(a, b):
        """Calculate the distance between 2 points."""
        return sqrt(abs(a[0] - b[0]) + abs(a[1] - b[1]))

    def look_ahead(self, direction):
        """Look ahead one space in a direction to see if it is a valid move."""
        head = self.body[0]
        move = tuple(map(sum, zip(head, direction)))
        if move in self.body or move not in self.board:
            return False
        else:
            return True
