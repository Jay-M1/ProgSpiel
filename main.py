import pygame
import numpy as np
from pathlib import Path
from numpy.random import randint
from copy import copy
from vector import Vector
from ball import Ball
from rect import Rect
from bat import RotatingObject

colors = {'white': (255, 255, 255),
          'black': (0, 0, 0),
          'red': (255, 0 , 0),
          'green': (0, 255, 0),
          'blue': (0, 0, 255)}

def main():

    def start(position, radius):
        if position.x == radius and position.y == 761:
            ball1.velocity = Vector(12,-25)
        
    def reset():
        ball1.velocity = Vector(0, 0)
        ball1.position = Vector(ball1.radius, screen.get_height())
        ball2.velocity = Vector(0.0, 0.0)
        ball2.position = Vector(500, screen.get_height())
       
    def GameOver():
        reset()
        

    # Initialize PyGame
    pygame.init()

    #Setup
    running = True
    spawn = False
    scores = []
    score = 0
    roundnr = 0
    scores.append(score)

    # Making display screen
    screen = pygame.display.set_mode((600, 800))
    pygame.display.set_caption('Flipper')
    
    # Clock
    clock = pygame.time.Clock()

    # Initialisation
    hole_h = 100
    ball1 = Ball(Vector(10, screen.get_height()),Vector(0,0),10)
    ball2 = Ball(Vector(500, screen.get_height()),Vector(0,0),10)
    big_ball = Ball(Vector(300,300), Vector(0,0), 30, grav=Vector(0,0))
    #rect1 = Rect(position= Vector(400,300), right=325, left=400+75, top=300-75, bottom=300+75)
    
    # Colors, Background
    bg_orig = pygame.image.load(Path(__file__).parents[0] / Path("graphics/bkg.jpg")).convert()
    test_font = pygame.font.Font(None,25)
    

    # Surfaces
    text_surface = test_font.render('Keys: Start: "click", Random: "M", Reset: "r", Links, Rechts Pfeil', False, 'Black')
    
    text_rect = text_surface.get_rect(midbottom = (320,50))
    hole_w = 150
    hole_h = hole_h
    hole_color = '#E6E6FA'
    hole1_surface = pygame.Surface((hole_w,hole_h))
    hole1_surface.fill(hole_color)
    hole2_surface = pygame.Surface((hole_w,hole_h))
    hole2_surface.fill(hole_color)
    
    
    # Starter
    left_bat = RotatingObject(Vector(screen.get_width()/2 - 150, 700), Vector(2, -25), -90, "left")
    right_bat = RotatingObject(Vector(screen.get_width()/2 + 150, 700), Vector(0, 0), 90, "right")
    all_sprites = pygame.sprite.Group(left_bat, right_bat)
    
    #Rects
    rect1 = Rect(Vector(300,300), status="static")
    rect2 = Rect(Vector(100,200), status= None)
    circle = 0
    
    starts = 5
    
    key_left = False
    key_right = False
    
    # Main event loop
    while running:
        
        if spawn: print('Ball2 spawnt')

        # Adjust screen
        s_width, s_height = screen.get_width(), screen.get_height()
        bg = pygame.transform.scale(bg_orig, (s_width, s_height))
        screen.blit(bg, (0, 0))
        ground_level = screen.get_height()-hole_h
        screen_borders = Vector(screen.get_width(),ground_level)
        
        acceleration = 1
        
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and starts >= 0:
                start(ball1.position, ball1.radius)
                starts -= 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    key_left = True
                if event.key == pygame.K_RIGHT:
                    key_right = True
                if event.key == pygame.K_r:
                    ball1.velocity = Vector(0, 0)
                    ball1.position = Vector(ball1.radius, screen.get_height())
                    ball2.velocity = Vector(0.0, 0.0)
                    ball2.position = Vector(500, screen.get_height())
                    roundnr += 1
                    score = 0
                    scores.append(score)
                if event.key == pygame.K_m:
                    ball1.velocity.x += randint(-10,20)
                    ball1.velocity.y += randint(-10,20)
                    ball2.velocity.x += randint(-10,20)
                    ball2.velocity.y += randint(-10,20)

        # Shapes
        all_sprites.draw(screen)
        
        screen.blit(text_surface,text_rect)

        score_surface = test_font.render(f'Score: {score}', False, 'Black')
        score_rect = score_surface.get_rect(midbottom = (300,100))
        screen.blit(score_surface,score_rect)

        scores[roundnr] = score
        #print(f"{scores} {score}")
        highscore = max(scores)
        highscore_surface = test_font.render(f'Highscore: {highscore}', False, 'Black')
        highscore_rect = highscore_surface.get_rect(midbottom = (300,120))
        screen.blit(highscore_surface,highscore_rect)

        pygame.draw.circle(screen, (35, 161, 224), [ball1.position.x,ball1.position.y] , ball1.radius)
        pygame.draw.circle(screen, 'green', [ball2.position.x,ball2.position.y] , ball2.radius)
        pygame.draw.circle(screen, 'green', [big_ball.position.x,big_ball.position.y] , big_ball.radius)

        hole1_rect = hole1_surface.get_rect(bottomleft = (0,screen.get_height()))
        hole2_rect = hole2_surface.get_rect(bottomright = (screen.get_width(),screen.get_height()))
        screen.blit(hole1_surface,hole1_rect)
        screen.blit(hole2_surface,hole2_rect)
        
        
        screen.blit(rect1.surface,(rect1.position.x,rect1.position.y))
        rect2.rotate(1)
        screen.blit(rect2.surface,(rect2.position.x,rect2.position.y))
        
        
        # Motion
        ball1.check_collision(ball2)
        spawn = ball1.check_collision(big_ball)
        if spawn: score += 1
        ball2.check_collision(big_ball)
        ball1.gravitate()
        ball2.gravitate()
        key_left = left_bat.update_left(key_left)
        key_right = right_bat.update_right(key_right)
        
        for ball in [ball1,ball2]:          # die Schleife checkt, ob ein Ball in die "Aus" Zone kommt
            if not (abs(ball.position.x - screen.get_width()/2) < (screen.get_width() - 2*hole_w)/2
                and screen.get_height() - ball.position.y < hole_h + ball.radius):
                ball.check_screen_collide(screen_borders)
                continue
            # Hier ist der Ball im Korb drin
            roundnr += 1
            score = 0
            scores.append(score)
            GameOver()
        
        # Settings
        pygame.display.flip() # Update the display of the full screen
        clock.tick(60) # 60 frames per second

if __name__ == '__main__':
    main()
