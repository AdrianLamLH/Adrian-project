# Import the libraries for pygame, math functions
# used for enemy AI and random for generating behaviours
import pygame
import math
import random
import numpy

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
BROWN = (165, 42, 42)
PURPLE = (128, 0, 128)
YELLOW = (255, 255, 0)

# Initialise the game engine
pygame.init()

# Initialise variables
pilot_x = 400
pilot_y = 384
bullet_x = 0
bullet_y = 0
pilot_x_speed = 0
pilot_y_speed = 0
enemy_speed_change = 0
gravity = 2.5
x_hitbox = 0
y_hitbox = 0
TotScore = 0
HitScore = 2
MobScore = 10
MobsDead = 0
PilotHealth = 3
killed_mob = 0
mob_got_killed = False
BlockMoving = True
row_spacing = 36
column_spacing = 36
ShortTimeMobs = 2500
LongTimeMobs = 3200
# Counts the number of flickers when hit
flickercount = 3
# Checks whether there is an active block currently on the grid
finished_moving = True
# Temp store to hold next block to be placed on the grid
next_block_store = 0
# Checks whether a quick drop is being performed, which would then mean the next block is added after the drop completes
quick_drop = False
# Checks if the spawn area is free of blocks before placing the next block on the grid
not_clear = False
# Setting up an event for firing the projectiles and spawning mobs
FireRate = pygame.USEREVENT
SpawnEnemy = pygame.USEREVENT+1
PilotHit = pygame.USEREVENT+2
PilotHitRecover = pygame.USEREVENT+3
Pilot_flickering = False
# Grace period for the damage taken
RecoverTime = pygame.USEREVENT+4
TimeShot = 220
# Time delay between movement of tetris blocks
MoveBlocks = pygame.USEREVENT+5
# Spawning mobs at random intervals in time range
TimeMobs = random.randint(ShortTimeMobs, LongTimeMobs)

# Setting up the screen
size = (1024, 768)
screen = pygame.display.set_mode(size)
# Labelling the program
pygame.display.set_caption("Game name here")

# To manage the fps
clock = pygame.time.Clock()

# Tetris board setup
TGrid = []
for TColumn in range(10):
    TGrid.append([])
    for TRow in range(20):
        TGrid[TColumn].append(0)


# Game classes

# Draw function

# Score


def drawing(text, text_size, color, x_pos, y_pos):
    font_style = pygame.font.SysFont("pressstart2p", text_size)
    printtext = font_style.render(str(text), False, color)
    screen.blit(printtext, (x_pos, y_pos))

# Health hearts


def show_health():
    heart_pic = pygame.image.load('heart_pic.png')
    rescaled_heart_pic = pygame.transform.smoothscale(heart_pic, (25, 25))
    if PilotHealth >= 3:
        screen.blit(rescaled_heart_pic, (750, 20))
        screen.blit(rescaled_heart_pic, (775, 20))
        screen.blit(rescaled_heart_pic, (800, 20))
    elif PilotHealth == 2:
        screen.blit(rescaled_heart_pic, (750, 20))
        screen.blit(rescaled_heart_pic, (775, 20))
    elif PilotHealth == 1:
        screen.blit(rescaled_heart_pic, (700, 20))


# Setting up pilot sprite


class Pilot(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([25, 25])
        # Creates the image of the pilot
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x = pilot_x
        self.rect.y = pilot_y


class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Setting up the design of the projectiles
        self.image = pygame.Surface([10, 10])
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = pilot_x
        self.rect.y = pilot_y

    def update(self):
        # Projectile starts with same coordinates as player but then moves over time
        self.rect.x += 12


class Enemy(pygame.sprite.Sprite):
    # No pass
    def __init__(self, mob_health, block_choice):
        super().__init__()
        # Sets the hitboxes according to which block it is
        if block_choice == JBlock or block_choice == LBlock or block_choice == SBlock or block_choice == ZBlock:
            self.x_hitbox = 60
            self.y_hitbox = 90
        elif block_choice == TBlock:
            self.x_hitbox = 90
            self.y_hitbox = 60
        elif block_choice == IBlock:
            self.x_hitbox = 30
            self.y_hitbox = 120
        elif block_choice == OBlock:
            self.x_hitbox = 60
            self.y_hitbox = 60
        self.image = pygame.Surface([self.x_hitbox, self.y_hitbox])
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        # Generic and basic attributes of an enemy
        self.rect.x = random.randint(1024, 1030)
        self.rect.y = random.randint(40, 725)
        self.Mob_Health = mob_health
        self.Block_Choice = block_choice
    # Enemy moves left

    def update(self):
        self.rect.x -= 2 + enemy_speed_change
        global TotScore
        global MobScore
        global Pilot_flickering
        global PilotHealth
        if Mob in list_mobs:
            # Detects when pilot is hit and the pilot flashes
            pilot_damaged = pygame.sprite.spritecollide(Pilot, list_mobs, False)
            # Need to fix flicker timing so it only triggers the flicker once during the collision
            # Introduced pilot_flickering so it only triggers the flicker upon first collision
            if pilot_damaged and Pilot_flickering is False:
                # print("Pilot character's position(", pilot_x, ", ", pilot_y, ")")
                # print("Enemy collided with and its  position is (", Mob.rect.x, ", ", Mob.rect.y, ")")
                pygame.time.set_timer(PilotHit, 1000)
                Pilot_flickering = True
                PilotHealth -= 1
                print("Pilot health is now", PilotHealth)


class BlockBlock(pygame.sprite.Sprite):
    def __init__(self, column, row, colour):
        super().__init__()
        self.valid_block_move = True  # Initializes the valid_block_move variable for checking if spaces are free
        self.column = column
        self.row = row
        self.block_colour = colour
        self.block_matrix = []  # Stores the block matrix arrangement
        self.block_dimensions = 0  # Stores the dimensions of the block
        self.y_max = 0  # Stores the height of the block
        self.x_max = 0  # Stores the width of the block
        self.rotated = False  # Stores whether the block has been rotated or not
        self.block_one = []
        self.block_two = []
        self.block_three = []
        self.block_four = []
        self.block_list = []  # Stores each of the individual blocks that make up the pieces
        self.block_lowest = []  # Position of block closest to the boundaries of the screen stored
        self.block_rightest = []
        self.block_leftest = []
        self.block_lowest_list = []  # List of blocks that are at the boundaries stored
        self.block_rightest_list = []
        self.block_leftest_list = []
        self.block_list_temp = []
        self.valid_blocks = 0
        self.valid_blocks_left = 0
        self.valid_blocks_right = 0
        self.xcounter = 0
        self.ycounter = 0
        self.flag = True
        self.block_dimensions_temp = []
        self.block_dimensions_prerotate = []
        self.block_lowest_prerotate = []
        self.block_rightest_prerotate = []
        self.block_leftest_prerotate = []
        self.block_one_prerotate = []
        self.block_two_prerotate = []
        self.block_three_prerotate = []
        self.block_four_prerotate = []

    def update_block_setup(self):  # Tracks the lowest blocks in the list that need to be accounted for
        self.block_lowest_list.clear()
        self.block_rightest_list.clear()
        self.block_leftest_list.clear()
        self.block_lowest_list = list(self.block_list)
        self.block_leftest_list = list(self.block_list)
        self.block_rightest_list = list(self.block_list)
        self.block_list_temp = list(self.block_list)

        # Lowest list

        if self.block_one in self.block_lowest_list and self.block_two in self.block_lowest_list:
            if self.block_one[0] == self.block_two[0]:
                if self.block_one[1] == self.block_two[1] - 1:
                    self.block_lowest_list.remove(self.block_one)
                elif self.block_one[1] == self.block_two[1] + 1:
                    self.block_lowest_list.remove(self.block_two)
        if self.block_two in self.block_lowest_list and self.block_three in self.block_lowest_list:
            if self.block_two[0] == self.block_three[0]:
                if self.block_two[1] == self.block_three[1] - 1:
                    self.block_lowest_list.remove(self.block_two)
                elif self.block_two[1] == self.block_three[1] + 1:
                    self.block_lowest_list.remove(self.block_three)
        if self.block_three in self.block_lowest_list and self.block_four in self.block_lowest_list:
            if self.block_three[0] == self.block_four[0]:
                if self.block_three[1] == self.block_four[1] - 1:
                    self.block_lowest_list.remove(self.block_three)
                elif self.block_three[1] == self.block_four[1] + 1:
                    self.block_lowest_list.remove(self.block_four)
        if self.block_two in self.block_lowest_list and self.block_four in self.block_lowest_list:
            if self.block_two[0] == self.block_four[0]:
                if self.block_two[1] == self.block_four[1] - 1:
                    self.block_lowest_list.remove(self.block_two)
                elif self.block_two[1] == self.block_four[1] + 1:
                    self.block_lowest_list.remove(self.block_four)
        if self.block_one in self.block_lowest_list and self.block_four in self.block_lowest_list:
            if self.block_one[0] == self.block_four[0]:
                if self.block_one[1] == self.block_four[1] - 1:
                    self.block_lowest_list.remove(self.block_one)
                elif self.block_one[1] == self.block_four[1] + 1:
                    self.block_lowest_list.remove(self.block_four)
        if self.block_one in self.block_lowest_list and self.block_three in self.block_lowest_list:
            if self.block_one[0] == self.block_three[0]:
                if self.block_one[1] == self.block_three[1] - 1:
                    self.block_lowest_list.remove(self.block_one)
                if self.block_one[1] == self.block_three[1] + 1:
                    self.block_lowest_list.remove(self.block_three)
            # Creates lowest_list, which stores blocks not obstructed vertically i.e. needs to be check_t_grided.
                    # Removes the blocks that are obstructed by block to on top

        # Leftest list
        if self.block_one in self.block_leftest_list and self.block_two in self.block_leftest_list:
            if self.block_one[1] == self.block_two[1]:
                if self.block_one[0] == self.block_two[0] + 1:
                    self.block_leftest_list.remove(self.block_one)
                elif self.block_one[0] == self.block_two[0] - 1:
                    self.block_leftest_list.remove(self.block_two)
        if self.block_two in self.block_leftest_list and self.block_three in self.block_leftest_list:
            if self.block_two[1] == self.block_three[1]:
                if self.block_two[0] == self.block_three[0] + 1:
                    self.block_leftest_list.remove(self.block_two)
                elif self.block_two[0] == self.block_three[0] - 1:
                    self.block_leftest_list.remove(self.block_three)
        if self.block_three in self.block_leftest_list and self.block_four in self.block_leftest_list:
            if self.block_three[1] == self.block_four[1]:
                if self.block_three[0] == self.block_four[0] + 1:
                    self.block_leftest_list.remove(self.block_three)
                elif self.block_three[0] == self.block_four[0] - 1:
                    self.block_leftest_list.remove(self.block_four)
        if self.block_two in self.block_leftest_list and self.block_four in self.block_leftest_list:
            if self.block_two[1] == self.block_four[1]:
                if self.block_two[0] == self.block_four[0] + 1:
                    self.block_leftest_list.remove(self.block_two)
                elif self.block_two[0] == self.block_four[0] - 1:
                    self.block_leftest_list.remove(self.block_four)
        if self.block_one in self.block_leftest_list and self.block_four in self.block_leftest_list:
            if self.block_one[1] == self.block_four[1]:
                if self.block_one[0] == self.block_four[0] + 1:
                    self.block_leftest_list.remove(self.block_one)
                elif self.block_one[0] == self.block_four[0] - 1:
                    self.block_leftest_list.remove(self.block_four)
        if self.block_one in self.block_leftest_list and self.block_three in self.block_leftest_list:
            if self.block_one[1] == self.block_three[1]:
                if self.block_one[0] == self.block_three[0] + 1:
                    self.block_leftest_list.remove(self.block_one)
                if self.block_one[0] == self.block_three[0] - 1:
                    self.block_leftest_list.remove(self.block_three)
                    # Creates leftest list, which stores blocks not obstructed horizontally i.e. needs to be check_t_grided.
                    # Removes the blocks that are obstructed by block to left
        # Rightest list
        if self.block_one in self.block_rightest_list and self.block_two in self.block_rightest_list:
            if self.block_one[1] == self.block_two[1]:
                if self.block_one[0] == self.block_two[0] - 1:
                    self.block_rightest_list.remove(self.block_one)
                elif self.block_one[0] == self.block_two[0] + 1:
                    self.block_rightest_list.remove(self.block_two)
        if self.block_two in self.block_rightest_list and self.block_three in self.block_rightest_list:
            if self.block_two[1] == self.block_three[1]:
                if self.block_two[0] == self.block_three[0] - 1:
                    self.block_rightest_list.remove(self.block_two)
                elif self.block_two[0] == self.block_three[0] + 1:
                    self.block_rightest_list.remove(self.block_three)
        if self.block_three in self.block_rightest_list and self.block_four in self.block_rightest_list:
            if self.block_three[1] == self.block_four[1]:
                if self.block_three[0] == self.block_four[0] - 1:
                    self.block_rightest_list.remove(self.block_three)
                elif self.block_three[0] == self.block_four[0] + 1:
                    self.block_rightest_list.remove(self.block_four)
        if self.block_two in self.block_rightest_list and self.block_four in self.block_rightest_list:
            if self.block_two[1] == self.block_four[1]:
                if self.block_two[0] == self.block_four[0] - 1:
                    self.block_rightest_list.remove(self.block_two)
                elif self.block_two[0] == self.block_four[0] + 1:
                    self.block_rightest_list.remove(self.block_four)
        if self.block_one in self.block_rightest_list and self.block_four in self.block_rightest_list:
            if self.block_one[1] == self.block_four[1]:
                if self.block_one[0] == self.block_four[0] - 1:
                    self.block_rightest_list.remove(self.block_one)
                elif self.block_one[0] == self.block_four[0] + 1:
                    self.block_rightest_list.remove(self.block_four)
        if self.block_one in self.block_rightest_list and self.block_three in self.block_rightest_list:
            if self.block_one[1] == self.block_three[1]:
                if self.block_one[0] == self.block_three[0] - 1:
                    self.block_rightest_list.remove(self.block_one)
                if self.block_one[0] == self.block_three[0] + 1:
                    self.block_rightest_list.remove(self.block_three)
                    # Creates righest list, which stores blocks not obstructed horizontally i.e. needs to be check_t_grided.
                    # Removes the blocks that are obstructed by block to right
        self.block_lowest = 0
        self.block_rightest = 0
        self.block_leftest = 0
        # Clears out the lowest/rightest/leftest block so that it can then be assigned using the most extremes in the respective lists
        self.block_lowest = self.block_lowest_list[0]
        self.block_rightest = self.block_rightest_list[0]
        self.block_leftest = self.block_leftest_list[0]
        for self.block_lowest_counter in range(len(self.block_lowest_list)):
            if self.block_lowest_list[self.block_lowest_counter][0] > self.block_lowest[1]:
                self.block_lowest = self.block_lowest_list[self.block_lowest_counter]
        for self.block_rightest_counter in range(len(self.block_rightest_list)):
            if self.block_rightest_list[self.block_rightest_counter][0] > self.block_rightest[0]:
                self.block_rightest = self.block_rightest_list[self.block_rightest_counter]
        for self.block_leftest_counter in range(len(self.block_leftest_list)):
            if self.block_leftest_list[self.block_leftest_counter][0] < self.block_leftest[0]:
                self.block_leftest = self.block_leftest_list[self.block_leftest_counter]
        #print("midlowest block", self.block_lowest_list)
        #print("midrightest block", self.block_rightest_list)
        #print("midleftest block", self.block_leftest)
        #print("midblock list", self.block_list)



    def check_t_grid_down(self):
        self.countercheckdown = 0
        self.countcheckdown = 0
        self.valid_blocks = 0
        self.valid_block_move = False
        if self.block_lowest[1] == 19:
            return "Reached bottom"  # Checks if the block has reached the bottom
        elif self.block_lowest[1] < 19:
            # If block hasn't reached bottom, check if the block below current is a part of itself
            for self.countercheckdown in range(len(self.block_lowest_list)):
                if TGrid[(self.block_lowest_list[self.countercheckdown])[0]][(self.block_lowest_list[self.countercheckdown])[1] + 1] != 0:
                    for self.countcheckdown in range(3):
                        if str((self.block_lowest_list[self.countercheckdown])[0]) + str((self.block_lowest_list[self.countercheckdown])[1] + 1) == str(self.block_list[self.countcheckdown][0]) + str(self.block_list[self.countcheckdown][1]):
                            # If the block is part of itself, the block is free to move
                            self.valid_blocks += 1
                else:
                    self.valid_blocks += 1
            if self.valid_blocks == len(self.block_lowest_list):
                self.valid_block_move = True
                return self.valid_block_move


    def check_t_grid_left(self):
        self.countercheckleft = 0
        self.countcheckleft = 0
        self.valid_blocks_left = 0
        self.valid_block_move = False
        if self.block_leftest[0] == 0:
            return "Reached left"  # Checks if the block has reached the left
        if self.block_leftest[0] > 0:
        # If block hasn't reached leftest, check if the block to the left of current is a part of itself
            for self.countercheckleft in range(len(self.block_leftest_list)):
                if TGrid[(self.block_leftest_list[self.countercheckleft])[0] - 1][(self.block_leftest_list[self.countercheckleft])[1]] != 0:
                    for self.countcheckleft in range(3):
                        if str((self.block_leftest_list[self.countercheckleft])[0] - 1) + str(
                                (self.block_leftest_list[self.countercheckleft])[1]) == str(
                                self.block_list[self.countcheckleft][0]) + str(self.block_list[self.countcheckleft][1]):
                            # If the block is part of itself, the block is free to move
                            self.valid_blocks_left += 1
                else:
                    self.valid_blocks_left += 1
            if self.valid_blocks_left == len(self.block_leftest_list):
                self.valid_block_move = True
                return self.valid_block_move

    def check_t_grid_right(self):
        self.countercheckright = 0
        self.countcheckright = 0
        self.valid_blocks_right = 0
        self.valid_block_move = False
        if self.block_rightest[0] == 9:
            return "Reached right"  # Checks if the block has reached the right
        if self.block_rightest[0] < 9:
            for self.countercheckright in range(len(self.block_rightest_list)):
                if TGrid[(self.block_rightest_list[self.countercheckright])[0] + 1][
                    (self.block_rightest_list[self.countercheckright])[1]] != 0:
                    for self.countcheckright in range(3):
                        if str((self.block_rightest_list[self.countercheckright])[0] + 1) + str(
                                (self.block_rightest_list[self.countercheckright])[1]) == str(
                            self.block_list[self.countcheckright][0]) + str(
                            self.block_list[self.countcheckright][1]):
                            # If the block is part of itself, the block is free to move
                            self.valid_blocks_right += 1
                else:
                    self.valid_blocks_right += 1
            if self.valid_blocks_right == len(self.block_rightest_list):
                self.valid_block_move = True
                return self.valid_block_move

    def move_t_grid_down(self):  # Previous space occupied by block cleared and moved into next space below
        self.block_list = list(self.block_list_temp)
        self.row += 1
        print(self.block_list)
        for self.countermovedown in range(4):
            TGrid[((self.block_list[self.countermovedown])[0])][(self.block_list[self.countermovedown])[1]] = 0
        for self.countmovedown in range(4):
            (self.block_list[self.countmovedown])[1] = (self.block_list[self.countmovedown])[1] + 1  # Update the moved blocks once moved
            TGrid[((self.block_list[self.countmovedown])[0])][(self.block_list[self.countmovedown])[1]] = BlockColour[self.block_colour]
        # print("Block pos after moving down:", self.block_list)

    def move_t_grid_left(self):  # Previous space occupied by block cleared and moved into next left space
        self.block_list = list(self.block_list_temp)
        self.column -= 1
        for self.countermoveleft in range(4):
            TGrid[((self.block_list[self.countermoveleft])[0])][(self.block_list[self.countermoveleft])[1]] = 0
        for self.countmoveleft in range(4):
            (self.block_list[self.countmoveleft])[0] = (self.block_list[self.countmoveleft])[0] - 1  # Update the moved blocks once moved
            TGrid[((self.block_list[self.countmoveleft])[0])][(self.block_list[self.countmoveleft])[1]] = BlockColour[self.block_colour]
        # print("Block pos after moving left:", self.block_list)

    def move_t_grid_right(self):   # Previous space occupied by block cleared and moved into next right space
        self.block_list = list(self.block_list_temp)
        self.column += 1
        for self.countermoveright in range(4):
            TGrid[((self.block_list[self.countermoveright])[0])][(self.block_list[self.countermoveright])[1]] = 0
        for self.countmoveright in range(4):
            (self.block_list[self.countmoveright])[0] = (self.block_list[self.countmoveright])[0] + 1  # Update the moved blocks once moved
            TGrid[((self.block_list[self.countmoveright])[0])][(self.block_list[self.countmoveright])[1]] = BlockColour[self.block_colour]
        # print("Block pos after moving right:", self.block_list)

    def check_rotate_valid(self):
        if self.block_lowest[1] > 19:
            return False
        elif self.block_rightest[0] > 9:
            return False
        elif self.block_leftest[0] < 0:
            return False
        else:
            return True

    def rotate(self):
        TGrid[self.block_one[0]][self.block_one[1]] = 0
        TGrid[self.block_two[0]][self.block_two[1]] = 0
        TGrid[self.block_three[0]][self.block_three[1]] = 0
        TGrid[self.block_four[0]][self.block_four[1]] = 0
        self.block_one_rotated = False
        self.block_two_rotated = False
        self.block_three_rotated = False
        self.block_four_rotated = False
        self.block_one_prerotate = self.block_one[:]
        self.block_two_prerotate = self.block_two[:]
        self.block_three_prerotate = self.block_three[:]
        self.block_four_prerotate = self.block_four[:]
        self.block_dimensions_prerotate = self.block_dimensions[:]
        self.block_lowest_prerotate = self.block_lowest[:]
        self.block_rightest_prerotate = self.block_rightest[:]
        self.block_leftest_prerotate = self.block_leftest[:]

        # Stores a copy of the blocks before the rotation has taken place
        self.block_dimensions = self.block_dimensions.transpose()
        self.block_dimensions = numpy.fliplr(self.block_dimensions)
        # print("prelowest block", self.block_lowest)
        # print("prerightest block", self.block_rightest)
        # print("preleftest block", self.block_leftest)
        # print("preblock list", self.block_list)
        # print("----------------------------")
        # print("LOOOK ATTT THISSSS", self.block_dimensions)
        # print("----------------------------")
        self.block_dimensions_temp = self.block_dimensions[:]
        for self.block_position, self.block_itself in numpy.ndenumerate(self.block_dimensions):
            print("blockpos: ", self.block_position, "                    ", "block_itself: ", self.block_itself)
        print(len(self.block_dimensions))
        for self.block_position, self.block_itself in numpy.ndenumerate(self.block_dimensions_temp):
            print("blockpos: ", self.block_position, "                    ", "block_itself: ", self.block_itself)
        for self.block_position, self.block_itself in numpy.ndenumerate(self.block_dimensions_temp):
            if self.block_itself == self.block_one and not self.block_one_rotated:
                print("before b1", self.block_one, self.block_position)
                self.block_one_rotated = True
                self.block_one[1] = self.row + self.block_position[0]
                self.block_one[0] = self.column + self.block_position[1]
                print("after", self.block_one)
                for self.block_position, self.block_itself in numpy.ndenumerate(self.block_dimensions_temp):
                    print("blockpos: ", self.block_position, "                    ", "block_itself: ",
                          self.block_itself)

            if self.block_itself == self.block_two and not self.block_two_rotated:
                print("before b2", self.block_two, self.block_position)
                self.block_two_rotated = True
                self.block_two[1] = self.row + self.block_position[0]
                self.block_two[0] = self.column + self.block_position[1]
                print("after", self.block_two)
                for self.block_position, self.block_itself in numpy.ndenumerate(self.block_dimensions_temp):
                    print("blockpos: ", self.block_position, "                    ", "block_itself: ",
                          self.block_itself)

            if self.block_itself == self.block_three and not self.block_three_rotated:
                print("before b3", self.block_three, self.block_position)
                self.block_three_rotated = True
                self.block_three[1] = self.row + self.block_position[0]
                self.block_three[0] = self.column + self.block_position[1]
                print("after", self.block_three)
                for self.block_position, self.block_itself in numpy.ndenumerate(self.block_dimensions_temp):
                    print("blockpos: ", self.block_position, "                    ", "block_itself: ",
                          self.block_itself)

            if self.block_itself == self.block_four and not self.block_four_rotated:
                print("before b4", self.block_four, self.block_position)
                self.block_four_rotated = True
                self.block_four[1] = self.row + self.block_position[0]
                self.block_four[0] = self.column + self.block_position[1]
                print("after", self.block_four)
                for self.block_position, self.block_itself in numpy.ndenumerate(self.block_dimensions_temp):
                    print("blockpos: ", self.block_position, "                    ", "block_itself: ",
                          self.block_itself)

                    #print("Block config after rotating :", self.block_list)
        self.block_list = [self.block_one, self.block_two, self.block_three, self.block_four]
        self.block_list_temp = list(self.block_list)
        print("rotated", self.block_list)
        # Extremeties was here
        self.update_block_setup()
        if self.check_rotate_valid():
            print("lowest block", self.block_lowest)
            print("rightest block", self.block_rightest)
            print("leftest block", self.block_leftest)
            print("block list", self.block_list)
        else:
            self.block_one = self.block_one_prerotate
            self.block_two = self.block_two_prerotate
            self.block_three = self.block_three_prerotate
            self.block_four = self.block_four_prerotate
            print("-----------------------", self.block_dimensions_prerotate,"-----------------",self.block_dimensions,"---------------------")
            self.block_dimensions = self.block_dimensions_prerotate
            self.update_block_setup()
        TGrid[self.block_one[0]][self.block_one[1]] = self.BlockColour
        TGrid[self.block_two[0]][self.block_two[1]] = self.BlockColour
        TGrid[self.block_three[0]][self.block_three[1]] = self.BlockColour
        TGrid[self.block_four[0]][self.block_four[1]] = self.BlockColour

    def show_block_list(self, x_or_y, which_block):
        return self.block_list[which_block][x_or_y]
            
    def block_list_length(self):
        return len(self.block_list)

    def reset_valid(self):
        # if true valid move is reset
        self.valid_block_move = True


class IBlockBlock(BlockBlock):
    def __init__(self, column, row, colour):
        super(IBlockBlock, self).__init__(column, row, colour)

    # Initial positioning of the chosen tetris blocks in the grid
    def store_block(self):
        self.block_one = [5, 0, BlockColour[IBlock]]
        self.block_two = [5, 1, BlockColour[IBlock]]
        self.block_three = [5, 2, BlockColour[IBlock]]
        self.block_four = [5, 3, BlockColour[IBlock]]  # Assigns the respective blocks to four separate lists
        self.block_list = [self.block_one, self.block_two, self.block_three, self.block_four]
        self.block_lowest = self.block_four  # Initializing the extremities of the block
        self.block_rightest = self.block_one
        self.block_leftest = self.block_one
        self.BlockColour = BlockColour[IBlock]
        self.block_rightest_list.append(self.block_one)
        self.block_leftest_list.append(self.block_one)
        self.column = self.block_three[0]
        self.row = self.block_three[1]
        self.block_matrix = [[0, self.block_one, 0], [0, self.block_two, 0], [0, self.block_three, 0], [0, self.block_four, 0]]  # Assigns the block_matrix to store this specific block shape
        self.block_dimensions = numpy.array(self.block_matrix)  # Stores the block shape as an array
        TGrid[5][0] = BlockColour[IBlock]
        TGrid[5][1] = BlockColour[IBlock]
        TGrid[5][2] = BlockColour[IBlock]
        TGrid[5][3] = BlockColour[IBlock]  # Block initialized by placing it onto the grid in its initial orientation


class JBlockBlock(BlockBlock):
    def __init__(self, column, row, colour):
        super(JBlockBlock, self).__init__(column, row, colour)

    def store_block(self):
        self.block_one = [6, 0, BlockColour[JBlock]]
        self.block_two = [6, 1, BlockColour[JBlock]]
        self.block_three = [6, 2, BlockColour[JBlock]]
        self.block_four = [5, 2, BlockColour[JBlock]]  # Assigns the respective blocks to four separate lists
        self.block_list = [self.block_one, self.block_two, self.block_three, self.block_four]
        self.block_lowest = self.block_three  # Initializing the extremities of the block
        self.block_rightest = self.block_one
        self.block_leftest = self.block_four
        self.BlockColour = BlockColour[JBlock]
        self.block_rightest_list.append(self.block_one)
        self.block_leftest_list.append(self.block_one)
        self.column = self.block_two[0]
        self.row = self.block_two[1]
        self.block_matrix = [[0, self.block_one], [0, self.block_two], [self.block_four, self.block_three]]  # Assigns the block_matrix to store this specific block shape
        self.block_dimensions = numpy.array(self.block_matrix)  # Stores the block shape as an array
        TGrid[6][0] = BlockColour[JBlock]
        TGrid[6][1] = BlockColour[JBlock]
        TGrid[6][2] = BlockColour[JBlock]
        TGrid[5][2] = BlockColour[JBlock]


class LBlockBlock(BlockBlock):
    def __init__(self, column, row, colour):
        super(LBlockBlock, self).__init__(column, row, colour)

    def store_block(self):
        self.block_one = [5, 0, BlockColour[LBlock]]
        self.block_two = [5, 1, BlockColour[LBlock]]
        self.block_three = [5, 2, BlockColour[LBlock]]
        self.block_four = [6, 2, BlockColour[LBlock]]  # Assigns the respective blocks to four separate lists
        self.block_list = [self.block_one, self.block_two, self.block_three, self.block_four]
        self.block_lowest = self.block_four  # Initializing the extremities of the block
        self.block_rightest = self.block_four
        self.block_leftest = self.block_one
        self.BlockColour = BlockColour[LBlock]
        self.block_rightest_list.append(self.block_one)
        self.block_leftest_list.append(self.block_one)
        self.column = self.block_two[0]
        self.row = self.block_two[1]
        self.block_matrix = [[self.block_one, 0], [self.block_two, 0], [self.block_three, self.block_four]]  # Assigns the block_matrix to store this specific block shape
        self.block_dimensions = numpy.array(self.block_matrix)  # Stores the block shape as an array
        TGrid[5][0] = BlockColour[LBlock]
        TGrid[5][1] = BlockColour[LBlock]
        TGrid[5][2] = BlockColour[LBlock]
        TGrid[6][2] = BlockColour[LBlock]


class OBlockBlock(BlockBlock):
    def __init__(self, column, row, colour):
        super(OBlockBlock, self).__init__(column, row, colour)

    def store_block(self):
        self.column = 5
        self.row = 0
        self.block_one = [5, 0, BlockColour[OBlock]]
        self.block_two = [6, 0, BlockColour[OBlock]]
        self.block_three = [5, 1, BlockColour[OBlock]]
        self.block_four = [6, 1, BlockColour[OBlock]]  # Assigns the respective blocks to four separate lists
        self.block_list = [self.block_one, self.block_two, self.block_three, self.block_four]
        self.block_lowest = self.block_four  # Initializing the extremities of the block
        self.block_rightest = self.block_two
        self.block_leftest = self.block_one
        self.BlockColour = BlockColour[OBlock]
        self.block_rightest_list.append(self.block_one)
        self.block_leftest_list.append(self.block_one)
        self.block_matrix = [[self.block_one, self.block_two], [self.block_three, self.block_four]]  # Assigns the block_matrix to store this specific block shape
        self.block_dimensions = numpy.array(self.block_matrix)  # Stores the block shape as an array
        TGrid[5][0] = BlockColour[OBlock]
        TGrid[6][0] = BlockColour[OBlock]
        TGrid[5][1] = BlockColour[OBlock]
        TGrid[6][1] = BlockColour[OBlock]


class TBlockBlock(BlockBlock):
    def __init__(self, column, row, colour):
        super(TBlockBlock, self).__init__(column, row, colour)

    def store_block(self):
        self.block_one = [5, 0, BlockColour[TBlock]]
        self.block_two = [6, 0, BlockColour[TBlock]]
        self.block_three = [7, 0, BlockColour[TBlock]]
        self.block_four = [6, 1, BlockColour[TBlock]]  # Assigns the respective blocks to four separate lists
        self.block_list = [self.block_one, self.block_two, self.block_three, self.block_four]
        self.block_lowest = self.block_four  # Initializing the extremities of the block
        self.block_rightest = self.block_three
        self.block_leftest = self.block_one
        self.BlockColour = BlockColour[TBlock]
        self.block_rightest_list.append(self.block_one)
        self.block_leftest_list.append(self.block_one)
        self.column = self.block_two[0]
        self.row = self.block_two[1]
        self.block_matrix = [[self.block_one, self.block_two, self.block_three], [0, self.block_four, 0]]  # Assigns the block_matrix to store this specific block shape
        self.block_dimensions = numpy.array(self.block_matrix)  # Stores the block shape as an array
        TGrid[5][0] = BlockColour[TBlock]
        TGrid[6][0] = BlockColour[TBlock]
        TGrid[7][0] = BlockColour[TBlock]
        TGrid[6][1] = BlockColour[TBlock]


class SBlockBlock(BlockBlock):
    def __init__(self, column, row, colour):
        super(SBlockBlock, self).__init__(column, row, colour)

    def store_block(self):
        self.block_one = [5, 0, BlockColour[SBlock]]
        self.block_two = [6, 0, BlockColour[SBlock]]
        self.block_three = [5, 1, BlockColour[SBlock]]
        self.block_four = [4, 1, BlockColour[SBlock]]  # Assigns the respective blocks to four separate lists
        self.block_list = [self.block_one, self.block_two, self.block_three, self.block_four]
        self.block_lowest = self.block_four  # Initializing the extremities of the block
        self.block_rightest = self.block_two
        self.block_leftest = self.block_four
        self.BlockColour = BlockColour[SBlock]
        self.block_rightest_list.append(self.block_one)
        self.block_leftest_list.append(self.block_one)
        self.column = self.block_three[0]
        self.row = self.block_three[1]
        self.block_matrix = [[0, self.block_one, self.block_two], [self.block_four, self.block_three, 0]]  # Assigns the block_matrix to store this specific block shape
        self.block_dimensions = numpy.array(self.block_matrix)  # Stores the block shape as an array
        TGrid[5][0] = BlockColour[SBlock]
        TGrid[6][0] = BlockColour[SBlock]
        TGrid[5][1] = BlockColour[SBlock]
        TGrid[4][1] = BlockColour[SBlock]


class ZBlockBlock(BlockBlock):
    def __init__(self, column, row, colour):
        super(ZBlockBlock, self).__init__(column, row, colour)

    def store_block(self):
        self.block_one = [5, 0, BlockColour[ZBlock]]
        self.block_two = [6, 0, BlockColour[ZBlock]]
        self.block_three = [6, 1, BlockColour[ZBlock]]
        self.block_four = [7, 1, BlockColour[ZBlock]]  # Assigns the respective blocks to four separate lists
        self.block_list = [self.block_one, self.block_two, self.block_three, self.block_four]
        self.block_lowest = self.block_four  # Initializing the extremities of the block
        self.block_rightest = self.block_four
        self.block_leftest = self.block_one
        self.BlockColour = BlockColour[ZBlock]
        self.block_rightest_list.append(self.block_one)
        self.block_leftest_list.append(self.block_one)
        self.column = self.block_two[0]
        self.row = self.block_two[1]
        self.block_matrix = [[self.block_one, self.block_two, 0], [0, self.block_three, self.block_four]]  # Assigns the block_matrix to store this specific block shape
        self.block_dimensions = numpy.array(self.block_matrix)  # Stores the block shape as an array
        TGrid[5][0] = BlockColour[ZBlock]
        TGrid[6][0] = BlockColour[ZBlock]
        TGrid[6][1] = BlockColour[ZBlock]
        TGrid[7][1] = BlockColour[ZBlock]


# Drawing the tetris boxes


def draw_t_box():
    global TColumn
    global TRow
    # Drawing tetris board
    for TColumn in range(10):
        column_pos = (TColumn + 0.3) * column_spacing
        for TRow in range(20):
            row_pos = (TRow + 1.25) * row_spacing
            if TGrid[TColumn][TRow] == GREEN:
                pygame.draw.rect(screen, GREEN, [column_pos, row_pos, 34, 34])
            elif TGrid[TColumn][TRow] == BLUE:
                pygame.draw.rect(screen, BLUE, [column_pos, row_pos, 34, 34])
            elif TGrid[TColumn][TRow] == YELLOW:
                pygame.draw.rect(screen, YELLOW, [column_pos, row_pos, 34, 34])
            elif TGrid[TColumn][TRow] == BROWN:
                pygame.draw.rect(screen, BROWN, [column_pos, row_pos, 34, 34])
            elif TGrid[TColumn][TRow] == PURPLE:
                pygame.draw.rect(screen, PURPLE, [column_pos, row_pos, 34, 34])
            elif TGrid[TColumn][TRow] == RED:
                pygame.draw.rect(screen, RED, [column_pos, row_pos, 34, 34])
            elif TGrid[TColumn][TRow] == ORANGE:
                pygame.draw.rect(screen, ORANGE, [column_pos, row_pos, 34, 34])
            elif TGrid[TColumn][TRow] == 0:
                pygame.draw.rect(screen, WHITE, [column_pos, row_pos, 34, 34])


# Placing the next block in queue on the grid
def place_next_block():
    global next_block_store
    if next_block_store != 1:
        if next_block_store == 0:
            # Condition to only store the latest killed block when there is no block queued
            BlockChosen = Mob.Block_Choice
        else:  # If there is a block queued, assign it as the next block to be placed on the grid
            BlockChosen = next_block_store
        if BlockChosen == IBlock:
            BlockObject = IBlockBlock(0, 0, IBlock)
        elif BlockChosen == JBlock:
            BlockObject = JBlockBlock(0, 0, JBlock)
        elif BlockChosen == LBlock:
            BlockObject = LBlockBlock(0, 0, LBlock)
        elif BlockChosen == OBlock:
            BlockObject = OBlockBlock(0, 0, OBlock)
        elif BlockChosen == TBlock:
            BlockObject = TBlockBlock(0, 0, TBlock)
        elif BlockChosen == SBlock:
            BlockObject = SBlockBlock(0, 0, SBlock)
        elif BlockChosen == ZBlock:
            BlockObject = ZBlockBlock(0, 0, ZBlock)
        if finished_moving:
            BlockObject.store_block()
            active_block.empty()
            active_block.add(BlockObject)  # Stores the current block that will be moving
            onscreen_blocks.add(BlockObject)  # Stores the current block into the list of blocks onscreen
            BlockObject.update_block_setup()
            next_block_store = 1  # Marks that the block store is empty
        else:
            next_block_store = BlockChosen


def shift_block():
    global finished_moving
    global not_clear
    for BlockObject in active_block:
        if BlockObject.check_t_grid_down() == "Reached bottom" or BlockObject.check_t_grid_down() != True:
            print("Not free")
            active_block.remove(BlockObject)
            # Block is quick dropped to the bottom of the available space in grid.
            finished_moving = True
            if not quick_drop and not check_clear_place():  # Only inserts the next block on the grid if quick drop does not take place
                print(check_clear_place())
                not_clear = False
                place_next_block()
        elif BlockObject.check_t_grid_down():
            # print("Free")
            finished_moving = False
            BlockObject.move_t_grid_down()  # Block is moved down the grid by one for the current cycle
        BlockObject.reset_valid()

# def fall_block():
#  global finished_moving
 #   for BlockObject in onscreen_blocks:
  #      if BlockObject.check_t_grid_down():
   #         BlockObject.move_t_grid_down()  # Block is moved down the grid by one for the current cycle
    #    BlockObject.reset_valid()

def check_clear_place():
    global not_clear
    not_clear = False
    for xpos in range(4, 7):
        for ypos in range(0, 2):
            if TGrid[xpos][ypos] != 0:
                not_clear = True
                # print("not clear", xpos, ypos)
    return not_clear
                # CONTINUE THIS CODE TO CHECK SPAWN AREA IS NOT OCCUPIED


def wipe_grid():
    for ypos in range(19):
        complete_row = True
        for xpos in range(10):
            # Searches through each row of the grid and checks if the row is filled
            if TGrid[xpos][ypos + 1] == 0:
                complete_row = False
        if complete_row:
            # Store the blocks involved in that row
            # Compute what happens to each block
            for BlockObject in onscreen_blocks:
                for BlockListCounter in range(BlockObject.block_list_length()):
                    if xpos == BlockObject.show_block_list(0, BlockListCounter) and ypos == BlockObject.show_block_list(1, BlockListCounter):
                        if BlockObject.check_t_grid_down():
                            BlockObject.move_t_grid_down()  # Block is moved down the grid by one for the current cycle
            # for xpos in range(10):
            #    TGrid[xpos][ypos + 1] = 0
            #    temp_block_store = TGrid[xpos][ypos]
            #    TGrid[xpos][ypos + 1] = temp_block_store
            #    TGrid[xpos][ypos] = 0
 #   fall_block()

# Types of enemies
# I Block


class IBlock(Enemy):
    def __init__(self, mob_health, block_choice):
        super(IBlock, self).__init__(mob_health, block_choice)
        self.image = pygame.Surface([30, 120])
        picture = pygame.image.load("IBlock.png")
        self.image = pygame.transform.smoothscale(picture, [30, 120])



# J Block

class JBlock(Enemy):
    def __init__(self, mob_health, block_choice):
        super(JBlock, self).__init__(mob_health, block_choice)
        self.image = pygame.Surface([60, 90])
        picture = pygame.image.load("JBlock.png")
        self.image = pygame.transform.smoothscale(picture, [60, 90])


# L Block


class LBlock(Enemy):
    def __init__(self, mob_health, block_choice):
        super(LBlock, self).__init__(mob_health, block_choice)
        self.image = pygame.Surface([60, 90])
        picture = pygame.image.load("LBlock.png")
        self.image = pygame.transform.scale(picture, [60, 90])

# O Block


class OBlock(Enemy):
    def __init__(self, mob_health, block_choice):
        super(OBlock, self).__init__(mob_health, block_choice)
        self.image = pygame.Surface([60, 60])
        picture = pygame.image.load("OBlock.png")
        self.image = pygame.transform.scale(picture, [60, 60])


# T Block


class TBlock(Enemy):
    def __init__(self, mob_health, block_choice):
        super(TBlock, self).__init__(mob_health, block_choice)
        picture = pygame.image.load("TBlock.png")
        self.image = pygame.transform.scale(picture, [90, 60])


# S Block


class SBlock(Enemy):
    def __init__(self, mob_health, block_choice):
        super(SBlock, self).__init__(mob_health, block_choice)
        self.image = pygame.Surface([60, 90])
        picture = pygame.image.load("SBlock.png")
        self.image = pygame.transform.scale(picture, [60, 90])


# Z Block


class ZBlock(Enemy):
    def __init__(self, mob_health, block_choice):
        super(ZBlock, self).__init__(mob_health, block_choice)
        self.image = pygame.Surface([60, 90])
        picture = pygame.image.load("ZBlock.png")
        self.image = pygame.transform.scale(picture, [60, 90])

# Randomly generates a new enemy at a random rate
pygame.time.set_timer(SpawnEnemy, TimeMobs)
# Moves the tetris blocks down one every 1.5 seconds
pygame.time.set_timer(MoveBlocks, 1500)
# Player and projectiles are updated/stored in sprite group
list_all_sprites = pygame.sprite.Group()
list_bullet = pygame.sprite.Group()
# Enemy are updated/stored in sprite group
list_mobs = pygame.sprite.Group()
# Current tetris block stored in sprite group
active_block = pygame.sprite.Group()
# All tetris blocks on the grid stored in sprite group
onscreen_blocks = pygame.sprite.Group()
# Player and bullet initialised
Pilot = Pilot()
list_all_sprites.add(Pilot)
# Initialise block types
BlockColour = {IBlock: GREEN, JBlock: BLUE, LBlock: YELLOW, OBlock: RED, TBlock: BROWN, SBlock: ORANGE, ZBlock: PURPLE}
# Loop until the user clicks the close button
done = False
# - - - - - - - - - Main program loop - - - - - - - - -
while not done:

    # - - - - - - - Main event loop - - - - - - - - - -
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("User asked to quit.")
            done = True  # Signals the program to end
        # Sets controls for the pilot
        elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                        pilot_y_speed = -10.5
        #                print("y position of the Pilot Character before moving", pilot_y)
                elif event.key == pygame.K_DOWN:
                        pilot_y_speed = 8
        #                print("y position of the Pilot Character before moving", pilot_y)
                elif event.key == pygame.K_LEFT:
                        pilot_x_speed = -8
        #                print("x position of the Pilot Character before moving", pilot_x)
                elif event.key == pygame.K_RIGHT:
                        pilot_x_speed = 8
        #                print("x position of the Pilot Character before moving", pilot_x)
                elif event.key == pygame.K_SPACE:
                    # Start shooting
                    pygame.time.set_timer(FireRate, TimeShot)

        # Tells the pilot to stop moving when key not pressed
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
        #        print("y position of the Pilot Character after moving", pilot_y)
                pilot_y_speed = 0
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
        #        print("x position of the Pilot Character after moving", pilot_x)
                pilot_x_speed = 0
            elif event.key == pygame.K_SPACE:
                Shot = Bullet()
                list_all_sprites.add(Shot)
                list_bullet.add(Shot)
                pygame.time.set_timer(FireRate, 0)
            elif event.key == pygame.K_q:
                quick_drop = True
                check_clear_place()
                for i in range(19):
                    shift_block()
                if not check_clear_place():
                    not_clear = True
                    place_next_block()
                quick_drop = False

            # Enemy block spawn shortcuts for easier debugging and playtesting
            elif event.key == pygame.K_i:
                BlockChoice = IBlock
                Mob = BlockChoice(4, BlockChoice)
                list_all_sprites.add(Mob)
                list_mobs.add(Mob)
                print(Mob)
            elif event.key == pygame.K_j:
                BlockChoice = JBlock
                Mob = BlockChoice(4, BlockChoice)
                list_all_sprites.add(Mob)
                list_mobs.add(Mob)
                print(Mob)
            elif event.key == pygame.K_l:
                BlockChoice = LBlock
                Mob = BlockChoice(4, BlockChoice)
                list_all_sprites.add(Mob)
                list_mobs.add(Mob)
                print(Mob)
            elif event.key == pygame.K_5:
                BlockChoice = SBlock
                Mob = BlockChoice(4, BlockChoice)
                list_all_sprites.add(Mob)
                list_mobs.add(Mob)
                print(Mob)
            elif event.key == pygame.K_z:
                BlockChoice = ZBlock
                Mob = BlockChoice(4, BlockChoice)
                list_all_sprites.add(Mob)
                list_mobs.add(Mob)
                print(Mob)
            elif event.key == pygame.K_t:
                BlockChoice = TBlock
                Mob = BlockChoice(4, BlockChoice)
                list_all_sprites.add(Mob)
                list_mobs.add(Mob)
                print(Mob)
            elif event.key == pygame.K_o:
                BlockChoice = OBlock
                Mob = BlockChoice(4, BlockChoice)
                list_all_sprites.add(Mob)
                list_mobs.add(Mob)
                print(Mob)


            elif event.key == pygame.K_a:
                if active_block:
                    for BlockObject in active_block:
                        if BlockObject.check_t_grid_left() and BlockObject.check_t_grid_left() != "Reached left":
                            BlockObject.move_t_grid_left()
                        else:
                            print("Stopped left")
                    BlockObject.reset_valid()
            elif event.key == pygame.K_d:
                if active_block:
                    for BlockObject in active_block:
                        if BlockObject.check_t_grid_right() and BlockObject.check_t_grid_right() != "Reached right":
                            BlockObject.move_t_grid_right()
                        else:
                            print("Stopped right")
                    BlockObject.reset_valid()
            elif event.key == pygame.K_s:
                if active_block:
                    for BlockObject in active_block:
                        if BlockObject.check_t_grid_down() and BlockObject.check_t_grid_down() != "Reached bottom":
                            BlockObject.move_t_grid_down()
                        else:
                            print("Reached bottom manually")
                    BlockObject.reset_valid()
            elif event.key == pygame.K_r:
                if active_block:
                    for BlockObject in active_block:
                        BlockObject.rotate()
        # The bullet continues to fire automatically
        elif event.type == FireRate:
            Shot = Bullet()
            list_all_sprites.add(Shot)
            list_bullet.add(Shot)
        # Mobs are spawned at random time intervals
        elif event.type == SpawnEnemy:
            BlockChoice = random.choice(list(BlockColour))
            Mob = BlockChoice(4, BlockChoice)
       #     print("position of the new Enemy spawned (", Mob.rect.x, ", ", Mob.rect.y, ")")
            list_all_sprites.add(Mob)
            list_mobs.add(Mob)
        # The pilot flashes red when it is hit
        elif event.type == PilotHit:
            if flickercount > 0:
                Pilot.image.fill(RED)
                enemy_speed_change -= 0.2
        # The time period for changing back to white is 500ms a.k.a half the time period of flickering pilot to red
                pygame.time.set_timer(PilotHitRecover, 500)
            else:
                pygame.time.set_timer(PilotHit, 0)
            # Recolours the pilot to white once flicker cycle is over
                Pilot.image.fill(WHITE)
                flickercount = 3
        elif event.type == PilotHitRecover:
            flickercount -= 1
        # Changed the flicker output so it only returns flicker when it is still in the flick cycle
            pygame.time.set_timer(PilotHitRecover, 0)
            if flickercount > 0:
                Pilot.image.fill(WHITE)
            else:
                Pilot_flickering = False
        elif event.type == MoveBlocks:
            if finished_moving:
                wipe_grid()
            shift_block()
            # for BlockObject in active_block:
                # BlockObject.pos()

    # - - - - - Game logic - - - - - - - -
    pilot_x += pilot_x_speed
    pilot_y += pilot_y_speed + gravity
    # Setting up the wall boundaries for the pilot
    if pilot_x > 997 and pilot_y > 741:
        pilot_x = 997
        pilot_y = 741
    elif pilot_x < 390 and pilot_y < 2:
        pilot_x = 390
        pilot_y = 2
    elif pilot_x > 997:
        pilot_x = 997
        if pilot_y < 2:
            pilot_y = 2
    elif pilot_x < 390:
        pilot_x = 390
        if pilot_y > 741:
            pilot_y = 741
    elif pilot_y > 741:
        pilot_y = 741
    elif pilot_y < 2:
        pilot_y = 2

    list_all_sprites.update()

    # - - - - - Drawing code - - - - - - -
    pygame.draw.rect(screen, BLACK, [0, 0, 384, 768], 0)
    pygame.draw.rect(screen, BLACK, [384, 0, 640, 768], 0)
    pygame.draw.rect(screen, WHITE, [384, 0, 640, 768], 1)
    pygame.draw.line(screen, GREEN, (384, 0), (384, 768), 8)

    # Scoring
    drawing("Score:", 16, WHITE, 860, 20)
    drawing(TotScore, 16, WHITE, 980, 20)

    # Display health
    show_health()

    # Removes off-screen mobs
    for Mob in list_mobs:
        if Mob.rect.x <= 364 or Mob.rect.y >= 740 or Mob.rect.y <= 20:
            list_all_sprites.remove(Mob)
            list_mobs.remove(Mob)

    # Removes off-screen projectiles
    for Shot in list_bullet:
        if Shot.rect.x >= pilot_x + 400 or Shot.rect.y >= 768:
            list_all_sprites.remove(Shot)
            list_bullet.remove(Shot)
        # Hit detection between bullet and Mob
        list_mobs_hit = pygame.sprite.spritecollide(Shot, list_mobs, False)
        # Score from hitting mobs
        for Mob in list_mobs_hit:
            TotScore += HitScore
            Mob.Mob_Health -= 1
            if Mob.Mob_Health == 0:
                next_block_store = 0
                #print("check clear place", check_clear_place())
                not_clear = False
                if not check_clear_place():
                    place_next_block()
                    not_clear = False
                #  BlockObject.pos()  # For printing the top left corner block of the tetris block
                list_mobs.remove(Mob)
                list_all_sprites.remove(Mob)
                list_mobs_hit.remove(Mob)
                mob_got_killed = True
                # Increase game scroll speed when enemy killed: difficulty progression
                enemy_speed_change += 0.1
                if ShortTimeMobs > 500:
                    ShortTimeMobs -= 30
                    LongTimeMobs -= 30
                TotScore += MobScore

    # Removing the projectiles if they land on an enemy
    for Mob in list_mobs:
        list_shots_landed = pygame.sprite.spritecollide(Mob, list_bullet, True)
        for Shot in list_shots_landed:
            list_all_sprites.remove(Shot)
            list_bullet.remove(Shot)
        MobHealthPercent = (Mob.Mob_Health/4)
        pygame.draw.line(screen, RED, (Mob.rect.left, Mob.rect.bottom + 10), (Mob.rect.left + Mob.x_hitbox * MobHealthPercent, Mob.rect.bottom + 10), 4)

    draw_t_box()

    list_all_sprites.draw(screen)

    # - - - - - Update screen drawn - - -
    pygame.display.flip()

    # - - - - - Set the fps - - - - - - -
    clock.tick(60)

# Shutdown python program
pygame.quit()