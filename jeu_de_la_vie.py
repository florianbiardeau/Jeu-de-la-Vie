import random
import sys
import pygame
import pygame.freetype
import math
import time
import pathlib

pygame.init()
pygame.font.init()
myfont_1 = pygame.font.Font(None, 30)
myfont_2 = pygame.font.Font(None, 40)
myfont_3 = pygame.font.Font(None, 55)
myfont_4 = pygame.font.Font(None, 70)
myfont_5 = pygame.font.Font(None, 100)

width, height = 700, 700
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Jeu de la vie")

clock = pygame.time.Clock()

BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
ROUGE = (255, 0, 0)


class Grille:
    def __init__(self, n, m):
        self.n, self.m = n, m
        self.grille = [[0 for i in range(m)] for i in range(n)]
        self.lc, self.hc = width // m, height // n
        self.clique = False
        self.appui = False
        self.mode = "stop"  # play ou stop

    def gestion_evt(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.clique = True
                self.appui = True
            elif event.type == pygame.MOUSEMOTION and self.appui:
                self.clique = True
            elif event.type == pygame.MOUSEBUTTONUP:
                self.appui = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.mode = "stop" if self.mode == "play" else "play"

    def recup_case(self, x, y):
        return y // self.hc, x // self.lc

    def mise_a_jour(self):
        x, y = pygame.mouse.get_pos()
        if self.clique:
            i, j = self.recup_case(x, y)
            self.grille[i][j] = 1 if self.grille[i][j] == 0 else 0
            self.clique = False
        elif self.mode == "play":
            self.generation()

    def generation(self):
        grille_suiv = [[0 for i in range(self.m)] for i in range(self.n)]
        for i in range(self.n):
            for j in range(self.m):
                nb_v = 0
                for iv in range(-1, 2):  # -1 / 0 / 1
                    for jv in range(-1, 2):
                        if 0 <= i + iv < self.n and 0 <= j + jv < self.m:
                            if self.grille[i + iv][j + jv] == 1 and not (iv == 0 and jv == 0):
                                nb_v += 1
                if nb_v == 3:
                    grille_suiv[i][j] = 1
                elif nb_v == 2:
                    grille_suiv[i][j] = self.grille[i][j]
                else:
                    grille_suiv[i][j] = 0
        self.grille = grille_suiv

    def afficher(self):
        screen.fill(NOIR)
        for i in range(self.n):
            for j in range(self.m):
                if self.grille[i][j] == 1:
                    x, y = j * self.lc, i * self.hc
                    pygame.draw.rect(screen, BLANC, (x + 1, y + 1, self.lc - 2, self.hc - 2), 0)
        pygame.display.flip()


if __name__ == "__main__":
    grille = Grille(70, 70)
    while True:
        grille.afficher()
        grille.gestion_evt()
        grille.mise_a_jour()
        clock.tick(20)