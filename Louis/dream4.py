import pygame

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
PLATFORM_HEIGHT = 10
PLATFORM_WIDTH = 100
GRAVITY = 1
JUMP_STRENGTH = -15

# Colors
BACKGROUND_COLOR = (127, 148, 143)  # Hex #7F948F
GREEN = (0, 255, 0)

# Load images
dreamer_img = pygame.image.load("dreamer.png")
jumper_img = pygame.image.load("jumper.png")

# Initialize variables
player_pos = [400, 300]
player_vel = [0, 0]
clock = pygame.time.Clock()
facing_right = True  # New variable
platforms = [[200, 500, PLATFORM_WIDTH, PLATFORM_HEIGHT],
             [400, 400, PLATFORM_WIDTH, PLATFORM_HEIGHT],
             [600, 300, PLATFORM_WIDTH, PLATFORM_HEIGHT]]

# Set up display
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Wandering Reverie Demo')

# Main game loop
run = True
while run:
    clock.tick(60)
    win.fill(BACKGROUND_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player_pos[0] -= 5
        facing_right = False
    if keys[pygame.K_RIGHT]:
        player_pos[0] += 5
        facing_right = True
    if keys[pygame.K_SPACE]:
        player_vel[1] = JUMP_STRENGTH

    # Apply gravity
    player_vel[1] += GRAVITY

    # Move player
    player_pos[0] += player_vel[0]
    player_pos[1] += player_vel[1]

    # Collision with floor and platforms
    in_air = True
    if player_pos[1] > SCREEN_HEIGHT - dreamer_img.get_height():
        player_pos[1] = SCREEN_HEIGHT - dreamer_img.get_height()
        player_vel[1] = 0
        in_air = False

    for plat in platforms:
        if (player_pos[0] < plat[0] + plat[2] and player_pos[0] + dreamer_img.get_width() > plat[0] and
                player_pos[1] < plat[1] + plat[3] and player_pos[1] + dreamer_img.get_height() > plat[1]):
            player_pos[1] = plat[1] - dreamer_img.get_height()
            player_vel[1] = 0
            in_air = False

    # Draw platforms
    for plat in platforms:
        pygame.draw.rect(win, GREEN, plat)

    # Decide which sprite to use
    if in_air:
        current_sprite = jumper_img
    else:
        current_sprite = dreamer_img

    # Flip sprite if facing left
    if not facing_right:
        current_sprite = pygame.transform.flip(current_sprite, True, False)

    # Draw player
    win.blit(current_sprite, (player_pos[0], player_pos[1]))

    pygame.display.update()

pygame.quit()

