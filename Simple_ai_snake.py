#!/usr/bin/env python3
"""A game of classic snake played by a simple classic AI."""

import sys
from math import sqrt
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

# Define global constants
CELL = 20
MARGIN = 1
WIDTH = 50  # 50 suggested
HEIGHT = 35  # 35 suggested
SCORE_BOARD = 40
SCREEN_WIDTH = WIDTH * CELL + (MARGIN * WIDTH + 1)
SCREEN_HEIGHT = HEIGHT * CELL + (MARGIN * HEIGHT + 1)

BLACK = (0, 0, 0)
GREY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Change to non-zero for human speed
FRAME_RATE = 0
DELAY = 0


class App:
    """Class to house the game."""

    def __init__(self):
        pygame.init()
        self.running = True
        self.screen = pygame.display.set_mode((
            SCREEN_WIDTH, SCREEN_HEIGHT + SCORE_BOARD
        ))
        self.snake = Snake()
        self.food = self.make_food()
        self.score = 0
        self.font = pygame.font.SysFont(None, 36)
        with open("high_score_simple_ai.txt", 'r') as file:
            self.high_score = file.readline()
        self.high_score = int(self.high_score)

        # Setup a clock for framerate
        self.clock = pygame.time.Clock()

    def on_event(self, event):
        """Handle events each game loop."""
        if event.type == pygame.QUIT:
            self.running = False
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, then stop the loop.
            if event.key == K_ESCAPE:
                self.running = False

    def on_loop(self):
        """Handle game logic each game loop."""
        if self.check_lose_conditions():
            return
        self.check_food_eaten()

        # Move the snake
        self.snake.move_snake(self.food)
        self.snake.update_body()

        # Ensure a human playable frame rate
        self.clock.tick(FRAME_RATE)

    def make_food(self):
        """Make a snake snack! Place only where snake isn't."""
        while True:
            coords = (randint(0, WIDTH - 1),
                      randint(0, HEIGHT - 1))
            if coords not in self.snake.body_coords:
                break

        return coords

    def on_render(self):
        """Render the screen each game loop."""
        # Draw a black background
        self.screen.fill(BLACK)

        # Draw the food
        pygame.draw.rect(self.screen, RED,
                         [(MARGIN + CELL) * self.food[0] + MARGIN,
                          (MARGIN + CELL) * self.food[1] + MARGIN,
                          CELL,
                          CELL
                          ])

        # Draw the snake
        for coord in self.snake.body_coords:
            pygame.draw.rect(self.screen, GREEN,
                             [(MARGIN + CELL) * coord[0] + MARGIN,
                              (MARGIN + CELL) * coord[1] + MARGIN,
                              CELL,
                              CELL
                              ])

        # Draw the scoreboard
        pygame.draw.rect(self.screen, GREY,
                         [
                             0,
                             (MARGIN + CELL) * HEIGHT + MARGIN,
                             (MARGIN + CELL) * WIDTH + MARGIN,
                             (MARGIN + CELL) * HEIGHT + MARGIN + SCORE_BOARD
                         ])
        current_score = self.font.render(f"Score: {self.score}", True, BLACK)
        if self.score < self.high_score:
            high_score = self.font.render(
                f"High Score: {self.high_score}", True, BLACK)
        else:
            high_score = self.font.render(
                f"High Score: {self.score}", True, BLACK)
        self.screen.blit(current_score, (5, (MARGIN + CELL)
                                         * HEIGHT + MARGIN + 5))

        self.screen.blit(high_score, (((MARGIN + CELL) * WIDTH +
                                       MARGIN) // 2, (MARGIN + CELL) *
                                      HEIGHT + MARGIN + 5))

        # Display the screen
        pygame.display.flip()

    def on_cleanup(self):
        """Exit the game."""
        # Update the high score if necessary
        if self.score > self.high_score:
            with open("high_score_simple_ai.txt", 'w') as file:
                file.write(f"{self.score}")
        # Exit pygame without errors
        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def on_execute(self):
        """Start the game loop."""
        while self.running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            if not self.running:
                pygame.time.delay(DELAY)
                break
            self.on_render()
        self.on_cleanup()

    def check_lose_conditions(self):
        """See if the game is over."""
        head = self.snake.body_coords[0]

        # Check if snake is out of bounds
        if head[0] < 0 or head[0] == WIDTH:
            self.running = False
            return True
        elif head[1] < 0 or head[1] == HEIGHT:
            self.running = False
            return True
        # Check if snake hits itself
        elif head in self.snake.body_coords[1:]:
            self.running = False
            return True

        return False

    def check_food_eaten(self):
        """See if the snake head collides with the food."""
        head = self.snake.body_coords[0]

        if head == self.food:
            self.food = self.make_food()  # Make new food
            self.score += 1  # Increment score
            self.snake.adding_segment_countdowns.append(
                len(self.snake.body_coords))


class Snake:
    """
    A class to house the snake. This snake uses a simple classical AI that
    calculates the distance between the head and food on the board and takes
    the shortest path to the food.

    It also utilizes a heuristic to hopefully avoid "boxing itself in" with its
    own body. When two valid moves result in the same distance to the food the
    snake is running into it's own body on the shortest path to the food and
    this can result in boxing itself in. I noticed that, more often than not,
    turning towards the tail in this scenario results in avoiding this.

    In 150 simulations of this heuristic behavior and 150 simulations of not
    using it, the heuristic resulted in higher average game scores (around 65
    compared to 45) and a higher overall high score for the AI (146 compared
    to 97).
    """

    def __init__(self):
        # Start with three segments
        self.body_coords = [
            (WIDTH // 2,
             HEIGHT // 2),
            (WIDTH // 2 + 1,
             HEIGHT // 2),
            (WIDTH // 2 + 2,
             HEIGHT // 2)
        ]
        # Start not moving
        self.direction = (-1, 0)
        # Init an empty list to countdown when to add segments
        self.adding_segment_countdowns = []

    def move_snake(self, food):
        """Move the snake and grow its body after eating food."""

        head = self.body_coords[0]
        tail = self.body_coords[-1]

        # Calculate distance from the head to the food for each possible move
        moves = {
            (0, -1): self.calc_dist(food, (head[0], head[1] - 1)),  # Up
            (0, 1): self.calc_dist(food, (head[0], head[1] + 1)),  # Down
            (-1, 0): self.calc_dist(food, (head[0] - 1, head[1])),  # Left
            (1, 0): self.calc_dist(food, (head[0] + 1, head[1]))  # Right
        }

        # Sort the dictionary of moves by distance
        sorted_moves = dict(sorted(moves.items(), key=lambda item: item[1]))

        # Create list of valid moves
        valid_moves = []
        for move in sorted_moves.keys():
            if self.look_ahead(move):
                valid_moves.append(move)

        # Heuristic:
        # See if the first two valid moves are tied in distance to the food
        # If so move towards the tail
        if len(valid_moves) >= 2:
            if moves[valid_moves[0]] == moves[valid_moves[1]]:
                # Calculate new head coordinates of moves
                first_move_coord = tuple(map(sum, zip(valid_moves[0] + head)))
                second_move_coord = tuple(map(sum, zip(valid_moves[1] + head)))
                # Calculate head distance to tail
                first_move_dist = self.calc_dist(first_move_coord, tail)
                second_move_dist = self.calc_dist(second_move_coord, tail)
                if first_move_dist < second_move_dist:
                    self.direction = valid_moves[0]
                else:
                    self.direction = valid_moves[1]

            # First 2 moves aren't tied for distance so chose the 1st
            else:
                self.direction = valid_moves[0]

        # Only 1 valid move so chose that
        elif len(valid_moves) == 1:
            self.direction = valid_moves[0]

        # No valid moves so just move anyway to end the game
        else:
            self.direction = (1, 0)

    @staticmethod
    def calc_dist(a, b):
        """Calculate the distance between 2 points."""
        return sqrt(abs(a[0] - b[0]) + abs(a[1] - b[1]))

    def look_ahead(self, direction):
        """Look ahead one space in a direction to see if it is a valid move."""
        head = self.body_coords[0]
        move = (head[0] + direction[0], head[1] + direction[1])
        if move in self.body_coords:
            return False
        elif move[0] < 0 or move[0] == WIDTH:
            return False
        elif move[1] < 0 or move[1] == HEIGHT:
            return False
        else:
            return True

    def update_body(self):
        """Add a segment in the direction of motion and take one away from the
        tail unless the snake ate food."""
        # Move the snake forward by adding a segment in the direction of motion
        self.body_coords.insert(
            0, tuple(map(sum, zip(self.body_coords[0], self.direction))))

        # Add a segment if food was eaten when it has passed the length of the
        # snake by counting down each instance of eating a food
        if len(self.adding_segment_countdowns) > 0:
            # Decrement each of the countdowns
            self.adding_segment_countdowns = [
                x - 1 for x in self.adding_segment_countdowns]

            # Remove the trailing segment only if the countdown hasn't finished
            if self.adding_segment_countdowns[0] > 0:
                self.body_coords.pop()

            # Get rid off finished countdowns
            if self.adding_segment_countdowns[0] == 0:
                self.adding_segment_countdowns.pop(0)

        # Remove the trailing segment if no countdowns
        else:
            self.body_coords.pop()


if __name__ == "__main__":
    game = App()
    game.on_execute()
