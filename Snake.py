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

FRAME_RATE = 7  # 7 is recommended


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
        with open("high_score.txt", 'r') as file:
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
        self.snake.move_snake(pygame.key.get_pressed())
        self.snake.update_body()

        # Ensure a human playable frame rate
        self.clock.tick(FRAME_RATE)

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
            with open("high_score.txt", 'w') as file:
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
                pygame.time.delay(500)
                break
            self.on_render()
        self.on_cleanup()

    def make_food(self):
        """Make a snake snack! Place only where snake isn't."""
        while True:
            coords = (randint(0, WIDTH - 1),
                      randint(0, HEIGHT - 1))
            if coords not in self.snake.body_coords:
                break

        return coords

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
    """A class to house the snake."""

    def __init__(self):
        # Start with three segments at center of screen
        self.body_coords = [
            (WIDTH // 2,
             HEIGHT // 2),
            (WIDTH // 2 + 1,
             HEIGHT // 2),
            (WIDTH // 2 + 2,
             HEIGHT // 2)
        ]
        # Start moving left
        self.direction = (-1, 0)
        # Init an empty list to countdown when to add segments
        self.adding_segment_countdowns = []

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
