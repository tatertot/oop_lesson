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

BOY = None
GAME_WIDTH = 8
GAME_HEIGHT = 8

#### Put class definitions here ####
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

class Boy(Character):
    IMAGE = "Boy"
    SOLID = True

    def interact(self,player):
        GAME_BOARD.draw_msg("Bonjour, Je m'appelle Pierre.")
        GAME_BOARD.del_el(self.x,self.y)
        GAME_BOARD.set_el((player.x-1),(player.y), self)

class Heart(GameElement):
    IMAGE = "Heart"
    SOLID = False
    
    def __init__(self):
        GameElement.__init__(self)
        self.timer = 0

    def update(self,dt):
        self.timer += dt
        if self.x == PLAYER.x and self.y == PLAYER.y:
            GAME_BOARD.draw_msg("Aw, trapped by love! Now you lose everything. Especially your pride. KEEP TRYING (hint: go to the door!")
            GAME_BOARD.del_el(BOY.x,BOY.y)

        if self.timer > .5:
            if self.y < 7:
                GAME_BOARD.del_el(self.x,self.y)
                GAME_BOARD.set_el(self.x,self.y+1,self)
                self.timer = 0
            else:
                GAME_BOARD.del_el(self.x,self.y)
                #GAME_BOARD.set_el(self.x-2,1,self)

    
    


    def interact(self, player):
        GAME_BOARD.draw_msg("Can you dodge the pain of love?")

        # GAME_BOARD.del_el(self.x,self.y)
        # GAME_BOARD.set_el((player.x-1),(player.y), self)

class Rock(GameElement):
    IMAGE = "Rock"
    SOLID = True
    def interact(self, player):
        GAME_BOARD.draw_msg("Ouch!") 


class Block(GameElement):
    IMAGE = "Block"
    SOLID = True
    def interact(self, player):
        GAME_BOARD.register(self)
        if KEYBOARD[key.DOWN]:
            GAME_BOARD.del_el(self.x,self.y)
            GAME_BOARD.set_el((player.x-1),(player.y+1), self)
        else:
            GAME_BOARD.draw_msg("Ouch!!!")

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
            GAME_BOARD.del_el(2,1)
            GAME_BOARD.del_el(1,2)
            GAME_BOARD.del_el(3,2)
            GAME_BOARD.del_el(1,3)
            global BOY
            BOY = Boy()
            GAME_BOARD.register(BOY)
            GAME_BOARD.set_el(6,5, BOY)

            heart = Heart()
            GAME_BOARD.register(heart)
            GAME_BOARD.set_el(4,1,heart)
            # i= 0
            # while i < 5:
            #     print heart.x, heart.y
            #     GAME_BOARD.del_el(heart.x,heart.y)
            #     GAME_BOARD.set_el(heart.x,heart.y+1,heart)
            #     i += 1
        else:
            GAME_BOARD.draw_msg("You must find the right key to open the chest!")


class DoorClosed(GameElement):
    IMAGE = "DoorClosed"
    SOLID = True
    def interact(self,player):
        if "OrangeGem" in player.inventory:
            #if key in thing:
               
            GAME_BOARD.draw_msg("Door is now opened. Enter the tunnel of love.")
            dooropen = DoorOpen()
            GAME_BOARD.register(dooropen)
            GAME_BOARD.set_el(1,6, dooropen)
            

class DoorOpen(GameElement):
    IMAGE = "DoorOpen"
    SOLID = True
    def interact(self,player):
        GAME_BOARD.draw_msg("You have avoided romantic tragedy. Also, you saved your mega hunk from the trunk of death. YOU WIN!")

    # def interact(self, player):
        # player.inventory.append(self)
        # GAME_BOARD.draw_msg("You have just acquired a key! You have %d items!" %(len(player.inventory)))




####   End class definitions    ####

def initialize():
    """Put game initialization code here"""
    rock_positions = [
            (2,1),
            (1,2),
            (3,2)
        ]
   
    rocks = []
    for pos in rock_positions:
        rock = Rock()
        GAME_BOARD.register(rock)
        GAME_BOARD.set_el(pos[0], pos[1], rock)
        rocks.append(rock)


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
    GAME_BOARD.set_el(1,6, doorclosed)

    block = Block()
    GAME_BOARD.register(block)
    GAME_BOARD.set_el(2,3, block)


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
        if next_x <= 0 or next_x >= (GAME_WIDTH-1):
            GAME_BOARD.draw_msg("You have reached out bounds. Try again!")
        elif next_y <= 0 or next_y >= (GAME_HEIGHT-1):
            GAME_BOARD.draw_msg("You have reached out bounds. Try again!")  
        elif existing_el is None or not existing_el.SOLID:
            GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
            GAME_BOARD.set_el(next_x, next_y, PLAYER)
            try:
                GAME_BOARD.del_el(BOY.x, BOY.y)
                GAME_BOARD.set_el(next_x+1, next_y, BOY)
            except:
                pass




        



