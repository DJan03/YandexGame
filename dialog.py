import pygame
from random import choice

WIDTH, HEIGHT = 800, 600

data = [i.split("-") for i in open("dialog.txt", "r", encoding="utf-8").read().split("\n")]

images = {
    "bads_finish":pygame.image.load("bads_finish.png"),
    "bads_o":pygame.image.load("bads_o.png"),
    "bads_hello":pygame.image.load("bads_hello.png")
}

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

nowIndex = 0

buttons = []

def render(screen):
    global buttons
    screen.fill((160, 160, 160))

    if data[nowIndex][3] != "":
        rect = images[data[nowIndex][3]].get_rect()
        rect.center = WIDTH // 2, HEIGHT * 7 // 20
        screen.blit(images[data[nowIndex][3]], rect)

    if len(data[nowIndex]) >= 5:
        buttons = []
        for i, dat in enumerate(data[nowIndex][4:]):
            buttons.append((WIDTH * 3 // 10, HEIGHT * (34 + i * 3) // 40, WIDTH * 2 // 5, HEIGHT // 20))

    pygame.draw.rect(screen, (125, 125, 125), (0, HEIGHT * 2 // 3, WIDTH, HEIGHT // 3))
    pygame.draw.rect(screen, (100, 100, 100), (WIDTH * 2 // 10, HEIGHT * 2 // 3 - HEIGHT // 40, WIDTH * 3 // 5, HEIGHT // 20))

    font = pygame.font.Font(None, 30)

    for i, button in enumerate(buttons):
        pygame.draw.rect(screen, (100, 100, 100), button)
        text = font.render(data[nowIndex][4 + i].split("=")[0], True, (255, 255, 255))
        rect = text.get_rect()
        rect.center = (button[0] + button[2] // 2, button[1] + button[3] // 2)
        screen.blit(text, rect)

    text = font.render(data[nowIndex][1], True, (255, 255, 255))
    rect = text.get_rect()
    rect.center = WIDTH // 2, HEIGHT * 2 // 3
    screen.blit(text, rect)

    font = pygame.font.Font(None, 25)
    text = font.render(data[nowIndex][2], True, (255, 255, 255))
    rect = text.get_rect()
    rect.center = WIDTH // 2, HEIGHT * 15 // 20
    screen.blit(text, rect)


run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                ex, ey = event.pos
                for i, a in enumerate(buttons):
                    x, y, w, h = a
                    if x <= ex <= x + w and y <= ey <= y + h:
                        nowIndex = int(data[nowIndex][4 + i].split("=")[1])
                        break

    screen.fill("black")

    render(screen)

    pygame.display.flip()

pygame.quit()