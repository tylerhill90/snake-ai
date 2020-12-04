#!/usr/bin/env python3

import Simple_ai_snake as simple_ai
import A_star_snake as a_star

import csv
import matplotlib.pyplot as plt


def run_trials(name, trials, ai):
    scores = []
    count = 0
    for x in range(trials):
        count += 1
        print(f"{name} Game: {count}")
        game = ai.App()
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
    trials = 200

    simple_scores = run_trials("Simple", trials, simple_ai)
    with open("simple_scores.csv", "w") as f_simp:
        write = csv.writer(f_simp)
        write.writerow(simple_scores)

    a_star_scores = run_trials("A*", trials, a_star)
    with open("a_star_scores.csv", "w") as f_a:
        write = csv.writer(f_a)
        write.writerow(a_star_scores)

    make_plot("Simple", trials, simple_scores)
    make_plot("A*", trials, a_star_scores)


if __name__ == "__main__":
    main()
