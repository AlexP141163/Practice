# Это основа для создания рабочего окна приложения:

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

# Создадим игровой цикл (каким образом после начала будет заканчиваться программа):
run = True      # Создаем переменную 'run' в которой будет храниться 'Thue'- в этой ситуации программа работает:
                # Создааем цикл 'while' в котором перебираются все события и сохраняются в переменной 'event':
while run:      # 'pygame.event.get()'б а это список событий который через 'get' извлекаются и присваиваются 'event':
    for event in pygame.event.get():             # 'pygame.QUIT' - это крестик закрытия окна на окне игры:
        if event.type == pygame.QUIT:   # Как только тип собития 'event.type' будет равняться 'pygame.QUIT':
            run = False                 # переменной 'run' присваивается 'False' и игра заканчивается:

    screen.fill((30,100,200))   # Заливаем дисплей цветом (RBG-от 0 до 255(0 -количество красного, 0 -голубого, 0 -зеленого):
    pygame.display.flip()  # Обновляем постояннон экран. Ьщжно использовать 'pygame.display.update()':


pygame.quit()  # Выход из игры:
