#!/usr/bin/env python3

"""
"""

from .Simple_ai_snake import Simple_ai_snake


class Neat_snake(Simple_ai_snake):
    """A class to house the NEAT AI snake."""

    def __init__(self, width, height):
        super().__init__(width, height)
        self.direction = (-1, 0)
        self.hunger = 0
        self.path = set()
        self.time_loop = 0
        self.alive = True
        self.vision = []

    def move_snake(self, network):
        self.hunger += 1
        output = network.activate(self.get_input())

        # Move right
        if output[0] == max(output):
            self.direction = (-1 * self.direction[1], -1 * self.direction[0])
        # Move left
        elif output[2] == max(output):
            self.direction = (self.direction[1], self.direction[0])
        # Else keep moving in the current direction

    def get_input(self):
        right = (-1 * self.direction[1], -1 * self.direction[0])
        diag_right = tuple([-1 * sum(self.direction) if x == 0 else x
                            for x in self.direction])
        forward = self.direction
        diag_left = tuple([sum(self.direction) if x == 0 else x
                           for x in self.direction])
        left = (self.direction[1], self.direction[0])

        directions_barrier = {
            right: 0,
            diag_right: 0,
            forward: 0,
            diag_left: 0,
            left: 0
        }
        directions_food = {
            right: 0,
            diag_right: 0,
            forward: 0,
            diag_left: 0,
            left: 0
        }

        self.vision = []
        for direction in directions_barrier:
            pointer = self.body[0]
            count = -1
            while True:
                count += 1
                look_at = tuple(map(sum, zip(direction, pointer)))
                pointer = look_at
                self.vision.append(look_at)
                if look_at in self.body:
                    directions_barrier[direction] = count
                    self.vision = self.vision[:-1]
                    break
                if look_at not in self.board:
                    directions_barrier[direction] = count
                    self.vision = self.vision[:-1]
                    break

        for direction in directions_food:
            pointer = self.body[0]
            while True:
                if sum(directions_food.values()) == 0:
                    count += 1
                    look_at = tuple(map(sum, zip(direction, pointer)))
                    pointer = look_at
                    if look_at == self.food:
                        directions_food[direction] = 1
                        break
                    if look_at not in self.board:
                        break
                else:
                    break

        # Normalize the barrier data and take the inverse
        for direction, distance in directions_barrier.items():
            # Looking left or right
            if forward[0] != 0:
                directions_barrier[direction] = 1 - (distance / self.width)
            # Looking up or down
            else:
                directions_barrier[direction] = 1- (distance / self.height)

        # Report the direction of the snake
        directions_snake = {
            (-1, 0): 0,
            (0, 1): 0,
            (1, 0): 0,
            (0, -1): 0
        }
        for direction in directions_snake.keys():
            if self.direction == direction:
                directions_snake[direction] = 1
                break

        # Report the direction(s) of the food relative to the head
        """directions_food = {
            (-1, 0): 0,
            (0, 1): 0,
            (1, 0): 0,
            (0, -1): 0
        }
        for direction in directions_food.keys():
            if self.food == direction:
                directions_food[direction] = 1"""
                

        return list(directions_barrier.values()) + list(directions_food.values()) + list(directions_snake.values())

    def check_food_eaten(self):
        """See if the snake head collides with the food."""
        head = self.body[0]

        if head == self.food:
            self.food = self.make_food()  # Make new food
            self.score += 1  # Increment score
            self.adding_segment_countdowns.append(len(self.body))
            return True

        return False

    def check_opposite(self, move):
        opposite = tuple(map(lambda x: x * -1, self.direction))
        if move == opposite:
            return False

        return True
