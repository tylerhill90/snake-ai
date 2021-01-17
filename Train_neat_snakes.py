#!/usr/bin/env python3

"""A game of classic snake."""

import sys
import os
from random import randint
import neat
import pickle
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
from snakes.Neat_snake import Neat_snake

# Define global constants
CELL = 7
MARGIN = 1
WIDTH = 50
HEIGHT = 35
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
        self.screen = pygame.display.set_mode((
            SCREEN_WIDTH * 4, SCREEN_HEIGHT * 3
        ))

        self.config = config

        self.den = []
        self.nets = []
        self.ge = []

        for _, g in genomes:
            net = neat.nn.feed_forward.FeedForwardNetwork.create(g, config)
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
            if snake.alive:
                head_1 = snake.body[0]

                # Move the snake
                snake.move_snake(self.nets[x])
                snake.update_body()

                head_2 = snake.body[0]

                # Increase fitness if closer to food and decrease otherwise
                if snake.calc_dist(head_1, snake.food) < snake.calc_dist(head_1, snake.food):
                    self.ge[x].fitness += 1
                else:
                    self.ge[x].fitness -= 1.5

                """# Decrease fitness if head is near the edge of board
                if 0 in head_2 or snake.width in head_2 or snake.height in head_2:
                    self.ge[x].fitness -= 1"""

                # Check if snake starves and decrease fitness if so
                if snake.hunger >= len(snake.body) * 75:
                    snake.direction = (0, 0)
                    snake.alive = False
                    self.ge[x].fitness -= 100 / len(snake.body)
                    continue

                # Check lose conditions
                if self.check_lose_conditions(snake):
                    snake.direction = (0, 0)
                    snake.alive = False
                    self.ge[x].fitness -= 100 / len(snake.body)
                    continue

                if snake.check_food_eaten():
                    self.ge[x].fitness += 10
                    snake.hunger = 0

        # Check if all snakes are dead
        dead = sum([1 for snake in self.den if not snake.alive])
        if dead == len(self.den):
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
        genomes_fitnesses = [(x, genome.fitness)
                             for x, genome in enumerate(self.ge)]
        best_fitness = sorted(
            genomes_fitnesses, key=lambda i: i[1], reverse=True)[:1]

        best_snake = best_fitness[0][0]

        # Draw a black background
        self.screen.fill(BLACK)

        count = 1
        for game, snake in enumerate(self.den):
            if game == best_snake:
                row, col = 0, 0
                self.render_game(snake, row, col)
            if count < 12:
                count += 1

                if count < 5:
                    row = 0
                elif 4 < count < 9:
                    row = 1
                else:
                    row = 2

                if count in [1, 5, 9]:
                    col = 0
                elif count in [2, 6, 10]:
                    col = 1
                elif count in [3, 7, 11]:
                    col = 2
                else:
                    col = 3

                self.render_game(snake, row, col)

        # Display the screen
        pygame.display.flip()

    def render_game(self, snake, row, col):
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
                with open("high_scores/high_score_neat_train.txt", 'w') as file:
                    file.write(f"{snake.score}")
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
        high_score_file = "high_scores/high_score_neat_train.txt"
        with open(high_score_file, 'r') as file:
            high_score = int(file.readline())

        return high_score


def save_object(obj, filename):
    with open(filename, 'wb') as output:
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)


def eval_genomes(genomes, config):
    return Training_app(genomes, config).on_execute()


def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)

    p = neat.population.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Reset high score for training
    with open("high_scores/high_score_neat_train.txt", "w") as file:
        file.write("0")

    winner = p.run(eval_genomes, 400)

    save_object(winner, "neat_snake_5.pickle")


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)
