import pygame


class Text:
    def __init__(self, x, y, text, color=(0, 0, 0), font_type="Fixedsys Excelsior", font_size=48):
        self.position = (x, y)
        self.font = pygame.font.SysFont(font_type, font_size)
        self.text = text
        self.text_surface = self.font.render(self.text, True, color)

    def draw(self, surface):
        surface.blit(self.text_surface, self.position)
