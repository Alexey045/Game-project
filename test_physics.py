import os
import sys
from pygame.locals import *
import pygame
import Box2D as b


def main():
    pygame.init()
    pygame.font.init()
    WIDTH = 600
    HEIGHT = 600
    DATA_FILE = 'data'
    size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    running = True
    world = b.b2World()
    world.gravity = (0, -100)
    ground = world.CreateStaticBody(position=(0, -5), shapes=b.b2PolygonShape(box=(59, 5)))
    player_image = load_image('project.png', DATA_FILE, -1)
    player_location = [100, HEIGHT - player_image.get_height()]
    # pygame.Rect(100, height - 220, player_image.get_width(),
    # player_image.get_height())
    person = Hero(world)
    while running:
        person.get_x_y()
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            person.movement(event)
        person.check()
        person.awake()
        person.set_x_y()
        screen.fill((220, 220, 0))
        person.drawPolygons(screen, size)
        screen.blit(player_image, player_location)
        # drawPolygons(screen, ground)
        pygame.display.flip()
        world.Step(1 / 60, 10, 10)
        clock.tick(60)
    terminate()


def load_image(name, DATA_FILE, color_key=None):
    fullname = os.path.join(DATA_FILE, name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


class Camera:  # ToDO
    def __init__(self, field_size):
        self.dx = 0
        self.dy = 0
        self.field_size = field_size

    def apply(self, obj):
        obj.rect.x += self.dx
        if obj.rect.x < -obj.rect.width:
            obj.rect.x += (self.field_size[0] + 1) * obj.rect.width
        if obj.rect.x >= (self.field_size[0]) * obj.rect.width:
            obj.rect.x += -obj.rect.width * (1 + self.field_size[0])
        obj.rect.y += self.dy
        if obj.rect.y < -obj.rect.height:
            obj.rect.y += (self.field_size[1] + 1) * obj.rect.height
        if obj.rect.y >= (self.field_size[1]) * obj.rect.height:
            obj.rect.y += -obj.rect.height * (1 + self.field_size[1])

    def update(self, target, WIDTH, HEIGHT):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


class Hero:
    def __init__(self, world):
        self.jump = False
        self.moving_left = False
        self.moving_right = False
        self.body = world.CreateDynamicBody(
            angle=0, position=(0.75, 22), shapes=b.b2PolygonShape(box=(0.75, 1.55)))  # 1 = 20 pixels
        self.x, self.y = 0, 0

    def get_x_y(self):
        self.x = self.body.linearVelocity.x
        self.y = self.body.linearVelocity.y

    def set_x_y(self):
        self.body.linearVelocity.x = self.x
        self.body.linearVelocity.y = self.y

    def awake(self):
        self.body.awake = True

    def movement(self, event):
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                self.moving_right = True
            if event.key == K_LEFT:
                self.moving_left = True
            if event.key == K_UP:
                if self.jump and len(self.body.contacts) != 0:
                    self.y += 50
                    self.jump = False
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                self.moving_right = False
            if event.key == K_LEFT:
                self.moving_left = False

    def check(self):
        if self.moving_left:
            if self.x > -15:
                self.x -= 1
        if self.moving_right:
            if self.x < 15:
                self.x += 1
        if len(self.body.contacts) != 0:  # ToDo сделать проверку на нижнюю грань
            self.jump = True

    def drawPolygons(self, screen, size):
        height = size[0]
        for fixture in self.body.fixtures:
            shape = fixture.shape
            vertices = [self.body.transform * v * 10 for v in shape.vertices]
            vertices = [(v[0], height - v[1]) for v in vertices]
            print(vertices)
            pygame.draw.polygon(screen, (255, 255, 255), vertices)


# formula = 0.05 * (WIDTH - 1) - нахождение позиции центра объекта
# vertical = 0.05 * (SIZE - 1) - нахождение размеров объетка

if __name__ == '__main__':
    main()
