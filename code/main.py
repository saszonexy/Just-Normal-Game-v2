import pygame
import sys
import os
import level2  # import file level2.py

# Inisialisasi pygame dan mixer
pygame.init()
pygame.mixer.init()

# Ukuran layar
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Platformer - Level 1")

# Warna
BG_COLOR = (219, 109, 87)
FLOOR_COLOR = (101, 0, 0)

# Path assets
assets_dir = os.path.join(os.path.dirname(__file__), "assets")

def load_image(name, scale=None, rotate=0):
    path = os.path.join(assets_dir, name)
    img = pygame.image.load(path).convert_alpha()
    if scale:
        img = pygame.transform.scale(img, scale)
    if rotate:
        img = pygame.transform.rotate(img, rotate)
    return img

# Load assets visual
bg_image = load_image("Back.png", (SCREEN_WIDTH, SCREEN_HEIGHT))
player_img = load_image("Player.png", (48, 96))
spike_img = load_image("Spike.png", (45, 45))
falling_spike_img = load_image("Spike.png", (45, 45), rotate=180)
door_img = load_image("Door.png", (100, 150))
retry_img = load_image("Retry.png", (45, 45))
back_img = load_image("Back.png", (45, 45))

# Load sound
jump_sound = pygame.mixer.Sound(os.path.join(assets_dir, "jump.mp3"))
death_sound = pygame.mixer.Sound(os.path.join(assets_dir, "death.mp3"))

# Objek posisi
player_rect = pygame.Rect(100, SCREEN_HEIGHT - 75 - 96, 48, 96)
player_velocity_y = 0
grounded = False
jump_count = 0
max_jumps = 2
gravity = 0.8
jump_strength = -16

spike_spacing = 280
spike_rects = []
for x in range(300, 1000, spike_spacing):
    spike_rects.append(pygame.Rect(x, SCREEN_HEIGHT - 75 - 45, 45, 45))
    spike_rects.append(pygame.Rect(x + 60, SCREEN_HEIGHT - 75 - 45, 45, 45))

floor_height = 75

falling_spike_rect = pygame.Rect(1050, 0, 45, 45)
falling_spike_speed = 20
falling_spike_triggered = False

retry_pos = pygame.Rect(700, 30, 45, 45)
back_pos = pygame.Rect(750, 30, 45, 45)
door_rect = pygame.Rect(1150, SCREEN_HEIGHT - 75 - 150, 100, 150)

clock = pygame.time.Clock()
running = True

# Gerakan
player_speed = 5
keys = {"left": False, "right": False}

def draw_floor():
    pygame.draw.rect(screen, FLOOR_COLOR, (0, SCREEN_HEIGHT - floor_height, SCREEN_WIDTH, floor_height))

def draw_header():
    font = pygame.font.SysFont("Arial", 24, bold=True)
    header_text = font.render("Press R to Retry | ESC to Quit", True, (255, 255, 255))
    screen.blit(header_text, (20, 20))
    screen.blit(retry_img, retry_pos)
    screen.blit(back_img, back_pos)

def reset_game():
    global player_rect, player_velocity_y, jump_count, falling_spike_triggered
    player_rect.topleft = (100, SCREEN_HEIGHT - 75 - 96)
    player_velocity_y = 0
    jump_count = 0
    falling_spike_rect.y = 0
    falling_spike_triggered = False

def play_death_animation():
    death_frames = []
    for i in range(1, 5):  # Player_dead1.png sampai Player_dead4.png
        frame = load_image(f"Died{i}.png", (48, 96))
        death_frames.append(frame)

    for frame in death_frames:
        screen.blit(bg_image, (0, 0))
        draw_floor()
        draw_header()
        for spike in spike_rects:
            screen.blit(spike_img, spike.topleft)
        screen.blit(falling_spike_img, falling_spike_rect)
        screen.blit(door_img, door_rect)
        screen.blit(frame, player_rect)
        pygame.display.update()
        pygame.time.delay(100)

while running:
    screen.fill(BG_COLOR)
    screen.blit(bg_image, (0, 0))
    draw_floor()
    draw_header()

    # Event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                keys["left"] = True
            elif event.key == pygame.K_RIGHT:
                keys["right"] = True
            elif event.key == pygame.K_SPACE and jump_count < max_jumps:
                player_velocity_y = jump_strength
                jump_count += 1
                grounded = False
                jump_sound.play()
            elif event.key == pygame.K_r:
                reset_game()
            elif event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                keys["left"] = False
            elif event.key == pygame.K_RIGHT:
                keys["right"] = False

    # Gerakan horizontal
    if keys["left"]:
        player_rect.x -= player_speed
    if keys["right"]:
        player_rect.x += player_speed

    # Gerakan vertikal
    player_velocity_y += gravity
    player_rect.y += player_velocity_y

    if player_rect.bottom >= SCREEN_HEIGHT - floor_height:
        player_rect.bottom = SCREEN_HEIGHT - floor_height
        player_velocity_y = 0
        grounded = True
        jump_count = 0

    # Trigger spike jatuh
    if not falling_spike_triggered and abs(player_rect.centerx - falling_spike_rect.centerx) <= 30:
        falling_spike_triggered = True

    if falling_spike_triggered:
        falling_spike_rect.y += falling_spike_speed
    if falling_spike_rect.y > SCREEN_HEIGHT:
        falling_spike_rect.y = 0
        falling_spike_triggered = False

    # Cek tabrakan spike
    for spike in spike_rects:
        if player_rect.colliderect(spike):
            death_sound.play()
            play_death_animation()
            print("Game Over!")
            pygame.time.wait(500)
            reset_game()

    # Spike jatuh kena player
    if falling_spike_rect.colliderect(player_rect):
        death_sound.play()
        play_death_animation()
        print("Game Over dari atas!")
        pygame.time.wait(500)
        reset_game()

    # Level selesai
    if player_rect.colliderect(door_rect):
        print("Next Level!")
        pygame.time.wait(500)
        level2.run_level2()  # Panggil level 2
        running = False


    # Gambar elemen
    screen.blit(player_img, player_rect)
    for spike in spike_rects:
        screen.blit(spike_img, spike.topleft)
    screen.blit(falling_spike_img, falling_spike_rect)
    screen.blit(door_img, door_rect)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
