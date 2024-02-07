import pygame
import numpy as np
import math
from pathlib import Path
from numpy.random import randint
from copy import copy
from vector import Vector
from ball import Ball
from rect import Rect
from bat import Bat
from rotatingrect import RectangleDrawer

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
    big_ball2 = Ball(Vector(400,200), Vector(0,0), 20, grav=Vector(0,0))
    #small_ball = Ball(Vector(300,480), Vector(0,0), 11, grav=Vector(0,0))
    #rect1 = Rect(position= Vector(400,300), right=325, left=400+75, top=300-75, bottom=300+75)
    
    # Colors, Background
    bg_orig = pygame.image.load(Path(__file__).parents[0] / Path("graphics/bkg.jpg")).convert()
    test_font = pygame.font.Font(None,25)
    
    # Music
    
    music = pygame.mixer.music.load(Path(__file__).parents[0] / Path("audio/Clown.mp3")) # Quelle https://www.chosic.com/download-audio/53609/
    #pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(.6)

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
    # left_bat = RotatingObject(Vector(screen.get_width()/2 - 150, 700), Vector(2, -25), -90, "left")
    # right_bat = RotatingObject(Vector(screen.get_width()/2 + 150, 700), Vector(0, 0), 90, "right")
    # all_sprites = pygame.sprite.Group(left_bat, right_bat)
    
    #Rects
    rect1 = Rect(Vector(300,400),100,80)
    rotating_rect = RectangleDrawer(screen)
    circle = 0

    nlb_height = Vector(0,20)
    nlb_width = Vector(120,0)
    nlb_bottomleft = Vector(150,700)
    nlb_points = (nlb_bottomleft , nlb_bottomleft + nlb_width, nlb_bottomleft + nlb_width + nlb_height , nlb_bottomleft + nlb_height)
    new_left_bat = Bat(screen, colors['green'], nlb_points)
    
    starts = 5
    
    key_left = False
    key_right = False
    
    rect_speed = 2
    big_ball_speed = 2

    varhoch = 1

    nlb_angle = 0
    
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
        # all_sprites.draw(screen)
                    
        new_left_bat.update(nlb_angle)
        nlb_angle += 3
        
        screen.blit(text_surface,text_rect)

        score_surface = test_font.render(f'Score: {score}', False, 'Black')
        score_rect = score_surface.get_rect(midbottom = (300,100))
        screen.blit(score_surface,score_rect)

        #paint_line((0,300), (150,700))

        scores[roundnr] = score
        #print(f"{scores} {score}")
        highscore = max(scores)
        highscore_surface = test_font.render(f'Highscore: {highscore}', False, 'Black')
        highscore_rect = highscore_surface.get_rect(midbottom = (300,120))
        screen.blit(highscore_surface,highscore_rect)
        
        #rotating_center_rect.rotate(1, True)

        # if rect1.position.x < 0 or (rect1.position.x + rect1.width) > screen.get_width():
        #     rect_speed *= -1
        # rect1.position.x += rect_speed
        
        if big_ball.position.x - big_ball.radius < 0:
            big_ball_speed *= -1
            big_ball.position.x = big_ball.radius
        elif big_ball.position.x + big_ball.radius > screen.get_width():
            big_ball_speed *= -1
            big_ball.position.x = screen.get_width() - big_ball.radius
        big_ball.position.x += big_ball_speed
        big_ball.move_horizontally()
        
        
        pygame.draw.circle(screen, (35, 161, 224), [ball1.position.x,ball1.position.y] , ball1.radius)
        pygame.draw.circle(screen, 'green', [ball2.position.x,ball2.position.y] , ball2.radius)
        pygame.draw.circle(screen, 'green', [big_ball.position.x,big_ball.position.y] , big_ball.radius)
        pygame.draw.circle(screen, 'green', [big_ball2.position.x, big_ball2.position.y] , big_ball2.radius)
        pygame.draw.rect(screen, 'blue', (rect1.position.x, rect1.position.y, rect1.width, rect1.height))
        # rotrect = rotating_center_rect.draw(screen)

        hole1_rect = hole1_surface.get_rect(bottomleft = (0,screen.get_height()))
        hole2_rect = hole2_surface.get_rect(bottomright = (screen.get_width(),screen.get_height()))
        screen.blit(hole1_surface,hole1_rect)
        screen.blit(hole2_surface,hole2_rect)   
        
        # Motion
        ball1.check_collision(ball2)
        spawn = ball1.check_collision(big_ball)
        spawn2 = ball1.check_collision(big_ball2)
        if spawn or spawn2: score += 1
        ball2.check_collision(big_ball)
        ball1.gravitate()
        ball2.gravitate()
        # key_left = left_bat.update_left(key_left)
        # key_right = right_bat.update_right(key_right)

        for ball in [ball1,ball2]:          # die Schleife checkt, ob ein Ball in die "Aus" Zone kommt
            
            if (abs(ball.position.x - screen.get_width()/2) < (screen.get_width() - 2*hole_w)/2
                and screen.get_height() - ball.position.y < 200):
                if screen.get_height() - ball.position.y < 1:
                    roundnr += 1
                    score = 0
                    scores.append(score)
                    ball.check_screen_collide(screen_borders)
                    #GameOver()
            else:
                ball.check_screen_collide(screen_borders)
                

        varhoch += 1
        # rotrect_points = draw_rectangle(200,200,50,100,colors['black'],i/4)
        # corners = []
        # for point in rotrect_points:
        #     vec = Vector(point[0],point[1])
        #     corners.append(vec)
        
        # for bla in range(len(corners)):
        #     edge = corners[(bla + 1) % len(corners)] - corners[bla]
        #     normal = Vector(-edge.y, edge.x).normalize()

        #     rect_projections = [p.dot(normal) for p in corners]
        #     circle_projection = ball1.position.dot(normal)

        #     min_rect = min(rect_projections)
        #     max_rect = max(rect_projections)

        #     if (circle_projection + ball1.radius < min_rect or circle_projection - ball1.radius > max_rect):
        #         # es gibt eine separierende Axe!
        #         print('abstand')
        #     else:
        #         print('colli')
        #         #ball1.velocity = ball1.velocity * (-1)
##############################################################################################################################
        # points = [(100,120),(150,100), (200,300)]
        # pygame.draw.polygon(screen, colors['red'], points)

        # #for i in ball1.collides_with(points): print(i)

        # if ball1.collides_with(points):
        #     pass
        #     #print('it collides')
################################################################################################################################################
        
        # rotating_rect.draw_rectangle(150,300,30,100,colors['green'],i)
        # for ball in [ball1,ball2]:
        #     if ball.is_rotrect_collision(rotating_rect, i/4):
        #         print('truu')
        #         _,normal = rect1.is_collision(ball)
        #         tangent = normal.rotate(90)
        #         normal = tangent.rotate(90)
        #         prevelo = ball.velocity
        #         velo = tangent * ball.velocity.dot(tangent) *  + normal * ball.velocity.dot(normal) *(-1)
        #         ball.position -= prevelo.normalize()
        #         ball.velocity =  velo*prevelo.abs()
        #         #print(velo)
        #         score += 1    


        

        
        #RECT COLLISIONS:
        for ball in [ball1,ball2]:
            if ball.is_rect_collision(rect1):
                _,normal = rect1.is_collision(ball)
                tangent = normal.rotate(90)
                prevelo = ball.velocity
                velo = tangent * ball.velocity.dot(tangent) * (1) + normal * ball.velocity.dot(normal) * (-1)
                ball.position -= prevelo.normalize()*10
                ball.velocity =  velo*prevelo.abs()
                #print(velo)
                score += 1
                

        #     condition,normal2 = rotating_center_rect.is_collision(ball,rotrect)
        #     if condition:
        #         tangent2 = normal2.rotate(90)
        #         normal2 = tangent2.rotate(90)
        #         absvelo = ball.velocity.abs()
        #         velo = tangent2 * ball.velocity.dot(tangent2) * (-1) + normal2 * ball.velocity.dot(normal2)
        #         ball.position += velo.normalize()
        #         ball.velocity =  velo*absvelo
        #         print(velo)
        #         score += 1

        #     for bat in [left_bat, right_bat]:
        #         if bat == left_bat: batrect = bat1_rect
        #         elif bat == right_bat: batrect = bat2_rect
        #         condition_bat, normal_bat = bat.is_collision(ball, batrect)
        #         if condition_bat:
        #             tangent_bat = normal_bat.rotate(90)
        #             normal_bat = tangent_bat.rotate(90)
        #             absvelo = ball.velocity.abs()
        #             velo = tangent_bat * ball.velocity.dot(tangent_bat) * (-1) + normal_bat * ball.velocity.dot(normal_bat)
        #             ball.position += velo.normalize()
        #             ball.velocity =  velo*absvelo
        #             print(velo)
        #             score += 1
                    
        
        
        
        # Settings
        pygame.display.flip() # Update the display of the full screen
        clock.tick(60) # 60 frames per second        

if __name__ == '__main__':
    main()
