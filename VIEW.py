import pygame
import os

main_dir = os.path.split(os.path.abspath(__file__))[0]
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

class Text:
    def __init__(self, x, y, text):
        self.font = pygame.font.SysFont("Fixedsys Excelsior", 48)
        self.x = x
        self.y = y
        self.position = (self.x, self.y)
        self.text = self.font.render(text, True, (255, 255, 255))


class CardSprite:

    def __init__(self):
        self.sheet = pygame.image.load(os.path.join(main_dir, 'UNO', "Copia UNO.jpg"))
        self.x = self.sheet.get_width()  # 800
        self.y = self.sheet.get_height()  # 882

    def load_grid_images(self):
        sheet_rect = self.sheet.get_rect()
        sheet_width, sheet_height = sheet_rect.size
        sprite_rects = []
        cardheighty = 0
        cardwidthx = 0
        cardsizex = self.x // 10
        cardsizey = 125
        for card in range(56):  # El rango sería mejor definirlo en función del número de cartas del mazo, revisar
            card_coordinates = [cardwidthx, cardheighty, cardsizex, cardsizey]
            sprite_rects.append(card_coordinates)
            cardwidthx += cardsizex
            if cardwidthx >= self.x:
                cardwidthx = 0
                cardheighty += cardsizey
        return self.images_at(sprite_rects)

    def image_at(self, rectangle, colorkey=None):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size)
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    def images_at(self, rects, colorkey=None):
        return [self.image_at(rect, colorkey) for rect in rects]

