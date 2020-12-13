#!/usr/bin/env python3

"""A game of classic snake."""

from random import randint
import pygame
from pygame.locals import (
    KEYDOWN,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_SPACE,
    K_ESCAPE,
    QUIT
)


class Snake:
    """A class to house the snake."""

    def __init__(self, width, height):
        # Start with three segments at center of screen
        self.width = width
        self.height = height
        self.body = [(width // 2,
                      height // 2)]
        self.food = self.make_food()
        self.score = 0
        # Start not moving
        self.direction = (0, 0)
        # Init an empty list to countdown when to add segments
        self.adding_segment_countdowns = []

        self.board = [(row, col) for row in range(self.width) for col in range(self.height)]

    def make_food(self):
        """Make a snake snack! Place only where snake isn't."""
        while True:
            coords = (randint(0, self.width - 1),
                      randint(0, self.height - 1))
            if coords not in self.body:
                break

        return coords

    def check_food_eaten(self):
        """See if the snake head collides with the food."""
        head = self.body[0]

        if head == self.food:
            self.food = self.make_food()  # Make new food
            self.score += 1  # Increment score
            self.adding_segment_countdowns.append(len(self.body))

    def move_snake(self, pressed_keys):
        """Move the snake."""

        # Check if the snake changes direction and don't allow back tracking
        if pressed_keys[K_UP] and self.direction != (0, 1):
            self.direction = (0, -1)
        elif pressed_keys[K_DOWN] and self.direction != (0, -1):
            self.direction = (0, 1)
        elif pressed_keys[K_LEFT] and self.direction != (1, 0):
            self.direction = (-1, 0)
        elif pressed_keys[K_RIGHT] and self.direction != (-1, 0):
            self.direction = (1, 0)
        # Pause the game
        elif pressed_keys[K_SPACE]:
            pause = True
            while pause:
                for event in pygame.event.get():
                    if event.type == KEYDOWN:
                        if event.key != K_SPACE:
                            pause = False

    def update_body(self):
        """Add a segment in the direction of motion and take one away from the
        tail unless the snake ate food."""
        if self.direction != (0, 0):
            # Move the snake forward by adding a segment in the direction of motion
            self.body.insert(
                0, tuple(map(sum, zip(self.body[0], self.direction))))

            # Add a segment if food was eaten when it has passed the length of the
            # snake by counting down each instance of eating a food
            if len(self.adding_segment_countdowns) > 0:
                # Decrement each of the countdowns
                self.adding_segment_countdowns = [
                    x - 1 for x in self.adding_segment_countdowns]

                # Remove the trailing segment only if the countdown hasn't finished
                if self.adding_segment_countdowns[0] > 0:
                    self.body.pop()

                # Get rid off finished countdowns
                if self.adding_segment_countdowns[0] == 0:
                    self.adding_segment_countdowns.pop(0)

            # Remove the trailing segment if no countdowns
            else:
                self.body.pop()
