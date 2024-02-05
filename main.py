import pygame
import numpy as np
from pathlib import Path
from numpy.random import randint
from copy import copy
from vector import Vector
from ball import Ball
from rect import Rect
from bat import RotatingObject
from rotatingrect import Rotating_rect

colors = {'white': (255, 255, 255),
          'black': (0, 0, 0),
          'red': (255, 0 , 0),
          'green': (0, 255, 0),
          'blue': (0, 0, 255)}

def main():

    def start(position, radius):
        ball1.velocity = Vector(12,-25)
        
    def reset():
        ball1.velocity = Vector(0, 0)
        ball1.position = Vector(ball1.radius, screen.get_height())
        ball2.velocity = Vector(0.0, 0.0)
        ball2.position = Vector(500, screen.get_height())
       
    def GameOver():
        reset()
    
    def paint_line(start, end, tast=9, ballhere = True):
            """
            Zeichnet eine Linie zum Reflektieren
            Input:  Anfangspunkt als Tuple
                    Endpunkt als Tupel
                    Tastabstand mit der die Linie zerlegt wird. Standartmäßig = 9
                    ballhere = False: Es wird nur geprüft ob Ball1 mit der Linie stößt, falls True dann auch für Ball2
            Output: Liste mit Punkten auf der Linie 
            """
            start_x = min(start[0],end[0])
            start_y = min(start[1],end[1])
            end_x = max(start[0],end[0])
            end_y = max(start[1],end[1])

            pygame.draw.line(screen, colors['white'], (start_x,start_y),(end_x,end_y))

            richtung = Vector(end_x - start_x , end_y - start_y)
            richtung = richtung * (1/(richtung.abs()))
            normale = richtung.rotate(90)
            l = Vector(start_x,start_y)
            points = [l] # erster Punkt

            while True:
                l = l + richtung * tast
                if l.x > end_x or l.y > end_y:
                    break
                points.append(l)
            
            for vec in points:
                distance = ball1.position + vec * (-1)
                if distance.abs() <= ball1.radius:
                    ball1_v_davor = ball1.velocity
                    ball1.position = ball1.position + normale * (ball1_v_davor * normale)*(-1)
                    ball1.velocity = richtung * (ball1_v_davor * richtung)*(-1) + normale * (ball1_v_davor * normale)*(1)
                    ball1.velocity = ball1.velocity * (-0.8)
                if ballhere:
                    distance = ball2.position + vec * (-0.8)
                    if distance.abs() <= ball2.radius:
                        ball2_v_davor = ball2.velocity
                        ball2.position = ball2.position + normale * (ball2_v_davor * normale)*(-1)
                        ball2.velocity = richtung * (ball2_v_davor * richtung)*(-1) + normale * (ball2_v_davor * normale)*(1)
                        ball2.velocity = ball2.velocity * (-0.8)
        
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
    rect1 = Rect(Vector(300,400),100,20)
    rotating_center_rect = Rotating_rect((200, 200), (25, 25), 0, 20, 100)
    circle = 0
    
    starts = 5
    
    key_left = False
    key_right = False
    
    rect_speed = 2
    
    # Main event loop
    while running:
        
        if spawn: print('Ball2 spawnt')

        # Adjust screen
        s_width, s_height = screen.get_width(), screen.get_height()
        bg = pygame.transform.scale(bg_orig, (s_width, s_height))
        screen.blit(bg, (0, 0))
        ground_level = screen.get_height()-hole_h
        screen_borders = Vector(screen.get_width(),ground_level)
        
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
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

        paint_line((0,300), (150,700))

        scores[roundnr] = score
        #print(f"{scores} {score}")
        highscore = max(scores)
        highscore_surface = test_font.render(f'Highscore: {highscore}', False, 'Black')
        highscore_rect = highscore_surface.get_rect(midbottom = (300,120))
        screen.blit(highscore_surface,highscore_rect)
        
        rotating_center_rect.rotate(1, True)

        if rect1.position.x < 0 or (rect1.position.x + rect1.width) > screen.get_width():
            rect_speed *= -1
        rect1.position.x += rect_speed
        
        
        pygame.draw.circle(screen, (35, 161, 224), [ball1.position.x,ball1.position.y] , ball1.radius)
        pygame.draw.circle(screen, 'green', [ball2.position.x,ball2.position.y] , ball2.radius)
        pygame.draw.circle(screen, 'green', [big_ball.position.x,big_ball.position.y] , big_ball.radius)
        pygame.draw.rect(screen, 'blue', (rect1.position.x, rect1.position.y, rect1.width, rect1.height))
        rotating_center_rect.draw(screen)

        hole1_rect = hole1_surface.get_rect(bottomleft = (0,screen.get_height()))
        hole2_rect = hole2_surface.get_rect(bottomright = (screen.get_width(),screen.get_height()))
        screen.blit(hole1_surface,hole1_rect)
        screen.blit(hole2_surface,hole2_rect)
        
        
    
        
        # Motion
        ball1.check_collision(ball2)
        spawn = ball1.check_collision(big_ball)
        if spawn: score += 1
        ball2.check_collision(big_ball)
        ball1.gravitate()
        ball2.gravitate()
        key_left = left_bat.update_left(key_left)
        key_right = right_bat.update_right(key_right)
        
        for ball in [ball1,ball2]:
            if ball.is_rect_collision(rect1):
                _,normal = rect1.is_collision(ball)
                tangent = normal.rotate(90)
                normal = tangent.rotate(90)
                absvelo = ball.velocity.abs()
                velo = tangent * ball.velocity.dot(tangent) * (-1) + normal * ball.velocity.dot(normal)
                ball.position += velo.normalize()
                ball.velocity =  velo*absvelo
                print(velo)
                score += 1
        
        for ball in [ball1,ball2]:          # die Schleife checkt, ob ein Ball in die "Aus" Zone kommt
            if not (abs(ball.position.x - screen.get_width()/2) < (screen.get_width() - 2*hole_w)/2
                and screen.get_height() - ball.position.y < hole_h + ball.radius):
                ball.check_screen_collide(screen_borders)
                continue
            # Hier ist der Ball im Korb drin
            roundnr += 1
            score = 0
            scores.append(score)
            #GameOver()
        
        # Settings
        pygame.display.flip() # Update the display of the full screen
        clock.tick(60) # 60 frames per second        

if __name__ == '__main__':
    main()
