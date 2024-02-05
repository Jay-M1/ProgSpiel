import pygame 
import random
import math
from vector import Vector


class Ball:

    def __init__(self, position: Vector, velocity: Vector, radius: float, grav=Vector(0.0,0.3)):
        self.position = position
        self.velocity = velocity
        self.radius = radius
        self.grav = grav

    def check_screen_collide(self, borders: Vector, damp=0.8,roll=0.99):
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
            

    def check_collision(self, other: object):

        connecting_vec = other.position - self.position
        distance = connecting_vec.abs()
        if distance == 0: distance = 1
        isbigball = False

        if distance <= max(self.radius, other.radius):
            

            if other.radius == 30: # ie is big ball
                isbigball = True

            self_v_davor = self.velocity
            other_v_davor = other.velocity 
            #Versatz
            self.position = self.position + connecting_vec * (-1/distance * 1)      # Klasse Vector versteht nur + und * deswegen diese komische Schreibweise hier. 
            if not isbigball:
                other.position = other.position + connecting_vec * (1/distance * 1)     # verschiebt die Bälle nach dem Stoß um 1 Pixel weg voneinander
                other.velocity = self_v_davor * 0.8
                self.velocity = other_v_davor * 0.8

            if isbigball:
                self.velocity = self.velocity * (-1.5)
                if self.velocity.abs() >= 2:
                    return True            

    def gravitate(self,DT=1):

        self.velocity = self.velocity + self.grav*DT
        self.position = self.position + self.velocity*DT + self.grav*DT**2*0.5
        
    # def is_collision(self, rect_pos, rect_width, rect_height):
    #     rect_left = rect_pos[0]
    #     rect_right = rect_pos[0] + rect_width
    #     rect_top = rect_pos[1]
    #     rect_bottom = rect_pos[1] + rect_height

    #     closest_x = max(rect_left, min(self.position.x, rect_right))
    #     closest_y = max(rect_top, min(self.position.y, rect_bottom))

    #     distance = math.sqrt((self.position.x - closest_x)**2 + (self.position.y - closest_y)**2)
        
    #     if distance < self.radius:
    #         self.velocity = self.velocity * (-1)
            
    
    
    def is_rect_collision(self, rect):
        return rect.is_collision(self)[0]
    
    def is_rotrect_collision(self,rect):
        return rect.is_collision(self)
