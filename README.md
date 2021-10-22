# Snake AI
A classic game of snake made with [PyGame](https://www.pygame.org/news) and implemented with OOP. Three AIs are available to play the game as well. They are as follows:

- A simple heuristic approach using euclidean distance to the food
- An A* pathfinding approach combined with the simple heuristic
- A machine learning model approach that uses [NEAT](http://nn.cs.utexas.edu/downloads/papers/stanley.ec02.pdf) via the [neat-python](https://neat-python.readthedocs.io/en/latest/) module.

## Quick start

To play or see an AI play clone the repository, install the requirements into a venv, and run the [App.py](./App.py) script with one of the following command line args:

- play
- simple
- a_star
- neat

```console
git clone https://github.com/tylerhill90/snake-ai.git
cd snake-ai
python3 -m venv env
source env/bin/activate
python3 -m pip install -r requirements.txt
./App.py a_star
```

## What does it look like?

Below are examples of the A* and NEAT AIs in progress. You can turn on the snake's "vision", the purple lines, by pressing the space bar when App.py is running. 

The A* snake has purple vision that shows the shortest path to the food while the NEAT snake's vision looks in straight lines around its head.

![Screenshot](static/example.gif)