# Import the libraries for pygame, math functions
# used for enemy AI and random for generating behaviours
import pygame
import math
import random

# Define colours
WHITE = (0, 0, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Initialise the game engine
pygame.init()

# Setting up the screen
size = (1024, 768)
screen = pygame.display.set_mode(size)
screen1 = (384, 768) # Splits the screen into two sides, 1/3rd for tetris and 2/3rd for bullethell
screen2 = (640, 768)
# Labelling the program
pygame.display.set_caption("Game name here")

# Loop until the user clicks the close button
done = False
# - - - - - - - - - Main program loop - - - - - - - - -
while not done:
    # - - - - - - - Main event loop - - - - - - - - - -
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("User asked to quit.")
            done = True # Signals the program to end

    # - - - - - Game logic - - - - - - - -

    # - - - - - Drawing code - - - - - - -

    # - - - - - Update screen drawn - - -
    pygame.draw.rect(screen1, RED, [0, 0, 384, 768], 1)
    pygame.draw.rect(screen2, BLUE, [384, 0, 1024, 768], 1)
    pygame.display.flip()

    # - - - - - Set the fps - - - - - - -
    clock.tick(60)

# Shutdown python program
pygame.quit()
