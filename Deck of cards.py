import arcade
import random

class card(arcade.Sprite):
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