import sys
from Box2D import b2Vec2
from pygame.locals import *
import pygame
import Box2D as b
import pytmx


def main():
    pygame.init()
    pygame.font.init()
    size = width, height = (600, 450)
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    moving_right = False
    moving_left = False
    moving_up = False
    running = True
    world = b.b2World()
    world.gravity = (0, -100)
    ground = world.CreateStaticBody(
        position=(0, -5), shapes=b.b2PolygonShape(box=(59, 5)))
    obj = world.CreateDynamicBody(
        angle=0, position=(10, 22), shapes=b.b2PolygonShape(box=(5, 5)))
    obj.friction = 0
    ground.friction = 0
    # obj.gravityScale = 0.0  # ставит гравитацию для обЪекта на ноль
    # player_image = pygame.image.load('project.png')
    # player_location = [100, height - 220]
    # pygame.Rect(100, height - 220, player_image.get_width(),
    #            player_image.get_height())
    jump = True
    count = 0
    while running:
        x, y = obj.__GetLinearVelocity()
        screen.fill((220, 220, 0))
        if moving_left:
            if x >= -20:
                x -= 1
        if moving_right:
            if x <= 20:
                x += 1
        if not moving_right and not moving_left:
            pass
        if moving_up and jump and count <= 1:  # увеличивает в зависимости от удержания
            count += 1  # ToDo
            y += + 10  # и не равномерно
            jump = False
            print(count)
        obj.__SetLinearVelocity([x, y])
        if len(obj.contacts) != 0:
            jump = True
            count = 0
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    moving_right = True
                if event.key == K_LEFT:
                    moving_left = True
                if event.key == K_UP:
                    moving_up = True
            if event.type == KEYUP:
                if event.key == K_RIGHT:
                    moving_right = False
                if event.key == K_LEFT:
                    moving_left = False
                if event.key == K_UP:
                    moving_up = False
        drawPolygons(screen, obj)
        # screen.blit(player_image, player_location)
        # drawPolygons(screen, ground)
        world.Step(1 / 60, 10, 10)
        pygame.display.flip()
        clock.tick(60)


def drawPolygons(screen, body):
    for fixture in body.fixtures:
        # print(fixture)
        shape = fixture.shape
        vertices = [body.transform * v * 10 for v in shape.vertices]
        # print(vertices)
        # print(vertices)
        vertices = [(v[0], 450 - v[1]) for v in vertices]
        # print(vertices)
        pygame.draw.polygon(screen, (255, 255, 255), vertices)


if __name__ == '__main__':
    main()
