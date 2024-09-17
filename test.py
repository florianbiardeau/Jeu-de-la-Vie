import pygame

pygame.init()

surface = pygame.display.set_mode((400, 300))

clique = False

def gestion_evt():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEMOTION:
            print("a")

while True:
    pygame.display.flip()
    gestion_evt()