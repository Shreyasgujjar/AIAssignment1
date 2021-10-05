# AI Assignment 1 - Sokoban Player

### Implemented algorithms - 
* Breadth First Search
* Depth First Search
* Greedy Best First Search
* A* Algorithm.

### Implemented Heuristics:
* Manhattan Distance.
* Non Trivial Huristic.

### How to run the program.
Program has been written in pure python.

#### Default game input.
```
OOOOOOOO
O   OR O
O    B O
OB  O  O
OOOOOBSO
    O SO
    OOOO
```

1. Basic code run with a default game input and default algorithm of BFS.
```
python3 Assignment1.py
```

2. To get basic documentation of the program.
```
python3 Assignment.py -h
```

3. To select a specific algorithm.
```
python3 Assignment1.py -a algorithm_name
```

4. To select a specific heuristic. (Available only for A* and Gredy Best First)
```
python3 Assignment.py -a astar -t heuristic_type
```

5. To show the stack trace/To see how the computer plays the game
```
python3 Assignment.py -s
```

Basic documentation of the game - 
```
Assignment 1
-h      help
-a      algorithm
-f      inputfile
-t      huristicType in txt format
-s      Show the stack trace


alorithm options -
1. bfs
2. dfs
3. gbf


heuristicOptions -
1. manhattan
2. nontrivial
```