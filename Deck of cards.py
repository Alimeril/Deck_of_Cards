import arcade # need to be installed: pip install arcade (or: pip3 install arcade)
import random

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 580

DECK_CENTER_X = 80
DECK_CENTER_Y = 80

CARD_SCALE = 0.4
DEAL_POS_X = 155
DEAL_POS_Y = 80

CARD_BACK = f"Cards/cardBack_blue2.png"
# CARD_BACK = f"Cards/cardBack_red2.png"
# CARD_BACK = f"Cards/cardBack_green2.png"

# Loading Sounds
SOUND_DRAW = arcade.load_sound("Sounds/draw.wav")
SOUND_SHUFFLE = arcade.load_sound("Sounds/shuffle.wav")
SOUND_TOGGLE_FACE = arcade.load_sound("Sounds/untap.wav")
SOUND_FLIP = arcade.load_sound("Sounds/tap.wav")
SOUND_RESET =  arcade.load_sound("Sounds/cuckoo.wav")

class Card(arcade.Sprite):
    def __init__(self,suit,value,scale,side):
        self.suit = suit
        self.value = value
        self.front_file = f"Cards/card{self.suit}{self.value}.png" 
        self.back_file = CARD_BACK
        self.side = side # Which side of the card is shown
        self.drag = False
        super().__init__(self.front_file,scale)
        if self.side == "front":
            self.texture = arcade.load_texture(self.front_file)
        elif self.side == "back":
            self.texture = arcade.load_texture(self.back_file)

    def flip(self):
        arcade.play_sound(SOUND_FLIP)
        if self.side == "front":
            self.side = "back"
            self.texture = arcade.load_texture(self.back_file)
        elif self.side == "back":
            self.side = "front"
            self.texture = arcade.load_texture(self.front_file)

class Deck(arcade.Sprite):
    def __init__(self, name, scale):
        self.name = name
        self.cards_in_deck = []
        self.faceup_deal = True # Show to deal the cards face_up or face-down
        super().__init__(CARD_BACK,scale)

    def is_empty(self):
        if len(self.cards_in_deck) == 0:
            return True
        else:
            return False

    def card_in(self,card: Card, card_list: arcade.SpriteList):
        card_list.remove(card)
        card.side = "back"
        card.in_deck = True
        self.cards_in_deck.append(card)
    
    def card_out(self,card: Card, card_list: arcade.SpriteList):
        self.cards_in_deck.remove(card)
        card.in_deck = False
        card_list.append(card)
        if self.faceup_deal:
            card.side = "front"
            card.texture = arcade.load_texture(card.front_file)
        else:
            card.side = "back"
            card.texture = arcade.load_texture(card.back_file)
        card.center_x = DEAL_POS_X
        card.center_y = DEAL_POS_Y
   
    def deal(self, card_list: arcade.SpriteList):
        if len(self.cards_in_deck) > 0:
            arcade.play_sound(SOUND_DRAW)
            self.card_out(self.cards_in_deck[len(self.cards_in_deck)-1],card_list)

    def shuffle(self):
        temp_list = []
        arcade.play_sound(SOUND_SHUFFLE)
        while len(self.cards_in_deck) > 0:
            index = random.randrange(len(self.cards_in_deck))
            card = self.cards_in_deck[index]
            temp_list.append(card)
            self.cards_in_deck.remove(card)
        self.cards_in_deck = temp_list
        del temp_list

class Button(arcade.Sprite):
    def __init__(self,scale,kind: int, *args: str):
        self.button_file =[f"Buttons/red_button11.png",f"Buttons/red_button04.png"]
        self.text = args
        self.textnum = 0
        self.condition = "face_up"
        self.pressed = False
        super().__init__(self.button_file[kind],scale)
    def draw(self, *, filter=None, pixelated=None, blend_function=None):
        super().draw(filter=filter, pixelated=pixelated, blend_function=blend_function)
        arcade.draw_text(self.text[self.textnum],self.center_x - 55,self.center_y-3,arcade.color.BLACK_BEAN,12, width = 110 ,align = "center", bold = True)

class MyGame(arcade.Window):
    # Main Game Window
    def __init__(self,width,height,title):
        super().__init__(width,height,title)
        arcade.set_background_color(arcade.color.AO)
        self.SUITS = ["Clubs","Diamonds","Hearts","Spades"]
        self.VALUES = ["2","3","4","5","6","7","8","9","10","J","Q","K","A"]
        self.deck = Deck("main_deck",CARD_SCALE)
        self.deck.center_x = DECK_CENTER_X
        self.deck.center_y = DECK_CENTER_Y
        self.card_list = arcade.SpriteList() # Cards on the table
        for suit in self.SUITS:
            for value in self.VALUES:
                card = Card(suit,value,CARD_SCALE,"back")
                self.card_list.append(card)
                self.deck.card_in(card,self.card_list)
        self.deck.shuffle()
        # Creating face-up or face-down dealing button
        self.button = Button(0.6,0,"Face-Up Deal","Face-Down Deal")
        self.button.center_x = SCREEN_WIDTH-61
        self.button.center_y = SCREEN_HEIGHT-20
        # Creating "help" button
        self.help = False
        self.help_button = Button(0.6,1,"?")
        self.help_button.center_x = 20
        self.help_button.center_y = SCREEN_HEIGHT - 20
        # Creating "reset" button
        self.reset_button = Button(0.42,0,"RESET")
        self.reset_button.center_x = DECK_CENTER_X
        self.reset_button.center_y = DECK_CENTER_Y + 60
        # Creating "shuffle" button
        self.shuffle_button = Button(0.42,0,"SHUFFLE")
        self.shuffle_button.center_x = DECK_CENTER_X
        self.shuffle_button.center_y = DECK_CENTER_Y + 83

    def reset(self):
        arcade.play_sound(SOUND_RESET)
        self.card_list.clear() # Clear the SpriteList
        self.deck.cards_in_deck = []
        for suit in self.SUITS:
            for value in self.VALUES:
                card = Card(suit,value,CARD_SCALE,"back")
                self.card_list.append(card)
                self.deck.card_in(card,self.card_list)
        

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
         # if deck clicked, it deals a card:
        if button == arcade.MOUSE_BUTTON_LEFT:
            if self.deck.collides_with_point((x,y)):
                self.deck.deal(self.card_list)
            # face-up, face-down deal mouse press:  
            if self.button.collides_with_point((x,y)):
                self.button.pressed = True
            # reset butten mouse press:
            if self.reset_button.collides_with_point((x,y)):
                self.reset_button.pressed = True
            # Shuffle button mouse press
            if self.shuffle_button.collides_with_point((x,y)):
                self.shuffle_button.pressed = True
            # Help button mouse press
            if self.help_button.collides_with_point((x,y)):
                self.help_button.pressed = True
            # if a card clicked, it comes on top and it's become ready for drag.
            collide_list = arcade.get_sprites_at_point((x,y), self.card_list)
            reverse_card_list = reversed(self.card_list)
            for card in reverse_card_list:
                if card in collide_list:
                    self.card_list.remove(card)
                    card.drag = True
                    self.card_list.append(card)
                    break
            del collide_list, reverse_card_list
        # right-click on cards, flips them
        elif button == arcade.MOUSE_BUTTON_RIGHT:
            collide_list = arcade.get_sprites_at_point((x,y),self.card_list)
            reverse_card_list = reversed(self.card_list)
            for card in reverse_card_list:
                if card in collide_list:
                    card.flip()
                    break
            del collide_list, reverse_card_list
            

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        for card in self.card_list:
            if card.drag:
                card.center_x += dx
                card.center_y += dy

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        for card in self.card_list:
            card.drag = False
        if button == arcade.MOUSE_BUTTON_LEFT:
            # face-up face-down deal button mouse release:
            if self.button.collides_with_point((x,y)):
                arcade.play_sound(SOUND_TOGGLE_FACE)
                if self.button.pressed:
                    if self.button.condition == "face_up":
                        self.button.condition = "face_down"
                        self.button.textnum = 1
                        self.button.pressed = False
                        self.deck.faceup_deal = False
                    else:
                        self.button.condition = "face_up"
                        self.button.textnum = 0
                        self.button.pressed = False
                        self.deck.faceup_deal = True
            # reset button mouse release:
            if self.reset_button.collides_with_point((x,y)):
                if self.reset_button.pressed:
                    self.reset()
                    self.reset_button.pressed = False
            # shuffle button mouse release:
            if self.shuffle_button.collides_with_point((x,y)):
                if self.shuffle_button.pressed:
                    self.deck.shuffle()
                    self.shuffle_button.pressed = False
            # Help button mouse release
            if self.help_button.collides_with_point((x,y)):
                if self.help_button.pressed:
                    self.help = not self.help
                    self.help_button.pressed = False
    
    def help_page(self):
        arcade.draw_rectangle_filled(SCREEN_WIDTH/2,SCREEN_HEIGHT/2,600,400,arcade.color_from_hex_string("#99ab6cf5"))
        arcade.draw_text("-Left click on the deck to draw a card.",SCREEN_WIDTH/2-300,SCREEN_HEIGHT/2+155,arcade.color_from_hex_string("#BF201f21"),font_size=25,width=600,align="center",font_name="Times New Roman",italic = True)
        arcade.draw_text("-Face-up/down Deal button: Toggle between face-up, face-down deal.",SCREEN_WIDTH/2-300,SCREEN_HEIGHT/2+105,arcade.color_from_hex_string("#BF201f21"),font_size=25,width=600,align="center",font_name="Times New Roman",italic = True)
        arcade.draw_text("-Right click on a card to flip.",SCREEN_WIDTH/2-300,SCREEN_HEIGHT/2+15,arcade.color_from_hex_string("#BF201f21"),font_size=25,width=600,align="center",font_name="Times New Roman",italic = True)
        arcade.draw_text("-Drag cards to move across the mat.",SCREEN_WIDTH/2-300,SCREEN_HEIGHT/2-35,arcade.color_from_hex_string("#BF201f21"),font_size=25,width=600,align="center",font_name="Times New Roman",italic = True)
        arcade.draw_text("-Reset button: Collects the cards into the deck and sorts the deck in order.",SCREEN_WIDTH/2-300,SCREEN_HEIGHT/2-85,arcade.color_from_hex_string("#BF201f21"),font_size=25,width=600,align="center",font_name="Times New Roman",italic = True)
        arcade.draw_text("-Shuffle button: Shuffles the deck.",SCREEN_WIDTH/2-300,SCREEN_HEIGHT/2-175,arcade.color_from_hex_string("#BF201f21"),font_size=25,width=600,align="center",font_name="Times New Roman",italic = True)

    def on_draw(self):
        # Clears the screen
        self.clear()
        # Drawing Buttons
        self.button.draw()
        self.help_button.draw()
        self.reset_button.draw()
        self.shuffle_button.draw()
        # Drawing Cards on Mat
        self.card_list.draw()
        # Drawing the Deck
        arcade.draw_rectangle_outline(DECK_CENTER_X,DECK_CENTER_Y,70,90,arcade.color.WHITE,border_width=5)
        if not self.deck.is_empty():
            self.deck.draw()
        if self.help:
            self.help_page()

def main():
    window = MyGame(SCREEN_WIDTH,SCREEN_HEIGHT,"Deck of Cards: A Sandbox")
    arcade.run()

if __name__ == "__main__":
    main()