import pygame
from vector import Vector
import math
from rect import Rect



# class Rotating_rect:
#     def __init__(self, position, pivot, rotation, width, height):
#         self.position = Vector(position[0], position[1])
#         self.pivot = Vector(pivot[0], pivot[1])
#         self.rotation = rotation
#         self.width = width
#         self.height = height
#         self.angle = 0

#     def rotate(self, direction, is_active):
#         if is_active:
#             self.angle += 4 * direction  # 4 Grad pro Frame (kann angepasst werden)

#     def draw(self, screen):
#         rotated_surface = self.calculate_surface()
#         rect_rotated_surface = rotated_surface.get_rect(center=(self.position.x, self.position.y))
#         screen.blit(rotated_surface, rect_rotated_surface)
#         # Weitere Zeichenanweisungen hier, je nach Bedarf
#         return rect_rotated_surface
        

#     def calculate_surface(self):
#         surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
#         pygame.draw.rect(surface, (0, 255, 0), (0, 0, self.width, self.height))
#         return pygame.transform.rotate(surface, self.angle)
    
#     def calculate_vertices(self, rect):
#         rect_rotated_surface = rect
#         corners = [
#                    Vector(rect_rotated_surface.topleft[0], rect_rotated_surface.topleft[1],),
#                    Vector(rect_rotated_surface.topright[0], rect_rotated_surface.topright[1]),
#                    Vector(rect_rotated_surface.bottomright[0], rect_rotated_surface.bottomright[1]),
#                    Vector(rect_rotated_surface.bottomleft[0], rect_rotated_surface.bottomleft[1]),
#                    ]
#         return corners
        
#     def is_collision(self, ball, rect):
#         rect_vertices = self.calculate_vertices(rect)
        
#         for i in range(len(rect_vertices)):
#             edge = rect_vertices[(i + 1) % len(rect_vertices)] - rect_vertices[i]
#             normal = Vector(-edge.y, edge.x).normalize()

#             rect_projections = [p.dot(normal) for p in rect_vertices]
#             circle_projection = ball.position.dot(normal)

#             min_rect = min(rect_projections)
#             max_rect = max(rect_projections)

#             if circle_projection + ball.radius < min_rect or circle_projection - ball.radius > max_rect:
#                 # es gibt eine separierende Axe!
#                 return False,normal

#         return True,normal

class RectangleDrawer:
    def __init__(self, screen):
        self.screen = screen

    def draw_rectangle(self, x, y, width, height, color, rotation=0):
    
        points = self.calculate_vertices(x, y, width, height, rotation)
        points = [(int(point.x), int(point.y)) for point in points]
        pygame.draw.polygon(self.screen, color, points)
        return points

    def calculate_vertices(self, x, y, width, height, rotation=0):
        
        vertices = []

        radius = math.sqrt((height / 2)**2 + (width / 2)**2)

    
        angle = math.atan2(height / 2, width / 2)

        angles = [angle, -angle + math.pi, angle + math.pi, -angle]
        
        rot_radians = (math.pi / 180) * rotation

        for angle in angles:
            y_offset = -1 * radius * math.sin(angle + rot_radians)
            x_offset = radius * math.cos(angle + rot_radians)
            vertices.append(Vector(x + x_offset, y + y_offset))

        return vertices

    def is_collision(self, ball, x, y, width, height, rotation=0):
        rect_vertices = self.calculate_vertices(x, y, width, height, rotation)
        
        # Erstelle ein Rechteck um den Ball
        ball_rect = Rect(Vector(ball.position.x - ball.radius, ball.position.y - ball.radius),
                        ball.radius * 2, ball.radius * 2)

        for i in range(len(rect_vertices)):
            # Berechne die Kante des Rechtecks als Vektor
            edge = Vector(rect_vertices[(i + 1) % len(rect_vertices)].x - rect_vertices[i].x, 
              rect_vertices[(i + 1) % len(rect_vertices)].y - rect_vertices[i].y)
            normal = Vector(-edge.y, edge.x).normalize()

            # Berechne Projektionen für das Rechteck und das Ball-Rechteck
            rect_projections = [p.dot(normal) for p in rect_vertices]
            ball_rect_projections = [p.dot(normal) for p in ball_rect.calculate_vertices()]


            min_rect = min(rect_projections)
            max_rect = max(rect_projections)
            min_ball_rect = min(ball_rect_projections)
            max_ball_rect = max(ball_rect_projections)

            # Überprüfe die Kollision zwischen dem Ball-Rechteck und dem Rechteck
            if max_ball_rect < min_rect or min_ball_rect > max_rect:
                # Es gibt eine separierende Achse!
                return False, normal

        # Wenn keine separierende Achse gefunden wurde, gibt es eine Kollision
        return True, normal