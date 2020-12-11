#!/usr/bin/env python3

"""
"""

from math import atan2

from Simple_ai_snake import Simple_ai_snake


class Neat_snake(Simple_ai_snake):
    """A class to house the NEAT AI snake."""

    def __init__(self, width, height):
        super().__init__(width, height)
        self.alive = True
        self.starvation = 0
        self.direction = (-1, 0)
        self.steps_taken = 0
        self.vision = []
        self.diag_len = self.calc_dist((0, 0), (self.width, self.height))

    def move_snake(self, network):
        food_vision = self.get_input(food_=True)
        barrier_vision = self.get_input()
        food_distance = self.calc_dist(self.body[0], self.food) / self.diag_len

        output = network.activate(barrier_vision + food_vision + (food_distance,))

        # Move right
        if output[0] == max(output):
            self.direction = (-1 * self.direction[1], -1 * self.direction[0])
        # Move left
        elif output[2] == max(output):
            self.direction = (self.direction[1], self.direction[0])

    def get_input(self, food_=False):
        right = (-1 * self.direction[1], -1 * self.direction[0])
        diag_right = tuple([-1 * sum(self.direction) if x == 0 else x
                            for x in self.direction])
        forward = self.direction
        diag_left = tuple([sum(self.direction) if x == 0 else x
                           for x in self.direction])
        left = (self.direction[1], self.direction[0])

        directions = {
            right: 0,
            diag_right: 0,
            forward: 0,
            diag_left: 0,
            left: 0
        }

        self.vision = []
        for direction in directions:
            pointer = self.body[0]
            count = -1
            while True:
                count += 1
                look_at = tuple(map(sum, zip(direction, pointer)))
                pointer = look_at
                if not food_:
                    self.vision.append(look_at)
                    if look_at in self.body:
                        directions[direction] = count
                        self.vision = self.vision[:-1]
                        break
                    if look_at not in self.board:
                        directions[direction] = count
                        self.vision = self.vision[:-1]
                        break
                else:
                    if look_at == food_:
                        directions[direction] = count
                        break
                    if look_at not in self.board:
                        break
                if count > self.width:
                    break

        # Normalize the data
        for direction, distance in directions.items():
            # Looking left or right
            if forward[0] != 0:
                directions[direction] = distance / self.width
            # Looking up or down
            else:
                directions[direction] = distance / self.height

        return tuple(directions.values())

    """def look_ahead(self, food_=None):
        """
    """
        directions = {
            (-1, 0): 0,
            (1, 0): 0,
            (0, -1): 0,
            (0, 1): 0
        }
        head = self.body[0]

        for direction in directions:
            count = 0
            while True:
                count += 1
                look_at = tuple(map(sum, zip(direction, head)))
                head = look_at
                if not food_:
                    if look_at in self.body:
                        directions[direction] = count
                        break
                    if look_at in self.board:
                        directions[direction] = count
                        break
                else:
                    if look_at == food_:
                        directions[direction] = count
                        break
                    if look_at in self.board:
                        break
                if count > self.width:
                    break

        return tuple(directions.values())"""

    def check_food_eaten(self):
        """See if the snake head collides with the food."""
        head = self.body[0]
        self.starvation += 1

        if head == self.food:
            self.food = self.make_food()  # Make new food
            self.score += 1  # Increment score
            self.starvation = 0
            self.adding_segment_countdowns.append(len(self.body))
            return True

        return False

    def check_opposite(self, move):
        opposite = tuple(map(lambda x: x * -1, self.direction))
        if move == opposite:
            return False

        return True
