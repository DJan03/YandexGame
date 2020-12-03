import pygame
from random import choice

WIDTH, HEIGHT = 800, 600

NONE = 0
BLOCK = 1

class World:
    def __init__(self):
        self.matrixWidth = 10
        self.matrixHeight = 10

        self.matrix = [[choice([NONE, NONE, NONE, NONE, BLOCK]) for _ in range(self.matrixHeight)] for _ in range(self.matrixWidth)]
        self.cellSize = 50

        self.renderDeltaX = 150
        self.renderDeltaY = 50

        self.selectedCellX = -1
        self.selectedCellY = -1

        self.playerCellX = 5
        self.playerCellY = 5
        self.matrix[self.playerCellX][self.playerCellY] = NONE

        self.path = []

    def pointToCell(self, x, y):
        newX, newY = (x - self.renderDeltaX) // self.cellSize, (y - self.renderDeltaY) // self.cellSize
        if 0 <= newX < self.matrixWidth and 0 <= newY < self.matrixHeight:
            return newX, newY
        else:
            return -1, -1

    def selectCell(self, x, y):
        self.selectedCellX = x
        self.selectedCellY = y

    def unselectCell(self):
        self.path = []
        self.selectedCellX = -1
        self.selectedCellY = -1

    def pathF(self, x, y, length):
        length += 1
        if self.cells[x][y] != -1 and self.cells[x][y] == 0 or self.cells[x][y] > length:
            self.cells[x][y] = length

            for i, j in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
                if 0 <= x + i < self.matrixWidth and 0 <= y + j < self.matrixHeight:
                    self.pathF(x + i, y + j, length)

            for i, j, x1, y1, x2, y2 in [(-1, -1, -1, 0, 0, -1), (1, -1, 1, 0, 0, -1), (-1, 1, -1, 0, 0, 1), (1, 1, 1, 0, 0, 1)]:
                if 0 <= x + i < self.matrixWidth and 0 <= y + j < self.matrixHeight:
                    if self.cells[x + x1][y + y1] != -1 and self.cells[x + x2][y + y2] != -1:
                        self.pathF(x + i, y + j, length)

    def generatePath(self):
        self.cells = [[0 if self.matrix[i][j] == NONE else -1 for j in range(self.matrixHeight)] for i in range(self.matrixWidth)]

        if self.cells[self.selectedCellX][self.selectedCellY] == 0:
            self.pathF(self.playerCellX, self.playerCellY, 0)

            if self.cells[self.selectedCellX][self.selectedCellY] != 0:
                x, y = self.selectedCellX, self.selectedCellY
                path = [(x, y)]

                while not(x == self.playerCellX and y == self.playerCellY):
                    length = self.cells[x][y]
                    for i, j in [(-1, 0), (0, -1), (0, 1), (1, 0), (1, -1), (1, 1), (-1, -1), (-1, 1)]:
                        if 0 <= x + i < self.matrixWidth and 0 <= y + j < self.matrixHeight:
                            if self.cells[x + i][y + j] == length - 1:
                                x += i
                                y += j
                                break
                    path.append((x, y))

                path.reverse()
                self.path = [i for i in path]
            else:
                self.path = []
        else:
            self.path = []

    def render(self, screen):
        for i in range(self.matrixWidth):
            for j in range(self.matrixHeight):
                color = (0, 0, 0)

                if self.matrix[i][j] == NONE:
                    color = (200, 200, 200)
                elif self.matrix[i][j] == BLOCK:
                    color = (125, 125, 125)

                if self.selectedCellX == i and self.selectedCellY == j:
                    color = (0, 255, 0)
                elif self.playerCellX == i and self.playerCellY == j:
                    color = (0, 0, 255)

                pygame.draw.rect(screen, color, (
                    self.renderDeltaX + i * self.cellSize,
                    self.renderDeltaY + j * self.cellSize,
                    self.cellSize,
                    self.cellSize
                ))
        if len(self.path) > 1:
            points = [(x * self.cellSize + self.renderDeltaX + self.cellSize // 2,
                       y * self.cellSize + self.renderDeltaY + self.cellSize // 2)
                      for x, y in self.path]
            pygame.draw.lines(screen, "white", False, points, self.cellSize // 5)

    def movePlayer(self):
        if len(self.path) > 1:
            self.playerCellX, self.playerCellY = self.path[1]
            self.path.pop(0)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    world = World()

    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                x1, y1 = world.pointToCell(x, y)

                if x1 == -1 and y1 == -1:
                    world.unselectCell()
                else:
                    world.selectCell(x1, y1)
                    world.generatePath()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    world.movePlayer()


        screen.fill("black")

        world.render(screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()