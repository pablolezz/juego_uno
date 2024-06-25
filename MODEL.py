import random
import pygame

from VIEW import CardSprite

class Card:
	suits = ["Rojo", "Amarillo", "Verde", "Azul", "Comodín"]
	ranks = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
			 "pierdeturno", "cambiasentido", "robados", "eligecolor", "robacuatro"]

	def __init__(self, suit=0, rank=0):
		self.suit = suit
		self.rank = rank

		cardSprite = CardSprite()
		self.hidden = cardSprite.image_at([0, 0, 80, 120])
		self.image = cardSprite.load_image(self.suit, self.rank)
		self.position = []

	def __repr__(self):
		if self.suit == 4:  # Comodín
			return f"{Card.ranks[self.rank]}"
		return f"{Card.ranks[self.rank]} de {Card.suits[self.suit]}"

class Deck:
	def __init__(self):
		self.image = CardSprite().image_at([0, 0, 80, 120])
		self.position = (650, 256)
		self._cards = []
		self._discard_cards = []
		self.initialize_deck()

	def initialize_deck(self):
		self._cards.clear()  # Limpiar el mazo
		sprite_sheet = CardSprite()
		for suit in range(4):
			for rank in range (0, 12):
				card = Card(suit, rank)
				self._cards.append(card)

	def shuffle(self):
		random.shuffle(self._cards)

	def refill_deck_from_discard(self):
		self.cards = self._discard_cards
		self.shuffle()
		self._discard_cards = []
		
	def discard(self, card):
		self._discard_cards.append(card)

	def pop(self):
		return self._cards.pop()
	
	def is_empty(self):
		return len(self._cards) == 0  # True si no quedan cartas en el mazo

	def deal(self, hands, num_cards=7):
		for _ in range(num_cards):
			for hand in hands:
				if self.is_empty():
					return
				hand.add(self.pop())

class Hand:
	def __init__(self):
		self.cards = []

	def is_empty(self):
		if len(self.cards) == 0:
			return True
		return False

	def add(self, card):
		self.cards.append(card)

	def remove(self, card):
		self.cards.remove(card)

	def __repr__(self):
		return f"Hand: {', '.join(str(card) for card in self.cards)}"

class Player:
	def __init__(self, name=""):
		self.name = name
		self.hand = Hand()

	def __repr__(self):
		return f"Player {self.name}, {self.hand}"

class Game:
	def __init__(self, player_human, player_ia):
		self.deck = Deck()

		self.players = [player_ia, player_human]
		self.current_player = 0
		
		self.card_in_play = Card(0,0)
		self.last_played_card = self.card_in_play

		self.play_area = (320, 264)

	def getCurrentPlayer(self):
		return self.players[self.current_player]

	def start_game(self):
		# Barajar el mazo
		self.deck.shuffle()

		# Repartir las cartas a cada jugador
		self.deck.deal([player.hand for player in self.players], num_cards=7)

		self.card_in_play = self.deck.pop()
		self.card_in_play.position = self.play_area