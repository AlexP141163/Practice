import pygame
import sys
import time

# Инициализация Pygame:
pygame.init()

# Настройки экрана:
screen_width, screen_height = 1180, 860
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Игра Арконоид")

# Цвета:
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_BLUE = (173, 216, 230)

# Шрифты:
font = pygame.font.SysFont(None, 46)

# Функция для отображения меню:
def show_menu():
    menu_running = True
    while menu_running:
        screen.fill(LIGHT_BLUE)
        start_text = font.render('Запуск', True, WHITE)
        exit_text = font.render('Выход', True, WHITE)

        start_button = start_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
        exit_button = exit_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))

        screen.blit(start_text, start_button)
        screen.blit(exit_text, exit_button)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(pygame.mouse.get_pos()):
                    menu_running = False
                elif exit_button.collidepoint(pygame.mouse.get_pos()):
                    pygame.quit()
                    sys.exit()
    main_game()


# Основной цикл игры:
def main_game():
    # Здесь будет ваш основной игровой код.
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle_x > 0:  # 'paddle_x > 0' не дает платформе выйти за пределы экрана:
            paddle_x -= paddle_speed
        if keys[pygame.K_RIGHT] and paddle_x < screen_width - paddle_width:
            paddle_x += paddle_speed

        # Движение мяча:
        ball_x += ball_speed_x
        ball_y += ball_speed_y

        # Столкновение с краями экрана:
        if ball_x <= 0 or ball_x >= screen_width:
            ball_speed_x = - ball_speed_x
            sound_2.play()  # Столкновение меча с краями экрана:
        if ball_y <= 0:
            ball_speed_y = - ball_speed_y
            sound_2.play()  # Столкновение меча с краями экрана:
        if ball_y + ball_radius >= screen_height:
            # Сброс мяча:
            ball_x, ball_y = screen_width // 2, paddle_y - ball_radius
            ball_speed_y = - ball_speed_y
            score -= 50  # За промах отнимаем 50 очков:
            score_fail += 1
            sound_6.play()
            if score_fail >= 3:
                sound_4.play()  # Воспроизведение звука завершения игры
                sound_7.play()
                screen.fill(LIGHT_BLUE)  # Очистка экрана
                final_score_text = font.render('Итоговый счёт: ' + str(score), True, WHITE)
                final_fails_text = font.render('Количество промахов: ' + str(score_fail), True, WHITE)
                screen.blit(final_score_text, (screen_width // 2 - 100, screen_height // 2 - 50))
                screen.blit(final_fails_text, (screen_width // 2 - 100, screen_height // 2))
                # Добавьте код для вывода текста "Вы проиграли":
                game_over_text = font.render('  Вы проиграли', True, WHITE)
                text_rect = game_over_text.get_rect(
                    center=(screen_width // 2, screen_height // 2 + 70))  # Центрирование текста
                screen.blit(game_over_text, text_rect)
                pygame.display.flip()  # Обновляем экран для отображения сообщения
                time.sleep(6)  # Пауза перед выходом для прочтения сообщения
                running = False

        for brick, color in bricks:
            brick_rect = pygame.Rect(brick[0], brick[1], brick_width, brick_height)
            pygame.draw.rect(screen, color, brick_rect)
        # brick_rects = [pygame.Rect(brick[0], brick[1], brick_width, brick_height) for brick in bricks]
        brick_rects = [pygame.Rect(brick[0][0], brick[0][1], brick_width, brick_height) for brick in bricks]
        for i, brick_rect in enumerate(brick_rects):
            if brick_rect.collidepoint(ball_x, ball_y):
                bricks.pop(i)  # Удаление кирпича:
                ball_speed_y = - ball_speed_y  # Изменение направления мяча:
                score += 30  # За разбитый кирпич - 30 очков:
                sound_1.play()  # Воспроизведенеи звука столкновения с кирпичом:
                break  # Выход после уничтожения одного кирпича, что бы не удалять несколько за один кадр:
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
        # Столкновение с платформой:
        if paddle_x <= ball_x <= paddle_x + paddle_width and paddle_y <= ball_y + ball_radius <= paddle_y + paddle_height:
            ball_speed_y = - ball_speed_y
            sound_3.play()  # Столкновение меча с краями экрана:

        # Очистка экрана:
        screen.fill(BLACK)
        # for brick in bricks:
        # pygame.draw.rect(screen, WHITE, pygame.Rect(brick[0], brick[1], brick_width, brick_height))
        # Отрисовка кирпичей
        for brick, color in bricks:
            brick_rect = pygame.Rect(brick[0], brick[1], brick_width, brick_height)
            pygame.draw.rect(screen, color, brick_rect)

        # Рисование объектов:
        pygame.draw.rect(screen, WHITE, (paddle_x, paddle_y, paddle_width, paddle_height))
        pygame.draw.circle(screen, BLUE, (ball_x, ball_y), ball_radius)
        score_text = font.render('Счет в игре: ' + str(score), True, WHITE)
        # screen.blit(score_text, (600, 400))  # Располагаем в верхнем левом углу
        score_rect = score_text.get_rect(center=(screen_width / 2, screen_height / 2))
        # Отображение текста на экране
        screen.blit(score_text, score_rect)
        score_text = font.render(f'Промахи (игра до 3): ' + str(score_fail), True, WHITE)
        screen.blit(score_text, (300, 450))  # Располагаем в верхнем левом углу
        # Отображаем итоговый счёт и количество промахов (уже обнуленное)

        # Проверка условий окончания игры:
        if len(bricks) == 0 or score >= 1500:
            screen.fill(LIGHT_BLUE)  # Очистка экрана
            if score >= 1500:
                victory_text = font.render('Поздравляем! Вы набрали 1500 очков!', True, WHITE)
            else:
                victory_text = font.render('Поздравляем! Вы разбили все кирпичи!', True, WHITE)
            text_rect = victory_text.get_rect(
                center=(screen_width // 2, screen_height // 2 - 50))  # Центрирование текста
            screen.blit(victory_text, text_rect)
            final_score_text = font.render('Итоговый счёт: ' + str(score), True, WHITE)
            screen.blit(final_score_text, (screen_width // 2 - 100, screen_height // 2))
            sound_5.play()
            pygame.display.flip()  # Обновляем экран для отображения сообщения
            time.sleep(5)  # Пауза перед выходом для прочтения сообщения
            running = False

        screen.fill(BLACK)
        pygame.display.flip()
show_menu()
# Показать меню перед началом игры:


# Запуск основной игры после выхода из меню:


pygame.quit()