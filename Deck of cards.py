import arcade # need to be installed: pip install arcade (or: pip3 install arcade)
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700

DECK_CENTER_X = 100
DECK_CENTER_Y = 100

CARD_SCALE = 0.5
DEAL_POS_X = 100
DEAL_POS_Y = 100

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
        self.center_x = DECK_CENTER_X
        self.center_y = DECK_CENTER_Y
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
        card.side = "front"
        card.center_x = DEAL_POS_X
        card.center_y = DEAL_POS_Y
   
    def deal(self):
        self.card_out(self.cards_in_deck[len(self.cards_in_deck)-1])

    def shuffle(self):
        temp_list = []
        while len(self.cards_in_deck) > 0:
            index = random.randrange(len(self.cards_in_deck))
            card = self.cards_in_deck[index]
            temp_list.append(card)
            self.cards_in_deck.remove(card)
        self.cards_in_deck = temp_list
        del temp_list

    def reset(self,card_list: arcade.SpriteList):
        for card in card_list:
            self.cards_in_deck.append(card)
            card_list.remove(card)
        self.shuffle()