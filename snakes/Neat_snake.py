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
        # Move straight
        else:
            pass

    def get_input(self):
        # Relative directions
        forward = self.direction
        diag_right = tuple([-1 * sum(self.direction) if x == 0 else x
                            for x in self.direction])
        right = (-1 * self.direction[1], -1 * self.direction[0])
        left = (self.direction[1], self.direction[0])
        diag_left = tuple([sum(self.direction) if x == 0 else x
                           for x in self.direction])

        """# Absolute directions
        barriers = {
            (0, 1): 0,  # North
            (1, 1): 0,  # Northeast
            (1, 0): 0,  # East
            (1, -1): 0,  # Southeast
            (0, -1): 0,  # South
            (-1, -1): 0,  # Southwest
            (-1, 0): 0,  # West
            (-1, 1): 0  # Northwest
        }"""
        barriers = {
            right: 0,
            diag_right: 0,
            forward: 0,
            diag_left: 0,
            left: 0
        }
        self.vision = []
        for direction in barriers:
            pointer = self.body[0]
            count = -1
            while True:
                count += 1
                look_at = tuple(map(sum, zip(direction, pointer)))
                pointer = look_at
                self.vision.append(look_at)
                if look_at in self.body:
                    barriers[direction] = count
                    self.vision = self.vision[:-1]
                    break
                if look_at not in self.board:
                    barriers[direction] = count
                    self.vision = self.vision[:-1]
                    break
        """# Normalize the barrier data and take the inverse
        for direction, distance in barriers.items():
            # Looking left or right
            if self.direction[0] != 0:
                barriers[direction] = 1 - (distance / self.width)
            # Looking up or down
            else:
                barriers[direction] = 1 - (distance / self.height)"""

        """dir_food = {
            (0, 1): 0,  # North
            (1, 1): 0,  # Northeast
            (1, 0): 0,  # East
            (1, -1): 0,  # Southeast
            (0, -1): 0,  # South
            (-1, -1): 0,  # Southwest
            (-1, 0): 0,  # West
            (-1, 1): 0  # Northwest
        }"""
        dir_food = {
            right: 0,
            diag_right: 0,
            forward: 0,
            diag_left: 0,
            left: 0
        }
        for direction in dir_food:
            pointer = self.body[0]
            while True:
                if sum(dir_food.values()) == 0:
                    look_at = tuple(map(sum, zip(direction, pointer)))
                    pointer = look_at
                    if look_at == self.food:
                        dir_food[direction] = 1
                        break
                    if look_at not in self.board:
                        break
                else:
                    break

        """warning = {
            (0, 1): 0,  # North
            (1, 1): 0,  # Northeast
            (1, 0): 0,  # East
            (1, -1): 0,  # Southeast
            (0, -1): 0,  # South
            (-1, -1): 0,  # Southwest
            (-1, 0): 0,  # West
            (-1, 1): 0  # Northwest
        }"""
        warning = {
            right: 0,
            diag_right: 0,
            forward: 0,
            diag_left: 0,
            left: 0
        }
        for direction in warning:
            look_at = tuple(map(sum, zip(direction, self.body[0])))
            if look_at in self.body or look_at not in self.board:
                warning[direction] = 1

        """# Report the direction of the snake
        snake_dir = {
            (0, 1): 0,  # North
            (1, 0): 0,  # East
            (0, -1): 0,  # South
            (-1, 0): 0  # West
        }
        for direction in snake_dir.keys():
            if self.direction == direction:
                snake_dir[direction] = 1
                break"""

        # Report if the snake is moving to the food
        moving_to_food = None
        if self.direction in [(-1, 0), (1, 0)]:
            sign_delta = self.food[0] - self.body[0][0]
            if self.direction[0] * sign_delta > 0:
                moving_to_food = 1
            else:
                moving_to_food = 0
        else:
            sign_delta = self.food[1] - self.body[0][1]
            if self.direction[1] * sign_delta > 0:
                moving_to_food = 1
            else:
                moving_to_food = 0

        """# Order inputs so the info for vision directions are side by side
        inputs = []
        for i in zip(list(dir_food.values()), list(warning.values())):
            inputs.append(i[0])
            inputs.append(i[1])
        inputs = inputs + list(snake_dir.values()) + [moving_to_food]"""

        inputs = list(barriers.values()) + \
            list(dir_food.values()) + \
            list(warning.values()) + [moving_to_food]

        return inputs

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
