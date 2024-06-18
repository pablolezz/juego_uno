import pygame
import random
import os
import sys

# Definición de variables globales
main_dir = os.path.split(os.path.abspath(__file__))[0]
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Clase para representar los botones del juego
class Button:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = (self.x, self.y, self.w, self.h)
        self.color = []
        self.text = []

    def contains_point(self, point):
        (my_x, my_y) = self.x, self.y
        my_width = self.w
        my_height = self.h
        (x, y) = point
        return my_x <= x < my_x + my_width and my_y <= y < my_y + my_height

# Clase para representar el texto en el juego
class Text:
    def __init__(self, x, y, text):
        self.font = pygame.font.SysFont("Fixedsys Excelsior", 48)
        self.x = x
        self.y = y
        self.position = (self.x, self.y)
        self.text = self.font.render(text, True, (255, 255, 255))

# Clase principal para el juego UNO
class UNOGame:
    def __init__(self):
        self.all_buttons = []
        self.main_surface = pygame.display.set_mode((1280, 640))  # Creación de la ventana del juego
        self.surface_color = (19, 136, 8)  # Color de fondo
        pygame.display.set_caption('UNO')  # Título de la ventana

    def start_UNO(self):
        # Código para la pantalla de inicio
        pygame.init()
        self.main_surface.fill(self.surface_color)
        pygame.display.flip()

    def play_UNO(self):
        running = True
        while running:
            # Lógica del juego
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Actualizar la pantalla
            pygame.display.flip()

def main():
    game = UNOGame()
    game.start_UNO()
    game.play_UNO()

if __name__ == '__main__':
    main()