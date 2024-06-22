from MODEL import Player
from MODEL import Game
from MODEL import Hand
from MODEL import Deck
from MODEL import Card
from VIEW import Button
import random
from Views.initialView import Initial_view
from Views.loginView import Login_view


import pygame
import os
import sys
from VIEW import Text

main_dir = os.path.split(os.path.abspath(__file__))[0]
class Game_controller:

    def __init__(self, main_surface):
        self.player_name = ""
        self.model = Game(Player(self.player_name), Player())
        print(main_surface)
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

    def initialView(self):
        self.view.start_view()
       # self.view.update()

    def loginView(self):
        self.view = Login_view(pygame.display.set_mode((1280, 640)))
        self.view.start_view()

        while self.game_state == 2:
            player_name = self.view.game_view()
            if player_name:
                self.player_name = player_name
                print(self.player_name)
                """ self.model.players[0].name = self.player_name -> SI QUEREMOS QUE PUEDAN JUGAR MÁS DE 1 JUGADOR"""
                self.game_state += 1  # Avanza a la fase 3 al guardar el nombre
                break

    def gameView(self):
        self.view = Initial_view(pygame.display.set_mode((1280, 640)))
        self.view.start_view()

    def update(self):
        while True:
            self.event_poll()
            if self.game_state == 1:
                self.initialView()
            if self.game_state == 2:
                self.loginView()
            if self.game_state == 3:
                self.gameView()
            self.view.update()

            self.view.update()