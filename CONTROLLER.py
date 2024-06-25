from MODEL import Card, Player
from MODEL import Game
from VIEW import Button, Game_view
import pygame
import os
import sys
import random

main_dir = os.path.split(os.path.abspath(__file__))[0]

class Game_controller:
	def __init__(self, main_surface):
		self.model = Game(Player(""), Player("AI"))
		self.view = Game_view(main_surface)  # Pasar el controlador como argumento a la vista
		self.game_state = 1
		self.game_started = False  # Para controlar si el juego ya ha comenzado
		self.event = pygame.event.poll()

	def _start_update(self):
		if self.view.start_update():
			self.game_state = 2


	def _login_update(self):
		player_name = self.view.login_update()
		if player_name != "":
			self.model = Game(Player(player_name), Player("AI"))
			self.game_state = 3


	def _game_init(self):
		self.model.start_game()
		self.view.game_start(self.model)
		self.game_started = True
		
	def _game_update(self):
		self._game_logic_update()
		self.view.game_update(self.model)

	def update(self):
		while True:
			self.event = pygame.event.poll()
			self.view.event_poll_QUIT(self.event)
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


	def _game_logic_update(self):
		# Los efectos ya están consolidados (esperemos). Ahora hay que definir el cambio de turno
		self.playable_cards = []
		suits_in_hand = []

		self._player_turn(self.model.getCurrentPlayer(), suits_in_hand)
		#self._check_card_in_play_effect()

	def _go_next_turn(self):
		self.model.current_player += 1
		if self.model.current_player == len(self.model.players):
			self.model.current_player = 0

	def _player_turn(self, player, suits_in_hand):
		if player.name == "AI":
			self.AI_plays(player.hand)
		else:
			self.human_plays(player.hand)

#---CHECK IF GAME HAS ENDED---
		# Consideraciones de final de turno, a continuación
		if self.model.deck.is_empty():  # Si no quedan cartas en el mazo
			self.model.deck.refill_deck_from_discard()

		if player.hand.is_empty():  # Si no quedan cartas en la mano
			#   Cambiar al view de EndGame
			self.game_started = False
			self.game_state = 1

			#self.main_surface.fill(self.surface_color)
			#if player.name == "AI":
				#pygame.mixer.music.load(os.path.join(main_dir, 'UNO', "loss.mp3"))
				#pygame.mixer.music.play(-1)
				# loss = Text(100, 300, "¡Lo sentimos, " + self.player_name + "! El ordenador ha ganado la partida")
				# self.main_surface.blit(loss.text, loss.position)
			#else:
				#pygame.mixer.music.load(os.path.join(main_dir, 'UNO', "win.mp3"))
				#pygame.mixer.music.play(-1)
				# win = Text(100, 300, "¡Enhorabuena, " + self.player_name + "! Has ganado la partida")
				# self.main_surface.blit(win.text, win.position)
			#self.blit_buttons(6, 8)
			'''while end_game == 0:
			   for event in pygame.event.get():
					if event.type == pygame.QUIT:
						pygame.quit()
						sys.exit()
					if event.type == pygame.MOUSEBUTTONDOWN:  # Hemos hecho click
						place_of_click = event.dict["pos"]
						for button in self.all_buttons[6:8]:
							if button.contains_point(place_of_click):
								if button == self.all_buttons[6]:
									end_game = 1
									self.deck = Deck()
									self.deck.shuffle()
									self.play_UNO()
								else:
									pygame.quit()
									sys.exit()'''

	def _check_card_in_play_effect(self):
		if self.model.card_in_play.rank == 10:  # "pierdeturno": # El turno pasará al otro jugador
			self._go_next_turn()

		elif self.model.card_in_play.rank == 11:  # "cambiasentido":
			self._go_next_turn()

		elif self.model.card_in_play.rank == 12:  # "robados":
			# No queremos que al comenzar el siguiente turno se vuelvan a robar dos cartas
			self._go_next_turn()
			for n in range(2):
				if self.model.deck.is_empty():  # Si no quedan cartas en el mazo
					self.model.deck.refill_deck_from_discard()
				# Robo dos cartas y las añado a mi mano
				self.model.getCurrentPlayer().hand.add(self.model.deck.pop())

		elif self.model.card_in_play.rank == 13:  # "eligecolor":
			# No queremos que al final de este turno se vuelvan a robar cuatro cartas
			self._go_next_turn()
			# Aquí hay que añadir un árbol de decisión según sea jugador IA o jugador humano, para elegir el color
			if self.model.getCurrentPlayer().name == "AI":  # si el jugaselsdor es IA
				rng = random.Random()
				#self.color = rng.randrange(0, 4)
			else:  # si el jugador es humano
				#self.blit_buttons(0, 4)
				pygame.display.flip()
				has_picked_color = 0
				while has_picked_color == 0:
					for event in pygame.event.poll():
						if event.type == pygame.MOUSEBUTTONDOWN:  # Hemos hecho click
							place_of_click = event.dict["pos"]
							b = 0
							'''for button in self.all_buttons[0:4]:
								if button.contains_point(place_of_click):
									has_picked_color = 1
									self.color = b
								b += 1'''
		   # self.model.card_in_play.suit = self.color

		elif self.model.card_in_play.rank == 14:  # "robacuatro":
			self._go_next_turn()  # No queremos que al final de este turno se vuelvan a robar cuatro cartas
			#self.model.card_in_play.suit = self.color
			for n in range(4):
				if self.model.deck.is_empty():  # Si no quedan cartas en el mazo
					self.model.deck.refill_deck_from_discard()
				# Robo cuatro cartas y las añado a mi mano
				self.model.getCurrentPlayer().cards.append(self.model.deck.pop())
			# Aquí hay que añadir un árbol de decisión según sea jugador IA o jugador humano, para elegir el color
			if self.model.getCurrentPlayer().name == "AI":
				rng = random.Random()
				#self.color = rng.randrange(0, 4)
			else:  # si el jugador es humano
				#self.blit_buttons(0, 4)
				has_picked_color = 0

				while has_picked_color == 0:
					for event in pygame.event.poll():
						if event.type == pygame.MOUSEBUTTONDOWN:  # Hemos hecho click
							place_of_click = event.dict["pos"]
							b = 0
							'''for button in self.all_buttons[0:4]:
								if button.contains_point(place_of_click):
									has_picked_color = 1
									self.color = b
								b += 1'''

	def _get_playable_cards(self, cards):
		playable_cards = []
		for card in cards:
			if card.suit == self.model.card_in_play.suit or card.rank == self.model.card_in_play.rank or card.rank == 13:  # "eligecolor":
				# Si la carta comparte color o número con la que está en juego, o si es el comodín de elegir color
				playable_cards.append(card)
		if len(playable_cards) == 0:
			for card in cards:
				if card.suit != self.model.card_in_play.suit and (card.rank == 13 or card.rank == 14):
					playable_cards.append(card)  # Lo añadimos a las cartas que podemos jugar

		return playable_cards

	def _play_card(self, hand, card):
		self.model.card_in_play = card
		self.model.card_in_play.position = self.model.play_area

		hand.remove(card)
		self.model.deck.discard(card)

	def _draw_card(self, hand):
		if not self.model.deck.is_empty():
			hand.add(self.model.deck.pop())
			self._go_next_turn()
		else:
			self.model.deck.refill_deck_from_discard()
			self._draw_card(hand)

	def AI_plays(self, hand):
		pygame.time.wait(1000)
		playable_cards = self._get_playable_cards(hand.cards)
		if len(playable_cards) != 0:
			selected_card = playable_cards[random.Random().randrange(0, len(playable_cards))]
			self._play_card(hand, selected_card)
		else:
			self._draw_card(hand)

	def human_plays(self, hand):
		playable_cards = self._get_playable_cards(hand.cards)
		if len(playable_cards) != 0:
			selected_card = self.view.poll_cards(playable_cards, self.event)
			if selected_card is not None:
				self._play_card(hand, selected_card)
				print(f"Card played: {selected_card}")
			if self.view.poll_button("PASAR_TURNO", self.event):
				self._go_next_turn()
				print("Pasar turno")
		else:
			if self.view.poll_button("ROBAR", self.event):
				self._draw_card(hand)
				print("Robar carta")