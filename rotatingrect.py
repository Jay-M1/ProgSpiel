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
        rect_rotated_surface = rotated_surface.get_rect(center=(self.position.x, self.position.y))
        screen.blit(rotated_surface, rect_rotated_surface)
        # Weitere Zeichenanweisungen hier, je nach Bedarf
        return rect_rotated_surface
        

    def calculate_surface(self):
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(surface, (0, 255, 0), (0, 0, self.width, self.height))
        return pygame.transform.rotate(surface, self.angle)
    
    def calculate_vertices(self, rect):
        rect_rotated_surface = rect
        corners = [
                   Vector(rect_rotated_surface.topleft[0], rect_rotated_surface.topleft[1],),
                   Vector(rect_rotated_surface.topright[0], rect_rotated_surface.topright[1]),
                   Vector(rect_rotated_surface.bottomright[0], rect_rotated_surface.bottomright[1]),
                   Vector(rect_rotated_surface.bottomleft[0], rect_rotated_surface.bottomleft[1]),
                   ]
        return corners
        
    def is_collision(self, ball, rect):
        rect_vertices = self.calculate_vertices(rect)
        
        for i in range(len(rect_vertices)):
            edge = rect_vertices[(i + 1) % len(rect_vertices)] - rect_vertices[i]
            normal = Vector(-edge.y, edge.x).normalize()

            rect_projections = [p.dot(normal) for p in rect_vertices]
            circle_projection = ball.position.dot(normal)

            min_rect = min(rect_projections)
            max_rect = max(rect_projections)

            if circle_projection + ball.radius < min_rect or circle_projection - ball.radius > max_rect:
                # es gibt eine separierende Axe!
                return False,normal

        return True,normal
