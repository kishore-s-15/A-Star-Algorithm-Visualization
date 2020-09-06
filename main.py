# A Star Algorithm Visualization implementation in Python

# Importing the required libraries
import pygame
import math
from queue import PriorityQueue

# Importing all the colors from colors module
from colors import *

# Global Variables

# Width of the pygame window
WIDTH = 800

# Setting the Width and Height of the pygame window
WIN = pygame.display.set_mode((WIDTH, WIDTH))

# Setting the title the pygame window
pygame.display.set_caption("A Star Path Finding Algorithm")

# Class Node
class Node:
    def __init__(self, row, col, width, totalRows):
        self.row = row
        self.col = col
        self.width = width
        self.totalRows = totalRows

        self.x = row * width
        self.y = col * width

        self.color = WHITE

        self.neighbors = []

    # Method which return the position of the node within the pygame window
    def getPosition(self):
        return self.row, self.col

    # Method which checks if the node is open
    def isOpen(self):
        return self.color == GREEN

    # Method which checks if the node is closed
    def isClosed(self):
        return self.color == RED

    # Method which checks if the node is a barrier
    def isBarrier(self):
        return self.color == BLACK

    # Method which checks if the node is the starting node
    def isStart(self):
        return self.color == ORANGE

    # Method which checks if the node is the ending node
    def isEnd(self):
        return self.color == TURQUOISE

    # Method which resets the node
    def reset(self):
        self.color = WHITE

    # Method which makes the node open
    def makeOpen(self):
        self.color = GREEN

    # Method which makes the node closed
    def makeClosed(self):
        self.color = RED

    # Method which makes the node a barrier
    def makeBarrier(self):
        self.color = BLACK
    
    # Method which makes the node the starting node
    def makeStart(self):
        self.color = ORANGE

    # Method which makes the node the ending node
    def makeEnd(self):
        self.color = TURQUOISE

    # Method which makes the node a part of the path from source to destination node
    def makePath(self):
        self.color = PURPLE

    # Method which draws the node to the pygame window
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    # Method which updates the neighbors of the node
    def updateNeighbors(self, grid):
        self.neighbors = []
        
        # North Neighbor
        if self.row > 0 and not grid[self.row - 1][self.col].isBarrier():
            self.neighbors.append(grid[self.row - 1][self.col])

        # South Neighbor
        if self.row < self.totalRows - 1 and not grid[self.row + 1][self.col].isBarrier():
            self.neighbors.append(grid[self.row + 1][self.col])

        # East Neighbor
        if self.col < self.totalRows - 1 and not grid[self.row][self.col + 1].isBarrier():
            self.neighbors.append(grid[self.row][self.col + 1])

        # West Neighbor
        if self.col > 0 and not grid[self.row][self.col - 1].isBarrier():
            self.neighbors.append(grid[self.row][self.col - 1])


    def __lt__(self, other):
        return False

# Function which draws the path from the source to the destination node
def drawPath(predecessor, currentNode, draw):
    while currentNode in predecessor:
        currentNode = predecessor[currentNode]
        currentNode.makePath()
        draw()

# A Star Algorithm Function
def AStarAlgorithm(draw, grid, startNode, endNode):
    count = 0

    # OpenSet is a priority queue
    openSet = PriorityQueue()
    openSet.put((0, count, startNode))

    predecessor = {}

    # Global Score (gScore)
    gScore = {node: float("inf") for row in grid for node in row}
    gScore[startNode] = 0

    # Heuristic Score (fScore)
    fScore = {node: float("inf") for row in grid for node in row}
    fScore[startNode] = heuristicFunction(startNode.getPosition(), endNode.getPosition())

    openSetHash = {startNode}

    while not openSet.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = openSet.get()[2]
        openSetHash.remove(current)

        if current == endNode:
            drawPath(predecessor, endNode, draw)
            endNode.makeEnd()
            print(f"The End Node is {temp_gScore} units away from the Source Node")
            return True

        for neighbor in current.neighbors:
            temp_gScore = gScore[current] + 1

            if temp_gScore < gScore[neighbor]:
                predecessor[neighbor] = current
                gScore[neighbor] = temp_gScore
                fScore[neighbor] = temp_gScore + heuristicFunction(neighbor.getPosition(), endNode.getPosition())
                if neighbor not in openSetHash:
                    count += 1
                    openSet.put((fScore[neighbor], count, neighbor))
                    openSetHash.add(neighbor)
                    neighbor.makeOpen()

        draw()

        if current != startNode:
            current.makeClosed()

    return False

# Function for calculating the heuristic value
def heuristicFunction(d1, d2):
    x1, y1 = d1
    x2, y2 = d2

    # Euclidean Distance
    # return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    # Diagonal Distance
    # return max(abs(x1 - x2), abs(y1 - y2))

    # Manhattan Distance
    return abs(x1 - x2) + abs(y1 - y2)

# Function which makes a grid of nodes
def makeGrid(rows, width):
    grid = []
    gap = width // rows

    for i in range(rows):
        grid.append([])

        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)

    return grid

# Function for drawing the border of the nodes in the grid
def drawGrid(win, rows, width):
    gap = width // rows

    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))

        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

# Function which draws the nodes from the grid on the pygame window
def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(win)

    drawGrid(win, rows, width)
    pygame.display.update()

# Function which gets the mouse position within the pygame window
def getMouseClickPosition(position, rows, width):
    gap = width // rows
    y, x = position

    row = y // gap
    col = x // gap

    return row, col

# Main Function
def main(win, width):

    # Number of rows
    ROWS = 50

    grid = makeGrid(ROWS, width)
    
    # Initializing the starting and the ending node
    startNode = None
    endNode = None

    run = True

    while run:

        # Drawing the grid onto the pygame window
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            # Checking for Left Mouse Button click
            if pygame.mouse.get_pressed()[0]:
                position = pygame.mouse.get_pos()
                row, col = getMouseClickPosition(position, ROWS, width)
                node = grid[row][col]

                # If start node has not been set,
                # we set the node which is being clicked as starting node
                if not startNode and node != endNode:
                    startNode = node
                    startNode.makeStart()

                # If end node has not been set,
                # we set the node which is being clicked as ending node
                elif not endNode and node != startNode:
                    endNode = node
                    endNode.makeEnd()

                # If barrier node has not been set,
                # we set the node which is being clicked as barrier node
                elif node != startNode and node != endNode:
                    node.makeBarrier()                
            
            # Checking for Right Mouse Button click
            elif pygame.mouse.get_pressed()[2]:
                position = pygame.mouse.get_pos()
                row, col = getMouseClickPosition(position, ROWS, width)
                node = grid[row][col]
                node.reset()

                if node == startNode:
                    startNode = None
                elif node == endNode:
                    endNode = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and startNode and endNode:
                    for row in grid:
                        for node in row:
                            node.updateNeighbors(grid)

                    AStarAlgorithm(lambda: draw(win, grid, ROWS, width), grid, startNode, endNode)

                if event.key == pygame.K_c:
                    startNode = None
                    endNode = None
                    grid = makeGrid(ROWS, width)

    pygame.quit()

# Main Loop
if __name__ == "__main__":
    main(WIN, WIDTH)