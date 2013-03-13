import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
KEYBOARD = None
PLAYER = None
######################

GAME_WIDTH = 8
GAME_HEIGHT = 8

#### Put class definitions here ####
class Rock(GameElement):
    IMAGE = "Rock"
    SOLID = True

class BlueGem(GameElement):
    IMAGE = "BlueGem"
    SOLID = False
    def interact(self, player):
        player.inventory.append(self)
        GAME_BOARD.draw_msg("You have just acquired a gem! You have %d items!" %(len(player.inventory)))

class OrangeGem(GameElement):
    IMAGE = "OrangeGem"
    SOLID = False
    def interact(self, player):
        player.inventory.append(self.IMAGE)
        GAME_BOARD.draw_msg("You have just acquired a gem! You have %d items!" %(len(player.inventory)))

class Key(GameElement):
    IMAGE = "Key"
    SOLID = False
    def interact(self, player):
        player.inventory.append(self.IMAGE)
        GAME_BOARD.draw_msg("You have just acquired a key! You have %d items!" %(len(player.inventory)))

class Chest(GameElement):
    IMAGE = "Chest"
    SOLID = True
    def interact(self, player):
        if "Key" in player.inventory:
            #if key in thing:
            self.SOLID = False   
            GAME_BOARD.draw_msg("Chest is opened. Here is your Prince Charming!")
            boy = Boy()
            GAME_BOARD.register(boy)
            GAME_BOARD.set_el(6,5, boy)

            # if player.inventory[item] == 'Key':
            #     GAME_BOARD.draw_msg("OMGZ.")
            #     IMAGE = "Cat"
        # player.inventory.append(self)
        # INTERACT PLACE HERE

class Boy(GameElement):
    IMAGE = "Boy"
    SOLID = True

class DoorClosed(GameElement):
    IMAGE = "DoorClosed"
    SOLID = False
    if "OrangeGem" in player.inventory:
            #if key in thing:
            self.SOLID = False   
            GAME_BOARD.draw_msg("Door is now opened.")
            dooropen = DoorOpen()
            GAME_BOARD.register(dooropen)
            GAME_BOARD.set_el(3,6, dooropen)

class DoorOpen(GameElement):
    IMAGE = "DoorOpen"
    SOLID = True

    # def interact(self, player):
        # player.inventory.append(self)
        # GAME_BOARD.draw_msg("You have just acquired a key! You have %d items!" %(len(player.inventory)))

class Character(GameElement):
    IMAGE = "Horns"
    
    def __init__(self):
        GameElement.__init__(self)
        self.inventory = []
        
    def next_pos(self, direction):
        if direction == "up":
            return (self.x, self.y-1)
        elif direction == "down":
            return (self.x, self.y+1)
        elif direction == "left":
            return (self.x-1, self.y)
        elif direction == "right":
            return (self.x+1, self.y)

####   End class definitions    ####

def initialize():
    """Put game initialization code here"""
    rock_positions = [
            (2,1),
            (1,2),
            (3,2),
            (2,3)
        ]
   
    rocks = []
    for pos in rock_positions:
        rock = Rock()
        GAME_BOARD.register(rock)
        GAME_BOARD.set_el(pos[0], pos[1], rock)
        rocks.append(rock)

    rocks[-1].SOLID = False

    global PLAYER
    PLAYER = Character()
    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(2,2, PLAYER)
    print PLAYER

    GAME_BOARD.draw_msg("This game is wicked awesome.")
    bluegem = BlueGem()
    GAME_BOARD.register(bluegem)
    GAME_BOARD.set_el(3,1, bluegem)

    orangegem = OrangeGem()
    GAME_BOARD.register(orangegem)
    GAME_BOARD.set_el(4,4, orangegem)

    key = Key()
    GAME_BOARD.register(key)
    GAME_BOARD.set_el(5,2, key)

    chest = Chest()
    GAME_BOARD.register(chest)
    GAME_BOARD.set_el(5,5, chest)

    dooropen = DoorOpen()
    GAME_BOARD.register(dooropen)

    doorclosed = DoorClosed()
    GAME_BOARD.register(doorclosed)
    GAME_BOARD.set_el(3,6, doorclosed)

# keyboard commands

def keyboard_handler():
    direction = None

    if KEYBOARD[key.UP]:
        direction = "up"

    if KEYBOARD[key.DOWN]:
        direction = "down"

    if KEYBOARD[key.LEFT]:
        direction = "left"

    if KEYBOARD[key.RIGHT]:
        direction = "right"

    if direction:
        next_location = PLAYER.next_pos(direction)
        next_x = next_location[0]
        next_y = next_location[1]
        print next_y
        print next_x


        existing_el = GAME_BOARD.get_el(next_x, next_y)

        if existing_el:
            existing_el.interact(PLAYER)
        if next_x <= 0 or next_x >= 7:
            GAME_BOARD.draw_msg("You have reached out bounds. Try again!")
        elif next_y <= 0 or next_y >= 7:
            GAME_BOARD.draw_msg("You have reached out bounds. Try again!")  
        elif existing_el is None or not existing_el.SOLID:
            GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
            GAME_BOARD.set_el(next_x, next_y, PLAYER)


        



