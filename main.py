import pygame
import numpy as np
from pathlib import Path
from numpy.random import randint
from copy import copy
from vector import Vector

white = (255, 255, 255)
black = (0, 0, 0)
  
class Ball:

    def __init__(self, position : Vector, velocity : Vector, radius):
        self.position = position
        self.velocity = velocity
        self.radius = radius

    def check_screen_collide(self,borders,damp=0.8,roll=0.99):
        if self.position.y > borders.y - self.radius:
            self.position.y = borders.y - self.radius + 1
            self.velocity.y = self.velocity.y * damp * (-1)
            self.velocity.x = self.velocity.x * roll         # Rollwiderstand
        if self.position.y < 0:
            self.position.y = -1
            self.velocity.y = self.velocity.y * damp * (-1)
        if self.position.x > borders.x:
            self.position.x = borders.x + 1
            self.velocity.x = self.velocity.x * damp * (-1)
        if self.position.x < 0:
            self.position.x = -1
            self.velocity.x = self.velocity.x * damp * (-1)

    def check_collision(self,other):

        connecting_vec = other.position - self.position
        distance = connecting_vec.abs()

        if distance <= max(self.radius, other.radius):

            self_v_davor = self.velocity
            other_v_davor = other.velocity 
            #Versatz
            self.position = self.position + connecting_vec * (-1/distance * 1)      # Klasse Vector versteht nur + und * deswegen diese komische Schreibweise hier. 
            other.position = other.position + connecting_vec * (1/distance * 1)     # verschiebt die Bälle nach dem Stoß um 1 Pixel weg voneinander

            # Stoßprozess Anfang
            other.velocity = self_v_davor * 0.8
            self.velocity = other_v_davor * 0.8
            # Stoßprozess Ende       

    def gravitate(self,grav=Vector(0.0,0.3),DT=1):

        self.velocity = self.velocity + grav*DT
        self.position = self.position + self.velocity*DT + grav*DT**2*0.5
        
class Rect:
    def __init__(self, position, right, left, top, bottom):
        self.posotion = copy(position)
        self.right = right
        self.left = left
        self.top = top
        self.bottom = bottom
        
    def collide_with_ball(self, ball):
        
        if ball.position.x + ball.radius >= self.right and ball.position.y >= self.top:
            ball.velocity = ball.velocity * -0.8
        if ball.position.x - ball.radius <= self.left and ball.position.y >= self.top:
            ball.velocity = ball.velocity * -0.8
            
    def rotate(self, w):
        rotate = True
            
class RotatingObject(pygame.sprite.Sprite):
    def __init__(self, position, pivot, rotation, direction):
        super().__init__()
        self.image = pygame.image.load("basebat_blue.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 150))
        self.rotation = rotation
        self.image = pygame.transform.rotate(self.image, self.rotation)
        self.original_image = self.image
        if direction == "right":
            self.rect = self.image.get_rect(midright = (position.x - pivot.x, position.y - pivot.y))
        if direction == "left":
            self.rect = self.image.get_rect(midleft = (position.x - pivot.x, position.y - pivot.y))
        self.position = position
        self.pivot = pivot
        self.mask = pygame.mask.from_surface(self.image)
        self.angle = 0
        
    def update_right(self):
        self.angle -= 1
        image_rect = self.original_image.get_rect(midright = (self.position.x - self.pivot.x, self.position.y - self.pivot.y))
        offset_center_to_pivot = self.position - Vector(image_rect.center[0], image_rect.center[1])
        rotated_offset = offset_center_to_pivot.rotate(-self.angle) # dreht in die andere Richtung wie pygame.transform.rotate()
        rotated_image_center = (self.position.x - rotated_offset.x, self.position.y - rotated_offset.y)
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center = rotated_image_center)
        self.mask = pygame.mask.from_surface(self.image)
        
    def update_left(self):
        self.angle += 1
        image_rect = self.original_image.get_rect(midleft = (self.position.x - self.pivot.x, self.position.y - self.pivot.y))
        offset_center_to_pivot = self.position - Vector(image_rect.center[0], image_rect.center[1])
        rotated_offset = offset_center_to_pivot.rotate(-self.angle) # dreht in die andere Richtung wie pygame.transform.rotate()
        rotated_image_center = (self.position.x - rotated_offset.x, self.position.y - rotated_offset.y)
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center = rotated_image_center)
        self.mask = pygame.mask.from_surface(self.image)
    
  
   # def push(self, a):
        
        

def main():
    def start(position, radius):
        if position.x == radius and position.y == 761:
            ball1.velocity = Vector(5,-33)
    def reset():
        ball1.velocity = Vector(0, 0)
        ball1.position = Vector(ball1.radius, screen.get_height())
        ball2.velocity = Vector(0.0, 0.0)
        ball2.position = Vector(500, screen.get_height())
    def GameOver():
        reset()
        
    def check_collision(ball_x, ball_y, ball_radius, rect_x, rect_y, mask):
        """
        # Berechnung des Abstands zwischen Ballmittelpunkt und Rechteckmittelpunkt
        dx = abs(ball_x - (rect_x + rect_width/2))
        dy = abs(ball_y - (rect_y + rect_height/2))

        # Prüfen, ob der Abstand kleiner ist als die Summe der Radien
        if dx > rect_width/2 + ball_radius or dy > rect_height/2 + ball_radius:
            return False
        if dx <= rect_width/2 or dy <= rect_height/2:
            return True

        # Prüfen auf Kollision an den Ecken des Rechtecks
        return (dx - rect_width/2)**2 + (dy - rect_height/2)**2 <= ball_radius**2
        """
    # Maske für den Ball erstellen
        ball_mask = pygame.mask.from_surface(pygame.Surface((2*ball_radius, 2*ball_radius), pygame.SRCALPHA))

    # Position der Masken setzen
        ball_mask_rect = ball_mask.get_rect(center=(ball_x, ball_y))
        rect_mask_rect = mask.get_rect(topleft=(rect_x, rect_y))

    # Kollisionstest
        return mask.overlap(ball_mask, (ball_mask_rect.x - rect_mask_rect.x, ball_mask_rect.y - rect_mask_rect.y)) is not None

        
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
    hole_h = 30
    ball1 = Ball(Vector(10, screen.get_height()),Vector(0,0),10)
    ball2 = Ball(Vector(500, screen.get_height()),Vector(0,0),10)
    #rect1 = Rect(position= Vector(400,300), right=325, left=400+75, top=300-75, bottom=300+75)
    
    # Colors, Background
    bg_orig = pygame.image.load(Path(__file__).parents[0] / Path("graphics/bkg.jpg")).convert()
    test_font = pygame.font.Font(None,25)
    
    #balls 
    ball_surface = pygame.Surface((screen.get_width(), screen.get_height()))

    # Surfaces
    text_surface = test_font.render('Keys: Start: "click", Random: "Space", Reset: "r"', False, 'Black')
    text_rect = text_surface.get_rect(bottomright = (400,50))
    hole_w = 250
    hole_h = hole_h
    hole_color = '#E6E6FA'
    hole1_surface = pygame.Surface((hole_w,hole_h))
    hole1_surface.fill(hole_color)
    hole2_surface = pygame.Surface((hole_w,hole_h))
    hole2_surface.fill(hole_color)
    
    
    # Starter
    rotating_object = RotatingObject(Vector(screen.get_width()/2 - 150, 700), Vector(10, 0), -90, "left")
    rotating_object2 = RotatingObject(Vector(screen.get_width()/2 + 150, 700), Vector(-10, 0), 90, "right")
    rotating_object2.angle = 25
    rotating_object.angle = -25
    rotating_object.update_left()
    rotating_object2.update_right()
    all_sprites = pygame.sprite.Group(rotating_object,rotating_object2)
    
    
    starts = 5
    
    rot =  30 % 360
    # Main event loop
    while running:
        
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
                    for i in range(30):
                        rotating_object.update_left()
                        i += 1
                if event.key == pygame.K_RIGHT:
                    for i in range(30):
                        rotating_object2.update_right()
                        i += 1
                if event.key == pygame.K_r:
                    ball1.velocity = Vector(0, 0)
                    ball1.position = Vector(ball1.radius, screen.get_height())
                    ball2.velocity = Vector(0.0, 0.0)
                    ball2.position = Vector(500, screen.get_height())
                if event.key == pygame.K_m:
                    ball1.velocity.x += randint(-10,20)
                    ball1.velocity.y += randint(-10,20)
                    ball2.velocity.x += randint(-10,20)
                    ball2.velocity.y += randint(-10,20)

            continue
        
        
        for ball in [ball1,ball2]:          # die Schleife checkt, ob ein Ball in die "Aus" Zone kommt
            if check_collision(ball.position.x, ball.position.y, ball.radius, rotating_object.rect.x, rotating_object.rect.y, rotating_object.mask):
                ball.velocity = ball.velocity * -0.8
                print("Kollision!")
                continue
        
        
        # Events
        all_sprites.draw(screen)
        # Shapes
        #pygame.draw.rect(screen,'Pink',text_rect)
        #pygame.draw.rect(screen,'Pink',text_rect,200)
        screen.blit(text_surface,text_rect)
        pygame.draw.circle(screen, (35, 161, 224), [ball1.position.x,ball1.position.y] , ball1.radius)
        pygame.draw.circle(screen, 'green', [ball2.position.x,ball2.position.y] , ball2.radius)

        hole1_rect = hole1_surface.get_rect(bottomleft = (0,screen.get_height()))
        hole2_rect = hole2_surface.get_rect(bottomright = (screen.get_width(),screen.get_height()))
        screen.blit(hole1_surface,hole1_rect)
        screen.blit(hole2_surface,hole2_rect)
    
        # Motion
        ball1.check_collision(ball2)
        #rect1.collide_with_ball(ball1)
        #rect1.collide_with_ball(ball2)
        ball1.gravitate()
        ball2.gravitate()
        #rotating_object.check_collision(ball1)
        
        for ball in [ball1,ball2]:          # die Schleife checkt, ob ein Ball in die "Aus" Zone kommt
            if not (abs(ball.position.x - screen.get_width()/2) < (screen.get_width() - 2*hole_w)/2
                and screen.get_height() - ball.position.y < hole_h + ball.radius):
                ball.check_screen_collide(screen_borders)
                continue
            # Hier ist der Ball im Korb drin
            GameOver()
        # Settings
        pygame.display.flip() # Update the display of the full screen
        clock.tick(60) # 60 frames per second

if __name__ == '__main__':
    main()
