import pygame
import sys

# Инициализация 'Pygame':
pygame.init()
clock = pygame.time.Clock()  # Исправил опечатку с 'clok' на 'clock'
fps = 60

# Определяем переменную в которой будет храниться размер рабочего окна:
screen_width, screen_height = 1280, 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Игра Арконоид")

# Загрузим файл изображения:
image = pygame.image.load("image/test.png")
image_rect = image.get_rect()

# Размеры изображения
image_width = 100
image_height = 100

# Создаем игровой цикл:
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEMOTION:
            mouse_X, mouse_Y = pygame.mouse.get_pos()
            # Устанавливаем новые координаты для image_rect, учитывая положение мыши
            # и делаем корректировку, чтобы изображение перемещалось с центром на курсоре:
            new_x = mouse_X - image_width // 2  # 'mage_width // 2' - размер изображения по ширине деленное на попалам:
            new_y = mouse_Y - image_height // 2 # 'image_height // 2 - размер изображения по высоте деленное на попалам:

            # Ограничиваем перемещение по X:
            # Проверка проверяет, переместилась ли левая часть изображениея 'new_x'за левую часть экрана.
            # Если да 'new_x < 0' то 'new_x = 0'  и изображение не будет выходить за левый край экрана.
            # Также проверка проверяет не выходит ли правый край изибражения 'new_x + image_width > screen_width',
            # за правый край экрана. Если да, то 'new_x = screen_width - image_width' т.е. правый край экрана минус
            # ширину изображения. По оси 'Y' по такому же принципу:
            if new_x < 0:
                new_x = 0
            elif new_x + image_width > screen_width:
                new_x = screen_width - image_width

            # Ограничиваем перемещение по Y:
            if new_y < 0:
                new_y = 0
            elif new_y + image_height > screen_height:
                new_y = screen_height - image_height

            # Применяем ограниченные координаты к рамке (контору) изображения:
            image_rect.x = new_x
            image_rect.y = new_y

    # Заливаем дисплей цветом:
    screen.fill((30, 100, 200))
    # Отрисовка изображения:
    screen.blit(image, image_rect)
    # Обновляем экран:
    pygame.display.flip()

    # Ограничение FPS:
    clock.tick(fps)

pygame.quit()  # Выход из игры