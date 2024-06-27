import random
from CARDSPRITE import CardSprite

class Card:
	suits = ["Rojo", "Verde", "Amarillo", "Azul", "Comodín"]
	ranks = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
			 "robados", "cambiasentido", "pierdeturno", "eligecolor", "robacuatro"]

	def __init__(self, suit=0, rank=0):
		self.suit = suit
		self.rank = rank

		cardSprite = CardSprite()
		self.hidden = cardSprite.image_at([0, 0, 80, 120])
		self.image = cardSprite.load_image(self.suit, self.rank)
		self.position = [0, 0]

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
		self.color_cards = []
		self.set_color_cards()
		
		self.initialize_deck()
		
	def set_color_cards(self):
		self.color_cards = [Card(4, 2), Card(4, 3), Card(4, 4), Card(4, 5)]
		
		i = 0
		for card in self.color_cards:
			card.suit = i
			card.rank = -1
			card.position = (320, 264)
			i += 1

	def initialize_deck(self):
		self._cards.clear()
		for suit in range(0, 4):
			for rank in range (0, 13):
				self._cards.append(Card(suit, rank))
		for i in range(0, 4):
			card = Card(4, 13)
			card.image = CardSprite().load_image(4, 0)
			self._cards.append(card)
			
			card = Card(4, 14)
			card.image = CardSprite().load_image(4, 1)
			self._cards.append(card)

	def shuffle(self):
		random.shuffle(self._cards)

	def refill_deck_from_discard(self):
		for card in self._discard_cards:
			self._cards.append(card)

		top_card = self._cards.pop()
		self.shuffle()
		
		self._discard_cards = []
		self._discard_cards.append(top_card)

	def discard(self, card):
		self._discard_cards.append(card)

	def pop(self):
		return self._cards.pop()

	def is_empty(self):
		return len(self._cards) == 0

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
		return card

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
		self.current_player = 1
		
		self.card_in_play = Card(0,0)

		self.play_area = (320, 264)

	def get_current_player(self):
		return self.players[self.current_player]
	
	def get_next_player(self):
		next_player = self.current_player + 1
		if next_player == len(self.players):
			next_player = 0
		return self.players[next_player]




	def start_game(self,num_cartas_jugadas):
		self.deck.shuffle()
		self.deck.deal([player.hand for player in self.players], num_cards=num_cartas_jugadas)
		self.card_in_play = self.deck.pop()
		self.card_in_play.position = self.play_area