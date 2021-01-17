import pygame
import sys
from typing import Tuple, List


pygame.init()

WIDTH = 800
HEIGHT = 800
WHITE = (255, 255, 255)


class Paddle:
    """
    A generic paddle used to implement PlayerPaddle and PlayerPaddleKeyBoard.
    """
    def __init__(self, name: str, color: Tuple[int, int, int], x_corr: int,
                 y_corr: int, player_num: int) -> None:
        """
        :param name: The name of the paddle
        :param color: Color used to display the paddle and score in game
        :param x_corr: The initial x coordinate of the paddle
        :param y_corr: The initial y coordinate of the paddle
        :param player_num: an int of value 1 or 2. Used to determine how the
            paddle collides with the ball
        """
        if player_num == 1:
            self.mul = 1
        else:
            self.mul = -1
        self.name = name
        self.color = color
        self.x_corr = x_corr
        self.y_corr = y_corr

    def get_new_y(self) -> int:
        """
        :return: The new y coordinate of the paddle
        """
        pass

    def move(self, screen: pygame.display, ball) -> None:
        """
        Move the paddle and check for collision with the ball.

        :param screen: The screen of the game
        :param ball: The ball used in the game
        """
        ym = self.get_new_y()
        if ym + 150 <= HEIGHT:
            self.y_corr = ym
            pygame.draw.rect(screen, self.color,
                             (self.x_corr, self.y_corr, 15, 150))
        else:
            pygame.draw.rect(screen, self.color,
                             (self.x_corr, HEIGHT - 150, 15, 150))

        # Ball Collision
        if ball.x == self.x_corr + self.mul*15 and self.y_corr - 15 <= \
                ball.y <= self.y_corr + 50 + 15:
            ball.speed[0] = -ball.speed[0]
            ball.speed[1] = -1
        elif ball.x == self.x_corr + self.mul*15 and self.y_corr + 50 <= \
                ball.y <= self.y_corr + 100:
            ball.speed[0] = -ball.speed[0]
            ball.speed[1] = 0
        elif ball.x == self.x_corr + self.mul*15 and self.y_corr + 100 \
                <= ball.y <= self.y_corr + 150:
            ball.speed[0] = -ball.speed[0]
            ball.speed[1] = 1


class PlayerPaddle(Paddle):
    """
    Paddle that uses mouse controls
    """
    def get_new_y(self):
        return pygame.mouse.get_pos()[1]


class PlayerPaddleKeyBoard(Paddle):
    """
    Paddle that uses KeyBoard controls
    """
    def get_new_y(self):
        key_states = pygame.key.get_pressed()
        if key_states[pygame.K_w]:
            return self.y_corr - 1
        elif key_states[pygame.K_s]:
            return self.y_corr + 1
        else:
            return self.y_corr


class Ball:
    """
    Ball used for pong game.
    """
    x: int
    y: int
    speed: List[int]

    def __init__(self, x: int, y: int):
        """
        :param x: x coordinate of the ball
        :param y: y coordinate of the ball
        """
        self.x = x
        self.y = y
        self.speed = [-1, 0]

    def move(self) -> None:
        """
        Update x and y coordinates based on speed attribute.
        """
        self.x += self.speed[0]
        self.y += self.speed[1]


class Pong:
    """
    Class used to run the pong game
    """
    p1: Paddle
    p2: Paddle
    ball: Ball
    p1_score: int
    p2_score: int

    def __init__(self, P1_name: str, P1_color: Tuple[int, int, int],
                 P2_name: str, P2_color: Tuple[int, int, int]) -> None:
        """
        :param P1_name: Player one's name
        :param P1_color: Player one's color
        :param P2_name: Player two's name
        :param P2_color: Player two's color
        """
        self.p1 = PlayerPaddle(P1_name, P1_color, 100, 400, 1)
        self.p2 = PlayerPaddleKeyBoard(P2_name, P2_color, WIDTH - 100, 400, 2)
        self.ball = Ball(WIDTH//2, HEIGHT//2)
        self.p1_score = 0
        self.p2_score = 0

    def start(self) -> None:
        """
        Method used to start pong game.
        """

        # Set window name
        pygame.display.set_caption('Pong')

        # Set window dimensions
        screen = pygame.display.set_mode((WIDTH, HEIGHT))

        # Setup player score graphics for player one and two
        font = pygame.font.Font('freesansbold.ttf', 32)
        p1_text = font.render(f'{self.p1.name}: {self.p1_score}', True,
                              self.p1.color)
        p1_textbox = p1_text.get_rect()
        p1_textbox.center = (125, 50)

        p2_text = font.render(f'{self.p2.name}: {self.p2_score}', True,
                              self.p2.color)
        p2_textbox = p2_text.get_rect()
        p2_textbox.center = (WIDTH-125, 50)

        pygame.mouse.set_pos(self.p1.x_corr, self.p1.y_corr)
        game_over = False

        while not game_over:
            # Wipe the window
            screen.fill((0, 0, 0))

            # Display player scores
            p1_text = font.render(f'{self.p1.name}: {self.p1_score}', True,
                                  self.p1.color)

            p2_text = font.render(f'{self.p2.name}: {self.p2_score}', True,
                                  self.p2.color)
            screen.blit(p1_text, p1_textbox)
            screen.blit(p2_text, p2_textbox)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)

            # Draw P1
            self.p1.move(screen, self.ball)

            # Draw P2
            self.p2.move(screen, self.ball)

            # Ball collision with top and bottom window borders
            if self.ball.y <= 0 or self.ball.y >= HEIGHT:
                self.ball.speed[1] = -self.ball.speed[1]

            self.ball.move()

            # Check if ball got passed a paddle and update player scores
            if not (self.ball.x in range(WIDTH)):
                if self.ball.speed[0] > 0:
                    self.p1_score += 1
                else:
                    self.p2_score += 1
                self.ball = Ball(WIDTH//2, HEIGHT//2)

            # Draw Ball
            pygame.draw.circle(screen, WHITE,(int(self.ball.x), int(self.ball.y)), 10)

            # Update display
            pygame.display.update()


if __name__ == '__main__':
    game = Pong("p1", WHITE, "P2", (0, 128, 0))
    game.start()
