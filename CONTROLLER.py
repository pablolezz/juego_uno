from MODEL import Card, Player
from MODEL import Game
from VIEW import Button, Game_view
import pygame
import os
import sys
import random
from Views.initialView import Initial_view
from Views.loginView import Login_view

main_dir = os.path.split(os.path.abspath(__file__))[0]

class Game_controller:
	def __init__(self, main_surface):
		self.model = Game(Player(""), Player("AI"))
		self.view = Initial_view(main_surface)  # Pasar el controlador como argumento a la vista
		self.game_state = 1
		self.game_started = False
		self.pick_color = False
		self.event = pygame.event.poll()
	def _initial_view(self):
		self.game_started = True
		if self.view.start_view():
			self.game_state = 2

	def _login_view(self):

		self.view = Login_view(pygame.display.set_mode((1280, 640)))
		player_name = self.view.start_view()
		if player_name != "":
			self.model = Game(Player(player_name), Player("AI"))
			self.game_state = 3


	def _game_init(self):
		self.model.start_game()
		self.view.game_start(self.model)
		self.game_started = True
		
	def _game_update(self):
		self._player_turn(self.model.get_current_player())
		self.view = Initial_view(pygame.display.set_mode((1280, 640)))
		self.view.start_view()
		self.view.game_update(self.model)
	def ending_update(self):
		self.view.ending_view(self.model)
	def update(self):

		while True:
			self.event = pygame.event.poll()
			self.view.event_poll_QUIT(self.event)
			match self.game_state:
				case 1:
					self._initial_view()
				case 2:
					self._login_view()
				case 3:
					if not self.game_started:
						self._game_init()
					else:
						self._game_update()
				case 4:
						self.ending_update()

	def _go_next_turn(self):
		self.model.current_player += 1
		if self.model.current_player == len(self.model.players):
			self.model.current_player = 0

	def _player_turn(self, player):
		if player.name == "AI":
			self.AI_plays(player.hand)
		else:
			self.human_plays(player.hand)

		if self.pick_color:
			self._pick_card_color()
		
		self._check_if_game_has_ended(player)

	def _check_if_game_has_ended(self, player):
		if player.hand.is_empty():
			self.game_started = False
			self.game_state = 4

	def _get_playable_cards(self, cards):
		playable_cards = []
		for card in cards:
			if card.suit == self.model.card_in_play.suit or card.rank == self.model.card_in_play.rank or card.rank == 13 or card.rank == 14:
				playable_cards.append(card)
		return playable_cards

	def _play_card(self, hand, card):
		print(f"Card played: {card}")
		self.model.card_in_play = card
		self.model.card_in_play.position = self.model.play_area

		self.model.deck.discard(hand.remove(card))
		
		self._go_next_turn()
		self._check_card_in_play_effect()

	def _check_card_in_play_effect(self):
		if self.model.card_in_play.rank == 11 or self.model.card_in_play.rank == 12:
			self._go_next_turn()
		
		elif self.model.card_in_play.rank == 10:
			current_player_hand = self.model.get_current_player().hand
			self._draw_cards(current_player_hand, 2)
			self._go_next_turn()
		
		elif self.model.card_in_play.rank == 13:
			self._go_next_turn()
			self.pick_color = True

		elif self.model.card_in_play.rank == 14:
			current_player_hand = self.model.get_current_player().hand
			self._draw_cards(current_player_hand, 4)
			self._go_next_turn()
			self.pick_color = True

	def _pick_card_color(self):
		selected_color = -1
		if self.model.get_current_player().name == "AI":
			selected_color = random.Random().randrange(0, 4)
		else:
			selected_color = self.view.poll_color(self.event)
		
		if selected_color != -1:
			card_is_eligecolor = self.model.card_in_play.rank == 13
			self.model.card_in_play = self.model.deck.color_cards[selected_color]
			self.pick_color = False
			
			if (card_is_eligecolor):
				self._go_next_turn()

	def _draw_cards(self, hand, number_of_cards):
		for i in range(0, number_of_cards):
			if self.model.deck.is_empty():
				self.model.deck.refill_deck_from_discard()
			hand.add(self.model.deck.pop())

	def AI_plays(self, hand):
		pygame.time.wait(1000)
		playable_cards = self._get_playable_cards(hand.cards)
		if len(playable_cards) != 0:
			selected_card = playable_cards[random.Random().randrange(0, len(playable_cards))]
			self._play_card(hand, selected_card)
		else:
			self._draw_cards(hand, 1)

	def human_plays(self, hand):
		playable_cards = self._get_playable_cards(hand.cards)
		if len(playable_cards) != 0:
			selected_card = self.view.poll_cards(playable_cards, self.event)
			if selected_card is not None:
				self._play_card(hand, selected_card)
		elif not self.pick_color:
			if self.view.poll_button("ROBAR", self.event):
				self._draw_cards(hand, 1)
				print("Robar carta")