from pygame.locals import *
import pygame
import Box2D as b


def main():
    pygame.init()
    pygame.font.init()
    size = width, height = (600, 450)
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    moving_right = False
    moving_left = False
    running = True
    world = b.b2World()
    world.gravity = (0, -100)
    ground = world.CreateStaticBody(
        position=(0, -5), shapes=b.b2PolygonShape(box=(59, 5)))
    obj = world.CreateDynamicBody(
        angle=0, position=(10, 22), shapes=b.b2PolygonShape(box=(5, 5)))
    obj.friction = 0
    ground.friction = 0
    # player_image = pygame.image.load('project.png')
    # player_location = [100, height - 220]
    # pygame.Rect(100, height - 220, player_image.get_width(),
    # player_image.get_height())
    jump = False
    while running:
        x, y = obj.__GetLinearVelocity()
        print(x)
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    moving_right = True
                if event.key == K_LEFT:
                    moving_left = True
                if event.key == K_UP:
                    if jump and len(obj.contacts) != 0:
                        y += 50
                        jump = False
            if event.type == KEYUP:
                if event.key == K_RIGHT:
                    moving_right = False
                if event.key == K_LEFT:
                    moving_left = False
        if moving_left:
            if x > -15:
                x -= 1
        if moving_right:
            if x < 15:
                x += 1
        if len(obj.contacts) != 0:
            jump = True
        obj.__SetLinearVelocity([x, y])
        screen.fill((220, 220, 0))
        drawPolygons(screen, obj)
        # screen.blit(player_image, player_location)
        drawPolygons(screen, ground)
        world.Step(1 / 60, 10, 10)
        pygame.display.flip()
        clock.tick(60)


def drawPolygons(screen, body):
    for fixture in body.fixtures:
        shape = fixture.shape
        vertices = [body.transform * v * 10 for v in shape.vertices]
        vertices = [(v[0], 450 - v[1]) for v in vertices]
        pygame.draw.polygon(screen, (255, 255, 255), vertices)


if __name__ == '__main__':
    main()
