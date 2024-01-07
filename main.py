#"""
import pygame
from pathlib import Path
from numpy.random import randint

# Initialize PyGame
pygame.init()

# Initial window size
s_width = 1080
s_height = 720

# Define spacetime 
GRAVITY_X = 0.0
GRAVITY_Y = 0.3
DT = 1 # ms (discretization of time) 

# Making display screen
screen = pygame.display.set_mode((s_width, s_height), pygame.RESIZABLE)
pygame.display.set_caption('Flipper')

# insert game icon
# code

# Clock
clock = pygame.time.Clock()

# Setup 
running = True

# Initialisation
damp = 0.8

ball1_x = 100
ball1_y = 150
ball1_vx = 0
ball1_vy = 0

ball1_radius = 10

ball2_x = 200
ball2_y = 150
ball2_vx = 0
ball2_vy = 0

player_vx = 0
player_vy = 0

ball2_radius = 20

# Colors, Background
bg_orig = pygame.image.load(Path(__file__).parents[0] / Path("graphics/bkg.jpg")).convert()
test_font = pygame.font.Font(None,50)

# Surfaces
text_surface = test_font.render('ff', False, 'Black')
text_rect = text_surface.get_rect(center = (400,50))

snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surface.get_rect(midbottom = (400, 400))

player_surf = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom = (90,400))

###############################################################################################################################################################################################################################
#keys = pygame.key.get_pressed()
    #if keys[pygame.K_SPACE]:
        #print('jump')
#if player_rect.colliderect(snail_rect): print('collision')
#mouse_pos = pygame.mouse.get_pos()
 #if player_rect.collidepoint(mouse_pos): print(pygame.mouse.get_pressed())
###############################################################################################################################################################################################################################

# Main event loop
while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            ball1_vx += randint(-10,10)
            ball1_vy += randint(-10,10)
            ball2_vx += randint(-10,10)
            ball2_vy += randint(-10,10)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print('key down')

        continue

    # Adjust screen
    s_width, s_height = screen.get_width(), screen.get_height()
    bg = pygame.transform.scale(bg_orig, (s_width, s_height))
    screen.blit(bg, (0, 0))

    # Shapes
    pygame.draw.rect(screen,'Pink',text_rect)
    pygame.draw.rect(screen,'Pink',text_rect,200)
    screen.blit(text_surface,text_rect)
    screen.blit(snail_surface,snail_rect)
    screen.blit(player_surf,player_rect)
    pygame.draw.ellipse(screen, 'Brown', pygame.Rect(10,100,200,100))
    pygame.draw.circle(screen, (35, 161, 224), [ball1_x,ball1_y] , ball1_radius)
    pygame.draw.circle(screen, (35, 161, 224), [ball2_x,ball2_y] , ball2_radius)

    # Motion
    ball1_vy = ball1_vy + GRAVITY_Y*DT
    ball2_vy = ball2_vy + GRAVITY_Y*DT

    if ball1_y > screen.get_height() - ball1_radius:
        ball1_y = screen.get_height() - ball1_radius
        ball1_vy = ball1_vy * damp * (-1)
    if ball1_y < 0:
        ball1_y = -1
        ball1_vy = ball1_vy * damp * (-1)
    if ball1_x > screen.get_width():
        ball1_x = screen.get_width() + 1
        ball1_vx = ball1_vx * damp * (-1)
    if ball1_x < 0:
        ball1_x = -1
        ball1_vx = ball1_vx * damp * (-1)
    if ball2_y > screen.get_height():
        ball2_y = screen.get_height() + 1
        ball2_vy = ball2_vy * damp * (-1)
    if ball2_y < 0:
        ball2_y = -1
        ball2_vy = ball2_vy * damp * (-1)
    if ball2_x > screen.get_width():
        ball2_x = screen.get_width() + 1
        ball2_vx = ball2_vx * damp * (-1)
    if ball2_x < 0:
        ball2_x = -1
        ball2_vx = ball2_vx * damp * (-1)
    

    ball1_y = ball1_y + ball1_vy*DT + 0.5 * GRAVITY_Y*DT**2
    ball2_y = ball2_y + ball2_vy*DT + 0.5 * GRAVITY_Y*DT**2
    ball1_x = ball1_x + ball1_vx*DT + 0.5 * GRAVITY_X*DT**2
    ball2_x = ball2_x + ball2_vx*DT + 0.5 * GRAVITY_X*DT**2

    snail_rect.left -= 5
    if snail_rect.left < -100 : snail_rect.left = 800
    player_rect.left += 1

    # Settings
    pygame.display.flip() # Update the display of the full screen
    clock.tick(60) # 60 frames per second
#"""
"""
import pygame
from pathlib import Path

# Initialize PyGame
pygame.init()

# Initial window size
s_width = 600
s_height = 800

# Define spacetime 
GRAVITY_X = 0.0
GRAVITY_Y = 0.3
DT = 1 # ms (discretization of time) 

# Making display screen
screen = pygame.display.set_mode((s_width, s_height), pygame.RESIZABLE)
bg_orig=pygame.image.load(Path(__file__).parents[0] / Path("bkg.jpg")).convert()
clock = pygame.time.Clock()

# Setup 
running = True

# You could declare components (the initial ball, the other items, ...) here

ball_x = 100
ball_y = 150
ball_vx = 0
ball_vy = 0

ball_radius = 30

ball2_x = 200
ball2_y = 150
ball2_vx = 0
ball2_vy = 0

ball2_radius = 40


# Main event loop
while running:
    for event in pygame.event.get():
        # Get's all the user action (keyboard, mouse, joysticks, ...)
        continue

    # Adjust screen
    s_width, s_height = screen.get_width(), screen.get_height()
    bg = pygame.transform.scale(bg_orig, (s_width, s_height))
    screen.blit(bg, (0, 0)) # redraws background image


    # Here the action could take place

    # s = s0 + v0*t + 1/2a*t**2

    ball_vy = ball_vy + GRAVITY_Y*DT
    ball2_vy = ball2_vy + GRAVITY_Y*DT

    if ball_y >= screen.get_height():
        ball_vy = ball_vy * (-1)
    if ball2_y >= screen.get_height():
        ball2_vy = ball2_vy * (-1)

    ball_y = ball_y + ball_vy*DT + 0.5 * GRAVITY_Y*DT**2
    ball2_y = ball2_y + ball2_vy*DT + 0.5 * GRAVITY_Y*DT**2

    pygame.draw.circle(screen, (35, 161, 224), [ball_x,ball_y] , ball_radius)
    pygame.draw.circle(screen, (35, 161, 224), [ball2_x,ball2_y] , ball2_radius)


    pygame.display.flip() # Update the display of the full screen
    clock.tick(60) # 60 frames per second

# Done! Time to quit.
"""