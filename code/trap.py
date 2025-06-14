import pygame
import os

class Spike:
    def __init__(self, x, y, scale=1.0):
        image_path = os.path.join(os.path.dirname(__file__), "../assets/Spike.png")
        self.original_image = pygame.image.load(image_path).convert_alpha()

        # Ubah ukuran jika perlu
        width = int(self.original_image.get_width() * scale)
        height = int(self.original_image.get_height() * scale)
        self.image = pygame.transform.scale(self.original_image, (width, height))

        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        pass  # disiapkan untuk future movement

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        

class FallingSpike:
    def __init__(self, x, y, speed=4):
        import os
        image_path = os.path.join(os.path.dirname(__file__), "../assets/Spike.png")
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.flip(self.original_image, False, True)  # dibalik vertikal
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > 600:
            self.rect.y = -self.rect.height  # reset ke atas

    def draw(self, screen):
        screen.blit(self.image, self.rect)
