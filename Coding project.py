# Import the libraries for pygame, math functions
# used for enemy AI and random for generating behaviours
import pygame
import math
import random

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Initialise the game engine
pygame.init()

# Initialise variables
pilot_x = 400
pilot_y = 384
pilot_x_speed = 0
pilot_y_speed = 0
gravity = 2.5
validx = True
validy = True
# Setting up the screen
size = (1024, 768)
screen = pygame.display.set_mode(size)
# Labelling the program
pygame.display.set_caption("Game name here")

# To manage the fps
clock = pygame.time.Clock()

# Game classes

# Setting up pilot sprite
class Pilot(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([10, 10])
        # Creates the image of the pilot
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x = pilot_x
        self.rect.y = pilot_y

list_all_sprites = pygame.sprite.Group()
Pilot = Pilot()
list_all_sprites.add(Pilot)
# Loop until the user clicks the close button
done = False
# - - - - - - - - - Main program loop - - - - - - - - -
while not done:
    # - - - - - - - Main event loop - - - - - - - - - -
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("User asked to quit.")
            done = True  # Signals the program to end
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and validy is True:
                pilot_y_speed = -5
            elif event.key == pygame.K_DOWN and validy is True:
                pilot_y_speed = 5
            elif event.key == pygame.K_LEFT and validx is True:
                pilot_x_speed = -5
            elif event.key == pygame.K_RIGHT and validx is True:
                pilot_x_speed = 5
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                pilot_y_speed = 0
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                pilot_x_speed = 0
        if pilot_x > 1023 or pilot_x < 385:
            validx = False
        else:
             validx = True
        if pilot_y > 767 or pilot_y < 1:
            validy = False
        else:
            validy = True

    # - - - - - Game logic - - - - - - - -

    list_all_sprites.update()
    pilot_x += pilot_x_speed
    pilot_y += pilot_y_speed + gravity
    # - - - - - Drawing code - - - - - - -
    pygame.draw.rect(screen, WHITE, [0, 0, 384, 768], 0)
    pygame.draw.rect(screen, BLACK, [384, 0, 640, 768], 0)
    pygame.draw.line(screen, GREEN, (384, 0), (384, 768), 8)
    list_all_sprites.draw(screen)
    # - - - - - Update screen drawn - - -
    pygame.display.flip()

    # - - - - - Set the fps - - - - - - -
    clock.tick(60)

# Shutdown python program
pygame.quit()
