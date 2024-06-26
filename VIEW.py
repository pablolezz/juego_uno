from faulthandler import is_enabled
from operator import is_
import time
from tkinter import BUTT

import pygame
import os
import sys

main_dir = os.path.split(os.path.abspath(__file__))[0]

class PygameObject:
	def __init__(self, is_enabled = True):
		self.is_enabled = is_enabled

class Button(PygameObject):
	def __init__(self, pygameRect = pygame.Rect(0, 0, 0, 0), color = (255, 255, 255), text = "", text_color = (0, 0, 0)):
		super().__init__()
		self.rect = pygameRect
		self.color = color
		
		self.text = Text(self.rect.x + (self.rect.w / 2), self.rect.y + (self.rect.h / 2), text, text_color, "Arial", 20)
		self.text.position = (self.rect.x + (self.rect.w / 2) - self.text.text_surface.get_width() / 2, self.rect.y + (self.rect.h / 2) - self.text.text_surface.get_height() / 2)

	def draw(self, surface):
		surface.fill(self.color, self.rect)
		self.text.draw(surface)

	def contains_point(self, point):
		return self.rect.collidepoint(point)

	def handle_event(self, event):
		if event.type == pygame.MOUSEBUTTONDOWN:
			if self.rect.collidepoint(event.pos):
				return True
		return False

class Text:
	def __init__(self, x, y, text, color = (0, 0, 0), font_type = "Fixedsys Excelsior", font_size = 48):
		self.position = (x, y)
		self.font = pygame.font.SysFont(font_type, font_size)
		self.text = text
		self.text_surface = self.font.render(self.text, True, color)
		
	def draw(self, surface):
		surface.blit(self.text_surface, self.position)

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

class InputBox:
	def __init__(self, x, y, w, h, text=""):
		self.rect = pygame.Rect(x, y, w, h)
		self.color_inactive = pygame.Color("lightskyblue3")
		self.color_active = pygame.Color("dodgerblue2")
		self.color = self.color_inactive
		self.text = text
		self.font = pygame.font.Font(None, 32)
		self.txt_surface = self.font.render(text, True, self.color)
		self.active = False

	def handle_event(self, event):
		if event.type == pygame.MOUSEBUTTONDOWN:
			if self.rect.collidepoint(event.pos):
				self.active = not self.active
			else:
				self.active = False
			self.color = self.color_active if self.active else self.color_inactive

		if event.type == pygame.KEYDOWN:
			if self.active:
				if event.key == pygame.K_RETURN:
					print(self.text)  # Aquí podrías manejar el texto ingresado
				elif event.key == pygame.K_BACKSPACE:
					self.text = self.text[:-1]
				else:
					self.text += event.unicode
				self.txt_surface = self.font.render(self.text, True, self.color)

	def update(self):
		width = max(200, self.txt_surface.get_width() + 10)
		self.rect.w = width

	def draw(self, screen):
		screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
		pygame.draw.rect(screen, self.color, self.rect, 2)


class Game_view:
	def __init__(self, main_surface):
		self.all_buttons = dict()
		self.main_surface = main_surface

		# Asignamos 3 colores para las 3 "fases"
		self.surface_color_1 = (19, 136, 8)
		self.surface_color_2 = (255, 0, 0)
		self.surface_color_3 = (0, 255, 255)

		self.play_area = (320, 264)
		self.colors = ([255, 0, 0], [0, 255, 2], [255, 255, 0], [0, 0, 255])

	def event_poll_QUIT(self, event):
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

	def start_update(self):
		self.main_surface.fill(self.surface_color_1)
		logo = pygame.image.load(os.path.join(main_dir, 'UNO', "UNO_logo_small.png"))
		
		welcome_text = Text(345, 580, "Pulsa cualquier tecla para continuar")
		
		self.main_surface.blit(logo, (1280 // 2 - logo.get_width() // 2, 640 // 2 - logo.get_height() // 2))
		welcome_text.draw(self.main_surface)

		event = pygame.event.poll()
		if event.type == pygame.KEYDOWN:
			return True

		pygame.display.flip()


	def login_update(self):
		type_name_text = Text(500, 100, "¿Cómo te llamas?")
		input_box = InputBox(500, 150, 280, 32)
		start_button = Button(pygame.Rect(500, 300, 200, 50), (255, 255, 255), "CONTINUAR")

		while True:
			for event in pygame.event.get():
				input_box.handle_event(event)
				if start_button.handle_event(event):
					return input_box.text

			input_box.update()

			self.main_surface.fill(self.surface_color_2)
			
			type_name_text.draw(self.main_surface)
			input_box.draw(self.main_surface)
			start_button.draw(self.main_surface)

			pygame.display.flip()


	def game_start(self, game_model):
		self._define_game_buttons()

	def game_update(self, game_model):
		self.main_surface.fill(self.surface_color_3)
		
		player_turn_text = Text(300, 200, f"Player turn: {game_model.get_current_player().name}")
		player_turn_text.draw(self.main_surface)

		self._update_game_cards(game_model)
		self._render_game_cards(game_model)

		self._render_game_buttons()
		pygame.display.flip()



	def _update_game_cards(self, game_model):
		# Definimos un patrón para pegar las cartas una junto a otra
		[paste_x, paste_y] = [64, 480]
		[paste_xAI, paste_yAI] = [64, 32]

		for player in game_model.players:
			for card in player.hand.cards:
				card.hidden = game_model.deck.image
				if player.name == "AI":
					card.position = [paste_xAI, paste_yAI]
					paste_xAI += 85
				else:
					card.position = [paste_x, paste_y]
					paste_x += 85

	def ending_view(self,model):
		self.main_surface.fill(self.surface_color_1)
		print(model.get_next_player)
		if model.get_next_player == 1:

			final_text_vicoria = Text(200, 100, "Has ganado!!, quieres volver a jugar ?")
			final_text_vicoria.draw(self.main_surface)

		else:

			final_text_derrota = Text(200, 100, "Has perdido, quieres volver a jugar ?")
			final_text_derrota.draw(self.main_surface)

		VOLVER_A_JUGAR = Button(pygame.Rect(225, 400, 175, 30), self.colors[0], "Volver a jugar")
		SALIR = Button(pygame.Rect(575, 400, 175, 30), self.colors[3], "Salir del juego")

		VOLVER_A_JUGAR.draw(self.main_surface)
		SALIR.draw(self.main_surface)


		pygame.display.flip()
	def _render_game_cards(self, game_model):
		for player in game_model.players:
			for card in player.hand.cards:
				if player.name == "AI":
					self.main_surface.blit(card.hidden, card.position)
				else:
					self.main_surface.blit(card.image, card.position)
		self.main_surface.blit(game_model.deck.image, game_model.deck.position)
		self.main_surface.blit(game_model.card_in_play.image, game_model.card_in_play.position)

	def poll_cards(self, cards, event):
		for card in cards:
			rect = pygame.Rect([card.position[0], card.position[1], 80, 120])
			button = Button(rect)
			if button.handle_event(event):
				return card

	def _define_game_buttons(self):
		x = self.play_area[0] - 55
		y = self.play_area[1]

		self.all_buttons["COLOR_0"] = Button(pygame.Rect(x,			y + 145, 45, 45), self.colors[0])
		self.all_buttons["COLOR_1"] = Button(pygame.Rect(x + 50,	y + 145, 45, 45), self.colors[1])
		self.all_buttons["COLOR_2"] = Button(pygame.Rect(x + 100,	y + 145, 45, 45), self.colors[2])
		self.all_buttons["COLOR_3"] = Button(pygame.Rect(x + 150,	y + 145, 45, 45), self.colors[3])

		self.all_buttons["ROBAR"] = Button(pygame.Rect(650, 245, 125, 25), (255, 255, 255), "Robar carta")
		self.all_buttons["VOLVER_A_JUGAR"] = Button(pygame.Rect(225, 400, 175, 30), self.colors[0], "Volver a jugar")
		self.all_buttons["SALIR"] = Button(pygame.Rect(575, 400, 175, 30), self.colors[3], "Salir del juego")
		
		for button in self.all_buttons.values():
			button.is_enabled = False

	def _render_game_buttons(self):
		for button in self.all_buttons.values():
			if button.is_enabled:
				button.draw(self.main_surface)

	def poll_button(self, button_name, event):
		self.all_buttons[button_name].is_enabled = True
		if self.all_buttons[button_name].handle_event(event):
			self.all_buttons[button_name].is_enabled = False
			return True
		return False

	def poll_color(self, event):
		for color in range(0, 4):
			self.all_buttons[f"COLOR_{color}"].is_enabled = True
			if self.all_buttons[f"COLOR_{color}"].handle_event(event):
				for i in range(0, 4):
					self.all_buttons[f"COLOR_{i}"].is_enabled = False
				return color
		return -1
