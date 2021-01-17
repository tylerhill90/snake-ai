# Snake AI
A classic game of snake implemented with OOP. Three AIs have been implemented to play the game as well. They are as follows:

- A simple heuristic approach using euclidean distance to the food
- An A* pathfinding approach combined with the simple heuristic
- A machine learning model approach that uses [NEAT](http://nn.cs.utexas.edu/downloads/papers/stanley.ec02.pdf) via the [neat-python](https://neat-python.readthedocs.io/en/latest/) module

To play or see an AI play run the [App.py](./App.py) script with the following options:

- play
- simple
- a_star
- neat

Example:
```
./App.py neat
```

Below are examples of the A* and NEAT AIs in progress. You can turn on the snake's "vision", the purple lines, by pressing the space bar when App.py is running. The A* snake has purple vision that finds the shortest path to the food while the NEAT snake's vision looks in straight lines around its head.

![Screenshot](static/example.gif)