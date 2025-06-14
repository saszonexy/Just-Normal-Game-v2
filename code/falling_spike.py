import pygame
import os

class FallingSpike:
    def __init__(self, x, y, speed=5):
        self.image = pygame.image.load(os.path.join(os.path.dirname(__file__), "../assets/Spike.png")).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.original_y = y
        self.speed = speed
        self.falling = False

    def update(self, player_rect):
        if not self.falling and self.rect.colliderect(player_rect.inflate(50, 0)):  # aktif jika pemain di bawahnya
            self.falling = True

        if self.falling:
            self.rect.y += self.speed

    def reset(self):
        self.rect.y = self.original_y
        self.falling = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)
