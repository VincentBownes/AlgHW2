import copy
import sys
import time

def DFSfindOptimal(path):
    n,m,k,floor = readFromInputfile(path)
    printFloor(floor)
    minStepCount = 100000000
    minFound = False
    maxSteps = (n-(k-1)) * (m-(k-1))
    #set of candidates
    #using list G as stack
    startState = floorState(floor, None, 0)
    G = [startState]
    #make sure start state is not a solution
    if solutionChecker(n, m, startState.floor):
        minStepCount = 0
        minFound = True

    while minFound == False:
        #next state generator
        #find the most promising parent and generate children from it
        bestNextParent = None
        mostTiles = 0
        for floor in G:
            x = countTiles(floor.floor)
            if x > mostTiles:
                mostTiles = x
                bestNextParent = floor
                G.remove(floor)
        #printFloor(bestNextParent.floor)
        #print()
        #time.sleep(4)
        for line in range(0,n):
            for col in range(0,m):
                #copy floor of parent
                newFloor = copy.deepcopy(bestNextParent.floor)
                #make sure flipper is not outside the bounds of the floor
                if line + k <= n and col + k <= m:
                    tileFilpper([line,col], newFloor, k)
                    #feasibility check to make sure states are not repeated
                    if checkParentStates(bestNextParent, newFloor, bestNextParent.steps+1) == True:
                        #the third argument "steps" is the objective funciton
                        #representing how many levels down from the root node the child is
                        newCandidate = floorState(newFloor, bestNextParent, bestNextParent.steps+1)
                        #check if new candidate is a solution
                        if solutionChecker(n, m, newCandidate.floor):
                            if newCandidate.steps < minStepCount:
                                minStepCount = newCandidate.steps
                        #push new candidate onto the stack if there is not already a solution higher in the tree
                        elif(newCandidate.steps <= minStepCount and newCandidate.steps <= maxSteps):
                            G.append(newCandidate)
                        
        if not G:
            minFound = True
    if minStepCount == 100000000:
        minStepCount = -1

    return minStepCount

class floorState:
    def __init__(self,floorMatrix, parent, numOfSteps):
        self.floor = floorMatrix
        self.parent = parent
        self.steps = numOfSteps
    visited = False

#tileCoords are [row, column]
def tileFilpper(topLeftCoord, floorMatrix, sizeOfFlipper):
    for line in range(0,sizeOfFlipper):
        for col in range(0,sizeOfFlipper):
            if floorMatrix[topLeftCoord[0] + line][topLeftCoord[1] + col] == 0:
                floorMatrix[topLeftCoord[0] + line][topLeftCoord[1] + col] = 1
            else:
                floorMatrix[topLeftCoord[0] + line][topLeftCoord[1] + col] = 0

def countTiles(floorMatrix):
    count = 0
    for line in floorMatrix:
        for col in line:
            if col == 1:
                count+=1
    return count

#makes printed output visually match the intuitive understanding of floor layout
def printFloor(floorMatrix):
    for line in floorMatrix:
        print(line)

def checkParentStates(parent, newFloor, steps):
    if parent == None or steps > parent.steps + 900:
        return True
    elif parent.floor == newFloor:
        return False
    else: 
        return checkParentStates(parent.parent, newFloor, steps)

def solutionChecker(n, m, floor):
    for line in range(0,n):
        for col in range(0,m):
            if floor[line][col] == 0:
                return False
    return True

def readFromInputfile(path):
    f = open(path, "r")
    n = int(f.read(2))
    m = int(f.read(2))
    k = int(f.read(2))
    floorMatrix = [[0 for x in range(m)] for y in range(n)] 
    for line in range(0,n):
        for col in range(0,m):
            floorMatrix[line][col] = int(f.read(2))
    return n, m, k, floorMatrix

def runTests():
    testNums = [1,2,3,4,6,9,44,46,47]
    f = open("C:\\Users\\user\\Desktop\\alg\\AlgHW2\\truthData.txt", "r")
    truthData = []
    for line in f:
        truthData.append(int(line))
    for x in range(0,len(testNums)):
        path = "C:\\Users\\user\\Desktop\\alg\\AlgHW2\\TestCases\\testInput" + str(testNums[x]) + ".txt"
        start = time.time()
        print(DFSfindOptimal(path))
        end = time.time()
        print(str(end - start) + " seconds")

runTests()