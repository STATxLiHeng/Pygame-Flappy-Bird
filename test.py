import pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                print("Left!")
            elif event.key == pygame.K_RIGHT:
                print("Right!")
            elif event.key == pygame.K_SPACE:
                print("Space!")
    pygame.display.update()
