import pygame

class Player:
    def __init__(self, x, y):
        import os
        self.image = pygame.image.load(os.path.join(os.path.dirname(__file__), "../assets/Player.png")).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vel_y = 0
        self.on_ground = False

    def update(self):
        keys = pygame.key.get_pressed()
        dx = 0

        if keys[pygame.K_LEFT]:
            dx = -5
        if keys[pygame.K_RIGHT]:
            dx = 5
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = -15
            self.on_ground = False

        self.vel_y += 1  # gravity
        self.rect.y += self.vel_y

        if self.rect.bottom >= 560:  # batas tanah
            self.rect.bottom = 560
            self.vel_y = 0
            self.on_ground = True

        self.rect.x += dx

    def draw(self, screen):
        screen.blit(self.image, self.rect)
