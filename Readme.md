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

* Basic code run with a default game input and default algorithm of BFS.
```
python3 Assignment1.py
```

* To get basic documentation of the program.
```
python3 Assignment1.py -h
```

* To run the code for a specifit input file.
```
python3 Assignment1.py -f file_name.txt
``

* To select a specific algorithm.
```
python3 Assignment1.py -a algorithm_name
```

* To select a specific heuristic. (Available only for A* and Gredy Best First)
```
python3 Assignment1.py -a astar -t heuristic_type
```

* To show the stack trace/To see how the computer plays the game
```
python3 Assignment1.py -s
```

Basic documentation of the game - 
```
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