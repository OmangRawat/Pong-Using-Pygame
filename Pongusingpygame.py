import pygame
from random import randint

white = (255, 255, 255)
black = (0, 0, 0)

pygame.init()     # initializing pygame

# Screen
dim = (700, 700)
screen = pygame.display.set_mode(dim)
pygame.display.set_caption("Pong")

# background = pygame.image.load("orig.jpg")

clock = pygame.time.Clock()    # To keep in check how fast the screen updates


# Making class
class Paddle(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(black)
        self.image.set_colorkey(black)
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        self.rect = self.image.get_rect()

    def move_up(self, pixels):
        self.rect.y -= pixels
        if self.rect.y < 0:
            self.rect.y = 0

    def move_down(self, pixels):
        self.rect.y += pixels
        if self.rect.y > 600:
            self.rect.y = 600


class Ball(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(black)
        self.image.set_colorkey(black)
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        self.velocity = [randint(4, 8), randint(-8, 8)]
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

    def bounce(self):
        self.velocity[0] = -self.velocity[0]
        self.velocity[1] = randint(-8, 8)


# Making objects
p1 = Paddle(white, 20, 100)
p1.rect.x = 0
p1.rect.y = 300

p2 = Paddle(white, 20, 100)
p2.rect.x = 680
p2.rect.y = 300

ball = Ball(white, 10, 10)
ball.rect.x = 345
ball.rect.y = 345

# Making list to add all the elements
sprite_list = pygame.sprite.Group()
sprite_list.add(p1)
sprite_list.add(p2)
sprite_list.add(ball)

run = True

score1 = 0
score2 = 0

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                run = False

    # screen.blit(background, (0, 0))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        p1.move_up(5)
    if keys[pygame.K_s]:
        p1.move_down(5)
    if keys[pygame.K_UP]:
        p2.move_up(5)
    if keys[pygame.K_DOWN]:
        p2.move_down(5)

    sprite_list.update()    # updating the screen

    if ball.rect.x >= 690:
        score1 += 1
        ball.velocity[0] = -ball.velocity[0]
        ball.rect.x = 350
        ball.rect.y = 350
    if ball.rect.x <= 0:
        score2 += 1
        ball.rect.x = 350
        ball.rect.y = 350
        ball.velocity[0] = -ball.velocity[0]
    if ball.rect.y > 690:
        ball.velocity[1] = -ball.velocity[1]
    if ball.rect.y < 0:
        ball.velocity[1] = -ball.velocity[1]

    if pygame.sprite.collide_mask(ball, p1) or pygame.sprite.collide_mask(ball, p2):
        ball.bounce()

    screen.fill(black)   # clearing the screen to black

    pygame.draw.line(screen, white, [349, 0], [349, 700], 5)   # Drawing the dividing line

    sprite_list.draw(screen)   # Draw all the sprites on the screen

    # Displaying Score
    font = pygame.font.Font(None, 74)
    text = font.render(str(score1), 1, white)
    screen.blit(text, (250, 10))
    text = font.render(str(score2), 1, white)
    screen.blit(text, (420, 10))

    pygame.display.flip()     # Update the screen with the elements we have drawn

    clock.tick(60)     # Limit frames to 60 per second

pygame.quit()