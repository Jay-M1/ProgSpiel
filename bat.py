import pygame
import random   
from vector import Vector
from copy import copy

class Bat:
    def __init__(self, screen, color, points, angle=0, richtung=1, count=0, active=1, right=False):

        '''
        Tupel sind für die Aktualisierung der Positionen der Ecken
        Vectoren sind NUR für die Berechnung!
        '''

        self.screen = screen
        self.color = color
        self.points_vec = points
        self.points_tuple = [_.int_tuple() for _ in points]
        self.width = points[1] - points[0]
        self.height = points[3] - points[0]
        self.center = (self.points_vec[0] - self.points_vec[2])/2 + self.points_vec[2]
        #self.center = points[0] + self.height * 0.5 + self.width * 0.5
        self.angle = angle
        self.richtung = richtung
        self.count = count
        self.active = active
        if right: self.right = -1
        if not right: self.right = 1

    def update(self):
        pygame.draw.polygon(self.screen, self.color, self.flip())
        # for point in self.points_tuple: pygame.draw.line(self.screen, (0,0,255), (0,0), point)    # funktioniert
        # pygame.draw.line(self.screen, (0,0,255), (0,0), self.center.int_tuple())                  # funktioniert

    def flip(self):

        if self.angle == -50 * self.right:
            self.richtung *= -1
        elif self.angle == 20 * self.right:
            self.richtung *= -1
            self.count += 1

            
        self.angle -= 2 * self.richtung * self.active
        rotated_points_vec = []
        rotated_points_tuple = []

        drehpunkt = self.points_vec[0]
        for thing in self.points_vec:
            thing = thing - drehpunkt 
            thing = thing.rotate(self.angle) + drehpunkt
            rotated_points_tuple.append(thing.int_tuple())
            rotated_points_vec.append(thing)
  
        #print(self.angle)
        if self.count >= 1: self.active = 0
        if self.count < 1: self.active = 1
        
        self.points_tuple = rotated_points_tuple
        self.center = (Vector(self.points_tuple[0][0], self.points_tuple[0][1]) - Vector(self.points_tuple[2][0], self.points_tuple[2][1]))/2 + Vector(self.points_tuple[2][0], self.points_tuple[2][1])
        return rotated_points_tuple



# class RotatingObject(pygame.sprite.Sprite):
#     def __init__(self, position, pivot, rotation, direction):
#         super().__init__()
#         self.image = pygame.Surface((100, 100), pygame.SRCALPHA)
#         pygame.draw.rect(self.image, (0, 255, 0), (0, 0, 50, 100)) #pygame.image.load("basebat_blue.png").convert_alpha()
#         self.image = pygame.transform.scale(self.image, (50, 135))
#         self.rotation = rotation
#         self.image = pygame.transform.rotate(self.image, self.rotation)
#         self.original_image = self.image
#         if direction == "right":
#             self.rect = self.image.get_rect(midright = (position.x - pivot.x, position.y - pivot.y))
#         if direction == "left":
#             self.rect = self.image.get_rect(midleft = (position.x - pivot.x, position.y - pivot.y))
#         self.position = position
#         self.pivot = pivot
#         self.angle = 0
        
#     def update_right(self, is_aktiv):
#         if is_aktiv:
#             if self.angle < -35:
#                 return False, self.rect
            
#             self.angle -= 4
#             image_rect = self.original_image.get_rect(midright = (self.position.x - self.pivot.x, self.position.y - self.pivot.y))
#             offset_center_to_pivot = self.position - Vector(image_rect.center[0], image_rect.center[1])
#             rotated_offset = offset_center_to_pivot.rotate(-self.angle) # dreht in die andere Richtung wie pygame.transform.rotate()
#             rotated_image_center = (self.position.x - rotated_offset.x, self.position.y - rotated_offset.y)
#             self.image = pygame.transform.rotate(self.original_image, self.angle)
#             self.rect = self.image.get_rect(center = rotated_image_center)
#             return True, self.rect
#         else:
#             if self.angle <= 20:
                
#                 self.angle += 4
#                 image_rect = self.original_image.get_rect(midright = (self.position.x - self.pivot.x, self.position.y - self.pivot.y))
#                 offset_center_to_pivot = self.position - Vector(image_rect.center[0], image_rect.center[1])
#                 rotated_offset = offset_center_to_pivot.rotate(-self.angle) # dreht in die andere Richtung wie pygame.transform.rotate()
#                 rotated_image_center = (self.position.x - rotated_offset.x, self.position.y - rotated_offset.y)
#                 self.image = pygame.transform.rotate(self.original_image, self.angle)
#                 self.rect = self.image.get_rect(center = rotated_image_center)
#             return False, self.rect
        
#     def update_left(self, is_aktiv):
#         if is_aktiv:
#             if self.angle > 35:
#                 return False, self.rect
            
#             self.angle += 4
#             image_rect = self.original_image.get_rect(midleft = (self.position.x - self.pivot.x, self.position.y - self.pivot.y))
#             offset_center_to_pivot = self.position - Vector(image_rect.center[0], image_rect.center[1])
#             rotated_offset = offset_center_to_pivot.rotate(-self.angle) # dreht in die andere Richtung wie pygame.transform.rotate()
#             rotated_image_center = (self.position.x - rotated_offset.x, self.position.y - rotated_offset.y)
#             self.image = pygame.transform.rotate(self.original_image, self.angle)
#             self.rect = self.image.get_rect(center = rotated_image_center)
#             self.mask = pygame.mask.from_surface(self.image)
#             return True, self.rect
#         else:
#             if self.angle >= -20:
                
#                 self.angle -= 4
#                 image_rect = self.original_image.get_rect(midleft = (self.position.x - self.pivot.x, self.position.y - self.pivot.y))
#                 offset_center_to_pivot = self.position - Vector(image_rect.center[0], image_rect.center[1])
#                 rotated_offset = offset_center_to_pivot.rotate(-self.angle) # dreht in die andere Richtung wie pygame.transform.rotate()
#                 rotated_image_center = (self.position.x - rotated_offset.x, self.position.y - rotated_offset.y)
#                 self.image = pygame.transform.rotate(self.original_image, self.angle)
#                 self.rect = self.image.get_rect(center = rotated_image_center)
#                 self.mask = pygame.mask.from_surface(self.image)
#             return False, self.rect
        
    # def is_collision(self, ball, bat):
    #     rect_rotated_surface = bat
    #     corners = [
    #                Vector(rect_rotated_surface.topleft[0], rect_rotated_surface.topleft[1],),
    #                Vector(rect_rotated_surface.topright[0], rect_rotated_surface.topright[1]),
    #                Vector(rect_rotated_surface.bottomright[0], rect_rotated_surface.bottomright[1]),
    #                Vector(rect_rotated_surface.bottomleft[0], rect_rotated_surface.bottomleft[1]),
    #                ]
    #     rect_vertices = corners
        
    #     for i in range(len(rect_vertices)):
    #         edge = rect_vertices[(i + 1) % len(rect_vertices)] - rect_vertices[i]
    #         normal = Vector(-edge.y, edge.x).normalize()

    #         rect_projections = [p.dot(normal) for p in rect_vertices]
    #         circle_projection = ball.position.dot(normal)

    #         min_rect = min(rect_projections)
    #         max_rect = max(rect_projections)

    #         if circle_projection + ball.radius < min_rect or circle_projection - ball.radius > max_rect:
    #             # es gibt eine separierende Axe!
    #             return False,normal

    #     return True,normal