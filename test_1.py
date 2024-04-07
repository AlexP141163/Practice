import pygame
import sys

# Инициализация Pygame
pygame.init()
pygame.font.init()

clock = pygame.time.Clock()
fps = 60

# Настройки экрана
screen_width, screen_height = 1280, 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Игра Арконоид")

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
brick_colors = [(255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255)]

# Загрузка и настройка звуков
sound_effects = { 'hit': pygame.mixer.Sound("sound/sound_1.wav"),
                  'wall': pygame.mixer.Sound("sound/sound_2.wav"),
                  'paddle': pygame.mixer.Sound("sound/sound_3.wav"),
                  'game_over': pygame.mixer.Sound("sound/sound_4.wav") }
for sound in sound_effects.values():
    sound.set_volume(0.5)

# Инициализация игровых объектов
paddle = pygame.Rect(screen_width // 2 - 50, screen_height - 40, 100, 20)
ball = pygame.Vector2(screen_width // 2, paddle.y - 10)
ball_velocity = pygame.Vector2(4, -4)
bricks = [((col * ((screen_width // 10) - 5) + 5, row * 25 + 5), brick_colors[row % len(brick_colors)])
          for row in range(5) for col in range(10)]

font = pygame.font.SysFont(None, 46)
score = 0
score_text = font.render('Счет: 0', True, WHITE)

# Функция для отрисовки кирпичей
def draw_bricks():
    for brick, color in bricks:
        pygame.draw.rect(screen, color, pygame.Rect(brick, ((screen_width // 10) - 5, 20)))

# Основной цикл игры
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.move_ip(-6, 0)
    if keys[pygame.K_RIGHT] and paddle.right < screen_width:
        paddle.move_ip(6, 0)

    ball += ball_velocity
    if ball.x <= 0 or ball.x >= screen_width:
        ball_velocity.x = -ball_velocity.x
        sound_effects['wall'].play()
    if ball.y <= 0:
        ball_velocity.y = -ball_velocity.y
        sound_effects['wall'].play()
    if ball.y >= screen_height:
        sound_effects['game_over'].play()
        running = False

    # Обработка столкновения мяча с платформой
    if paddle.collidepoint(ball.x, ball.y):
        ball_velocity.y = -ball_velocity.y
        sound_effects['paddle'].play()

    # Обработка столкновения мяча с кирпичами
    bricks = [(brick, color) for brick, color in bricks if not pygame.Rect(brick, ((screen_width // 10) - 5, 20)).collidepoint(ball)]
    if len(bricks) < 5 * 10:  # Если мяч ударил кирпич
        ball_velocity.y = -ball_velocity.y
        score += 10
        score_text = font.render(f'Счет: {score}', True, WHITE)
        sound_effects['hit'].play()

    # Отрисовка
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, paddle)
    pygame.draw.circle(screen, BLUE, (int(ball.x), int(ball.y)), 10)
    draw_bricks()
    screen.blit(score_text, (5, 5))

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
sys.exit()