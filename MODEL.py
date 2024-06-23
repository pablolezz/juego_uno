import random
import pygame

class Card:
    suits = ["Rojo", "Amarillo", "Verde", "Azul", "Comodín"]
    ranks = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
             "pierdeturno", "cambiasentido", "robados", "eligecolor", "robacuatro"]

    def __init__(self, suit=0, rank=0):
        self.suit = suit
        self.rank = rank

        rect = pygame.Rect([720 , 750, 80, 125])
        self.image = pygame.Surface(rect.size)
        self.hidden = pygame.Surface(rect.size)
        self.position = []

    def __repr__(self):
        if self.suit == 4:  # Comodín
            return f"{Card.ranks[self.rank]}"
        return f"{Card.ranks[self.rank]} de {Card.suits[self.suit]}"

# Clase Deck representa el mazo de cartas
class Deck:
    def __init__(self):
        self.cards = []
        self.initialize_deck()

    def initialize_deck(self):
        self.cards.clear()  # Limpiar el mazo
        for suit in range(4):  # Suits del 0 al 3
            for rank in range(0, 10):  # Números del 0 al 9 (incluye 0)
                self.cards.append(Card(suit, rank))
                if rank != 0:  # Agregar una segunda carta para números 1-9
                    self.cards.append(Card(suit, rank))
            for rank in range(10, 13):  # Acciones: pierdeturno, cambiasentido, robados
                self.cards.append(Card(suit, rank))
                self.cards.append(Card(suit, rank))
        for rank in range(13, 15):  # Comodines: eligecolor, robacuatro
            for _ in range(4):  # Agregar cuatro de cada comodín
                self.cards.append(Card(4, rank))

    def shuffle(self):
        random.shuffle(self.cards)

    def pop(self):
        return self.cards.pop()  # Retirar la última carta

    def is_empty(self):
        return len(self.cards) == 0  # True si no quedan cartas en el mazo

    def deal(self, hands, num_cards=7):
        for _ in range(num_cards):
            for hand in hands:
                if self.is_empty():
                    return
                hand.add(self.pop())

# Clase Hand representa la mano de un jugador
class Hand:
    def __init__(self):
        self.cards = []

    def add(self, card):
        self.cards.append(card)

    def __repr__(self):
        return f"Hand: {', '.join(str(card) for card in self.cards)}"

# Clase Player representa a un jugador
class Player:
    def __init__(self, name=""):
        self.name = name
        self.hand = Hand()

    def __repr__(self):
        return f"Player {self.name}, {self.hand}"

# Clase Game gestiona la lógica del juego
class Game:
    def __init__(self, player_human, player_ia):
        self.deck = Deck()
        self.player_human = player_human
        self.player_ia = player_ia
        self.players = [player_ia, player_human]
        self.card_in_play = Card(0,0)

        #Esto se puede ver si se sustituye por un Card Type: last_played_card
        self.color = self.card_in_play.suit
        self.number = self.card_in_play.rank

        self.play_area = (320, 264)

    def start_game(self):
        # Barajar el mazo
        self.deck.shuffle()

        # Repartir las cartas a cada jugador
        self.deck.deal([player.hand for player in self.players], num_cards=7)

        # Mostrar las cartas de cada jugador
        print("Cartas repartidas:")
        for player in self.players:
            print(player)

        self.card_in_play = self.deck.pop()
        self.card_in_play.position = self.play_area

        self.color = self.card_in_play.suit  # Me interesa separar el color de la carta, para poder implementar el comodín eligecolor
        self.number = self.card_in_play.rank

        turn = 0
        pierdeturno = 0
        self.has_drawn = 2  # Para cubrir el caso en que la carta inicial sea una carta de efectos
        i = 0