import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
PLATFORM_HEIGHT = 10
PLATFORM_WIDTH = 100
GRAVITY = 1
JUMP_STRENGTH = -15
NUM_PLATFORMS = 10  # Number of platforms to generate
NUM_STARS = 15  # Number of stars to generate

# Colors
BACKGROUND_COLOR = (127, 148, 143)  # Hex #7F948F
GREEN = (0, 255, 0)

# Load images
dreamer_img = pygame.image.load("dreamer.png")
jumper_img = pygame.image.load("jumper.png")
star_img = pygame.image.load("star.png")

# Initialize variables
player_pos = [400, 300]
player_vel = [0, 0]
clock = pygame.time.Clock()
facing_right = True
score = 0

# Generate platforms
platforms = []
for _ in range(NUM_PLATFORMS):
    x = random.randint(0, SCREEN_WIDTH - PLATFORM_WIDTH)
    y = random.randint(0, SCREEN_HEIGHT - PLATFORM_HEIGHT)
    platforms.append([x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT])

# Generate stars
stars = []
for _ in range(NUM_STARS):
    x = random.randint(0, SCREEN_WIDTH - star_img.get_width())
    y = random.randint(0, SCREEN_HEIGHT - star_img.get_height())
    stars.append([x, y])

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

    # Collect stars and keep score
    for star in stars:
        if (player_pos[0] < star[0] + star_img.get_width() and player_pos[0] + dreamer_img.get_width() > star[0] and
                player_pos[1] < star[1] + star_img.get_height() and player_pos[1] + dreamer_img.get_height() > star[1]):
            stars.remove(star)
            score += 1

    # Draw platforms
    for plat in platforms:
        pygame.draw.rect(win, GREEN, plat)

    # Draw stars
    for star in stars:
        win.blit(star_img, (star[0], star[1]))

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

    # Display score
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    win.blit(score_text, (10, 10))

    pygame.display.update()

pygame.quit()

