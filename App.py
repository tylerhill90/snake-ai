#!/usr/bin/env python3

"""A game of classic snake."""

import sys
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
from Snake import Snake
from Simple_ai_snake import Simple_ai_snake
from A_star_snake import A_star_snake

# Define global constants
CELL = 20
MARGIN = 1
WIDTH = 50
HEIGHT = 35
SCORE_BOARD = 40
SCREEN_WIDTH = WIDTH * CELL + (MARGIN * WIDTH + 1)
SCREEN_HEIGHT = HEIGHT * CELL + (MARGIN * HEIGHT + 1)

BLACK = (0, 0, 0)
GREY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PURPLE = (147, 132, 240)


class App:
    """Class to house the game."""

    def __init__(self, snake, frame_rate=100):
        pygame.init()
        self.running = True
        self.screen = pygame.display.set_mode((
            SCREEN_WIDTH, SCREEN_HEIGHT + SCORE_BOARD
        ))
        self.snake = snake
        if isinstance(self.snake, Simple_ai_snake):
            self.frame_rate = frame_rate
        else:
            self.frame_rate = 7
        self.food = self.make_food()
        self.score = 0
        self.font = pygame.font.SysFont(None, 36)
        self.high_score = self.get_high_score()

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
            # Pause the game
            if isinstance(self.snake, A_star_snake):
                if event.key == K_SPACE:
                    self.snake.render_path = not self.snake.render_path

    def on_loop(self):
        """Handle game logic each game loop."""
        if self.check_lose_conditions():
            return
        self.check_food_eaten()

        # Move the snake
        if isinstance(self.snake, Simple_ai_snake):
            self.snake.move_snake(self.food)
        else:
            self.snake.move_snake(pygame.key.get_pressed())

        self.snake.update_body()

        # Ensure a human playable frame rate
        self.clock.tick(self.frame_rate)

    def on_render(self):
        """Render the screen each game loop."""
        # Draw a black background
        self.screen.fill(BLACK)

        # Draw the path to the food if requested as decreasing shades of purple
        if isinstance(self.snake, A_star_snake):
            if self.snake.render_path:
                count = 0
                for coord in self.snake.path[::-1]:
                    count += 1
                    # Shade each cell of the path based on the cell's distance in
                    # the path
                    shade = tuple(
                        x - 4 * count if x > 4 * count else 0 for x in PURPLE)
                    self.render_cell(shade, coord)

        # Draw the food
        self.render_cell(RED, self.food)

        # Draw the snake
        for coord in self.snake.body:
            self.render_cell(GREEN, coord)

        # Draw the scoreboard
        pygame.draw.rect(self.screen, GREY,
                         [0,
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
            with open("high_score_a_star.txt", 'w') as file:
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
                break
            self.on_render()
        self.on_cleanup()

    def get_high_score(self):
        if isinstance(self.snake, A_star_snake):
            high_score_file = "high_score_a_star.txt"
        elif isinstance(self.snake, Simple_ai_snake):
            high_score_file = "high_score_simple.txt"
        else:
            high_score_file = "high_score.txt"
        with open(high_score_file, 'r') as file:
            high_score = int(file.readline())

        return high_score

    def make_food(self):
        """Make a snake snack! Place only where snake isn't."""
        while True:
            coords = (randint(0, WIDTH - 1),
                      randint(0, HEIGHT - 1))
            if coords not in self.snake.body:
                break

        return coords

    def check_lose_conditions(self):
        """See if the game is over."""
        head = self.snake.body[0]

        # Check if snake is out of bounds
        if head[0] < 0 or head[0] == WIDTH:
            self.running = False
            return True
        elif head[1] < 0 or head[1] == HEIGHT:
            self.running = False
            return True
        # Check if snake hits itself
        elif head in self.snake.body[1:]:
            self.running = False
            return True

        return False

    def check_food_eaten(self):
        """See if the snake head collides with the food."""
        head = self.snake.body[0]

        if head == self.food:
            self.food = self.make_food()  # Make new food
            self.score += 1  # Increment score
            self.snake.adding_segment_countdowns.append(
                len(self.snake.body))

    def render_cell(self, color, coord):
        """Render a single cell of the game board."""
        pygame.draw.rect(self.screen, color,
                         [(MARGIN + CELL) * coord[0] + MARGIN,
                             (MARGIN + CELL) * coord[1] + MARGIN,
                             CELL,
                             CELL
                          ])


if __name__ == "__main__":
    game = App(A_star_snake(WIDTH, HEIGHT))
    game.on_execute()
