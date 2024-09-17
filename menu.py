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

BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
ROUGE = (255, 0, 0)
GRIS = (96, 96, 96)


class Menu:
    def __init__(self, parent):
        self.parent = parent
        self.background = GRIS

        self.voisin_survivre = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        self.voisin_naitre = [0, 1, 2, 3, 4, 5, 6, 7, 8]

        self.text1, self.text2, self.nombres1, self.boutons1, self.nombres2, self.boutons2, self.text_gen = self.generer_all()

        self.mouse_button_up = False
        self.clique = True

    def gestion_evts_from_main(self):
        if self.mouse_button_up:
            self.clique = True
            self.mouse_button_up = False

    def mise_a_jour(self, x, y):
        if self.clique:
            for bouton in self.boutons1:
                if bouton.clique_on(x, y):
                    nom = bouton.nom
                    if bouton.cliquer:
                        self.parent.grille.pr_vivre.add(nom)
                    else:
                        self.parent.grille.pr_vivre.discard(nom)
            for bouton in self.boutons2:
                if bouton.clique_on(x, y):
                    nom = bouton.nom
                    if bouton.cliquer:
                        self.parent.grille.pr_rester.add(nom)
                    else:
                        self.parent.grille.pr_rester.discard(nom)
            self.clique = False

    def generer_all(self):
        text1 = None    # labels
        text2 = None    # labels
        text_gen = None # labels
        nombres1 = []   # labels
        boutons1 = []   # checkbutton
        nombres2 = []   # labels
        boutons2 = []   # checkbutton

        dist_haut = 20
        text1 = myfont_1.render("Voisin pour vivre :", True, BLANC) # dist_haut
        dist_gauche = self.parent.largeur - 210
        for nb in self.voisin_survivre:
            nombres1.append(myfont_1.render(f"{nb}", True, BLANC))           # dist_haut + 30
            bouton = CheckButton(self, nb, dist_gauche, dist_haut+50)
            boutons1.append(bouton)     # dist_haut + 50
            if nb == 3:
                bouton.cliquer = True
            dist_gauche += 20

        dist_haut = 140
        text2 = myfont_1.render("Voisin pour rester :", True, BLANC)  # dist_haut
        dist_gauche = self.parent.largeur - 210
        for nb in self.voisin_naitre:
            nombres2.append(myfont_1.render(f"{nb}", True, BLANC))          # dist_haut + 30
            bouton = CheckButton(self, nb, dist_gauche, dist_haut + 50)
            boutons2.append(bouton)  # dist_haut + 50
            if nb == 2:
                bouton.cliquer = True
            dist_gauche += 20

        text_gen = myfont_1.render(f"Génertion n°: {str(self.parent.grille.gen)}", True, BLANC) # dist_haut
        
        return text1, text2, nombres1, boutons1, nombres2, boutons2, text_gen

    def afficher(self):
        rect = pygame.Surface((240, 330))  # the size of your rect
        rect.set_alpha(128)  # alpha level
        rect.fill((255, 255, 255))  # this fills the entire surface
        self.parent.screen.blit(rect, (self.parent.largeur - 240, 0))

        dist_haut = 20
        self.parent.screen.blit(self.text1, (self.parent.largeur - 225, dist_haut))
        dist_gauche = self.parent.largeur - 210
        for i in range(len(self.nombres1)):
            self.parent.screen.blit(self.nombres1[i], (dist_gauche, dist_haut + 30))
            self.boutons1[i].affichage()
            dist_gauche += 20


        dist_haut = 140
        self.parent.screen.blit(self.text2, (self.parent.largeur - 225, dist_haut))
        dist_gauche = self.parent.largeur - 210
        for i in range(len(self.nombres2)):
            self.parent.screen.blit(self.nombres2[i], (dist_gauche, dist_haut + 30))
            self.boutons2[i].affichage()
            dist_gauche += 20
            
        self.text_gen = myfont_1.render(f"Génertion n°: {str(self.parent.grille.gen)}", True, BLANC)
        self.parent.screen.blit(self.text_gen, (self.parent.largeur - 225, 240))
        pygame.display.flip()

class CheckButton:
    def __init__(self, parent, nom, x, y):
        self.parent = parent
        self.nom = nom
        self.x, self.y = x, y
        self.largeur, self.hauteur =20, 20
        self.couleur = BLANC
        self.rect = pygame.Rect((x, y), (20, 20))
        self.focus_in = False
        self.cliquer = False

    def _focus_in(self, x, y):
        if self.rect.collidepoint(x, y):
            self.focus_in = True
            return True
        self.focus_in = False
        return False

    def clique_on(self, x, y):
        """Méthode appelée que si un clique a été détecté sur la page courante"""
        if self._focus_in(x, y):
            self.focus_in = False
            self.cliquer = not self.cliquer
            return True

    def affichage(self):
        if self.cliquer:
            pygame.draw.line(self.parent.parent.screen, self.couleur, (self.x, self.y),
                             (self.x + self.largeur, self.y + self.hauteur), 1)
            pygame.draw.line(self.parent.parent.screen, self.couleur, (self.x + self.largeur, self.y),
                             (self.x, self.y + self.hauteur), 1)
        pygame.draw.rect(self.parent.parent.screen, self.couleur, self.rect, 1)
