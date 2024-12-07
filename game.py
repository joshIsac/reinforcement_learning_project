import pygame
import random

# Game Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10
BALL_SIZE = 10
BRICK_WIDTH = 60
BRICK_HEIGHT = 20
FPS = 60

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

class Brick:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)

class Paddle:
    def __init__(self):
        self.rect = pygame.Rect(SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2, SCREEN_HEIGHT - 50, PADDLE_WIDTH, PADDLE_HEIGHT)

    def move(self, direction):
        if direction == "left" and self.rect.left > 0:
            self.rect.x -= 10
        elif direction == "right" and self.rect.right < SCREEN_WIDTH:
            self.rect.x += 10

class Ball:
    def __init__(self):
        self.rect = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60, BALL_SIZE, BALL_SIZE)
        self.dx = random.choice([-4, 4])
        self.dy = -4

    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

    def reset(self):
        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT - 60
        self.dx = random.choice([-4, 4])
        self.dy = -4

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.paddle = Paddle()
        self.ball = Ball()
        self.bricks = [Brick(x * (BRICK_WIDTH + 10), y * (BRICK_HEIGHT + 10)) for x in range(10) for y in range(5)]
        self.score = 0
        self.game_over = False

    def reset(self):
        self.score = 0
        self.ball.reset()
        self.paddle.rect.x = SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2
        self.bricks = [Brick(x * (BRICK_WIDTH + 10), y * (BRICK_HEIGHT + 10)) for x in range(10) for y in range(5)]
        self.game_over = False

    def update(self):
        self.ball.move()

        # Check for collision with walls
        if self.ball.rect.left <= 0 or self.ball.rect.right >= SCREEN_WIDTH:
            self.ball.dx *= -1
        if self.ball.rect.top <= 0:
            self.ball.dy *= -1
        if self.ball.rect.bottom >= SCREEN_HEIGHT:
            self.game_over = True  # Game over if the ball falls below the screen

        # Check for collision with paddle
        if self.ball.rect.colliderect(self.paddle.rect):
            self.ball.dy *= -1
            self.ball.rect.bottom = self.paddle.rect.top

        # Check for collision with bricks
        for brick in self.bricks:
            if self.ball.rect.colliderect(brick.rect):
                self.ball.dy *= -1
                self.bricks.remove(brick)
                self.score += 1
                break

    def render(self):
        self.screen.fill(WHITE)
        pygame.draw.rect(self.screen, BLUE, self.paddle.rect)
        pygame.draw.ellipse(self.screen, GREEN, self.ball.rect)
        for brick in self.bricks:
            pygame.draw.rect(self.screen, RED, brick.rect)
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f'Score: {self.score}', True, (0, 0, 0))
        self.screen.blit(score_text, (10, 10))
        pygame.display.flip()

    def run(self):
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.paddle.move("left")
            if keys[pygame.K_RIGHT]:
                self.paddle.move("right")

            self.update()
            self.render()
            self.clock.tick(FPS)

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()