import pygame
import os
import sys


def run_level2():
    pygame.init()
    pygame.mixer.init()

    SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Platformer - Level 2")

    assets_dir = os.path.join(os.path.dirname(__file__), "assets")

    def load_image(name, scale=None):
        path = os.path.join(assets_dir, name)
        img = pygame.image.load(path).convert_alpha()
        if scale:
            img = pygame.transform.scale(img, scale)
        return img

    bg_image = load_image("Back.png", (SCREEN_WIDTH, SCREEN_HEIGHT))
    player_img = load_image("Player.png", (48, 96))
    spike_img = load_image("Spike.png", (45, 45))
    door_img = load_image("Door.png", (100, 150))

    jump_sound = pygame.mixer.Sound(os.path.join(assets_dir, "jump.mp3"))
    death_sound = pygame.mixer.Sound(os.path.join(assets_dir, "death.mp3"))

    floor_height = 75
    gravity = 0.8
    jump_strength = -16
    player_speed = 5
    max_jumps = 2

    player_rect = pygame.Rect(100, SCREEN_HEIGHT - 75 - 96, 48, 96)
    player_velocity_y = 0
    jump_count = 0

    spike_rects = [
        pygame.Rect(600, SCREEN_HEIGHT - 75 - 45, 45, 45)
    ]

    door_rect = pygame.Rect(1100, SCREEN_HEIGHT - 75 - 150, 100, 150)

    clock = pygame.time.Clock()
    keys = {"left": False, "right": False}
    running = True

    while running:
        screen.fill((100, 149, 237))
        screen.blit(bg_image, (0, 0))
        pygame.draw.rect(screen, (30, 30, 30), (0, SCREEN_HEIGHT - floor_height, SCREEN_WIDTH, floor_height))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    keys["left"] = True
                elif event.key == pygame.K_RIGHT:
                    keys["right"] = True
                elif event.key == pygame.K_SPACE and jump_count < max_jumps:
                    player_velocity_y = jump_strength
                    jump_count += 1
                    jump_sound.play()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    keys["left"] = False
                elif event.key == pygame.K_RIGHT:
                    keys["right"] = False

        if keys["left"]:
            player_rect.x -= player_speed
        if keys["right"]:
            player_rect.x += player_speed

        player_velocity_y += gravity
        player_rect.y += player_velocity_y

        if player_rect.bottom >= SCREEN_HEIGHT - floor_height:
            player_rect.bottom = SCREEN_HEIGHT - floor_height
            player_velocity_y = 0
            jump_count = 0

        for spike in spike_rects:
            if player_rect.colliderect(spike):
                death_sound.play()
                pygame.time.wait(500)
                player_rect.topleft = (100, SCREEN_HEIGHT - 75 - 96)
                jump_count = 0

        if player_rect.colliderect(door_rect):
            print("Level 2 Selesai!")
            pygame.time.wait(1000)
            running = False

        screen.blit(player_img, player_rect)
        for spike in spike_rects:
            screen.blit(spike_img, spike.topleft)
        screen.blit(door_img, door_rect)

        pygame.display.update()
        clock.tick(60)
