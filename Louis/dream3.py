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
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BACKGROUND_COLOR = (127, 148, 143)  # Hex #7F948F

# Load images
dreamer_img = pygame.image.load("dreamer.png")
jumper_img = pygame.image.load("jumper.png")

# Set up display
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Wandering Reverie Demo')

# Initialize variables
player_pos = [400, 300]
player_vel = [0, 0]
clock = pygame.time.Clock()
platforms = [[200, 500, PLATFORM_WIDTH, PLATFORM_HEIGHT],
             [400, 400, PLATFORM_WIDTH, PLATFORM_HEIGHT],
             [600, 300, PLATFORM_WIDTH, PLATFORM_HEIGHT]]

# Main game loop
run = True
while run:
    clock.tick(60)
    win.fill(BACKGROUND_COLOR)  # Set background color


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player_pos[0] -= 5
    if keys[pygame.K_RIGHT]:
        player_pos[0] += 5
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

    # Draw player
    if in_air:
        win.blit(jumper_img, (player_pos[0], player_pos[1]))
    else:
        win.blit(dreamer_img, (player_pos[0], player_pos[1]))

    pygame.display.update()

pygame.quit()

