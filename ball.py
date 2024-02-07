import pygame 
import random
import math
import numpy as np
from vector import Vector
from bat import Bat

colors = {'white': (255, 255, 255),
          'black': (0, 0, 0),
          'red': (255, 0 , 0),
          'green': (0, 255, 0),
          'blue': (0, 0, 255)}


class Ball:

    def __init__(self, sc, position: Vector, velocity: Vector, radius: float, grav=Vector(0.0,0.3)):
        self.position = position
        self.velocity = velocity
        self.radius = radius
        self.grav = grav
        self.screen = sc

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
            

            if other.radius >= 11: # ie is big ball
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
        
    def move_horizontally(self):
        self.position.x += self.velocity.x
        self.velocity.y = 0
        
        
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
    
    def is_rotrect_collision(self,rect, i):
        return rect.is_collision(self, 150,300,30,100,i)[0]
    
    def collides_with(self, p_of_obj):

        vec_of_points = []
        for vec in p_of_obj:
            thing = Vector(vec[0],vec[1])
            vec_of_points.append(thing)
            

        return vec_of_points
    
    def sat_algo(self, points, other):

        vec_points = [Vector(point[0], point[1]) for point in points]

        # SAT Beginn
        vertices = []
        for index in range(len(vec_points)):
            vertice = vec_points[index-1] - vec_points[index]
            vertices.append(vertice)
            
            # pygame.draw.line(self.screen, colors['black'], vec_points[index].int_tuple(), vec_points[index-1].int_tuple())

        # # Erstelle ein Rechteck um den Ball
        # ball_rect = Rect(Vector(ball.position.x - ball.radius, ball.position.y - ball.radius),
        #                  ball.radius * 2, ball.radius * 2)

        normals = []
        overlaps = []
        for vertice in vertices:
            normal = vertice.rotate(90).normalize()
            normals.append(normal)

            obj_projections = [p.dot(normal) for p in vec_points]
            ball_projections = [self.position.dot(normal) + self.radius, self.position.dot(normal) - self.radius]

            min_rect = min(obj_projections)
            max_rect = max(obj_projections)
            min_ball = min(ball_projections)
            max_ball = max(ball_projections)

            overlap =  min(max_rect, max_ball) - max(min_rect, min_ball)
            overlaps.append(overlap)

            if max_ball < min_rect or min_ball > max_rect:
                # Es gibt eine separierende Achse!
                return False, 0

        # Wenn keine separierende Achse gefunden wurde, gibt es eine Kollision
        min_overlap = np.argmin(overlaps)
        self.collide(normals[min_overlap], other)
    
    def collide(self, n, other):
        '''
        Lets the ball reflect from massive obj
        Input: normal n
        '''
        boost = other.active * 0.5
        t = n.rotate(-90)
        old_velo = self.velocity
        new_velo = n * old_velo.dot(n) * (-1) + t * old_velo.dot(t)
        self.position += new_velo.normalize() * 10
        self.velocity = new_velo * old_velo.abs() * (1+boost)

