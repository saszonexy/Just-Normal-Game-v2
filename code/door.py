import pygame

class Door:
    def __init__(self, x, y):
        import os
        self.image = pygame.image.load(os.path.join(os.path.dirname(__file__), "../assets/Door.png")).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)
