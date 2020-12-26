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
    # obj.gravityScale = 0.0  # ставит гравитацию для обЪекта на ноль
    # player_image = pygame.image.load('project.png')
    # player_location = [100, height - 220]
    # pygame.Rect(100, height - 220, player_image.get_width(),
    #            player_image.get_height())
    velocity = x, y = 0, 0
    while running:
        screen.fill((220, 220, 0))
        """Линейная скорость хороша, как константа. Но если в падении двигаться, 
        то скорость падения уменьшается. А импульс и сила не знаю как ограничить.
         Надо найти решение. и подумать как обЪединить со спрайтом."""
        if moving_left:  # ToDo линейная скорость ведет себя странно
            if x <= -20:
                x = -20
            elif x > 0:
                x = 0
            else:
                x -= 1
            obj.linearVelocity = (x, y)
            # obj.ApplyLinearImpulse(b2Vec2(-0.3, 0), (2.5, 2.5), True)
        if moving_right:
            if x >= 20:
                x = 20
            elif x < 0:
                x = 0
            else:
                x += 1
            obj.linearVelocity = (x, y)
            # obj.ApplyForceToCenter(b2Vec2(50, 0), True)
            # obj.ApplyLinearImpulse(b2Vec2(0.3, 0), (2.5, 2.5), True)
        if not moving_up:  # ToDo что-то в таком роде.
            if y > 0 and len(obj.contacts) == 0:
                y -= 1
        if moving_up:
            # obj.ApplyForceToCenter(b2Vec2(0, 50), True)
            # obj.linearVelocity = (0, 5)
            # obj.ApplyLinearImpulse(b2Vec2(0, 0.3), (2.5, 2.5), True)
            if y >= 20:
                y = 20
            elif y < 0:
                y = 0
            else:
                y += 1
            obj.linearVelocity = (x, y)
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
