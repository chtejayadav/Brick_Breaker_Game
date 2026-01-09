import pygame

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 900, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brick Breaker Game")

# Colors
WHITE = (255, 255, 255)
RED = (220, 60, 60)
BLUE = (80, 140, 255)
BLACK = (0, 0, 0)
GRAY = (40, 40, 40)

# Font
font = pygame.font.SysFont("arial", 26)

# Clock
clock = pygame.time.Clock()

# Paddle settings
paddle_width = 120
paddle_height = 15
paddle_x = WIDTH // 2 - paddle_width // 2
paddle_y = HEIGHT - 50
paddle_speed = 8

# Ball settings
ball_radius = 9
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_dx = 5
ball_dy = -5

# Brick settings
brick_rows = 5
brick_cols = 10
brick_width = 75
brick_height = 28
brick_gap = 6
bricks = []

for row in range(brick_rows):
    for col in range(brick_cols):
        x = col * (brick_width + brick_gap) + 60
        y = row * (brick_height + brick_gap) + 80
        bricks.append(pygame.Rect(x, y, brick_width, brick_height))

score = 0

# Gradient background
def draw_background():
    for y in range(HEIGHT):
        shade = int(20 + (y / HEIGHT) * 40)
        pygame.draw.line(screen, (shade, shade, shade), (0, y), (WIDTH, y))

# Game loop
running = True
while running:
    draw_background()

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Paddle movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle_x > 0:
        paddle_x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle_x < WIDTH - paddle_width:
        paddle_x += paddle_speed

    paddle = pygame.Rect(paddle_x, paddle_y, paddle_width, paddle_height)

    # Ball movement
    ball_x += ball_dx
    ball_y += ball_dy

    # Wall collision
    if ball_x - ball_radius <= 0 or ball_x + ball_radius >= WIDTH:
        ball_dx *= -1
    if ball_y - ball_radius <= 0:
        ball_dy *= -1

    # Paddle collision
    if paddle.collidepoint(ball_x, ball_y + ball_radius):
        ball_dy *= -1

    # Brick collision
    for brick in bricks[:]:
        if brick.collidepoint(ball_x, ball_y):
            bricks.remove(brick)
            ball_dy *= -1
            score += 10
            break

    # Game over
    if ball_y > HEIGHT:
        running = False

    # Draw paddle (rounded)
    pygame.draw.rect(screen, BLUE, paddle, border_radius=8)

    # Draw ball
    pygame.draw.circle(screen, WHITE, (ball_x, ball_y), ball_radius)

    # Draw bricks (with outline)
    for brick in bricks:
        pygame.draw.rect(screen, RED, brick, border_radius=5)
        pygame.draw.rect(screen, WHITE, brick, 1, border_radius=5)

    # Draw score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (20, 20))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
