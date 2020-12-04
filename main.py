import pygame
from random import choice

WIDTH, HEIGHT = 800, 600

NONE = 0
BLOCK = 1

WORLD_WIDTH = 10
WORLD_HEIGHT = 10

WORLD_RENDER_DELTA_X = 150
WORLD_RENDER_DELTA_Y = 50

CELL_SIZE = 50

class Player:
    def __init__(self):
        self.cellX = 5
        self.cellY = 5

        self.path = []

        self.selectedCellX = -1
        self.selectedCellY = -1

        self.cells = []

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
                if 0 <= x + i < WORLD_WIDTH and 0 <= y + j < WORLD_HEIGHT:
                    self.pathF(x + i, y + j, length)

            for i, j, x1, y1, x2, y2 in [(-1, -1, -1, 0, 0, -1), (1, -1, 1, 0, 0, -1), (-1, 1, -1, 0, 0, 1), (1, 1, 1, 0, 0, 1)]:
                if 0 <= x + i < WORLD_WIDTH and 0 <= y + j < WORLD_HEIGHT:
                    if self.cells[x + x1][y + y1] != -1 and self.cells[x + x2][y + y2] != -1:
                        self.pathF(x + i, y + j, length)

    def generatePath(self, world):
        self.cells = [[0 if world.matrix[i][j] == NONE else -1 for j in range(WORLD_HEIGHT)] for i in range(WORLD_WIDTH)]

        if self.cells[self.selectedCellX][self.selectedCellY] == 0:
            self.pathF(self.cellX, self.cellY, 0)

            if self.cells[self.selectedCellX][self.selectedCellY] != 0:
                x, y = self.selectedCellX, self.selectedCellY
                path = [(x, y)]

                while not(x == self.cellX and y == self.cellY):
                    length = self.cells[x][y]
                    for i, j in [(-1, 0), (0, -1), (0, 1), (1, 0), (1, -1), (1, 1), (-1, -1), (-1, 1)]:
                        if 0 <= x + i < WORLD_WIDTH and 0 <= y + j < WORLD_HEIGHT:
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

    def move(self):
        if len(self.path) > 1:
            self.cellX, self.cellY = self.path[1]
            self.path.pop(0)

    def render(self, screen):
        pygame.draw.rect(screen, (0, 0, 255), (
            WORLD_RENDER_DELTA_X + self.cellX * CELL_SIZE + 5,
            WORLD_RENDER_DELTA_Y + self.cellY * CELL_SIZE + 5,
            CELL_SIZE - 10, CELL_SIZE - 10
        ))

        if self.selectedCellX != -1 and self.selectedCellY != -1:
            pygame.draw.rect(screen, (0, 255, 0), (
                WORLD_RENDER_DELTA_X + self.selectedCellX * CELL_SIZE,
                WORLD_RENDER_DELTA_Y + self.selectedCellY * CELL_SIZE,
                CELL_SIZE, CELL_SIZE
            ), 10)

        if len(self.path) > 1:
            points = [(x * CELL_SIZE + WORLD_RENDER_DELTA_X + CELL_SIZE // 2,
                       y * CELL_SIZE + WORLD_RENDER_DELTA_Y + CELL_SIZE // 2)
                      for x, y in self.path]
            pygame.draw.lines(screen, "white", False, points, CELL_SIZE // 5)

class World:
    def __init__(self):
        self.matrix = [[choice([NONE, NONE, NONE, NONE, BLOCK]) for _ in range(WORLD_HEIGHT)] for _ in range(WORLD_WIDTH)]

        self.selectedCellX = -1
        self.selectedCellY = -1

        self.cellX = 5
        self.cellY = 5
        self.matrix[self.cellX][self.cellY] = NONE

        self.path = []

    def pointToCell(self, x, y):
        newX, newY = (x - WORLD_RENDER_DELTA_X) // CELL_SIZE, (y - WORLD_RENDER_DELTA_Y) // CELL_SIZE
        if 0 <= newX < WORLD_WIDTH and 0 <= newY < WORLD_HEIGHT:
            return newX, newY
        else:
            return -1, -1

    def render(self, screen):
        for i in range(WORLD_WIDTH):
            for j in range(WORLD_HEIGHT):
                color = (0, 0, 0)

                if self.matrix[i][j] == NONE:
                    color = (200, 200, 200)
                elif self.matrix[i][j] == BLOCK:
                    color = (125, 125, 125)
                
                pygame.draw.rect(screen, color, (
                    WORLD_RENDER_DELTA_X + i * CELL_SIZE,
                    WORLD_RENDER_DELTA_Y + j * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE
                ))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    world = World()
    player = Player()

    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                x1, y1 = world.pointToCell(x, y)

                if x1 == -1 and y1 == -1:
                    player.unselectCell()
                else:
                    player.selectCell(x1, y1)
                    player.generatePath(world)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    player.move()


        screen.fill("black")

        world.render(screen)
        player.render(screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()