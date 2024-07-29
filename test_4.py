import pygame
import sys
import time

pygame.init()
pygame.font.init()

class Paddle:
    def __init__(self, screen_width, screen_height):
        self.width = 100
        self.height = 15
        self.screen_width = screen_width
        self.x = (screen_width - self.width) // 2
        self.y = screen_height - (self.height * 2)
        self.speed = 8

    def move_left(self):
        if self.x > 0:
            self.x -= self.speed

    def move_right(self):
        if self.x + self.width < self.screen_width:
            self.x += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, (155, 56, 124), (self.x, self.y, self.width, self.height))

class Ball:
    def __init__(self, screen_width, screen_height, paddle_y):
        self.radius = 10
        self.x = screen_width // 2
        self.y = paddle_y - self.radius
        self.speed_x = 4
        self.speed_y = -4

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

    def draw(self, screen):
        pygame.draw.circle(screen, (0, 0, 255), (self.x, self.y), self.radius)

class Brick:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class Game:
    def __init__(self):
        self.screen_width = 1180
        self.screen_height = 860
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        self.fps = 70
        self.running = True
        self.paddle = Paddle(self.screen_width, self.screen_height)
        self.ball = Ball(self.screen_width, self.screen_height, self.paddle.y)
        self.font = pygame.font.SysFont(None, 46)
        self.score = 0
        self.lives = 3
        self.bricks = self.create_bricks()
        self.load_sounds()
        self.bricks_grid = self.create_bricks_grid()

    def create_bricks_grid(self):
        grid_size = 50  # Размер ячейки сетки
        grid = {}
        for brick in self.bricks:
            grid_x = brick.rect.x // grid_size
            grid_y = brick.rect.y // grid_size
            if (grid_x, grid_y) not in grid:
                grid[(grid_x, grid_y)] = []
            grid[(grid_x, grid_y)].append(brick)
        return grid

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.paddle.move_left()
            if keys[pygame.K_RIGHT]:
                self.paddle.move_right()

            self.ball.move()
            self.handle_collisions()

            self.screen.fill((0, 150, 200))
            self.paddle.draw(self.screen)
            self.ball.draw(self.screen)
            for brick in self.bricks:
                brick.draw(self.screen)
            self.draw_score()
            self.check_game_over()

            pygame.display.flip()
            self.clock.tick(self.fps)

    def handle_collisions(self):
        if self.ball.x <= 0 or self.ball.x >= self.screen_width:
            self.ball.speed_x *= -1
            self.sounds['hit_edge'].play()
        if self.ball.y <= 0:
            self.ball.speed_y *= -1
            self.sounds['hit_edge'].play()
        if self.paddle.x <= self.ball.x <= self.paddle.x + self.paddle.width and self.paddle.y <= self.ball.y + self.ball.radius:
            self.ball.speed_y *= -1
            self.sounds['hit_paddle'].play()
            self.score += 10

        grid_size = 50
        grid_x = self.ball.x // grid_size
        grid_y = self.ball.y // grid_size
        potential_collisions = []
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                cell = (grid_x + dx, grid_y + dy)
                if cell in self.bricks_grid:
                    potential_collisions.extend(self.bricks_grid[cell])

        remaining_bricks = []
        for brick in potential_collisions:
            if brick.rect.collidepoint(self.ball.x, self.ball.y):
                self.ball.speed_y *= -1
                self.sounds['hit_brick'].play()
                self.score += 30
            else:
                remaining_bricks.append(brick)
        self.bricks = remaining_bricks

        if self.ball.y > self.screen_height:
            self.lives -= 1
            self.sounds['lose_life'].play()
            if self.lives > 0:
                self.reset_ball()

    def draw_score(self):
        score_text = self.font.render('Score: ' + str(self.score), True, (255, 255, 255))
        lives_text = self.font.render('Lives: ' + str(self.lives), True, (255, 255, 255))
        self.screen.blit(score_text, (10, 150))
        self.screen.blit(lives_text, (self.screen_width - 120, 150))

    def check_game_over(self):
        if self.lives <= 0:
            self.display_message("Game Over")
        elif not self.bricks:
            self.display_message("You Win!")

    def display_message(self, message):
        self.screen.fill((0, 0, 0))
        text = self.font.render(message, True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()
        time.sleep(3)
        self.running = False

    def create_bricks(self):
        bricks = []
        brick_rows, brick_cols = 5, 10
        brick_width = (self.screen_width // brick_cols) - 5
        brick_height = 20
        colors = [(255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255)]
        for row in range(brick_rows):
            for col in range(brick_cols):
                x = col * (brick_width + 5)
                y = row * (brick_height + 5)
                color = colors[row % len(colors)]
                bricks.append(Brick(x, y, brick_width, brick_height, color))
        return bricks

    def reset_ball(self):
        self.ball = Ball(self.screen_width, self.screen_height, self.paddle.y)

    def load_sounds(self):
        self.sounds = {
            'hit_brick': pygame.mixer.Sound("sound/sound_1.wav"),
            'hit_paddle': pygame.mixer.Sound("sound/sound_2.wav"),
            'hit_edge': pygame.mixer.Sound("sound/sound_3.wav"),
            'lose_life': pygame.mixer.Sound("sound/sound_4.wav"),
            'game_over': pygame.mixer.Sound("sound/sound_5.wav"),
            'win_game': pygame.mixer.Sound("sound/sound_6.wav")
        }
        for sound in self.sounds.values():
            sound.set_volume(0.5)

if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()
