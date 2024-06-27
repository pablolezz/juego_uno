import pygame
from TEXT import Text


class PygameObject:

    def __init__(self, is_enabled=True):
        self.is_enabled = is_enabled


class Button(PygameObject):
    def __init__(self, pygameRect=pygame.Rect(0, 0, 0, 0), color=(255, 255, 255), text="", text_color=(0, 0, 0)):
        super().__init__()
        self.rect = pygameRect
        self.color = color

        self.text = Text(self.rect.x + (self.rect.w / 2), self.rect.y + (self.rect.h / 2), text, text_color, "Arial",
                         20)
        self.text.position = (self.rect.x + (self.rect.w / 2) - self.text.text_surface.get_width() / 2,
                              self.rect.y + (self.rect.h / 2) - self.text.text_surface.get_height() / 2)

    def draw(self, surface):
        surface.fill(self.color, self.rect)
        self.text.draw(surface)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False
