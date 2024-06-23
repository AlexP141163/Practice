import pygame
import sys
import json
import random

# Инициализация Pygame
pygame.init()
pygame.font.init()

# Основные настройки
SCREEN_WIDTH, SCREEN_HEIGHT = 1180, 860
FONT = pygame.font.SysFont(None, 36)
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
COLOR_TEXT = pygame.Color('white')


# Классы для элементов управления
class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Проверка клика в пределах прямоугольника поля ввода
            if self.rect.collidepoint(event.pos):
                # Активируем или деактивируем поле ввода
                self.active = not self.active
            else:
                self.active = False
            # Изменение цвета поля ввода в зависимости от активности
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.active = False
                self.color = COLOR_INACTIVE
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]  # Удаление последнего символа
            else:
                self.text += event.unicode  # Добавление символа
            # Обновление текстовой поверхности для отображения
            self.txt_surface = FONT.render(self.text, True, self.color)

    def draw(self, screen):
        # Отрисовка поля ввода и текста в нем
        pygame.draw.rect(screen, self.color, self.rect, 2)
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))

class Button:
    def __init__(self, x, y, w, h, text, callback):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.callback = callback
        self.color = COLOR_INACTIVE

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.callback()

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        txt_surface = FONT.render(self.text, True, COLOR_TEXT)
        screen.blit(txt_surface, (self.rect.x + 10, self.rect.y + 10))


# Классы игры
class Paddle:
    def __init__(self, screen_width, screen_height):
        self.width = 100
        self.height = 10
        self.x = (screen_width - self.width) // 2
        self.y = screen_height - (self.height * 2)
        self.speed = 8

    def move_left(self):
        self.x = max(0, self.x - self.speed)

    def move_right(self, screen_width):
        self.x = min(screen_width - self.width, self.x + self.speed)

    def draw(self, screen):
        pygame.draw.rect(screen, (155, 56, 124), (self.x, self.y, self.width, self.height))

class Brick:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class Ball:
    def __init__(self, screen_width, screen_height, paddle_y, speed_multiplier=1.0):
        self.radius = 12
        self.x = screen_width // 2
        self.y = paddle_y - self.radius
        self.speed_x = 4 * speed_multiplier
        self.speed_y = -4 * speed_multiplier

    def move(self, screen_width, screen_height):
        self.x += self.speed_x
        self.y += self.speed_y
        if self.x - self.radius <= 0 or self.x + self.radius >= screen_width:
            self.speed_x *= -1
        if self.y - self.radius <= 0:
            self.y = self.radius
            self.speed_y *= -1

    def draw(self, screen):
        pygame.draw.circle(screen, (0, 0, 255), (self.x, self.y), self.radius)


class Game:
    def __init__(self, player_name, difficulty):
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        self.fps = 70
        self.running = True
        self.paddle = Paddle(self.screen_width, self.screen_height)
        self.ball = Ball(self.screen_width, self.screen_height, self.paddle.y, 1.0 + 0.2 * int(difficulty))
        self.bricks = [Brick(50 + j * 100, 30 + i * 30, 90, 20, (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))) for i in range(5) for j in range(10)]
        self.score = 0
        self.lives = 3

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.screen.fill((0, 150, 200))
            self.paddle.draw(self.screen)
            self.ball.draw(self.screen)
            for brick in self.bricks:
                brick.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)
            
def main_menu():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    input_boxes = [InputBox(50, 100, 200, 50, "Enter Name"), InputBox(50, 200, 200, 50, "Enter Difficulty (1-5)")]
    buttons = [Button(350, 300, 100, 50, "Start", lambda: start_game(input_boxes[0].text, input_boxes[1].text))]

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            for box in input_boxes:
                box.handle_event(event)  # Правильный вызов метода handle_event для каждого input box
            for button in buttons:
                button.handle_event(event)  # Правильный вызов метода handle_event для кнопки

        screen.fill((30, 30, 30))
        for box in input_boxes:
            box.draw(screen)  # Отрисовка каждого input box
        for button in buttons:
            button.draw(screen)  # Отрисовка кнопки

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


def start_game(player_name, difficulty):
    try:
        difficulty = int(difficulty)
        if not player_name.strip() or not 1 <= difficulty <= 5:
            raise ValueError("Invalid input.")
    except ValueError:
        print("Invalid input. Please enter a valid name and difficulty level (1-5).")
        return
    game = Game(player_name, difficulty)
    game.run()

# Запустить главное меню
if __name__ == '__main__':
    main_menu()