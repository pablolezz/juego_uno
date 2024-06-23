from MODEL import Player
from MODEL import Game
from VIEW import Game_view
import pygame
import os
import sys


main_dir = os.path.split(os.path.abspath(__file__))[0]
class Game_controller:

    def __init__(self, main_surface):
        self.model = Game(Player(""), Player("AI"))
        self.view = Game_view(main_surface)  # Pasar el controlador como argumento a la vista
        self.game_state = 1
        self.game_started = False  # Para controlar si el juego ya ha comenzado

    def _start_update(self):
        if self.view.start_loop():
            self.game_state = 2
    def _login_update(self):
        player_name = self.view.login_loop()
        if player_name != "":
            self.model = Game(Player(player_name), Player("AI"))
            self.game_state = 3

    def _game_init(self):
        self.model.start_game()
        self.view.game_start(self.model)
        self.game_started = True

    def _game_update(self):
        self.view.game_loop(self.model)
        self._game_logic_update()

    def update(self):
        while True:
            match self.game_state:
                case 1:
                    self._start_update()
                case 2:
                    self._login_update()
                case 3:
                    if not self.game_started:
                        self._game_init()
                    else:
                        self._game_update()

            self.view.poll_event_QUIT()

    def _game_logic_update(self):
        print("GAME CONTROLLER UPDATE")
        print(self.model.player_ia)


