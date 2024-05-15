import pygame
import os
from CONTROLLER import Game_controller

main_dir = os.path.split(os.path.abspath(__file__))[0]
class Window_context:

    def __init__(self):
        self.game_controller = Game_controller(pygame.display.set_mode((1280, 640)))
        pygame.display.set_caption('UNO')

    def context_init(self):
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(os.path.join(main_dir, 'UNO', "lobby.mp3"))
        pygame.mixer.music.play(-1)

    def context_execute(self):
        self.game_controller.update()

def main():
    game = Window_context()
    game.context_init()
    game.context_execute()

if __name__ == '__main__':
    main()