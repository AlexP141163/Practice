import pygame
import sys
import time
import json

# Инициализация Pygame
pygame.init()
pygame.font.init()

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

class Ball:
    def __init__(self, screen_width, screen_height, paddle_y, speed_multiplier=1.0):
        self.radius = 10
        self.x = screen_width // 2
        self.y = paddle_y - self.radius
        self.speed_x = 4 * speed_multiplier
        self.speed_y = -4 * speed_multiplier

    def move(self, screen_width, screen_height):
        self.x += self.speed_x
        self.y += self.speed_y
        # Collision with left or right
        if self.x - self.radius <= 0 or self.x + self.radius >= screen_width:
            self.speed_x *= -1
        # Collision with the top
        if self.y - self.radius <= 0:
            self.speed_y *= -1

    def draw(self, screen):
        pygame.draw.circle(screen, (0, 0, 255), (self.x, self.y), self.radius)

class Brick:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class Game:
    def __init__(self, player_name, difficulty):
        self.screen_width = 1180
        self.screen_height = 860
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        self.fps = 70
        self.running = True
        self.paddle = Paddle(self.screen_width, self.screen_height)
        speed_multiplier = 1.0 + 0.2 * difficulty  # Increase speed based on difficulty
        self.ball = Ball(self.screen_width, self.screen_height, self.paddle.y, speed_multiplier)
        self.font = pygame.font.SysFont(None, 46)
        self.score = 0
        self.lives = 3
        self.bricks = self.create_bricks()
        self.player_name = player_name
        self.high_scores = self.load_high_scores()
        self.load_sounds()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.paddle.move_left()
            if keys[pygame.K_RIGHT]:
                self.paddle.move_right(self.screen_width)

            self.ball.move(self.screen_width, self.screen_height)
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
        # Ball collision with the window edges
        if self.ball.x <= 0 or self.ball.x >= self.screen_width:
            self.ball.speed_x *= -1
            self.sounds['hit_edge'].play()
        if self.ball.y <= 0:
            self.ball.speed_y *= -1
            self.sounds['hit_edge'].play()
        # Ball collision with the paddle
        if self.paddle.x <= self.ball.x <= self.paddle.x + self.paddle.width and self.paddle.y <= self.ball.y + self.ball.radius:
            self.ball.speed_y *= -1
            self.sounds['hit_paddle'].play()
            self.score += 10

        # Ball collision with bricks
        remaining_bricks = []
        for brick in self.bricks:
            if brick.rect.collidepoint(self.ball.x, self.ball.y):
                self.ball.speed_y *= -1
                self.sounds['hit_brick'].play()
                self.score += 30
                continue
            remaining_bricks.append(brick)
        self.bricks = remaining_bricks

        # Ball falls below the paddle
        if self.ball.y > self.screen_height:
            self.lives -= 1
            self.sounds['lose_life'].play()
            if self.lives > 0:
                self.reset_ball()
            else:
                self.update_high_scores()

    def draw_score(self):
        score_text = self.font.render('Score: ' + str(self.score), True, (255, 255, 255))
        lives_text = self.font.render('Lives: ' + str(self.lives), True, (255, 255, 255))
        self.screen.blit(score_text, (10, 150))
        self.screen.blit(lives_text, (self.screen_width - 120, 150))

    def check_game_over(self):
        if self.lives <= 0:
            self.sounds['game_over'].play()
            self.display_message("Game Over")
        elif not self.bricks:
            self.sounds['win_game'].play()
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
        speed_multiplier = 1.0 + 0.2 * difficulty  # Reset with initial speed multiplier
        self.ball = Ball(self.screen_width, self.screen_height, self.paddle.y, speed_multiplier)

    def load_high_scores(self):
        try:
            with open('high_scores.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def update_high_scores(self):
        # Add current score to high scores and keep the top 5 scores
        self.high_scores.append({'name': self.player_name, 'score': self.score})
        self.high_scores = sorted(self.high_scores, key=lambda x: x['score'], reverse=True)[:5]
        with open('high_scores.json', 'w') as file:
            json.dump(self.high_scores, file)

    def display_high_scores(self):
        # Display high scores on the screen
        self.screen.fill((0, 0, 0))
        for i, score in enumerate(self.high_scores):
            text = self.font.render(f"{i+1}. {score['name']} - {score['score']}", True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.screen_width // 2, 100 + i * 30))
            self.screen.blit(text, text_rect)
        pygame.display.flip()
        time.sleep(5)

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
    player_name = input("Enter your name: ")
    difficulty = int(input("Enter difficulty (1-5): "))
    game = Game(player_name, difficulty)
    game.run()
    game.display_high_scores()
    pygame.quit()
    sys.exit()
