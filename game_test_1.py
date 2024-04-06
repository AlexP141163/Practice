# Это основа для создания рабочего окна приложения:
# Загрузим картинку на экран и будем перемещать ее по экрану с помощью КЛАВИАТУРЫ:

# Импортируем 'pygame':
import pygame
import sys
# Инициализация 'Pygame':
pygame.init()
clok = pygame.time.Clock()
fps = 60

# Определяем переменную в которой будет храниться размер рабочего окна:
screen_width, screen_height = 1280, 800
screen = pygame.display.set_mode((screen_width, screen_height)) # В переменной 'screen' создаем экран с параметрами 'windows_size':
pygame.display.set_caption(" Игра Арконоид ")

# Помещаем загруженный объект на экран и отрисовываем его. Отрисовывать его нужно обязательно только в цикле,
# обязательно после заливки экрана.
image = pygame.image.load("image/test.png") # Загрузим файл изображения:
image_rect = image.get_rect() # В данной переменной сохраняем рамку объекта 'image', что бы определять соприкосновения:

speed = 2  # Скорость перемещения объекта:

# Создадим игровой цикл (каким образом после начала будет заканчиваться программа):
run = True      # Создаем переменную 'run' в которой будет храниться 'Thue'- в этой ситуации программа работает:
                # Создааем цикл 'while' в котором перебираются все события и сохраняются в переменной 'event':
while run:      # 'pygame.event.get()'б а это список событий который через 'get' извлекаются и присваиваются 'event':
    for event in pygame.event.get():             # 'pygame.QUIT' - это крестик закрытия окна на окне игры:
        if event.type == pygame.QUIT:   # Как только тип собития 'event.type' будет равняться 'pygame.QUIT':
            run = False                 # переменной 'run' присваивается 'False' и игра заканчивается:

    keys = pygame.key.get_pressed()     # Работа с клавиатурой. Получаем комаду от нажатия клавиши и сохраняем в 'ktes':
    if keys[pygame.K_LEFT]:             # Условие: Усли нажать стрелку в Лево '[pygame.K_LEFT]':
        image_rect.x -= speed           # Нужно будет уменьшать координаты по оси 'X' со скоростью 'speed':
    if keys[pygame.K_RIGHT]:            # 'image_rect'-координаты рамки объекта:
        image_rect.x += speed
    if keys[pygame.K_UP]:
        image_rect.y -= speed           # Знак '-' значит координата по оси 'Y' уменьшается и объект двигается вверх:
    if keys[pygame.K_DOWN]:
        image_rect.y += speed           # Здесь '+' -здесь объект будет двигаться вниз - Особенность координат в Python:

    # Ограничение по левой границе
    # Ограничиваем перемещение по X:
    # Проверка проверяет, переместилась ли левая часть изображениея 'new_x'за левую часть экрана.
    # Если да 'new_x < 0' то 'new_x = 0'  и изображение не будет выходить за левый край экрана.
    # Также проверка проверяет не выходит ли правый край изибражения 'new_x + image_width > screen_width',
    # за правый край экрана. Если да, то 'new_x = screen_width - image_width' т.е. правый край экрана минус
    # ширину изображения. По оси 'Y' по такому же принципу:
    if image_rect.x < 0:
        image_rect.x = 0
    # Ограничение по правой границе
    if image_rect.x + image_rect.width > screen_width:
        image_rect.x = screen_width - image_rect.width
    # Ограничение по верхней границе
    if image_rect.y < 0:
        image_rect.y = 0
    # Ограничение по нижней границе
    if image_rect.y + image_rect.height > screen_height:
        image_rect.y = screen_height - image_rect.height

    screen.fill((30,100,200))   # Заливаем дисплей цветом (RBG-от 0 до 255(0 -количество красного, 0 -голубого, 0 -зеленого):
    screen.blit(image, image_rect) # Отрисовка загруженного изображения. Отрисовывается 'image' и 'image_rect' контур(рамку) изображения;
    pygame.display.flip()  # Обновляем постояннон экран. Ьщжно использовать 'pygame.display.update()':


pygame.quit()  # Выход из игры: