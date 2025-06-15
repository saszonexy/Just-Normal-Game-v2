import pygame, sys, os, random

def run_level3():
    pygame.init()
    SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Platformer - Level 3")
    clock = pygame.time.Clock()

    assets_dir = os.path.join(os.path.dirname(__file__), "assets")

    # Load images
    player_img = pygame.image.load(os.path.join(assets_dir, "Player.png")).convert_alpha()
    door_img = pygame.image.load(os.path.join(assets_dir, "Door.png")).convert_alpha()
    spike_img = pygame.image.load(os.path.join(assets_dir, "Spike.png")).convert_alpha()
    button_img = pygame.image.load(os.path.join(assets_dir, "Buttonground.png")).convert_alpha()
    trampoline_img = pygame.image.load(os.path.join(assets_dir, "Trampoline.png")).convert_alpha()
    retry_img = pygame.image.load(os.path.join(assets_dir, "Retry.png")).convert_alpha()
    back_img = pygame.image.load(os.path.join(assets_dir, "Back.png")).convert_alpha()
    extra_button_img = pygame.image.load(os.path.join(assets_dir, "Buttonground.png")).convert_alpha()

    # Load sounds
    jump_sound = pygame.mixer.Sound(os.path.join(assets_dir, "jump.mp3"))
    death_sound = pygame.mixer.Sound(os.path.join(assets_dir, "death.mp3"))
    door_sound = pygame.mixer.Sound(os.path.join(assets_dir, "opendoor-.mp3"))

    # Resize images
    player_img = pygame.transform.scale(player_img, (45, 75))
    door_img = pygame.transform.scale(door_img, (70, 100))
    spike_img = pygame.transform.scale(spike_img, (25, 25))
    button_img = pygame.transform.scale(button_img, (60, 20))
    trampoline_img = pygame.transform.scale(trampoline_img, (60, 20))
    retry_img = pygame.transform.scale(retry_img, (30, 30))
    back_img = pygame.transform.scale(back_img, (30, 30))
    extra_button_img = pygame.transform.scale(extra_button_img, (50, 50))

    # Colors
    COLOR_TOP = (101, 0, 0)
    COLOR_BOTTOM = (219, 138, 114)
    COLOR_PLATFORM = (101, 0, 0)
    COLOR_BG = COLOR_TOP

    font_big = pygame.font.Font(pygame.font.match_font('freesansbold'), 50)

    player_rect = player_img.get_rect(topleft=(50, 565))
    player_y_velocity = 0
    gravity = 1
    is_jumping = False

    # Platforms
    platforms = [
        pygame.Rect(0, 450, 300, 400),
        pygame.Rect(300, 560, 120, 330),
        pygame.Rect(420, 450, 860, 400),
    ]

    door_rect = door_img.get_rect(midbottom=(1200, 450))
    button_rect = button_img.get_rect(topleft=(1050, 430))
    trampoline1_rect = trampoline_img.get_rect(topleft=(240, 430))
    trampoline2_rect = trampoline_img.get_rect(topleft=(340, 540))

    spike_positions = []
    spike_timer = 0
    spike_interval = 4000

    # Header button positions — tukar posisi
    back_rect = back_img.get_rect(topleft=(10, 10))
    retry_rect = retry_img.get_rect(topleft=(70, 10))
    extra_button_rect = extra_button_img.get_rect(topleft=(130, 10))

    header_rect = pygame.Rect(0, 0, SCREEN_WIDTH, 120)

    def play_death_animation():
        frames = []
        for i in range(1, 5):
            img = pygame.image.load(os.path.join(assets_dir, f"Died{i}.png")).convert_alpha()
            img = pygame.transform.scale(img, (60, 65))
            frames.append(img)
        for frame in frames:
            screen.fill(COLOR_BG)
            for p in platforms:
                pygame.draw.rect(screen, COLOR_PLATFORM, p)
            pygame.draw.rect(screen, COLOR_TOP, header_rect)
            screen.blit(frame, player_rect)
            screen.blit(back_img, back_rect)
            screen.blit(retry_img, retry_rect)
            screen.blit(extra_button_img, extra_button_rect)
            pygame.display.update()
            pygame.time.delay(100)

    running = True
    while running:
        dt = clock.tick(60)
        screen.fill(COLOR_TOP)
        pygame.draw.rect(screen, COLOR_BOTTOM, (0, 120, SCREEN_WIDTH, SCREEN_HEIGHT - 120))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                elif retry_rect.collidepoint(event.pos):
                    run_level3()
                    return
                elif extra_button_rect.collidepoint(event.pos):
                    print("Extra Button clicked!")

        keys = pygame.key.get_pressed()
        move_x = 0
        if keys[pygame.K_LEFT]:
            move_x = -5
        if keys[pygame.K_RIGHT]:
            move_x = 5
        if keys[pygame.K_SPACE] and not is_jumping:
            player_y_velocity = -18
            is_jumping = True
            jump_sound.play()

        player_rect.x += move_x
        for plat in platforms:
            if player_rect.colliderect(plat):
                if move_x > 0:
                    player_rect.right = plat.left
                elif move_x < 0:
                    player_rect.left = plat.right

        # Cegah masuk ke header
        if player_rect.colliderect(header_rect):
            player_rect.top = header_rect.bottom

        player_y_velocity += gravity
        player_rect.y += player_y_velocity
        for plat in platforms:
            if player_rect.colliderect(plat):
                if player_y_velocity > 0:
                    player_rect.bottom = plat.top
                    player_y_velocity = 0
                    is_jumping = False

        if player_rect.colliderect(button_rect):
            player_y_velocity = -30
            is_jumping = True
            jump_sound.play()

        for tramp in [trampoline1_rect, trampoline2_rect]:
            if player_rect.colliderect(tramp):
                player_y_velocity = -25
                is_jumping = True
                jump_sound.play()

        spike_timer += dt
        if spike_timer >= spike_interval:
            spike_positions = []
            for _ in range(4):
                x = random.randint(450, 1200)
                y = 450 - 25
                spike_positions.append(pygame.Rect(x, y, 25, 25))
            spike_timer = 0

        for spike_rect in spike_positions:
            if player_rect.colliderect(spike_rect):
                death_sound.play()
                play_death_animation()
                text_surface = font_big.render("GAME OVER", True, (255, 255, 255))
                screen.blit(text_surface, (SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 - 50))
                pygame.display.update()
                pygame.time.delay(1000)
                player_rect.topleft = (50, 565)
                player_y_velocity = 0

        if player_rect.colliderect(door_rect):
            door_sound.play()
            pygame.time.delay(500)
            running = False

        for plat in platforms:
            pygame.draw.rect(screen, COLOR_PLATFORM, plat)

        screen.blit(button_img, button_rect)
        screen.blit(trampoline_img, trampoline1_rect)
        screen.blit(trampoline_img, trampoline2_rect)
        for spike_rect in spike_positions:
            screen.blit(spike_img, spike_rect)
        screen.blit(door_img, door_rect)
        screen.blit(player_img, player_rect)

        # Header
        pygame.draw.rect(screen, COLOR_TOP, header_rect)
        text_surface = font_big.render("LEVEL 3", True, (255, 200, 200))
        screen.blit(text_surface, (SCREEN_WIDTH - 220, 15))

        screen.blit(back_img, back_rect)
        screen.blit(retry_img, retry_rect)
        screen.blit(extra_button_img, extra_button_rect)

        pygame.display.update()

if __name__ == "__main__":
    run_level3()
