import uuid
import time
from operator import itemgetter
import getopt, sys
import time

# Function to read the inital state of the board from a file
def readBoard(fileName):
    with open(fileName) as f:
        fileData = f.read()
        board_state = fileData.split("\n")
        board_state = list(filter(('').__ne__, board_state))
        print(board_state)
        return board_state

# Display the board state at any point of time
def showGame(data):
  for s in data:
    print(s)

# The program was initially written with a different format which did not work.
# Part of the older program is taken and implemented here.
# To enable the conversions between the previous and the current data type.
# This function has been implemented
# Function which converts to a matrix
def convertToNewFormat(node):
  returnData = []
  for data in node:
    returnData.append([char for char in data])
  return returnData

# The program was initially written with a different format which did not work.
# Part of the older program is taken and implemented here.
# To enable the conversions between the previous and the current data type.
# This function has been implemented
# Function which converts matrix to a simple array
def convertToOldFormat(node):
  returnData = []
  for data in node:
    returnData.append(''.join(data))
  return returnData

# This function check if there is any movement in the box from the previous state.
# This function is used only in the astar algorithm.
def isBoxMoved(node, parentNode):
  currentState = []
  prevState = []
  for data in node:
    if 'R' in data:
      currentState.append(data.replace('R', ' '))
    else:
      currentState.append(data)
  for data in parentNode:
    if 'R' in data:
      prevState.append(data.replace('R', ' '))
    else:
      prevState.append(data);
  return len(set(tuple(currentState)).intersection(set(tuple(prevState))))

# Checked the current possition of the robot and returns the x, y co-ordinates.
def findCurrentRobotPosition(currentPosition):
      for i in range(0, len(currentPosition)):
        if "R" in currentPosition[i]:
            for j in range(0, len(currentPosition[i])):
                if currentPosition[i][j] == "R":
                    return i, j

# checkes the current box position with the given board state.
# Returns the x, y co-ordinates of the boxes.
def findCurrentBoxPosition(currentPosition):
  x_list = []
  y_list = []
  for i in range(0, len(currentPosition)):
    if "B" in currentPosition[i]:
      for j in range(0, len(currentPosition[i])):
        if currentPosition[i][j] == "B":
          x_list.append(i)
          y_list.append(j)
  return x_list, y_list

# checkes the final position(goal state) with the initial board state.
# Returns the x, y co-ordinates of the final state.
def findGoalStateValues(node):
  x_list = []
  y_list = []
  for i in range(0, len(node)):
    if "S" in node[i]:
      for j in range(0, len(node[i])):
        if node[i][j] == "S":
          x_list.append(i)
          y_list.append(j)
  return x_list, y_list

# Calculated the manhattan distance leaving out all the obstacles
# previous distance is the number of moves the box has made in the previous state.
def manhattanDistance(node, prevDistance = 0):
  s_x, s_y = findGoalStateValues(board)
  b_x, b_y = findCurrentBoxPosition(node)
  final_distances = []
  goalStates = [(s_x[i], s_y[i]) for i in range(0, len(s_x))]
  boxPositions = [(b_x[i], b_y[i]) for i in range(0, len(b_x))]
  for positions in boxPositions:
    distances = []
    for states in goalStates:
      distances.append(abs(positions[0] - states[0]) + abs(positions[1] - states[1]))
    final_distances.append(min(distances))
  return sum(final_distances) + prevDistance

# Check if the box is stuck in some corner.
# This method is used only for the implementation of the non trivial heuristic.
def boxPushPossible(node):
  s_x, s_y = findGoalStateValues(board)
  b_x, b_y = findCurrentBoxPosition(node)
  returnList = []
  storagePos = []
  BoxPos = []
  for i in range(0, len(b_x)):
    BoxPos.append((b_x[i], b_y[i]))
  for i in range(0, len(s_x)):
    storagePos.append((s_x[i], s_y[i])) 
  for finalPos in storagePos:
    if finalPos in BoxPos:
      BoxPos.remove(finalPos)
  formatedNode = convertToNewFormat(node)
  for pos in BoxPos:
    count = 0
    if formatedNode[pos[0] - 1][pos[1]] == 'O':
      count = count + 1
    if formatedNode[pos[0] + 1][pos[1]] == 'O':
      count = count + 1
    if formatedNode[pos[0]][pos[1] - 1] == 'O':
      count = count + 1
    if formatedNode[pos[0]][pos[1] + 1] == 'O':
      count = count + 1
    returnList.append(count)
  try:
    return max(returnList) < 2
  except:
    return False
        
# Heuristic which calculates the distance similar to manhattan distance
# But checks if the box is stuck in some unmovable state and returns the distance to be 2500
def nonTrivialHuristicDistance(node, prevDistance = 0):
  s_x, s_y = findGoalStateValues(board)
  b_x, b_y = findCurrentBoxPosition(node)
  if boxPushPossible(node):
    final_distances = []
    goalStates = [(s_x[i], s_y[i]) for i in range(0, len(s_x))]
    boxPositions = [(b_x[i], b_y[i]) for i in range(0, len(b_x))]
    for positions in boxPositions:
      distances = []
      for states in goalStates:
        distances.append(abs(positions[0] - states[0]) + abs(positions[1] - states[1]))
      final_distances.append(min(distances))
    return sum(final_distances) + prevDistance
  else:
    return 2500

# Method to check if the goal state is achieved
def checkSolved(node):
  if node == False:
    return False
  s_x, s_y = findGoalStateValues(board)
  b_x, b_y = findCurrentBoxPosition(node)
  goalStates = [(s_x[i], s_y[i]) for i in range(0, len(s_x))]
  boxPositions = [(b_x[i], b_y[i]) for i in range(0, len(b_x))]
  return len(set(boxPositions)) == len(set(boxPositions).intersection(set(goalStates)))

# Methods implemented to check if the robot can move upwards, downwards and sideways.
def isMoveUpLegal(node):
  x, y = findCurrentRobotPosition(node)
  if x > 0:
    previous_row = x - 1
    if node[previous_row][y] == "B":
      previous_row = previous_row -1
      return node[previous_row][y] != "O" and node[previous_row][y] != "B"
    else:
      return node[previous_row][y] != "O" and node[previous_row][y] != "B"
  else:
    return False

def isMoveDownLegal(currentPosition):
  x, y = findCurrentRobotPosition(currentPosition)
  if x < len(currentPosition):
    next_row = x + 1
    if currentPosition[next_row][y] == "B":
      next_row = next_row + 1
      return currentPosition[next_row][y] != "O" and currentPosition[next_row][y] != "B"
    else:
      return currentPosition[next_row][y] != "O" and currentPosition[next_row][y] != "B"
  else:
    return False

def isMoveLeftLegal(currentPosition):
  x, y = findCurrentRobotPosition(currentPosition)
  if y > 0:
    previous_column = y - 1
    if currentPosition[x][previous_column] == "B":
      previous_column = previous_column -1
      return currentPosition[x][previous_column] != "O" and currentPosition[x][previous_column] != "B"
    else:
      return currentPosition[x][previous_column] != "O" and currentPosition[x][previous_column] != "B"
  else:
    return False

def isMoveRightLegal(currentPosition):
  x, y = findCurrentRobotPosition(currentPosition)
  if y < len(currentPosition[0]):
    next_column = y + 1
    if currentPosition[x][next_column] == "B":
      next_column = next_column + 1
      return currentPosition[x][next_column] != "O" and currentPosition[x][next_column] != "B"
    else:
      return currentPosition[x][next_column] != "O" and currentPosition[x][next_column] != "B"
  else:
    return False

# Make the robot go up and send the state
def moveUp(node):
  x, y = findCurrentRobotPosition(node)
  box_x, box_y = findCurrentBoxPosition(node)
  newData = convertToNewFormat(node)
  if isMoveUpLegal(node):
    if newData[x-1][y] == "B":
      newData[x-2][y] = "B"
    newData[x-1][y] = "R"
    newData[x][y] = " "
    if convertToOldFormat(newData) not in generatedNodes:
      generatedNodes.append(convertToOldFormat(newData))
      # showGame(convertToOldFormat(newData))
      return convertToOldFormat(newData)
    else:
      # print("This state is already explored")
      return False
  else:
    # print("Can't go up")
    return False
# Make the robot go down and send the state
def moveDown(node):
  x, y = findCurrentRobotPosition(node)
  box_x, box_y = findCurrentBoxPosition(node)
  newData = convertToNewFormat(node)
  if isMoveDownLegal(node):
    if newData[x+1][y] == "B":
      newData[x+2][y] = "B"
    newData[x+1][y] = "R"
    newData[x][y] = " "
    if convertToOldFormat(newData) not in generatedNodes:
      generatedNodes.append(convertToOldFormat(newData))
      # showGame(convertToOldFormat(newData))
      return convertToOldFormat(newData)
    else:
      # print("This state is already explored")
      return False
  else:
    # print("Can't go down")
    return False

# Make the robot go right and send the state
def moveRight(node):
  x, y = findCurrentRobotPosition(node)
  newData = convertToNewFormat(node)
  if isMoveRightLegal(node):
    if newData[x][y+1] == "B":
      newData[x][y+2] = "B"
    newData[x][y+1] = "R"
    newData[x][y] = " "
    if convertToOldFormat(newData) not in generatedNodes:
      generatedNodes.append(convertToOldFormat(newData))
      # showGame(convertToOldFormat(newData))
      return convertToOldFormat(newData)
    else:
      # print("This state is already explored")
      return False
  else:
    # print("Can't go right")
    return False

# Make the robot go left and send the state
def moveLeft(node):
  x, y = findCurrentRobotPosition(node)
  newData = convertToNewFormat(node)
  if isMoveLeftLegal(node):
    if newData[x][y-1] == "B":
      newData[x][y-2] = "B"
    newData[x][y-1] = "R"
    newData[x][y] = " "
    if convertToOldFormat(newData) not in generatedNodes:
      generatedNodes.append(convertToOldFormat(newData))
      # showGame(convertToOldFormat(newData))
      return convertToOldFormat(newData)
    else:
      # print("This state is already explored")
      return False
  else:
    # print("Can't go left")
    return False

# Function to generate the nodes
# Generates up, down, right and left movement nodes synchronously
# Adds meta data to the nodes to parse in the end
def generateNodes(node, parentId):
  global nodesToBeExplored
  upId = None
  downId = None
  leftId = None
  rightId = None
  upMove = moveUp(node)
  nodeParents[parentId] = []
  if upMove:
    id = str(uuid.uuid4())
    nodeTree[id] = {
        "id": id,
        "node": upMove,
        "move": "UP",
        "boxMoves": nodeTree[parentId]["boxMoves"] + isBoxMoved(upMove, nodeTree[parentId]["node"]),
        "parentId": parentId,
        "distance": manhattanDistance(upMove, 0 if algorithmUsed == 'gbf' else nodeTree[parentId]["boxMoves"]) if heuristic == 'manhattan' else nonTrivialHuristicDistance(upMove, 0 if algorithmUsed == 'gbf' else nodeTree[parentId]["boxMoves"])
    }
    nodeParents[parentId].append(list(nodeTree.keys())[-1])
    nodesToBeExplored.append(list(nodeTree.keys())[-1])
    upId = list(nodeTree.keys())[-1]
  downMove = moveDown(node)
  if downMove:
    id = str(uuid.uuid4())
    nodeTree[id] = {
        "id": id,
        "node": downMove,
        "move": "DOWN",
        "boxMoves": nodeTree[parentId]["boxMoves"] + isBoxMoved(downMove, nodeTree[parentId]["node"]),
        "parentId": parentId,
        "distance": manhattanDistance(downMove, 0 if algorithmUsed == 'gbf' else nodeTree[parentId]["boxMoves"]) if heuristic == 'manhattan' else nonTrivialHuristicDistance(downMove, 0 if algorithmUsed == 'gbf' else nodeTree[parentId]["boxMoves"])
    }
    nodeParents[parentId].append(list(nodeTree.keys())[-1])
    nodesToBeExplored.append(list(nodeTree.keys())[-1])
    downId = list(nodeTree.keys())[-1]
  rightMove = moveRight(node)
  if rightMove:
    id = str(uuid.uuid4())
    nodeTree[id] = {
        "id": id,
        "node": rightMove,
        "move": "RIGHT",
        "boxMoves": nodeTree[parentId]["boxMoves"] + isBoxMoved(rightMove, nodeTree[parentId]["node"]),
        "parentId": parentId,
        "distance": manhattanDistance(rightMove, 0 if algorithmUsed == 'gbf' else nodeTree[parentId]["boxMoves"]) if heuristic == 'manhattan' else nonTrivialHuristicDistance(rightMove, 0 if algorithmUsed == 'gbf' else nodeTree[parentId]["boxMoves"])
    }
    nodeParents[parentId].append(list(nodeTree.keys())[-1])
    nodesToBeExplored.append(list(nodeTree.keys())[-1])
    rightId = list(nodeTree.keys())[-1]
  leftMove = moveLeft(node)
  if leftMove:
    id = str(uuid.uuid4())
    nodeTree[id] = {
        "id": id,
        "node": leftMove,
        "move": "LEFT",
        "boxMoves": nodeTree[parentId]["boxMoves"] + isBoxMoved(leftMove, nodeTree[parentId]["node"]),
        "parentId": parentId,
        "distance": manhattanDistance(leftMove, 0 if algorithmUsed == 'gbf' else nodeTree[parentId]["boxMoves"]) if heuristic == 'manhattan' else nonTrivialHuristicDistance(leftMove, 0 if algorithmUsed == 'gbf' else nodeTree[parentId]["boxMoves"])
    }
    nodeParents[parentId].append(list(nodeTree.keys())[-1])
    nodesToBeExplored.append(list(nodeTree.keys())[-1])
    leftId = list(nodeTree.keys())[-1]
  if checkSolved(upMove) or checkSolved(downMove) or checkSolved(rightMove) or checkSolved(leftMove):
    return [upId, downId, leftId, rightId]
  else:
    if algorithmUsed.lower() == "gbf" or algorithmUsed.lower() == "astar":
        nodesToBeExplored = sortBasedOnDistance()
    return False

# Method used only for gbf and astar
# Sort the distance based on the non trivial or the manhattan distance
def sortBasedOnDistance():
  emptyList = []
  for ids in nodesToBeExplored:
    emptyList.append(nodeTree[ids])
  emptyList = sorted(emptyList, key=itemgetter('distance'))
  emptyList = [data['id'] for data in emptyList]
  return emptyList

# Check which nodes are to be expanded and expand those nodes
# Calculates the time taken for the complete execution of the program.
def expandNodes():
  global itereations
  startTime = time.time()
  while len(nodesToBeExplored):
    itereations = itereations + 1
    if algorithmUsed == "bfs":
        dataInNode = nodesToBeExplored.pop(0)
    elif algorithmUsed == "dfs":
        dataInNode = nodesToBeExplored.pop()
    else:
        dataInNode = nodesToBeExplored.pop(0)
    completed = generateNodes(nodeTree[dataInNode]["node"], dataInNode)
    if completed:
      checkStackTrace(completed)
      print("It takes - " + str(itereations) + " node searches to get to the answer")
      print("It takes " + str(round(time.time() - startTime, 3)) + " seconds to get to the solution using " + algorithmUsed + " algo")
      print("Number of unexpanded nodes - " + str(len(nodesToBeExplored)))
      print("Total number of board states generated - " + str(len(generatedNodes)))
      break
  if len(nodesToBeExplored) == 0:
    print("Solution could not be found for the given board state")

# Checks from which node the solution state is obtained and sends
# that node to be backtracked
def checkStackTrace(completedIds):
  for data in completedIds:
    if data is not None:
      if checkSolved(nodeTree[data]['node']):
        stackTrace(data, [], [chr])

# Method to print how the computer played the game
# If we want to see it in action use -s while running the program
def stackTrace(nodeId, moves, ids):
  if nodeTree[nodeId]['parentId'] == "firstNode":
    moves.reverse()
    ids.reverse()
    print("Completed in - " + str(len(moves)))
    print(moves)
    if showGamePlay:
        for id in ids:
            if id in nodeTree.keys():
                showGame(nodeTree[id]['node'])
                time.sleep(1)
  else:
    ids.append(nodeId)
    moves.append(nodeTree[nodeId]['move'])
    stackTrace(nodeTree[nodeId]['parentId'], moves, ids)

# Program start
if __name__ == "__main__":
    argumentList = sys.argv[1:]
    sample = []
    nodeTree = {}
    nodeParents = {}
    nodesToBeExplored = []
    prevLen = -1
    itereations = 0
    algorithmUsed = "bfs"
    showGamePlay = False
    heuristic = "manhattan"
    algoOptiions = ['bfs', 'dfs', 'gbf', 'astar']
    heuristicOptions = ['manhattan', 'nontrivial']
    board = ["OOOOOOOO", "O   OR O", "O    B O", "O   O  O", "OOOOOBSO", "    O SO", "    OOOO"]
    if '-h' in argumentList:
          print("Assignment 1\n-h\thelp\n-a\talgorithm\n-f\tinputfile\n-t\thuristicType in txt format\n-s\tShow the stack trace\n\n\nalorithm options -\n1.bfs\n2.dfs\n3.gbf\n\n\nheuristicOptions -\n1.manhattan\n2.nontrivial")
          exit()
    if '-f' in argumentList:
        print("Using file - " + argumentList[argumentList.index('-f') + 1])
        board = readBoard(argumentList[argumentList.index('-f') + 1])
    if '-a' in argumentList:
        algorithmUsed = argumentList[argumentList.index('-a') + 1].lower()
        if algorithmUsed not in algoOptiions:
          print("Please specify a valid algorithm - \n\n\tbfs\n\tdfs\n\tgbf\n\nExiting the program..\n")
          exit()
        print("Using algorithm - " + argumentList[argumentList.index('-a') + 1])
    if '-t' in argumentList:
        heuristic = argumentList[argumentList.index('-t') + 1].lower()
        if heuristic not in heuristicOptions:
          print("Please specify a valid heuristic - \n\n\tmanhattan\n\tontrivial\n\nExiting the program..\n")
          exit()
        print("Using heuristic - " + argumentList[argumentList.index('-t') + 1])
    if '-s' in argumentList:
        print("Show the game moves once the solution is found")
        showGamePlay = True
    run = False
    previouslyVisitedNodes = []
    generatedNodes = [board]

    nodeTree["initNode"] = {
            "node": board,
            "move": "",
            "boxMoves": 0,
            "parentId": "firstNode",
            "distance": 100
        }

    nodesToBeExplored = ["initNode"]
    expandNodes()