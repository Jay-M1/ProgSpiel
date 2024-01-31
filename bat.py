import pygame
import random   
from vector import Vector





class RotatingObject(pygame.sprite.Sprite):
    def __init__(self, position, pivot, rotation, direction):
        super().__init__()
        self.image = pygame.Surface((100, 100), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (0, 255, 0), (0, 0, 50, 200)) #pygame.image.load("basebat_blue.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 135))
        self.rotation = rotation
        self.image = pygame.transform.rotate(self.image, self.rotation)
        self.original_image = self.image
        if direction == "right":
            self.rect = self.image.get_rect(midright = (position.x - pivot.x, position.y - pivot.y))
        if direction == "left":
            self.rect = self.image.get_rect(midleft = (position.x - pivot.x, position.y - pivot.y))
        self.position = position
        self.pivot = pivot
        self.angle = 0
        
    def update_right(self, is_aktiv):
        if is_aktiv:
            if self.angle < -35:
                return False
            
            self.angle -= 4
            image_rect = self.original_image.get_rect(midright = (self.position.x - self.pivot.x, self.position.y - self.pivot.y))
            offset_center_to_pivot = self.position - Vector(image_rect.center[0], image_rect.center[1])
            rotated_offset = offset_center_to_pivot.rotate(-self.angle) # dreht in die andere Richtung wie pygame.transform.rotate()
            rotated_image_center = (self.position.x - rotated_offset.x, self.position.y - rotated_offset.y)
            self.image = pygame.transform.rotate(self.original_image, self.angle)
            self.rect = self.image.get_rect(center = rotated_image_center)
            return True
        else:
            if self.angle <= 20:
                
                self.angle += 4
                image_rect = self.original_image.get_rect(midright = (self.position.x - self.pivot.x, self.position.y - self.pivot.y))
                offset_center_to_pivot = self.position - Vector(image_rect.center[0], image_rect.center[1])
                rotated_offset = offset_center_to_pivot.rotate(-self.angle) # dreht in die andere Richtung wie pygame.transform.rotate()
                rotated_image_center = (self.position.x - rotated_offset.x, self.position.y - rotated_offset.y)
                self.image = pygame.transform.rotate(self.original_image, self.angle)
                self.rect = self.image.get_rect(center = rotated_image_center)
            return False
        
    def update_left(self, is_aktiv):
        if is_aktiv:
            if self.angle > 35:
                return False
            
            self.angle += 4
            image_rect = self.original_image.get_rect(midleft = (self.position.x - self.pivot.x, self.position.y - self.pivot.y))
            offset_center_to_pivot = self.position - Vector(image_rect.center[0], image_rect.center[1])
            rotated_offset = offset_center_to_pivot.rotate(-self.angle) # dreht in die andere Richtung wie pygame.transform.rotate()
            rotated_image_center = (self.position.x - rotated_offset.x, self.position.y - rotated_offset.y)
            self.image = pygame.transform.rotate(self.original_image, self.angle)
            self.rect = self.image.get_rect(center = rotated_image_center)
            self.mask = pygame.mask.from_surface(self.image)
            return True
        else:
            if self.angle >= -20:
                
                self.angle -= 4
                image_rect = self.original_image.get_rect(midleft = (self.position.x - self.pivot.x, self.position.y - self.pivot.y))
                offset_center_to_pivot = self.position - Vector(image_rect.center[0], image_rect.center[1])
                rotated_offset = offset_center_to_pivot.rotate(-self.angle) # dreht in die andere Richtung wie pygame.transform.rotate()
                rotated_image_center = (self.position.x - rotated_offset.x, self.position.y - rotated_offset.y)
                self.image = pygame.transform.rotate(self.original_image, self.angle)
                self.rect = self.image.get_rect(center = rotated_image_center)
                self.mask = pygame.mask.from_surface(self.image)
            return False