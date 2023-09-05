import pygame, sys, random
from pygame.locals import *

pygame.init()

FPS = 20
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
SNAKE_SIZE_IN_PIXELS = 15
DIRECTIONS = {
    "right": [SNAKE_SIZE_IN_PIXELS, 0],
    "left": [-SNAKE_SIZE_IN_PIXELS, 0],
    "up": [0, -SNAKE_SIZE_IN_PIXELS],
    "down": [0, SNAKE_SIZE_IN_PIXELS],
}

FramePerSec = pygame.time.Clock()

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
        self.direction = DIRECTIONS["right"]
        self.bodyParts = []
        self.positions = []
    
    def update(self):
        pressed_keys = pygame.key.get_pressed()
        
        if pressed_keys[K_UP]:
            if self.direction != DIRECTIONS["down"]:
                self.direction = DIRECTIONS["up"]
        if pressed_keys[K_DOWN]:
            if self.direction != DIRECTIONS["up"]:
                self.direction = DIRECTIONS["down"]
        if pressed_keys[K_LEFT]:
            if self.direction != DIRECTIONS["right"]:
                self.direction = DIRECTIONS["left"]
        if pressed_keys[K_RIGHT]:
            if self.direction != DIRECTIONS["left"]:
                self.direction = DIRECTIONS["right"]
    
    def move(self):
        self.positions.insert(0, self.rect.center)
        if(len(self.positions) > len(self.bodyParts) + 1):
            self.positions.pop()

        self.rect.move_ip(self.direction[0], self.direction[1])
        for i in range(len(self.bodyParts)):
            self.bodyParts[i].center = self.positions[i]

    def draw(self, surface):
        currentImage = self.getCurrentImage()
        
        surface.blit(currentImage, self.rect)

        for bodyPart in self.bodyParts:
            surface.blit(self.bodyImage, bodyPart)
    
    def isGameRunning(self, Status):
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH or self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            return False
        if(Status.time <= 0):
            return False
        if(self.checkSelfColision()):
            return False
        return True

    def checkCoin(self, Coin, Status):
        collide = self.rect.colliderect(Coin.rect)
        if collide:
            newPart = pygame.image.load("Corpo.png")
            newPartRect = newPart.get_rect()
            newPartRect.center = self.positions[-1]

            self.bodyParts.append(newPartRect)
            Coin.newPosition()
            Status.increaseScore()
            Status.updateTime()
    
    def checkSelfColision(self):
        for bodyPart in self.bodyParts:
            if(self.rect.colliderect(bodyPart)):
                return True
        
        return False

    def getCurrentImage(self):
        currentImage = self.image
        if(self.direction == DIRECTIONS["left"]):
            currentImage = pygame.transform.flip(self.image, True, False)
        elif(self.direction == DIRECTIONS["up"]):
            currentImage = pygame.transform.rotate(self.image, 90)
        elif(self.direction == DIRECTIONS["down"]):
            currentImage = pygame.transform.rotate(self.image, 270)
        
        return currentImage
    
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Moeda.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(20, SCREEN_WIDTH-20), random.randint(20, SCREEN_HEIGHT-20))
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)
    
    def newPosition(self):
        self.rect.center = (random.randint(20, SCREEN_WIDTH-20), random.randint(20, SCREEN_HEIGHT-20))

class Text(pygame.sprite.Sprite):
    def __init__(self, message, rectPosition):
        self.message = message
        self.pygameText = font.render(self.message, True, (255,255,255))
        self.rect = self.pygameText.get_rect()
        self.rect.center = rectPosition
    
    def update(self, message, rectPosition):
        self.message = message
        self.pygameText = font.render(self.message, True, (255,255,255))
        self.rect = self.pygameText.get_rect()
        self.rect.center = rectPosition
    
    def draw(self, surface):
        surface.blit(self.pygameText, self.rect)

class Status(pygame.sprite.Sprite):
    def __init__(self):
        self.score = 0
        self.cicles = 0
        self.time = 15
        self.scoreText = Text("Score: " + str(self.score), (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.timeText = Text("Time left: " + str(self.time), ((SCREEN_WIDTH // 2) + SNAKE_SIZE_IN_PIXELS, (SCREEN_HEIGHT // 2) + SNAKE_SIZE_IN_PIXELS))
    
    def update(self):
        if self.cicles == FPS:
            self.time -= 1
            self.cicles = 0
            self.timeText.update("Time left: " + str(self.time), ((SCREEN_WIDTH // 2) + 10, (SCREEN_HEIGHT // 2) + 10))
        else:
            self.cicles += 1
    
    def draw(self, surface):
        self.scoreText.draw(surface)
        self.timeText.draw(surface)

    def increaseScore(self):
        self.score += 1
        self.scoreText.update("Score: " + str(self.score), (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    
    def updateTime(self):
        if(self.score < 5):
            self.time += 5
            return
        elif(self.score < 10):
            self.time += 3
            return
        self.time += 2

Player = Snake()
GameCoin = Coin()
GameStatus = Status()

playerAlive = True
while playerAlive: #principal loop
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
        pygame.display.update()
    Player.update()
    Player.move()
    Player.checkCoin(GameCoin, GameStatus)
    GameStatus.update()

    DISPLAYSURF.fill((0,0,0))

    Player.draw(DISPLAYSURF)
    GameCoin.draw(DISPLAYSURF)
    GameStatus.draw(DISPLAYSURF)

    playerAlive = Player.isGameRunning(GameStatus)

    pygame.display.update()
    FramePerSec.tick(FPS)