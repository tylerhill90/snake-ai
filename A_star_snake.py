#!/usr/bin/env python3

"""A game of classic snake."""

from math import sqrt
from queue import PriorityQueue

from Simple_ai_snake import Simple_ai_snake


class A_star_snake(Simple_ai_snake):
    """A class to house the snake."""

    def __init__(self, width, height):
        super().__init__(width, height)
        self.render_path = True

    def move_snake(self, food):
        """Move the snake."""
        head = self.body[0]
        board = self.make_board()
        count = 0
        open_set = PriorityQueue()
        open_set.put((0, count, head))
        came_from = {}
        g_score = {coord: float("inf") for row in board for coord in row}
        g_score[head] = 0
        f_score = {coord: float("inf") for row in board for coord in row}
        f_score[head] = self.h(head, food)

        open_set_hash = {head}

        while not open_set.empty():
            # Look at the current node
            current = open_set.get()[2]
            # Synchronize the hash with the PriorityQueue
            open_set_hash.remove(current)

            # Handle finding the shortest path
            if current == food:
                # Create a list of the coordinates in the path
                self.path = []
                while current in came_from:
                    self.path.append(current)
                    current = came_from[current]
                # Get direction to move from difference of 2nd to last node in
                # path and head
                move = self.path[-1]
                move = tuple(map(lambda x: x[1] - x[0], zip(head, move)))
                if self.look_ahead(move):
                    self.direction = move
                return

            # Consider the neighbors of the current node
            for neighbor in self.get_neighbors(current):
                # Handle rare KeyErrors from edge cases
                try:
                    temp_g_score = g_score[current] + 1

                    # Update g score and path if necessary
                    if temp_g_score < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = temp_g_score
                        f_score[neighbor] = temp_g_score + \
                            self.h(neighbor, food)
                        if neighbor not in open_set_hash:
                            count += 1
                            open_set.put((f_score[neighbor], count, neighbor))
                            open_set_hash.add(neighbor)
                except KeyError:
                    print("KEY ERROR")
                    print("Neighbor:", neighbor)
                    print("Head:", head)
                    continue

        move = self.simple_move_snake(food)
        self.path = []
        return

    def get_neighbors(self, coord):
        neighbors = []
        row, col = coord
        # Down
        if row < self.width - 1 and (row + 1, col) not in self.body:
            neighbors.append((row + 1, col))

        # Up
        if row > 0 and (row - 1, col) not in self.body:
            neighbors.append((row - 1, col))

        # Right
        if col < self.height - 1 and (row, col + 1) not in self.body:
            neighbors.append((row, col + 1))

        # Left
        if col > 0 and (row, col - 1) not in self.body:
            neighbors.append((row, col - 1))

        return neighbors

    def simple_move_snake(self, food):
        super().move_snake(food)

    def make_board(self):
        board = []
        for row in range(self.width):
            board.append([])
            for col in range(self.height):
                board[row].append((row, col))
        return board

    @staticmethod
    def h(p1, p2):
        """Calculate the Manhattan distance between two points."""
        x1, y1 = p1
        x2, y2 = p2
        return abs(x1 - x2) + abs(y1 - y2)
