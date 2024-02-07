import pygame
from vector import Vector
import math
from rect import Rect


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