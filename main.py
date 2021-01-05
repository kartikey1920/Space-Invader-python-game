import pygame
import random
import math

pygame.init()

screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption("Space Invader")
icon = pygame.image.load('project.png')
pygame.display.set_icon(icon)

background = pygame.image.load('background.png')

playerimg = pygame.image.load('player.png')
X = 370
Y = 490
X_change = 0

enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_enemies = 6

for i in range(num_enemies):
    enemyimg.append(pygame.image.load('ufo.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(2)
    enemyY_change.append(30)

bulletimg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 490
bulletX_change = 0
bulletY_change = 4
bullet_state = "ready"

score_value = 0
font = pygame.font.Font('FunSized.ttf', 32)
textX = 340
textY = 20

# game over text
over_font = pygame.font.Font('FunSized.ttf', 66)


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (225, 225, 0))
    screen.blit(over_text, (200, 250))


def show_score(x, y):
    score = font.render("Score  " + str(score_value), True, (225, 225, 0))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerimg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))


def bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x + 16, y))


def iscollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True


running = True
while running:

    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                X_change -= 5
            if event.key == pygame.K_RIGHT:
                X_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = X
                    bullet(X, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                X_change = 0

    X += X_change

    if X <= 0:
        X = 0
    elif X >= 736:
        X = 736

    for i in range(num_enemies):
        # game over
        if enemyY[i] > 440:
            for j in range(num_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]

        collision = iscollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 490
            bullet_state = 'ready'
            score_value += 1
            print(score_value)
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    if bulletY <= 0:
        bulletY = 490
        bullet_state = "ready"
    if bullet_state == "fire":
        bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(X, Y)
    show_score(textX, textY)

    pygame.display.update()
