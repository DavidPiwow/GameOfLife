import random
import pygame
import sys

black = (0,0,0)
white = (255,255,255)
idle = (36, 60, 115)
screenSize = 600
amount = 20
margin = 0.5
rectSize = 20

colors = [(255,0,0),(0,255,0),(0,0,255)]

offset = (screenSize - (rectSize * amount)) // 2

neighborPos = [(-1,-1),(0,-1),(1,-1),
               (-1,0),        (1,0),
               (-1,1),(0, 1),(1, 1)]

class Grid:
    def __init__(self):
        self.size = amount
        self.grid = [[Cell(self,x,y) for x in range(self.size)] for y in range(self.size)]

        for i in range(0, 60):
            curCell = self.getRandomCell()
            while curCell.alive:
                curCell = self.getRandomCell()
            curCell.alive = True

    def display(self):
        for line in self.grid:
            for square in line:
                print(square.val,end="")
            print()

    def getRandomCell(self):
        x = random.randrange(0, self.size-1)
        y = random.randrange(0, self.size-1)

        return self.grid[x][y]
        
    def isAlive(self, x, y):
        if (self.grid[y][x].alive == True):
            return True
        return False

class Cell:
    def __init__(self, grid, x, y, alive=False):
        self.val = 0
        self.x = x
        self.time = 0
        self.grid = grid
        self.alive = alive
        self.y = y
        self.neighbors = 0
        self.surface = pygame.Surface((rectSize-margin, rectSize-margin))
        self.surface.fill(white)
        self.rect = self.surface.get_rect(center=(rectSize/2,rectSize/2))
        self.rect.midbottom  = (offset + x * rectSize, offset + y * rectSize)
    
    def update(self):
        self.val = self.findNeighbors()
       # self.surface.fill(white)
        cVal = self.time % 255 + 50
        if cVal > 255: 
            cVal = 255
        self.surface.fill((cVal, cVal, cVal))
        if self.alive:
            if self.val < 2 or self.val > 3:
                self.alive = False
        else:
            if self.val == 3:
                self.alive = True
        
        if not self.alive:
           # self.surface.fill(idle)
            self.time = 0
            self.val = "-"
        else:
            self.time += 10

    def findNeighbors(self):
        newCount = 0
        for (j,k) in neighborPos:
            xPos = self.x + j
            yPos = self.y + k
            if xPos <= self.grid.size - 1 and yPos <= self.grid.size - 1 and xPos >= 0 and yPos >= 0: 
                if self.grid.isAlive(xPos, yPos) == True:
                    newCount += 1
        self.neighbors = newCount
        return self.neighbors


def __main__():
    pygame.init()
    screen = pygame.display.set_mode((screenSize, screenSize))
    board = Grid()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        screen.fill((0,0,0))
        
        for row in board.grid:
                for cell in row:
                    cell.update()
                    if cell.alive:
                        screen.blit(cell.surface, cell.rect)

        pygame.time.delay(100)
        pygame.display.flip()
        board.display()
            
__main__()