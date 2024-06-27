import pygame
import os
main_dir = os.path.split(os.path.abspath(__file__))[0]

class CardSprite:

	def __init__(self):
		self.sheet = pygame.image.load(os.path.join(main_dir, 'UNO', "UNO_spriteSheet.png"))
		self.x = self.sheet.get_width()  # 800
		self.y = self.sheet.get_height()  # 882

	def load_image(self, suit, rank):
		card_width = 80
		card_height = 120
		card_x = rank * card_width
		card_y = 120 + (suit * card_height)
		return self.image_at([card_x, card_y, card_width, card_height])

	def image_at(self, rectangle, colorkey=None):
		rect = pygame.Rect(rectangle)
		image = pygame.Surface(rect.size)
		image.blit(self.sheet, (0, 0), rect)
		return image