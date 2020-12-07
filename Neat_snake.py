#!/usr/bin/env python3

"""
"""

from Simple_ai_snake import Simple_ai_snake


class Neat_snake(Simple_ai_snake):
    """A class to house the NEAT AI snake."""

    def __init__(self, width, height):
        super().__init__(width, height)

    def move_snake(self, food):
        barrier_distances = self.look_ahead()
        food_distance = self.look_ahead(food)

    def look_ahead(self, food=None):
        """
        """
        directions = {
            (-1, 0): 0,
            (1, 0): 0,
            (0, -1): 0,
            (0, 1): 0,
            (-1, -1): 0,
            (-1, 1): 0,
            (1, 1): 0,
            (1, -1): 0
        }

        for direction in directions.keys():
            head = self.body[0]
            count = 0
            while True:
                count += 1
                look_at = tuple(map(sum, zip(direction, head)))
                head = look_at
                if food == None:
                    if look_at in self.body:
                        directions[direction] = count
                        break
                    elif look_at[0] == -1 or look_at[0] == self.width:
                        directions[direction] = count
                        break
                    elif look_at[1] == -1 or look_at[1] == self.height:
                        directions[direction] = count
                        break
                else:
                    if look_at == food:
                        directions[direction] = count
                        break
                    elif look_at in self.boundaries:
                        break

        return list(directions.values())
