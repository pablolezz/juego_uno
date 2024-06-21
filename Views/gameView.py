import pygame
import os
from moviepy.editor import *

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)


class Text:
    def __init__(self, x, y, text_surface):
        self.position = (x, y)
        self.text_surface = text_surface  # El texto ya renderizado en pygame


class Game_view:
    def __init__(self, main_surface):
        self.all_buttons = []
        self.main_surface = main_surface
        self.surface_color = (19, 136, 8)
        self.play_area = (320, 264)
        self.colors = ([234, 26, 39], [248, 224, 0], [0, 164, 78], [2, 149, 216], [255, 165, 0], [0, 0, 0])
        # Rojo, amarillo, verde, azul, naranja, negro

    def start_view(self):
        self.main_surface.fill(self.surface_color)
        self.font = pygame.font.SysFont("Fixedsys Excelsior", 32)

        """ Imagen inicial """
        logo_path = os.path.join(parent_dir, 'UNO', 'gif_uno.gif')
        logo_surface = pygame.image.load(logo_path)
        logo_surface = pygame.transform.scale(logo_surface, (1280, 640))  # Escala la imagen al tamaño de la pantalla
        self.main_surface.blit(logo_surface, (0, 0))

        """GIF
        gif_filepath = os.path.join(parent_dir, 'UNO', 'gif_uno.gif')
        gif_clip = VideoFileClip(gif_filepath).fx(vfx.resize, width = 1280)

        frame_count = int(gif_clip.duration * gif_clip.fps)
        for i in range(frame_count):
            frame = gif_clip.get_frame(i / gif_clip.fps)
            frame_surface = pygame.image.fromstring(frame.tobytes(), gif_clip.size, "RGB")
            self.main_surface.blit(frame_surface, (0, 0))
            self.main_surface.blit(welcome.text_surface, welcome.position)
            pygame.display.flip()
            pygame.time.delay(int(1000 / gif_clip.fps))
        """

        # Renderiza el texto
        welcome_text = self.font.render("HE CAMBIADO", True, (0, 0, 0))
        text_width = welcome_text.get_width()
        welcome = Text(640 - text_width / 2, 580, welcome_text)
        self.main_surface.blit(welcome.text_surface, welcome.position)

    def load_gif_clip(self, gif_filepath):
        # Cargar el GIF como un clip de video usando moviepy
        gif_clip = VideoFileClip(gif_filepath, has_mask=True)
        return gif_clip

    def game_view(self):
        print("En la vista del juego")  # Aquí podrías agregar la lógica para dibujar el juego

    def update(self):
        pygame.display.flip()  # Actualiza la pantalla
