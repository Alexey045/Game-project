import sys

from Box2D import b2Vec2
from pygame.locals import *
import pygame
import Box2D as b


def main():
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((600, 450))
    clock = pygame.time.Clock()
    moving_right = False
    moving_left = False
    moving_up = False
    running = True
    world = b.b2World()
    world.gravity = (0, -5)
    ground = world.CreateStaticBody(
        position=(0, -5), shapes=b.b2PolygonShape(box=(59, 5)))
    obj = world.CreateDynamicBody(
        angle=0, position=(10, 22), shapes=b.b2PolygonShape(box=(5, 5)))
    while running:
        screen.fill((220, 220, 0))
        if moving_left:
            obj.ApplyLinearImpulse(b2Vec2(-2, 0), (2.5, 2.5), True)
        if moving_right:
            obj.ApplyForceToCenter(b2Vec2(50, 0), True)
        if moving_up:
            obj.ApplyForceToCenter(b2Vec2(0, 50), True)
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
        # drawPolygons(screen, ground)
        world.Step(1 / 60, 10, 10)
        pygame.display.flip()
        clock.tick(60)


def drawPolygons(screen, body):
    for fixture in body.fixtures:
        shape = fixture.shape
        vertices = [body.transform * v * 10 for v in shape.vertices]
        vertices = [(v[0], 450 - v[1]) for v in vertices]
        name = pygame.draw.polygon(screen, (255, 255, 255), vertices)


if __name__ == '__main__':
    main()
