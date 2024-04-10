import arcade
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700

class Card(arcade.Sprite):
    def __init__(self,suit,value,scale,side):
        self.suit = suit
        self.value = value
        self.scale = scale
        self.front_file = f"Cards/{self.suit}{self.value}.png" 
        self.back_file = f"Cards/back.png"
        self.side = side # Which side of the card is shown
        self.in_deck = True # The card is in a deck or not
        self.order = 1 # If cards are on top of each other, shows the order
        if self.side == "front":
            super().__init__(self.front_file,self.scale)
        elif self.side == "back":
            super().__init__(self.back_file,self.scale)

    def flip(self):
        if self.side == "front":
            self.side = "back"
            super().__init__(self.back_file,self.scale)
        elif self.side == "back":
            self.side = "front"
            super().__init__(self.front_file,self.scale)

class Deck(arcade.Sprite):
    def __init__(self, name,scale):
        self.center_x = 100
        self.center_y = 100
        self.name = name
        self.cards_in_deck = []
        super().__init__("Cards/back.png",self.scale)
    
    def card_in(self,card: Card, card_list: arcade.SpriteList):
        self.cards_in_deck.append(card)
        card.in_deck = True
        card_list.remove(card)
    
    def card_out(self,card: Card, card_list: arcade.SpriteList):
        self.cards_in_deck.remove(card)
        card.in_deck = False
        card.order = 1
        for c in card_list:
            c.order += 1
        card_list.append(card)
        card.center_x = 200
        card.center_y = 100
        