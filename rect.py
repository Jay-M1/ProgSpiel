import pygame
import random
import math
from vector import Vector



# class Rect:
#     def __init__(self, position):
#         self.original_surface = pygame.Surface((100, 20), pygame.SRCALPHA)
#         pygame.draw.rect(self.original_surface, (0, 255, 0), (0, 0, 100, 20))
#         self.surface = self.original_surface
#         self.position = position
#         self.angle = 0 
#         self.rect = self.surface.get_rect(center=self.position.int_tuple())

#     def rotate(self, angle=0):
#         self.angle += angle
#         rotated_surface = pygame.transform.rotate(self.original_surface, self.angle)
#         self.rect = rotated_surface.get_rect(center=(self.position).int_tuple())
#         self.surface = rotated_surface

class Rect:
    def __init__(self, position, width, height):
        self.position = position
        self.width = width
        self.height = height
        self.vertices = self.calculate_vertices()

    def calculate_vertices(self):
        return [
            Vector(self.position.x, self.position.y),
            Vector(self.position.x + self.width, self.position.y),
            Vector(self.position.x + self.width, self.position.y + self.height),
            Vector(self.position.x, self.position.y + self.height)
        ]
        
    def is_collision(self, ball):
        rect_vertices = self.calculate_vertices()
        
        for i in range(len(rect_vertices)):
            edge = rect_vertices[(i + 1) % len(rect_vertices)] - rect_vertices[i]
            normal = Vector(-edge.y, edge.x).normalize()

            rect_projections = [p.dot(normal) for p in rect_vertices]
            circle_projection = ball.position.dot(normal)

            min_rect = min(rect_projections)
            max_rect = max(rect_projections)

            if circle_projection + ball.radius < min_rect or circle_projection - ball.radius > max_rect:
                return False,normal

        return True,normal
