import pygame, sys, random
from pygame.locals import *

pygame.init()

FPS = 40
FramePerSec = pygame.time.Clock()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

darkGreen = (0,100,0)
lightGreen = (0,128,0)

DISPLAYSURF=pygame.display.set_mode((500,500))
font = pygame.font.SysFont("Monospace", 15, True, True)
pygame.display.set_caption("Snake game!")

class Snake(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Cabeca.png")
        self.bodyImage = pygame.image.load("Corpo.png")
        self.rect = self.image.get_rect()
        self.rect.center = (250,250)
        self.direction = [5, 0]
        self.bodyParts = []
        self.positions = []
    
    def update(self):
        pressed_keys = pygame.key.get_pressed()
        
        if pressed_keys[K_UP]:
            self.direction = [0, -5]
        if pressed_keys[K_DOWN]:
            self.direction = [0, 5]
        if pressed_keys[K_LEFT]:
            self.direction = [-5, 0]
        if pressed_keys[K_RIGHT]:
            self.direction = [5, 0]
    
    def move(self):
        self.positions.insert(0, self.rect.center)
        if(len(self.positions) > len(self.bodyParts) + 1):
            self.positions.pop()

        self.rect.move_ip(self.direction[0], self.direction[1])
        for i in range(len(self.bodyParts)):
            self.bodyParts[i].center = self.positions[i]

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        for bodyPart in self.bodyParts:
            surface.blit(self.bodyImage, bodyPart)
    
    def isGameRunning(self):
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH or self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            return False
        return True

    def checkCoin(self, Coin, Text):
        collide = self.rect.colliderect(Coin.rect)
        if collide:
            newPart = pygame.image.load("Corpo.png")
            newPartRect = newPart.get_rect()
            newPartRect.center = self.positions[-1]

            self.bodyParts.append(newPartRect)
            Coin.newPosition()
            Text.increaseScore()
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Moeda.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(10, SCREEN_WIDTH-10), random.randint(10, SCREEN_HEIGHT-10))
    
    def move(self):
        self.rect.center = (random.randint(10, SCREEN_WIDTH-10), random.randint(10, SCREEN_HEIGHT-10))
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)
    
    def newPosition(self):
        self.rect.center = (random.randint(10, SCREEN_WIDTH-10), random.randint(10, SCREEN_HEIGHT-10))

class Text(pygame.sprite.Sprite):
    def __init__(self):
        self.score = 0
        self.time = 30
        self.cicles = 0
        self.scoreMessage = "Score: " + str(self.score)
        self.timeMessage = "Time left: " + str(self.time)
        self.scoreText = font.render(self.scoreMessage, True, (255,255,255))
        self.timeText = font.render(self.timeMessage, True, (255,255,255))
        self.scoreRect = self.scoreText.get_rect()
        self.timeRect = self.timeText.get_rect()
        self.scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.timeRect.center = ((SCREEN_WIDTH // 2) + 10, (SCREEN_HEIGHT // 2) + 10)
    
    def update(self):
        if self.cicles == FPS:
            self.time -= 1
            self.cicles = 0
        else:
            self.cicles += 1

        self.scoreMessage = "Score: " + str(self.score)
        self.timeMessage = "Time left: " + str(self.time)

        self.scoreText = font.render(self.scoreMessage, True, (255,255,255))
        self.timeText = font.render(self.timeMessage, True, (255,255,255))

        self.scoreRect = self.scoreText.get_rect()
        self.timeRect = self.timeText.get_rect()

        self.scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.timeRect.center = ((SCREEN_WIDTH // 2) + 10, (SCREEN_HEIGHT // 2) + 10)

    def draw(self, surface):
        surface.blit(self.scoreText, self.scoreRect)
        surface.blit(self.timeText, self.timeRect)
    
    def increaseScore(self):
        self.score += 1

Player1 = Snake()
Coin1 = Coin()
Text = Text()

playerAlive = True
while playerAlive: #principal loop
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
        pygame.display.update()
    Player1.update()
    Player1.move()
    Player1.checkCoin(Coin1, Text)
    Text.update()

    DISPLAYSURF.fill((0,0,0))

    Player1.draw(DISPLAYSURF)
    Coin1.draw(DISPLAYSURF)
    Text.draw(DISPLAYSURF)

    playerAlive = Player1.isGameRunning()

    pygame.display.update()
    FramePerSec.tick(FPS)