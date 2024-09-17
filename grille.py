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
    def __init__(self, n, m, parent):
        self.parent  = parent
        self.n, self.m = n, m
        self.grille = [[0 for i in range(m)] for i in range(n)]
        self.lc, self.hc = width // m, height // n
        self.gen = 0
        
        self.mouse_button_down = False
        self.mouse_button_up = False
        self.clique = False
        
        self.pr_vivre = {3}
        self.pr_rester = {2}

    def gestion_evts_from_main(self):
        if self.mouse_button_down:
            self.mouse_button_down = False
            self.clique = True
        elif self.mouse_button_up:
            self.mouse_button_up = False
            self.clique = False

    def recup_case(self, x, y):
        return y // self.hc, x // self.lc

    def mise_a_jour(self, x, y):
        if 0 < x < self.n*self.hc and 0 < y < self.m*self.lc:
            if self.clique:
                i, j = self.recup_case(x, y)
                # voir pr mettre mode appui a 1 ou 0 en fonction de sur quelle case on est qd on clique
                if self.parent.g_or_d == "g":
                    self.grille[i][j] = 1
                elif self.parent.g_or_d == "d":
                    self.grille[i][j] = 0
        if self.parent.mode == "play":
            self.generation()

    def generation(self):
        self.gen += 1
        grille_suiv = [[0 for i in range(self.m)] for i in range(self.n)]
        for i in range(self.n):
            for j in range(self.m):
                nb_v = 0
                for iv in range(-1, 2):  # -1 / 0 / 1
                    for jv in range(-1, 2):
                        if 0 <= i + iv < self.n and 0 <= j + jv < self.m:
                            if self.grille[i + iv][j + jv] == 1 and not (iv == 0 and jv == 0):
                                nb_v += 1
                if nb_v in self.pr_vivre:                 # regle du jeu (mort et naissance)
                    grille_suiv[i][j] = 1
                elif nb_v in self.pr_rester:
                    grille_suiv[i][j] = self.grille[i][j]
                else:
                    grille_suiv[i][j] = 0
        self.grille = grille_suiv

    def afficher(self):
        for i in range(self.n):
            for j in range(self.m):
                if self.grille[i][j] == 1:
                    x, y = j * self.lc, i * self.hc
                    pygame.draw.rect(screen, BLANC, (x + 1, y + 1, self.lc - 2, self.hc - 2), 0)
        pygame.display.flip()


#if __name__ == "__main__":
#    grille = Grille(70, 70)
#    while True:
#        grille.afficher()
#        grille.gestion_evt()
#        grille.mise_a_jour()
#        clock.tick(20)


