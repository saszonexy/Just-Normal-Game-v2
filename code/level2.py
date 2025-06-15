import pygame, sys, os
from level3 import run_level3

def run_level2():
    pygame.init()
    SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Platformer - Level 2")

    clock = pygame.time.Clock()
    assets_dir = os.path.join(os.path.dirname(__file__), "assets")

    player_img = pygame.image.load(os.path.join(assets_dir, "Player.png")).convert_alpha()
    saw_img = pygame.image.load(os.path.join(assets_dir, "Saw.png")).convert_alpha()
    door_img = pygame.image.load(os.path.join(assets_dir, "Door.png")).convert_alpha()
    spike_img = pygame.image.load(os.path.join(assets_dir, "Spike.png")).convert_alpha()
    back_img = pygame.image.load(os.path.join(assets_dir, "Back.png")).convert_alpha()
    retry_img = pygame.image.load(os.path.join(assets_dir, "Retry.png")).convert_alpha()

    player_img = pygame.transform.scale(player_img, (45,75))
    saw_img = pygame.transform.scale(saw_img, (60, 60))
    door_img = pygame.transform.scale(door_img, (70, 100))
    spike_img = pygame.transform.scale(spike_img, (20, 20))
    back_img = pygame.transform.scale(back_img, (30, 30))
    retry_img = pygame.transform.scale(retry_img, (30, 30))

    jump_sound = pygame.mixer.Sound(os.path.join(assets_dir, "jump.mp3"))
    death_sound = pygame.mixer.Sound(os.path.join(assets_dir, "death.mp3"))
    door_open_sound = pygame.mixer.Sound(os.path.join(assets_dir, "opendoor-.mp3"))

    COLOR_BG = (219, 109, 87)
    COLOR_PLATFORM = (101, 0, 0)

    font_big = pygame.font.Font(pygame.font.match_font('freesansbold'), 100)
    header_rect = pygame.Rect(0, 0, SCREEN_WIDTH, 60)
    back_button_rect = back_img.get_rect(topleft=(10, 5))
    retry_button_rect = retry_img.get_rect(topleft=(70, 5))

    player_rect = player_img.get_rect(topleft=(50, 270))
    player_y_velocity = 0
    gravity = 1
    is_jumping = False

    platform_data = [
        (0, 320, 250, 400),
        (350, 0, 380, 470),
        (240, 640, 90, 80),
        (330, 570, 950, 200),
        (0, SCREEN_HEIGHT - 10, SCREEN_WIDTH, 10)
    ]
    platforms = [pygame.Rect(data) for data in platform_data]

    saw_rect = saw_img.get_rect()
    saw_rect.midbottom = (platforms[0].right, platforms[0].top)
    saw_pos = pygame.Vector2(saw_rect.topleft)
    saw_speed = 3.5

    patrol_points = [
        pygame.Vector2(platforms[0].right, platforms[0].top - 50),
        pygame.Vector2(platforms[1].left - 60, platforms[1].top + 20),
        pygame.Vector2(platforms[0].right, platforms[0].top - 50),
        pygame.Vector2(platforms[3].left - 50, platforms[3].top - 50),
        pygame.Vector2(platforms[3].centerx, platforms[3].top - 50),
        pygame.Vector2(platforms[3].left - 50, platforms[3].top - 50),
        pygame.Vector2(platforms[0].right, platforms[0].top - 50),
    ]
    patrol_index = 0

    door_rect = door_img.get_rect()
    door_rect.midbottom = (1150, platforms[3].top)

    spike_rects = []
    for i in range(3):
        spike_rect = spike_img.get_rect()
        spike_rect.midbottom = (platforms[2].left + 15 + i * 30, platforms[2].top)
        spike_rects.append(spike_rect)

    spike_visible = False
    spike_timer = 0
    spike_interval = 2000

    def show_game_over():
        death_sound.play()
        blended_color = (
            (COLOR_PLATFORM[0] + COLOR_BG[0]) // 2,
            (COLOR_PLATFORM[1] + COLOR_BG[1]) // 2,
            (COLOR_PLATFORM[2] + COLOR_BG[2]) // 2
        )
        shadow_surface = font_big.render("GAME OVER", True, (0, 0, 0))
        shadow_rect = shadow_surface.get_rect(center=(SCREEN_WIDTH // 2 + 5, SCREEN_HEIGHT // 2 + 5))
        screen.blit(shadow_surface, shadow_rect)
        text_surface = font_big.render("GAME OVER", True, blended_color)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text_surface, text_rect)
        pygame.display.update()
        pygame.time.wait(2000)

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
            screen.blit(frame, player_rect)
            pygame.display.update()
            pygame.time.delay(100)

    running = True
    while running:
        dt = clock.tick(60)
        screen.fill(COLOR_BG)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if back_button_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()  # Ganti dengan return jika ingin kembali ke menu
                elif retry_button_rect.collidepoint(mouse_pos):
                    run_level2()
                    return  # Agar tidak ada duplikasi game loop

        keys = pygame.key.get_pressed()
        move_x = 0
        if keys[pygame.K_LEFT]: move_x = -5
        if keys[pygame.K_RIGHT]: move_x = 5
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

        player_y_velocity += gravity
        player_rect.y += player_y_velocity
        for plat in platforms:
            if player_rect.colliderect(plat):
                if player_y_velocity > 0:
                    player_rect.bottom = plat.top
                    player_y_velocity = 0
                    is_jumping = False

        target = patrol_points[patrol_index]
        if (target - saw_pos).length() != 0:
            direction = (target - saw_pos).normalize()
            saw_pos += direction * saw_speed
            saw_rect.topleft = (round(saw_pos.x), round(saw_pos.y))

        if (target - saw_pos).length() < 3:
            patrol_index = (patrol_index + 1) % len(patrol_points)

        if player_rect.colliderect(saw_rect):
            play_death_animation()
            show_game_over()
            run_level2()
            return

        if player_rect.colliderect(door_rect):
            door_open_sound.play()
            pygame.time.wait(300)
            running = False
            run_level3()
            return

        spike_timer += dt
        if spike_timer >= spike_interval:
            spike_visible = not spike_visible
            spike_timer = 0

        if spike_visible:
            for spike in spike_rects:
                if player_rect.colliderect(spike):
                    play_death_animation()
                    show_game_over()
                    run_level2()
                    return

        for plat in platforms:
            pygame.draw.rect(screen, COLOR_PLATFORM, plat)

        screen.blit(player_img, player_rect)
        screen.blit(saw_img, saw_rect)
        screen.blit(door_img, door_rect)

        if spike_visible:
            for spike in spike_rects:
                screen.blit(spike_img, spike)

        pygame.draw.rect(screen, (101, 0, 0), header_rect)
        screen.blit(back_img, back_button_rect)
        screen.blit(retry_img, retry_button_rect)

        pygame.display.update()
