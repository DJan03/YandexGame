import pygame
from random import choice

WIDTH, HEIGHT = 800, 600

NONE = 0
BLOCK = 1

WORLD_WIDTH = 16
WORLD_HEIGHT = 11

CELL_SIZE = 50

WORLD_RENDER_DELTA_X = 0
WORLD_RENDER_DELTA_Y = 0

DO_TURN = False


class Rendered:
    def render(self, screen):
        pass


class Entity(Rendered):
    def __init__(self, world, cellX, cellY, mobile=True):
        self.cellX = cellX
        self.cellY = cellY

        self.path = []

        self.selectedCellX = -1
        self.selectedCellY = -1

        self.distance = []

        if mobile:
            self.updateDistance(world, [])

        self.health = 100

    def selectCell(self, x, y):
        self.selectedCellX = x
        self.selectedCellY = y

    def unselectCell(self):
        self.path = []
        self.selectedCellX = -1
        self.selectedCellY = -1

    def pathF(self, x, y, length):
        length += 1
        if self.distance[x][y] != -1 and self.distance[x][y] == 0 or self.distance[x][y] > length:
            self.distance[x][y] = length

            for i, j in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
                if 0 <= x + i < WORLD_WIDTH and 0 <= y + j < WORLD_HEIGHT:
                    self.pathF(x + i, y + j, length)

            for i, j, x1, y1, x2, y2 in [(-1, -1, -1, 0, 0, -1), (1, -1, 1, 0, 0, -1), (-1, 1, -1, 0, 0, 1),
                                         (1, 1, 1, 0, 0, 1)]:
                if 0 <= x + i < WORLD_WIDTH and 0 <= y + j < WORLD_HEIGHT:
                    if self.distance[x + x1][y + y1] != -1 and self.distance[x + x2][y + y2] != -1:
                        self.pathF(x + i, y + j, length)

    def updateDistance(self, world, entities):
        y = lambda i, j: (i in [x.cellX for x in entities] and j in [y.cellY for y in entities])
        self.distance = [[0 if ((world.matrix[i][j] == NONE) or y(i, j)) else -1 for j in range(WORLD_HEIGHT)] for i in range(WORLD_WIDTH)]
        self.pathF(self.cellX, self.cellY, 0)

    def generatePath(self):
        if self.distance[self.selectedCellX][self.selectedCellY] not in [0, -1]:
            x, y = self.selectedCellX, self.selectedCellY
            path = [(x, y)]

            while not (x == self.cellX and y == self.cellY):
                length = self.distance[x][y]
                for i, j in [(-1, 0), (0, -1), (0, 1), (1, 0), (1, -1), (1, 1), (-1, -1), (-1, 1)]:
                    if 0 <= x + i < WORLD_WIDTH and 0 <= y + j < WORLD_HEIGHT:
                        if self.distance[x + i][y + j] == length - 1:
                            x += i
                            y += j
                            break
                path.append((x, y))

            path.reverse()
            self.path = [i for i in path]
        else:
            self.path = []

    def move(self, world, entities):
        if len(self.path) > 1:
            if (self.path[1][0] in [i.cellX for i in entities] and self.path[1][1] in [i.cellY for i in entities]):
                return
            self.cellX, self.cellY = self.path[1]
            self.path.pop(0)
            self.updateDistance(world, entities)


class Enemy(Entity):
    def __init__(self, world, cellX, cellY, target, mobile=True):
        super().__init__(world, cellX, cellY, mobile)

        self.selectedCellX = target.cellX
        self.selectedCellY = target.cellY

    def doTurn(self, world, target, entities):
        self.selectedCellX = target.cellX
        self.selectedCellY = target.cellY
        self.generatePath()
        self.move(world, entities)

    def render(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (
            WORLD_RENDER_DELTA_X + self.cellX * CELL_SIZE + 5,
            WORLD_RENDER_DELTA_Y + self.cellY * CELL_SIZE + 5,
            CELL_SIZE - 10, CELL_SIZE - 10
        ))


class Player(Entity):
    def __init__(self, world, cellX, cellY):
        super().__init__(world, cellX, cellY, True)

    def onControl(self, event, world, entities):
        if event.type == pygame.MOUSEMOTION:
            x, y = event.pos
            x1, y1 = world.pointToCell(x, y)

            if x1 == -1 and y1 == -1:
                self.unselectCell()
            else:
                self.selectCell(x1, y1)
                self.generatePath()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                global DO_TURN
                DO_TURN = True
                self.move(world, entities)

    def render(self, screen):
        pygame.draw.rect(screen, (0, 0, 255), (
            WORLD_RENDER_DELTA_X + self.cellX * CELL_SIZE + 5,
            WORLD_RENDER_DELTA_Y + self.cellY * CELL_SIZE + 5,
            CELL_SIZE - 10, CELL_SIZE - 10
        ))

        if self.selectedCellX != -1 and self.selectedCellY != -1:
            s = pygame.Surface((CELL_SIZE, CELL_SIZE))
            s.set_alpha(125)
            s.fill((0, 255, 0))
            screen.blit(s, (WORLD_RENDER_DELTA_X + self.selectedCellX * CELL_SIZE,
                            WORLD_RENDER_DELTA_Y + self.selectedCellY * CELL_SIZE))

        if len(self.path) > 1:
            points = [(x * CELL_SIZE + WORLD_RENDER_DELTA_X + CELL_SIZE // 2,
                       y * CELL_SIZE + WORLD_RENDER_DELTA_Y + CELL_SIZE // 2)
                      for x, y in self.path]
            pygame.draw.lines(screen, "white", False, points, CELL_SIZE // 5)


class World(Rendered):
    def __init__(self):
        self.matrix = [[choice([NONE, NONE, NONE, NONE, BLOCK]) for _ in range(WORLD_HEIGHT)] for _ in
                       range(WORLD_WIDTH)]

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


def renderObjects(screen, objects):
    for obj in objects:
        obj.render(screen)


def main():
    global DO_TURN

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    world = World()
    player = Player(world, 5, 5)
    enemies = [Enemy(world, 8, i, player) for i in [4, 6]]

    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            player.onControl(event, world, enemies)

        if DO_TURN:
            DO_TURN = False
            for i in range(len(enemies)):
                enemies[i].doTurn(world, player, enemies[:i] + enemies[i + 1:] + [player])

        screen.fill("black")

        renderObjects(screen, [world, player] + enemies)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
