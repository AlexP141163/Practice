import pygame
import sys
import time
pygame.font.init()
# Инициализация 'Pygame':
pygame.init()
clock = pygame.time.Clock()  # Исправил опечатку с 'clock' на 'clock'
fps = 60
score = 0  # Инициализация переменной счет в игре:
score_fail = 0 # Инициализация переменной счета промаха в игре:
font = pygame.font.SysFont(None, 46)  # Инициализируем модуль шрифтов:
# Загрузим звуки игры:
sound_1 = pygame.mixer.Sound("sound/sound_1.wav")
sound_2 = pygame.mixer.Sound("sound/sound_2.wav")
sound_3 = pygame.mixer.Sound("sound/sound_3.wav")
sound_4 = pygame.mixer.Sound("sound/sound_4.wav")
# Установка громкости звуков:
sound_1.set_volume(0.5)
sound_2.set_volume(0.5)
sound_3.set_volume(0.5)
sound_4.set_volume(0.5)

# Определяем переменную в которой будет храниться размер рабочего окна:
screen_width, screen_height = 1280, 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Игра Арконоид")

# Цвета:
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
# Определение цветов кирпичей
brick_colors = [(255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255)]

# Параметры кирпичей:
brick_rows = 5
brick_cols = 10
brick_gap = 5 # Промежуток между кирпичами:
brick_width = (screen_width // brick_cols) - brick_gap
brick_height = 20
# Список кирпичей:

bricks = [((col * (brick_width + brick_gap), row * (brick_height + brick_gap)), brick_colors[row % len(brick_colors)]) for row in range(brick_rows) for col in range(brick_cols)]

# параметры платформы:
paddle_width, paddle_height = 100, 10
paddle_x = (screen_width - paddle_width) // 2
paddle_y = screen_height - (paddle_height * 2)
paddle_speed = 6

# Параметры мяча:
ball_radius = 10
ball_x = screen_width // 2
ball_y = paddle_y - ball_radius
ball_speed_x = 4
ball_speed_y = -4

# Запуск основного цикла игры:
running = True
while running:
    # Обработка событий:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Движение платформы:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle_x > 0: # 'paddle_x > 0' не дает платформе выйти за пределы экрана:
        paddle_x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle_x < screen_width - paddle_width:
        paddle_x += paddle_speed

# Движение мяча:
    ball_x += ball_speed_x
    ball_y += ball_speed_y

# Столкновение с краями экрана:
    if ball_x <= 0 or ball_x >= screen_width:
        ball_speed_x = - ball_speed_x
        sound_2.play() # Столкновение меча с краями экрана:
    if ball_y <= 0:
        ball_speed_y = - ball_speed_y
        sound_2.play()  # Столкновение меча с краями экрана:
    if ball_y + ball_radius >= screen_height:
# Сброс мяча:
        ball_x, ball_y = screen_width // 2, paddle_y - ball_radius
        ball_speed_y = - ball_speed_y
        score -= 50  # За промах отнимаем 50 очков:
        score_fail += 1
        if score_fail >= 3:
            sound_4.play()  # Воспроизведение звука завершения игры
            screen.fill(BLACK)  # Очистка экрана
            final_score_text = font.render('Итоговый счёт: ' + str(score), True, WHITE)
            final_fails_text = font.render('Количество промахов: ' + str(score_fail), True, WHITE)
            screen.blit(final_score_text, (screen_width // 2 - 100, screen_height // 2 - 50))
            screen.blit(final_fails_text, (screen_width // 2 - 100, screen_height // 2))
        # Добавьте код для вывода текста "Вы проиграли":
            game_over_text = font.render('  Вы проиграли', True, WHITE)
            text_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2 + 70))  # Центрирование текста
            screen.blit(game_over_text, text_rect)
            pygame.display.flip()  # Обновляем экран для отображения сообщения
            time.sleep(5)  # Пауза перед выходом для прочтения сообщения
            running = False

    for brick, color in bricks:
        brick_rect = pygame.Rect(brick[0], brick[1], brick_width, brick_height)
        pygame.draw.rect(screen, color, brick_rect)
    #brick_rects = [pygame.Rect(brick[0], brick[1], brick_width, brick_height) for brick in bricks]
    brick_rects = [pygame.Rect(brick[0][0], brick[0][1], brick_width, brick_height) for brick in bricks]
    for i, brick_rect in enumerate(brick_rects):
        if brick_rect.collidepoint(ball_x, ball_y):
            bricks.pop(i) # Удаление кирпича:
            ball_speed_y = - ball_speed_y # Изменение направления мяча:
            score += 30    # За разбитый кирпич - 30 очков:
            sound_1.play() # Воспроизведенеи звука столкновения с кирпичом:
            break # Выход после уничтожения одного кирпича, что бы не удалять несколько за один кадр:
    # Отрисовка кирпичей
    remaining_bricks = []
    for brick, color in bricks:
        brick_rect = pygame.Rect(brick[0], brick[1], brick_width, brick_height)
        if brick_rect.collidepoint(ball_x, ball_y):
            ball_speed_y = -ball_speed_y
            score += 30
            sound_1.play()
            continue
        pygame.draw.rect(screen, color, brick_rect)
        remaining_bricks.append((brick, color))
    bricks = remaining_bricks
    #Столкновение с платформой:
    if paddle_x <= ball_x <= paddle_x + paddle_width and paddle_y <= ball_y + ball_radius <= paddle_y + paddle_height:
        ball_speed_y = - ball_speed_y
        sound_3.play()  # Столкновение меча с краями экрана:

    # Очистка экрана:
    screen.fill(BLACK)
    #for brick in bricks:
        #pygame.draw.rect(screen, WHITE, pygame.Rect(brick[0], brick[1], brick_width, brick_height))
    # Отрисовка кирпичей
    for brick, color in bricks:
        brick_rect = pygame.Rect(brick[0], brick[1], brick_width, brick_height)
        pygame.draw.rect(screen, color, brick_rect)

    # Рисование объектов:
    pygame.draw.rect(screen, WHITE, (paddle_x, paddle_y, paddle_width, paddle_height))
    pygame.draw.circle(screen, BLUE, (ball_x, ball_y), ball_radius)
    score_text = font.render('Счет в игре: ' + str(score), True, WHITE)
    #screen.blit(score_text, (600, 400))  # Располагаем в верхнем левом углу
    score_rect = score_text.get_rect(center=(screen_width / 2, screen_height / 2))
    # Отображение текста на экране
    screen.blit(score_text, score_rect)
    score_text = font.render('Количество промахов : ' + str(score_fail), True, WHITE)
    screen.blit(score_text, (450, 450))  # Располагаем в верхнем левом углу
    # Отображаем итоговый счёт и количество промахов (уже обнуленное)

    # Обновление экрана:
    pygame.display.flip()

    # Контроль FPS:
    clock.tick(fps)
pygame.quit()
sys.exit()

