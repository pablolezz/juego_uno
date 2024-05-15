from pygame import Rect
from pygame.sprite import Sprite

from VIEW import CardSprite
import random


class Card(Sprite, Rect):
    suits = ["Rojo", "Amarillo", "Verde", "Azul", "Comodín"]
    ranks = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
             "pierdeturno", "cambiasentido", "robados", "eligecolor", "robacuatro"]

    def __init__(self, suit=0,
                 rank=0):
        self.suit = suit
        self.rank = rank
        self.position = []
        self.image = None

    def contains_point(self, point):
        (my_x, my_y) = self.position
        my_width = self.image.get_width()
        my_height = self.image.get_height()
        (x, y) = point
        return my_x <= x < my_x + my_width and my_y <= y < my_y + my_height
class Deck:
    def __init__(self):
        self.cards = []
        for suit in range(4):
            for rank in range(0, 10):
                self.cards.append(Card(suit, rank))
        for suit in range(4):
            for rank in range(10, 13):
                self.cards.append(Card(suit, rank))
        for suit in range(4, 5):
            for rank in range(13, 15):
                self.cards.append(Card(suit, rank))
                self.cards.append(Card(suit, rank))

        sprite = CardSprite()
        images = sprite.load_grid_images()

        i = 0
        for image in images:
            self.cards[i].image = image
            i += 1

        questionmark = sprite.image_at([720, 750, 80, 125])
        self.image = questionmark
        self.position = (650, 256)

    def shuffle(self):
        rng = random.Random()
        rng.shuffle(self.cards)

    def remove(self, card):
        if card in self.cards:
            self.cards.remove(card)
            return True
        return False

    def pop(self):
        return self.cards.pop()  # Pop toma la última carta y la reparte

    def is_empty(self):
        return self.cards == []  # True si no quedan cartas en el mazo

    def deal(self, hands, num_cards=999):
        num_hands = len(hands)
        for i in range(num_cards):
            if self.is_empty():
                break
            card = self.pop()
            hand = hands[i % num_hands]
            hand.add(card)

    def contains_point(self, point):
        """ Return True if my sprite rectangle contains point pt """
        (my_x, my_y) = self.position
        my_width = self.image.get_width()
        my_height = self.image.get_height()
        (x, y) = point
        return my_x <= x < my_x + my_width and my_y <= y < my_y + my_height
class Hand(Deck):
    pass

    def __init__(self):
        super().__init__()
        self.cards = []

    def add(self, card):
        self.cards.append(card)
class Player(Hand):
     def __init__(self, name=""):
        super().__init__()
        self.name = name
        if name == "AI":
            self.status = 1  # jugador controlado por el ordenador
        else:
            self.status = 0  # jugador humano
class Game:

    def __init__(self, player_human, player_ia):
        self.deck = Deck()
        self.player_human = player_human
        self.player_ia = player_ia

if __name__ == '__main__':
    c = Card()
    c.suit