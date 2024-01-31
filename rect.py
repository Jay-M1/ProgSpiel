import pygame
import random
import math
from vector import Vector



class Rect:
    def __init__(self, position, status):
        self.original_surface = pygame.Surface((100, 100), pygame.SRCALPHA)
        pygame.draw.rect(self.original_surface, (0, 255, 0), (0, 0, 100, 20))
        if status == "static":
            self.original_surface = pygame.transform.rotate(self.original_surface, 45)
        self.surface = self.original_surface
        self.position = position
        self.angle = 0 
        self.rect = self.surface.get_rect(center=self.position.int_tuple())

    def rotate(self, angle=0):
        self.angle += angle
        rotated_surface = pygame.transform.rotate(self.original_surface, self.angle)
        self.rect = rotated_surface.get_rect(center=(self.position).int_tuple())
        self.surface = rotated_surface
        
    def collide_with_ball(self, ball):
        
        if ball.position.x + ball.radius >= self.right and ball.position.y >= self.top:
            ball.velocity = ball.velocity * -0.8
        if ball.position.x - ball.radius <= self.left and ball.position.y >= self.top:
            ball.velocity = ball.velocity * -0.8