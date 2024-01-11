import pygame
import numpy as np
from pathlib import Path
from numpy.random import randint

class Ball:

    def __init__(self,r,v,radius):
        self.r = r
        self.x = r[0]
        self.y = r[1]
        self.v = v
        self.vx = v[0]
        self.vy = v[1]
        self.radius = radius
        self.rho = np.sqrt(self.x**2 + self.y**2)

    def check_screen_collide(self,borders,damp=0.8,roll=0.99):
        if self.y > borders[1] - self.radius:
            self.y = borders[1] - self.radius + 1
            self.vy = self.vy * damp * (-1)
            self.vx = self.vx * roll         # Rollwiderstand
        if self.y < 0:
            self.y = -1
            self.vy = self.vy * damp * (-1)
        if self.x > borders[0]:
            self.x = borders[0] + 1
            self.vx = self.vx * damp * (-1)
        if self.x < 0:
            self.x = -1
            self.vx = self.vx * damp * (-1)

    def can_collide(self,other):
        if abs(self.rho - other.rho) > max(self.radius, other.radius):
            return True
        else:
            return False

    def gravitate(self,grav=(0.0,0.3),DT=1):
        self.vx = self.vx + grav[0]*DT
        self.vy = self.vy + grav[1]*DT
        self.x = self.x + self.vx*DT + 0.5 * grav[0]*DT**2
        self.y = self.y + self.vy*DT + 0.5 * grav[1]*DT**2

    def collide(self,other):

        if self.can_collide(other) and abs(self.rho - other.rho) <= max(self.radius,other.radius):

            self_v_davor = self.v
            other_v_davor = other.v

            # Stoßprozess Anfang
            other.vx = self_v_davor[0] * 0.8
            other.vy = self_v_davor[1] * 0.8
            self.vx = other_v_davor[0] * 0.8
            self.vy = other_v_davor[1] * 0.8
            # Stoßprozess Ende

def main():

    # Initialize PyGame
    pygame.init()

    #Setup
    running = True

    # Making display screen
    screen = pygame.display.set_mode((600, 800), pygame.RESIZABLE)
    pygame.display.set_caption('Flipper')

    # insert game icon
    # code

    # Clock
    clock = pygame.time.Clock()

    # Initialisation
    ball1 = Ball((100,150),(0,0),10)
    ball2 = Ball((200,150),(0,0),10)

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
                ball1.vx += randint(-10,10)
                ball1.vy += randint(-10,10)
                ball2.vx += randint(-10,10)
                ball2.vy += randint(-10,10)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print('key down')

            continue

        # Adjust screen
        s_width, s_height = screen.get_width(), screen.get_height()
        bg = pygame.transform.scale(bg_orig, (s_width, s_height))
        screen.blit(bg, (0, 0))
        screen_borders = (screen.get_width(),screen.get_height())

        # Shapes
        pygame.draw.rect(screen,'Pink',text_rect)
        pygame.draw.rect(screen,'Pink',text_rect,200)
        screen.blit(text_surface,text_rect)
        screen.blit(snail_surface,snail_rect)
        screen.blit(player_surf,player_rect)
        pygame.draw.ellipse(screen, 'Brown', pygame.Rect(10,100,200,100))
        pygame.draw.circle(screen, (35, 161, 224), [ball1.x,ball1.y] , ball1.radius)
        pygame.draw.circle(screen, 'green', [ball2.x,ball2.y] , ball2.radius)

        # Motion
        ball1.collide(ball2)
        ball1.check_screen_collide(screen_borders)
        ball2.check_screen_collide(screen_borders)
        ball1.gravitate()
        ball2.gravitate()

        snail_rect.left -= 5
        
        if snail_rect.left < -100 : snail_rect.left = 800
        player_rect.left += 1

        # Settings
        pygame.display.flip() # Update the display of the full screen
        clock.tick(60) # 60 frames per second

if __name__ == '__main__':
    main()
