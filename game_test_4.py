class Ball:
    def __init__(self, x, y, radius, speed_x, speed_y, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.color = color

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

    def bounce_x(self):
        self.speed_x = -self.speed_x

    def bounce_y(self):
        self.speed_y = -self.speed_y

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

class Paddle:
    def __init__(self, x, y, width, height, speed, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.color = color

    def move(self, direction, screen_width):
        if direction == "left" and self.x > 0:
            self.x -= self.speed
        elif direction == "right" and self.x < screen_width - self.width:
            self.x += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))


class Brick:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))



# Инициализация Pygame и создание окна
pygame.init()
screen = pygame.display.set_mode((1180, 860))
pygame.display.set_caption("Игра Арконоид")
pygame.display.set_icon(pygame.image.load("image/4123.jpg"))

# Инициализация звуков
sounds = [pygame.mixer.Sound(f"sound/sound_{i}.wav") for i in range(1, 8)]
for sound in sounds:
    sound.set_volume(0.5)

# Инициализация цветов, шрифта, счета
BLACK, WHITE, BLUE, LIGHT_BLUE = (0, 160, 255), (255, 255, 255), (0, 0, 255), (255, 0, 0)
brick_colors = [(255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255)]
font = pygame.font.SysFont(None, 46)
score, score_fail = 0, 0

# Создание объектов игры
ball = Ball(590, 820, 10, 4, -4, BLUE)
paddle = Paddle(540, 840, 100, 10, 6, WHITE)
bricks = [Brick(col * 118, row * 30, 113, 20, brick_colors[row % len(brick_colors)]) for row in range(5) for col in range(10)]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Управление платформой
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        paddle.move("left", screen.get_width())
    if keys[pygame.K_RIGHT]:
        paddle.move("right", screen.get_width())

    # Движение мяча и обработка столкновений
    ball.move()
    # Столкновение с границами экрана и платформой здесь

    # Отрисовка объектов
    screen.fill(LIGHT_BLUE)
    ball.draw(screen)
    paddle.draw(screen)
    for brick in bricks:
        brick.draw(screen)

    # Обновление экрана и контроль FPS
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
sys.exit()
