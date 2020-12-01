import pygame
import sys
from pygame.locals import *

pygame.init()  # инициализируем pygame
clock = pygame.time.Clock()  # обновление экрана через тики
pygame.display.set_caption('Test')  # название окна
WindowSize = (600, 400)  # размер окна
display = pygame.Surface((300, 200))
screen = pygame.display.set_mode(WindowSize, 0)

player_image = pygame.image.load('hero.png')
dirt = pygame.image.load('brick.png')

game_map = [[]]

player_location = [50, 50]
player_y_momentum = 0
player_rect = pygame.Rect(player_location[0], player_location[1], player_image.get_width(),
                          player_image.get_height())
test_rect = pygame.Rect(100, 100, 100, 50)
dirt_rect = pygame.Rect(32, 32, 50, 200)

moving_right = False
moving_left = False

while True:  # игровой цикл
    screen.fill((255, 255, 255))  # заполнение заднего плана белым цветом
    screen.blit(player_image, player_location)  # отображение персонажа
    screen.blit(dirt, [50, 200])
    if player_location[1] > WindowSize[1] - player_image.get_height():
        player_y_momentum = - player_y_momentum
    else:
        player_y_momentum += 0.2
    player_location[1] += player_y_momentum

    if moving_left:
        player_location[0] -= 4
    if moving_right:
        player_location[0] += 4

    player_rect.x = player_location[0]
    player_rect.y = player_location[1]
    for event in pygame.event.get():  # нажатие на кнопки
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False
    pygame.display.update()  # обновлние определнных чатсей на экране
    clock.tick(60)  # 60 фпс
