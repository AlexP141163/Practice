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
windows_size = (1280, 800)
screen = pygame.display.set_mode(windows_size) # В переменной 'screen' создаем экран с параметрами 'windows_size':
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

    screen.fill((30,100,200))   # Заливаем дисплей цветом (RBG-от 0 до 255(0 -количество красного, 0 -голубого, 0 -зеленого):
    screen.blit(image, image_rect) # Отрисовка загруженного изображения. Отрисовывается 'image' и 'image_rect' контур(рамку) изображения;
    pygame.display.flip()  # Обновляем постояннон экран. Ьщжно использовать 'pygame.display.update()':


pygame.quit()  # Выход из игры: