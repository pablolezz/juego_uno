from MODEL import Player
from MODEL import Game
from MODEL import Hand
from MODEL import Deck
from MODEL import Card
from VIEW import Button
import random
from Views.initialView import Initial_view
from Views.gameView import Game_view


import pygame
import os
import sys
from VIEW import Text

main_dir = os.path.split(os.path.abspath(__file__))[0]
class Game_controller:

    def __init__(self, main_surface):
        self.player_name = ""
        self.model = Game(Player(self.player_name), Player())
        self.view = Initial_view(main_surface)
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

    def game_loop(self, main_surface):
        self.view = Game_view(self.main_surface)


    def update(self):
        while True:
            print(self.game_state)
            self.event_poll()
            if self.game_state == 1:
                self.start_loop()
            if self.game_state == 2:
                self.game_loop()
                player_name = self.view.game_view()
                if player_name:
                    self.player_name = player_name
                    self.model.players[0].name = self.player_name
                    self.game_state += 1  # Avanza a la fase 3 al guardar el nombre
            if self.game_state == 3:
                self.uno_loop()
            self.view.update()

            self.view.update()