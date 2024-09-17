import random
import sys
import pygame
import pygame.freetype
import math
import time
import pathlib
from grille import Grille
from menu import Menu

pygame.init()
pygame.font.init()
myfont_1 = pygame.font.Font(None, 30)
myfont_2 = pygame.font.Font(None, 40)
myfont_3 = pygame.font.Font(None, 55)
myfont_4 = pygame.font.Font(None, 70)
myfont_5 = pygame.font.Font(None, 100)

width, height = 940, 700 # 700 + 240
screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF)
pygame.display.set_caption("Jeu de la vie")

clock = pygame.time.Clock()

BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
ROUGE = (255, 0, 0)


class Main:
    def __init__(self, n, m, largeur, hauteur, screen):
        self.screen = screen
        self.largeur, self.hauteur = largeur, hauteur

        self.grille = Grille(n, m, self)
        self.menu = Menu(self)

        self.grille_on = True
        self.menu_on = True
        
        self.mode = "stop"  # play ou stop
        
        self.mouse_button_down = False
        self.mouse_button_up = False
        self.fen_to_evts = {self.grille: ["mouse_button_down", "mouse_button_up"],
                     self.menu: ["mouse_button_up"]}

    def gestion_evt(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.mode = "stop" if self.mode == "play" else "play"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_button_down = True
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_button_up = True
                
        for fen in self.fen_to_evts:
            if self.mouse_button_down and "mouse_button_down" in self.fen_to_evts[fen]:
                fen.mouse_button_down = True
            if self.mouse_button_up and "mouse_button_up" in self.fen_to_evts[fen]:
                fen.mouse_button_up = True
                
        self.grille.gestion_evts_from_main()
        if self.mode == "stop":
            self.menu.gestion_evts_from_main()
        
        self.mouse_button_down = False
        self.mouse_button_up = False
        
    def recup_mouse_pos(self):
        x, y = pygame.mouse.get_pos()
        self.grille.mise_a_jour(x, y)
        if self.mode == "stop":     # a enlever si on veut changer els regles en plein milieu d'une partie
            self.menu.mise_a_jour(x, y)
        
    def afficher(self):
        screen.fill(NOIR)
        
        self.grille.afficher()
        self.menu.afficher()


if __name__ == "__main__":
    main = Main(70, 70, width, height, screen)
    while True:
        main.afficher()
        main.gestion_evt()
        main.recup_mouse_pos()
        clock.tick(50)


