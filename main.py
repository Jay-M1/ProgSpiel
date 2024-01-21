import pygame
import numpy as np
from pathlib import Path
from numpy.random import randint
from copy import copy
import math

white = (255, 255, 255)
black = (0, 0, 0)

class Vector:
    """
    A class representing a vector in 2 dimensions.

    Attributes:
        x : float or int
        y : float or int

    Methods:
        __init__(self, x, y, z)
        __str__(self)
        Operator +
        Operator *
        abs(self)
    """

    def __init__(self, x, y):
        """
        Initialize a new instance of vector
        """
        self.x = x
        self.y = y

    def __str__(self):
        """
        return a string for the class vector as "Vector(x,y,z)"
        """
        return f"Vector({self.x}, {self.y})"

    def __add__(self,other):
        """
        Overload the + Operator for the class Vector
        Implements the summation of two instances of class Vector
        """
        return Vector(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        if isinstance(other, self.__class__):
            return Vector(self.x - other.x, self.y - other.y)
        return Vector(self.x - other, self.y - other)
    
    def __mul__(self, other):
        if isinstance(other, self.__class__):
            return Vector(self.x * other.x, self.y * other.y)
        return Vector(self.x * other, self.y * other)

    def abs(self):
        """
        Return the absolute value of the Vector instance.
        """
        return float(np.sqrt((self.x*self.x + self.y*self.y)))
 
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
            
class RotatingObject(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.org_image = pygame.image.load("basebat_blue.png").convert_alpha()
        self.image = self.org_image
        self.rect = self.image.get_rect(center=(position.x, position.y))
        self.angle = 0
        self.mask = pygame.mask.from_surface(self.org_image)

    def update(self):
        self.image = pygame.transform.rotate(self.org_image, self.angle)
        self.angle += 10
        self.rect = self.image.get_rect(center=self.rect.center)
        
    def check_collision(self, ball):
        if soldier_mask.overlap(bullet_mask, (pos[0] - soldier_rect.x, pos[1] - soldier_rect.y)):
            col = RED
        else:
            col = GREEN
        
   # def push(self, a):
        
        

def main():
    def start(position, radius):
        if position.x == radius and position.y >= 790:
            ball1.velocity = Vector(5,-33)

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
    ball1 = Ball(Vector(10, screen.get_height()),Vector(0,0),10)
    ball2 = Ball(Vector(500, screen.get_height()),Vector(0,0),10)
    #rect1 = Rect(position= Vector(400,300), right=325, left=400+75, top=300-75, bottom=300+75)
    
    # Colors, Background
    bg_orig = pygame.image.load(Path(__file__).parents[0] / Path("graphics/bkg.jpg")).convert()
    test_font = pygame.font.Font(None,50)
    
    #balls 
    ball_surface = pygame.Surface((screen.get_width(), screen.get_height()))

    # Surfaces
    text_surface = test_font.render('Keys: Start: "click", Random: "Space", Reset: "r"', False, 'Black')
    text_rect = text_surface.get_rect(center = (400,50))
    
    # Starter
    rotating_object = RotatingObject(Vector(screen.get_width() // 2, screen.get_height() // 2))
    all_sprites = pygame.sprite.Group(rotating_object)

    starts = 5
    
    rot =  30 % 360
    # Main event loop
    while running:
        
    
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and starts >= 0:
                start(ball1.position, ball1.radius)
                starts -= 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    all_sprites.update()
                if event.key == pygame.K_r:
                    ball1.velocity = Vector(0, 0)
                    ball1.position = Vector(ball1.radius, screen.get_height())
                    ball2.velocity = Vector(0.0, 0.0)
                    ball2.position = Vector(500, screen.get_height())
                if event.key == pygame.K_m:
                    ball1.velocity.x += randint(-10,10)
                    ball1.velocity.y += randint(-10,10)
                    ball2.velocity.x += randint(-10,10)
                    ball2.velocity.y += randint(-10,10)

            continue
        
        # Adjust screen
        s_width, s_height = screen.get_width(), screen.get_height()
        bg = pygame.transform.scale(bg_orig, (s_width, s_height))
        screen.blit(bg, (0, 0))
        screen_borders = Vector(screen.get_width(),screen.get_height())
        all_sprites.draw(screen)
        # Shapes
        #pygame.draw.rect(screen,'Pink',text_rect)
        #pygame.draw.rect(screen,'Pink',text_rect,200)
        screen.blit(text_surface,text_rect)
        pygame.draw.circle(ball_surface, (35, 161, 224), [ball1.position.x,ball1.position.y] , ball1.radius)
        pygame.draw.circle(ba, 'green', [ball2.position.x,ball2.position.y] , ball2.radius)
    
        # Motion
        ball1.check_collision(ball2)
        ball1.check_screen_collide(screen_borders)
        ball2.check_screen_collide(screen_borders)
        #rect1.collide_with_ball(ball1)
        #rect1.collide_with_ball(ball2)
        ball1.gravitate()
        ball2.gravitate()
        rotating_object.check_collision(ball1)
        

        # Settings
        pygame.display.flip() # Update the display of the full screen
        clock.tick(60) # 60 frames per second

if __name__ == '__main__':
    main()
