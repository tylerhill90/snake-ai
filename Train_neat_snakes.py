#!/usr/bin/env python3

"""A game of classic snake."""

import sys
import os
from random import randint
import neat
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
from Simple_ai_snake import Simple_ai_snake
from A_star_snake import A_star_snake
from Neat_snake import Neat_snake

# Define global constants
CELL = 7
MARGIN = 1
WIDTH = 20
HEIGHT = 20
SCORE_BOARD = 35
SCREEN_WIDTH = (WIDTH * CELL + (MARGIN * WIDTH + 1))
SCREEN_HEIGHT = (HEIGHT * CELL + (MARGIN * HEIGHT + 1)) + SCORE_BOARD

BLACK = (0, 0, 0)
GREY = (200, 200, 200)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 75)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PURPLE = (147, 132, 240)


class Training_app:
    """Class to house the game."""

    def __init__(self, genomes, config, frame_rate=0):
        pygame.init()
        self.running = True
        self.render_vision = False
        self.frame = 0
        self.screen = pygame.display.set_mode((
            SCREEN_WIDTH * 4, SCREEN_HEIGHT * 3
        ))

        self.den = []
        self.nets = []
        self.ge = []

        for _, g in genomes:
            net = neat.nn.FeedForwardNetwork.create(g, config)
            self.nets.append(net)
            self.den.append(Neat_snake(WIDTH, HEIGHT))
            g.fitness = 0
            self.ge.append(g)

        self.frame_rate = frame_rate
        self.font = pygame.font.SysFont(None, 35)
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
            if event.key == K_SPACE:
                self.render_vision = not self.render_vision

    def on_loop(self):
        """Handle game logic each game loop."""

        for x, snake in enumerate(self.den):
            if snake.starvation >= 80:
                snake.direction = (0, 0)
                snake.alive = False
            if snake.alive:
                if self.check_lose_conditions(snake):
                    snake.direction = (0, 0)
                    snake.alive = False
                    self.ge[x].fitness -= 20
                    continue

                if snake.check_food_eaten():
                    self.ge[x].fitness += 5

                # Move the snake for AI
                snake.move_snake(self.nets[x])
                snake.update_body()

        # Check if all snakes are dead
        dead = sum([1 for snake in self.den if not snake.alive])
        if dead == 100:
            self.running = False

        # Ensure a human playable frame rate
        self.clock.tick(self.frame_rate)

    def check_lose_conditions(self, snake):
        """See if the game is over."""
        head = snake.body[0]

        # Check if snake is out of bounds or hits itself
        if head not in snake.board or head in snake.body[1:]:
            return True

        return False

    def on_render(self):
        """Render the screen each game loop."""
        # Draw a black background
        self.screen.fill(BLACK)

        for game, snake in enumerate(self.den, start=1):
            if game < 13:
                if game < 5:
                    row = 0
                elif 4 < game < 9:
                    row = 1
                else:
                    row = 2

                if game in [1, 5, 9]:
                    col = 0
                elif game in [2, 6, 10]:
                    col = 1
                elif game in [3, 7, 11]:
                    col = 2
                else:
                    col = 3

                # Draw the snake vision
                if self.render_vision:
                    updated_vision = [tuple(map(
                        sum, zip(snake.direction, snake.vision[x])))
                        for x in range(len(snake.vision))]
                    for cell in updated_vision:
                        self.render_cell(PURPLE, cell, row, col)

                # Draw the food
                self.render_cell(RED, snake.food, row, col)

                # Draw the snake
                for coord in snake.body:
                    self.render_cell(GREEN, coord, row, col)

                # Draw the head of the snake
                self.render_cell(DARK_GREEN, snake.body[0], row, col)

                # Draw the scoreboard background
                pygame.draw.rect(self.screen, GREY,
                                [0 + col * SCREEN_WIDTH,
                                ((MARGIN + CELL) * HEIGHT + MARGIN) +
                                row * SCREEN_HEIGHT,
                                ((MARGIN + CELL) * WIDTH + MARGIN),
                                SCORE_BOARD
                                ])

                # Store text for scores
                current_score = self.font.render(
                    f"Score: {snake.score}", True, BLACK)
                if snake.score < self.high_score:
                    high_score = self.font.render(
                        f"High Score: {self.high_score}", True, BLACK)
                else:
                    high_score = self.font.render(
                        f"High Score: {snake.score}", True, BLACK)

                # Draw Scores
                self.screen.blit(current_score, (5 + col * SCREEN_WIDTH,
                                                (MARGIN + CELL) * HEIGHT + MARGIN + 5 + row * SCREEN_HEIGHT))
                self.screen.blit(high_score, ((((MARGIN + CELL) * WIDTH +
                                                MARGIN) // 2) + col * SCREEN_WIDTH, (MARGIN + CELL) *
                                            HEIGHT + MARGIN + 5 + row * SCREEN_HEIGHT))

        # Display the screen
        pygame.display.flip()

    def render_cell(self, color, coord, row, col):
        """Render a single cell of the game board."""
        pygame.draw.rect(self.screen, color,
                         [(((MARGIN + CELL) * coord[0] + MARGIN)) + col * SCREEN_WIDTH,
                             ((MARGIN + CELL) *
                              coord[1] + MARGIN) + row * SCREEN_HEIGHT,
                             CELL,
                             CELL
                          ])

    def on_cleanup(self):
        """Exit the game."""
        # Update the high score if necessary
        for snake in self.den:
            if snake.score > self.high_score:
                with open("neat_high_score.txt", 'w') as file:
                    file.write(f"{snake.score}")
        # Exit pygame without errors
        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def on_execute(self):
        """Start the game loop."""

        while self.running:
            self.frame += 1
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            if not self.running:
                break
            self.on_render()
        self.on_cleanup()

    def get_high_score(self):
        high_score_file = "neat_high_score.txt"
        with open(high_score_file, 'r') as file:
            high_score = int(file.readline())

        return high_score


def eval_genomes(genomes, config):
    return Training_app(genomes, config, frame_rate=10).on_execute()


def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(eval_genomes, 300)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)
