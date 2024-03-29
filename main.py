import pygame
import random

# Initialize Pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('space.png')

# Title and Icon
pygame.display.set_caption("Tacos Invade")
icon = pygame.image.load('rocket.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('Ironman.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = pygame.image.load('taco.png')
enemyX = random.randint(0, 800)
enemyY = random.randint(50, 150)
enemyX_change = 0.3
enemyY_change = 40

# Explosion
explosionImg = pygame.image.load('explosion.png')
explosion_state = "ready"

# Bullet
bulletImg = pygame.image.load('egg.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1
bullet_state = "ready"

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y):
    screen.blit(enemyImg, (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = ((enemyX - bulletX)**2 + (enemyY - bulletY)**2)**0.5
    if distance < 27:
        return True
    else:
        return False

def explode(x, y):
    global explosion_state
    explosion_state = "exploded"
    screen.blit(explosionImg, (x, y))

# Game Loop
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.7
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.7
            if event.key == pygame.K_UP:
                if bullet_state == "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    enemyX += enemyX_change
    if enemyX <= 0:
        enemyX_change = 0.3
        enemyY += enemyY_change
    elif enemyX >= 736:
        enemyX_change = -0.3
        enemyY += enemyY_change

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    collision = isCollision(enemyX, enemyY, bulletX, bulletY)
    if collision:
        explode(enemyX, enemyY)
        bulletY = 480
        bullet_state = "ready"
        enemyX = random.randint(0, 800)
        enemyY = random.randint(50, 150)

    if bulletY < 0:
        bulletY = 480
        bullet_state = "ready"

    if explosion_state == "exploded":
        explode(enemyX, enemyY)
        explosion_state = "ready"

    player(playerX, playerY)
    enemy(enemyX, enemyY)

    pygame.display.update()
