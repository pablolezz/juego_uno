from MODEL import Player
from MODEL import Game
from MODEL import Hand
from MODEL import Deck
from MODEL import Card
from VIEW import Button
import random


import pygame
import os
import sys
from VIEW import Text

main_dir = os.path.split(os.path.abspath(__file__))[0]
class Game_controller:

    def __init__(self, main_surface):
        self.player_name = ""
        self.model = Game(Player(self.player_name), Player())
        self.view = Game_view(main_surface)
        self.game_state = 1
        self.names = [self.player_name, "AI"]

    def event_poll(self):
        event = pygame.event.poll()

        if event.type == pygame.KEYDOWN and self.game_state == 1:
            self.game_state += 1
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    def start_loop(self):
        self.view.start_view()
       # self.view.update()

    def game_loop(self):
        self.view.game_view()


    def update(self):
        while True:

            self.event_poll()

            print(self.game_state)

            if self.game_state == 1:
                self.start_loop()

            if self.game_state == 2:
                self.game_loop()

            if self.game_state == 3:
                break

            self.view.update()

class Game_view:
# BOTNES,TEXTOS,FUNETES, SPRITES, EL BACKGROUND, TAMAÑO, SURFACE "FUNCIONES DE UPADATE DEL RENDERER",
    def __init__(self, main_surface):
        self.all_buttons = []
        self.main_surface = main_surface
        self.surface_color = (19, 136, 8)
        self.play_area = (320, 264)
        self.colors = ([234, 26, 39], [248, 224, 0], [0, 164, 78], [2, 149, 216], [255, 165, 0],[0, 0, 0])
                         # Rojo, amarillo, verde, azul, naranja, negro

       # self.color_in_play = self.card_in_play.suits[self.color]
    def start_view(self):
        self.main_surface.fill(self.surface_color)
        self.font = pygame.font.SysFont("Fixedsys Excelsior", 32)
        logo = pygame.image.load(os.path.join(main_dir, 'UNO', "UNO_logo_small.png"))
        h = logo.get_height()
        w = logo.get_width()
        welcome = Text(345, 580, "Pulsa cualquier tecla para continuar")
        surface_sizex = 1280  # Ancho del tablero, en píxeles
        surface_sizey = 640  # Alto del tablero, en píxeles
        self.main_surface.blit(logo, (surface_sizex // 2 - w // 2, surface_sizey // 2 - h // 2))
        self.main_surface.blit(welcome.text, welcome.position)

    def game_view(self):
        print()

    def update(self):
        pygame.display.flip()

