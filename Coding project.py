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
bullet_x = 0
bullet_y = 0
pilot_x_speed = 0
pilot_y_speed = 0
gravity = 2.5
TotScore = 0
HitScore = 2
MobScore = 10
MobsDead = 0
PilotHealth = 3
killed_mob = 0
column_spacing = 36
row_spacing = 36
# Counts the number of flickers when hit
flickercount = 3
# Setting up an event for firing the projectiles and spawning mobs
FireRate = pygame.USEREVENT
SpawnEnemy = pygame.USEREVENT+1
PilotHit = pygame.USEREVENT+2
PilotHitRecover = pygame.USEREVENT+3
Pilot_flickering = False
# Grace period for the damage taken
RecoverTime = pygame.USEREVENT+4
TimeShot = 220
# Spawning mobs at random intervals in time range
TimeMobs = random.randint(3500, 4200)



# Setting up the screen
size = (1024, 768)
screen = pygame.display.set_mode(size)
# Labelling the program
pygame.display.set_caption("Game name here")

# To manage the fps
clock = pygame.time.Clock()



# Tetris board setup
TGridBlock = []
TGrid = []
for TRow in range(10):
    TGrid.append([])
    TGridBlock.append([])
    for TColumn in range(20):
        TGrid[TRow].append(0)
        TGridBlock[TRow].append(0)


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
    def __init__(self, mob_health):
        super().__init__()
        self.image = pygame.Surface([30, 30])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        # Generic and basic attributes of an enemy
        self.rect.x = random.randint(1024, 1030)
        self.rect.y = random.randint(20, 735)
        self.Mob_Health = mob_health
    # Enemy moves left

    def update(self):
        self.rect.x -= 2
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
                print("hurt")
                pygame.time.set_timer(PilotHit, 1000)
                Pilot_flickering = True
                PilotHealth -= 1



# Types of enemies
# I Block


class IBlock(Enemy):
    def __init__(self, mob_health):
        super(IBlock, self).__init__(mob_health)
        global killed_mob
        self.image = pygame.Surface([30, 120])
        self.image.fill(BLUE)
        picture = pygame.image.load("/Users/adrianlam/Documents/GitHub/Adrian-project/IBlock.png")
        self.image = pygame.transform.scale(picture, [30, 120])
        if mob_health == 0:
            killed_mob = "I"


# J Block


class JBlock(Enemy):
    def __init__(self, mob_health):
        super(JBlock, self).__init__(mob_health)
        global killed_mob
        self.image = pygame.Surface([60, 90])
        self.image.fill(BLUE)
        picture = pygame.image.load("/Users/adrianlam/Documents/GitHub/Adrian-project/JBlock.png")
        self.image = pygame.transform.smoothscale(picture, [60, 90])
        if mob_health == 0:
            killed_mob = "J"

# L Block


class LBlock(Enemy):
    def __init__(self, mob_health):
        super(LBlock, self).__init__(mob_health)
        global killed_mob
        self.image = pygame.Surface([60, 90])
        self.image.fill(BLUE)
        picture = pygame.image.load("/Users/adrianlam/Documents/GitHub/Adrian-project/LBlock.png")
        self.image = pygame.transform.scale(picture, [60, 90])
        if mob_health == 0:
            killed_mob = "L"

# O Block


class OBlock(Enemy):
    def __init__(self, mob_health):
        super(OBlock, self).__init__(mob_health)
        global killed_mob
        self.image = pygame.Surface([60, 60])
        self.image.fill(BLUE)
        picture = pygame.image.load("/Users/adrianlam/Documents/GitHub/Adrian-project/OBlock.png")
        self.image = pygame.transform.scale(picture, [60, 60])
        if mob_health == 0:
            killed_mob = "O"

# T Block


class TBlock(Enemy):
    def __init__(self, mob_health):
        super(TBlock, self).__init__(mob_health)
        global killed_mob
        self.image = pygame.Surface([60, 90])
        self.image.fill(BLUE)
        picture = pygame.image.load("/Users/adrianlam/Documents/GitHub/Adrian-project/TBlock.png")
        self.image = pygame.transform.scale(picture, [60, 90])
        if mob_health == 0:
            killed_mob = "T"

# S Block


class SBlock(Enemy):
    def __init__(self, mob_health):
        super(SBlock, self).__init__(mob_health)
        global killed_mob
        self.image = pygame.Surface([60, 90])
        self.image.fill(BLUE)
        picture = pygame.image.load("/Users/adrianlam/Documents/GitHub/Adrian-project/SBlock.png")
        self.image = pygame.transform.scale(picture, [60, 90])
        if mob_health == 0:
            killed_mob = "S"

# Z Block


class ZBlock(Enemy):
    def __init__(self, mob_health):
        super(ZBlock, self).__init__(mob_health)
        global killed_mob
        self.image = pygame.Surface([60, 90])
        self.image.fill(BLUE)
        picture = pygame.image.load("/Users/adrianlam/Documents/GitHub/Adrian-project/ZBlock.png")
        self.image = pygame.transform.scale(picture, [60, 90])
        if mob_health == 0:
            killed_mob = "Z"


# All sprites are refreshed in their positions
pygame.time.set_timer(FireRate, TimeShot)
# Randomly generates a new enemy at a random rate
pygame.time.set_timer(SpawnEnemy, TimeMobs)
# Player and projectiles are updated/stored in sprite group
list_all_sprites = pygame.sprite.Group()
list_bullet = pygame.sprite.Group()
# Enemy are updated/stored in sprite group
list_mobs = pygame.sprite.Group()
# Player and bullet initialised
Pilot = Pilot()
list_all_sprites.add(Pilot)

# Initialise block types
BlockType = [IBlock, JBlock, LBlock, OBlock, SBlock, ZBlock]

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
                elif event.key == pygame.K_DOWN:
                        pilot_y_speed = 8
                elif event.key == pygame.K_LEFT:
                        pilot_x_speed = -8
                elif event.key == pygame.K_RIGHT:
                        pilot_x_speed = 8

        # Tells the pilot to stop moving when key not pressed
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                pilot_y_speed = 0
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                pilot_x_speed = 0
        # The bullet continues to fire automatically
        elif event.type == FireRate:
            Shot = Bullet()
            list_all_sprites.add(Shot)
            list_bullet.add(Shot)
        # Mobs are spawned at random time intervals
        elif event.type == SpawnEnemy:
            BlockChoice = random.choice(BlockType)
            Mob = BlockChoice(2)
            list_all_sprites.add(Mob)
            list_mobs.add(Mob)
        # The pilot flashes red when it is hit
        elif event.type == PilotHit:
            if flickercount > 0:
                Pilot.image.fill(RED)
                print("hit")
        # The time period for changing back to white is 500ms a.k.a half the time period of flickering pilot to red
                pygame.time.set_timer(PilotHitRecover, 500)
            else:
                print("Done hit")
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
                print("flicker")
            else:
                Pilot_flickering = False
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
    drawing("Score:", 16, WHITE, 880, 20)
    drawing(TotScore, 16, WHITE, 980, 20)

    # Display health
    show_health()

    # Removes off-screen mobs
    for Mob in list_mobs:
        if Mob.rect.x <= 384 or Mob.rect.y >= 768:
            list_all_sprites.remove(Mob)
            list_mobs.remove(Mob)

    # Removes off-screen projectiles
    for Shot in list_bullet:
        if Shot.rect.x >= 1024 or Shot.rect.y >= 768:
            list_all_sprites.remove(Shot)
            list_bullet.remove(Shot)
        # Hit detection between bullet and Mob
        list_mobs_hit = pygame.sprite.spritecollide(Shot, list_mobs, False)
        # Score from hitting mobs
        for Mob in list_mobs_hit:
            TotScore += HitScore
            Mob.Mob_Health -= 1
            if Mob.Mob_Health == 0:
                list_mobs.remove(Mob)
                list_all_sprites.remove(Mob)
                list_mobs_hit.remove(Mob)
                TotScore += MobScore
    # Removing the projectiles if they land on an enemy
    for Mob in list_mobs:
        list_shots_landed = pygame.sprite.spritecollide(Mob, list_bullet, True)
        for Shot in list_shots_landed:
            list_all_sprites.remove(Shot)
            list_bullet.remove(Shot)
            print(TotScore)

    # Drawing tetris board

    for TRow in range(10):
        row_pos = (TRow + 0.3) * row_spacing
        for TColumn in range(20):
            column_pos = (TColumn + 1.25) * column_spacing
            pygame.draw.rect(screen, WHITE, [row_pos, column_pos, 34, 34])

    list_all_sprites.draw(screen)

    # - - - - - Update screen drawn - - -
    pygame.display.flip()

    # - - - - - Set the fps - - - - - - -
    clock.tick(60)

# Shutdown python program
pygame.quit()
