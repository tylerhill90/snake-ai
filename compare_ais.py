#!/usr/bin/env python3

from App import App
from Simple_ai_snake import Simple_ai_snake
from A_star_snake import A_star_snake

import csv
import matplotlib.pyplot as plt


WIDTH = 50
HEIGHT = 35


def make_plot(name, trials, scores):
    plt.hist(scores, bins='auto')
    plt.title(f"{name} AI Scores in {trials} games")
    plt.xlabel('Score')
    plt.ylabel('Frequency')
    plt.show()
    return


def main():
    trials = 30

    a_star_scores = []
    for x in range(trials):
        print(f"Simple Game: {x + 1}")
        game = App(A_star_snake(WIDTH, HEIGHT), frame_rate=0)
        game.on_execute()
        a_star_scores.append(game.score)
        print(f"SCORE: {game.score}")

    with open("a_star_scores.csv", "w") as f_a:
        write = csv.writer(f_a)
        write.writerow(a_star_scores)

    make_plot("Simple", trials, simple_scores)
    make_plot("A*", trials, a_star_scores)


if __name__ == "__main__":
    main()
