#!/usr/bin/env python3

from App import App
from Simple_ai_snake import Simple_ai_snake
from A_star_snake import A_star_snake

import csv
import matplotlib.pyplot as plt


WIDTH = 50
HEIGHT = 35


def run_trials(name, snake, trials):
    scores = []
    count = 0
    for x in range(trials):
        count += 1
        print(f"{name} Game: {count}")
        game = App(snake, frame_rate=0)
        game.on_execute()
        scores.append(game.score)

    return scores


def make_plot(name, trials, scores):
    plt.hist(scores, bins='auto')
    plt.title(f"{name} AI Scores in {trials} games")
    plt.xlabel('Score')
    plt.ylabel('Frequency')
    plt.show()
    return


def main():
    trials = 30

    simple_scores = run_trials(
        "Simple", Simple_ai_snake(WIDTH, HEIGHT), trials)
    with open("simple_scores.csv", "w") as f_a:
        write = csv.writer(f_a)
        write.writerow(simple_scores)

    a_star_scores = run_trials(
        "A*", A_star_snake(WIDTH, HEIGHT), trials)
    with open("a_star_scores.csv", "w") as f_a:
        write = csv.writer(f_a)
        write.writerow(a_star_scores)

    make_plot("Simple", trials, simple_scores)
    make_plot("A*", trials, a_star_scores)


if __name__ == "__main__":
    main()
