import pygame
import math
import random

# Define colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
# Define symbols
PI = 3.141592653

# Initialize the game engine
pygame.init()

# Creating the screen
size = (700, 500)
screen = pygame.display.set_mode(size)

# Setting the window title
pygame.display.set_caption("ProgramArcadeGames practice game")

# Create an empty array for snow
snow_list = []

# Loop to add snow particles
for i in range(20):
    x_position = random.randrange(0, 500)
    y_position = 0
    snow_list.append([x_position, y_position])

# Loop until the user clicks the close button
done = False

# Used to manage fps
clock = pygame.time.Clock()

# - - - - - - - - Main program loop - - - - - - - - -
while not done:
    # Clear the screen and set white background
    screen.fill(WHITE)
    # - - - Main event loop - - -
    for event in pygame.event.get(): #User did something
        if event.type == pygame.QUIT:
            print("User asked to quit.")
            done = True # Flag that we are done and exit the loop
        elif event.type == pygame.KEYDOWN:
            print("User pressed a key.")
        elif event.type == pygame.KEYUP:
            print("User let go of a key.")
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print("User pressed a mouse button")

        # - - - Game logic here - - -

        # - - - Drawing code here - - -
        # First clear the screen to white. Don't put other drawing commands above this, or
        # they will be erased with this command
        screen.fill(WHITE)

        pygame.draw.rect(screen, RED, [55, 50, 20, 25], 1)
        # Draw green line on screen 5 pixels wide from (0, 0) to (100, 100)
        pygame.draw.line(screen, GREEN, [0, 0], [100, 100], 5)
        pygame.draw.line(screen, GREEN, [50, 50], [300, 300], 2)
        # Draw on screen several lines from (0, 10) to (100, 110) 5 pixels wide using while loop
        y_offset = 0
        while y_offset < 100:
            pygame.draw.line(screen, RED, [0, 10 + y_offset], [100, 110 + y_offset], 5)
            y_offset = y_offset + 10
        # Complex offsets
        for index in range(200):
            radians_x = index/20
            radians_y = index/6
            x = int(75 * math.sin(radians_x))
            y = int(75 * math.cos(radians_y))

        for x_offset in range(30, 300, 30):
            pygame.draw.line(screen, BLACK, [x_offset, 100], [x_offset - 10, 90], 2)
            pygame.draw.line(screen, BLACK, [x_offset, 90], [x_offset - 10, 100], 2)

            pygame.draw.line(screen, BLACK, [x, y], [x+5, y], 5)

        # Draw rectangle, (20, 20) is top left coordinate of rectangle
        pygame.draw.rect(screen, BLACK, [20, 20, 250, 100], 2)

        # Filled in rectangle
        pygame.draw.rect(screen, BLACK, [50, 80, 125, 50], 0)

        # Draw an ellipse using rectangle
        pygame.draw.ellipse(screen, RED, [20, 20, 250, 100], 0)
        pygame.draw.arc(screen, BLUE, [20, 20, 250, 100], PI / 2, PI, 4)
        pygame.draw.arc(screen, BLACK, [20, 20, 250, 100], PI, (3/2) * PI, 4)
        pygame.draw.arc(screen, BLUE, [20, 20, 250, 100], (3/2) * PI, 0, 4)
        pygame.draw.arc(screen, BLACK, [20, 20, 250, 100], 0, PI / 2, 4)

        # Draw a triangle
        pygame.draw.polygon(screen, BLACK, [[100, 100], [0, 200], [200, 200]], 5)

        # Draw text (Font chosen, size, bold, italics)
        font = pygame.font.SysFont('Arial', 25, True, False)
        text = font.render("Test text", True, RED)
        screen.blit(text, [250, 250])

        # Draw snow particles
        for i in range(len(snow_list)):
            if snow_list[i][0] > 400 or snow_list[i][1] > 700:
                snow_list[i][0] = random.randrange(0, 500)
                snow_list[i][1] = 0
            else:
                snow_list[i][0] = random.randrange(x_position-6, x_position+6)
                snow_list[i][1] = random.randrange(y_position-1, y_position+3)
            pygame.draw.circle(screen, BLUE, snow_list[i], 1)

        # Update screen drawn
        pygame.display.flip()

        # - - - Limit to 60 fps
        clock.tick(60)

# Shutdown python program
pygame.quit()
