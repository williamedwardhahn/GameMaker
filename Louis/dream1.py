import pygame

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
PLAYER_SIZE = 50
PLATFORM_HEIGHT = 10
PLATFORM_WIDTH = 100
GRAVITY = 1
JUMP_STRENGTH = -15

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

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
    win.fill(WHITE)

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
    if player_pos[1] > SCREEN_HEIGHT - PLAYER_SIZE:
        player_pos[1] = SCREEN_HEIGHT - PLAYER_SIZE
        player_vel[1] = 0

    for plat in platforms:
        if (player_pos[0] < plat[0] + plat[2] and player_pos[0] + PLAYER_SIZE > plat[0] and
                player_pos[1] < plat[1] + plat[3] and player_pos[1] + PLAYER_SIZE > plat[1]):
            player_pos[1] = plat[1] - PLAYER_SIZE
            player_vel[1] = 0

    # Draw platforms
    for plat in platforms:
        pygame.draw.rect(win, GREEN, plat)

    # Draw player
    pygame.draw.rect(win, BLUE, (player_pos[0], player_pos[1], PLAYER_SIZE, PLAYER_SIZE))

    pygame.display.update()

pygame.quit()

