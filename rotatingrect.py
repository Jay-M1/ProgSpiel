import pygame
from vector import Vector
import math



class Rotating_rect:
    def __init__(self, position, pivot, rotation, width, height):
        self.position = Vector(position[0], position[1])
        self.pivot = Vector(pivot[0], pivot[1])
        self.rotation = rotation
        self.width = width
        self.height = height
        self.angle = 0

    def rotate(self, direction, is_active):
        if is_active:
            self.angle += 4 * direction  # 4 Grad pro Frame (kann angepasst werden)

    def draw(self, screen):
        rotated_surface = self.calculate_surface()
        screen.blit(rotated_surface, rotated_surface.get_rect(center=(self.position.x, self.position.y)))
        # Weitere Zeichenanweisungen hier, je nach Bedarf

    def calculate_surface(self):
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(surface, (0, 255, 0), (0, 0, self.width, self.height))
        return pygame.transform.rotate(surface, self.angle)
