import os
import sys
from pygame.locals import *
import pygame
import pytmx
import Box2D as b


def main():
    class Hero:
        def __init__(self, level):
            self.jump = False
            self.moving_left = False
            self.moving_right = False
            self.sprite = load_image('project.png', DATA_FILE, -1)
            self.player_location = [113, HEIGHT - self.sprite.get_height() - 48]
            self.body = level.CreateDynamicBody(
                angle=0, position=(self.coordinates()),
                shapes=b.b2PolygonShape(box=(self.size())))  # 1 = 20 pixel
            self.x, self.y = 0, 0
            self.check_jump = 0

        def coordinates(self):
            formula_x = 0.1 * (self.player_location[0] + (self.sprite.get_width() / 2))
            if formula_x > 0:
                formula_x -= 0.05
            elif formula_x < 0:
                formula_x += 0.05
            formula_y = 0.1 * ((HEIGHT - self.player_location[1]) - (self.sprite.get_height() / 2))
            if formula_y > 0:
                formula_y -= 0.05
            elif formula_y < 0:
                formula_y += 0.05
            return formula_x, formula_y

        def merge(self):
            x, y = person.body.position
            self.player_location = [x / 0.1 - (self.sprite.get_width() / 2) + 0.05,
                                    -(y / 0.1 - HEIGHT + (self.sprite.get_height() / 2))]

        def size(self):
            size_x = 0.05 * (self.sprite.get_width() - 1)
            size_y = 0.05 * (self.sprite.get_height() - 1)
            return size_x, size_y

        def get_x_y(self):
            self.x = self.body.linearVelocity.x
            self.y = self.body.linearVelocity.y

        def set_x_y(self):
            self.body.linearVelocity.x = self.x
            self.body.linearVelocity.y = self.y

        def awake(self):
            self.body.awake = True

        def movement(self, events):
            if events.type == KEYDOWN:
                if events.key == K_RIGHT:
                    self.moving_right = True
                if events.key == K_LEFT:
                    self.moving_left = True
                if events.key == K_UP:
                    if self.jump and len(self.body.contacts) != 0:
                        self.y += 40
                        self.jump = False
                        self.check_jump = 0
            if events.type == KEYUP:
                if events.key == K_RIGHT:
                    self.moving_right = False
                if events.key == K_LEFT:
                    self.moving_left = False

        def check(self):
            if self.moving_left:
                if self.x > -13:
                    self.x -= 1
            if self.moving_right:
                if self.x < 13:
                    self.x += 1
            if len(self.body.contacts) != 0:
                if self.check_jump != 8:
                    self.check_jump += 1
                if self.check_jump == 8 and self.y == 0:
                    self.jump = True

        def drawPolygons(self, py_screen):
            for fixture in self.body.fixtures:
                shape = fixture.shape
                vertices = [self.body.transform * v * 10 for v in shape.vertices]
                vertices = [(v[0], 240 - v[1]) for v in vertices]
                pygame.draw.polygon(py_screen, (255, 255, 255), vertices)

        def animation(self):
            pass

        def death(self):
            pass

    pygame.init()
    pygame.font.init()
    WIDTH = 320
    HEIGHT = 240
    SIZE = (WIDTH, HEIGHT)
    SKY = (119, 128, 225)
    screen = pygame.display.set_mode(SIZE)
    clock = pygame.time.Clock()
    running = True
    world = b.b2World()
    world.gravity = (0, -100)
    world.CreateStaticBody(position=(0, -5), shapes=b.b2PolygonShape(box=(70, 5)))
    DATA_FILE = 'data'
    person = Hero(world)
    labyrinth = Labyrinth('test.tmx', world, DATA_FILE, HEIGHT)
    while running:
        person.merge()
        person.awake()
        person.get_x_y()
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            person.movement(event)
        person.check()
        person.set_x_y()
        # camera.update(player)
        screen.fill(SKY)
        labyrinth.render(screen)
        # person.drawPolygons(screen)
        screen.blit(person.sprite, person.player_location)
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


# Todo
"""class Camera:
    def __init__(self, field_size):
        self.dx = 0
        self.dy = 0
        # self.field_size = field_size # 20, 15
        self.field_size = 20, 15

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
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)"""


def link_file(name, DATA_FILE):
    if not isinstance(name, str):
        raise TypeError('file name must be str type')
    fullname = os.path.join(DATA_FILE, name)
    if os.path.exists(fullname):
        return fullname
    else:
        raise FileNotFoundError(f'Cannot find image: {name}')


def size(image, last, first):
    size_x = 0.05 * ((image.get_width() - 1) * (last - first + 1)) + 0.1
    size_x += int(size_x / 0.85) * 0.05 - 0.05
    size_y = 0.05 * (image.get_height() - 1)
    return size_x, size_y


def drawPolygons(screen, i):
    for fixture in i.fixtures:
        shape = fixture.shape
        vertices = [i.transform * v * 10 for v in shape.vertices]
        vertices = [(v[0], 240 - v[1]) for v in vertices]
        pygame.draw.polygon(screen, (255, 255, 255), vertices)


class Labyrinth:
    def __init__(self, filename, world, DATAFILE, HEIGHT):
        self.map = pytmx.load_pygame(link_file(filename, DATAFILE))
        self.world = world
        self.height = self.map.height
        self.width = self.map.width
        self.tile_height = self.map.tileheight
        self.tile_width = self.map.tilewidth
        self.col = True
        self.tile = 16
        self.HEIGHT = HEIGHT

    def get_tile_id(self, pos):
        return self.map.tiledgidmap[self.map.get_tile_gid(*pos, 0)]

    def render(self, screen):
        first_x = 0
        first = False
        for y in range(self.height):
            for x in range(self.width):
                image = self.map.get_tile_image(x, y, 0)
                if image is not None:
                    if not first:
                        first_x = x
                        first = True
                    if self.col:
                        if x == self.width - 1:
                            last_x = x
                            first = False
                            self.collision(size(image, last_x, first_x),
                                           self.coordinates(image, first_x, y, self.HEIGHT, last_x, first_x))
                        elif self.map.get_tile_image(x + 1, y, 0) is None:
                            last_x = x
                            first = False
                            self.collision(size(image, last_x, first_x),
                                           self.coordinates(image, first_x, y, self.HEIGHT, last_x, first_x))
                        else:
                            first = True
                    screen.blit(image, (x * self.tile_width, y * self.tile_height))
        self.col = False

    def collision(self, sizes, coordinates):
        self.world.CreateStaticBody(position=coordinates,
                                    shapes=b.b2PolygonShape(box=sizes))

    def coordinates(self, image, x, y, HEIGHT, last, first):
        formula_x = 0.1 * ((x * image.get_width()) + (image.get_width() * (last - first + 1) / 2))
        if formula_x > 0:
            formula_x += 0.05
        elif formula_x < 0:
            formula_x += 0.05
        formula_y = 0.1 * (HEIGHT - self.tile_height * y - (image.get_height() / 2))
        if formula_y > 0:
            formula_y += 0.025
        elif formula_y < 0:
            formula_y += 0.05
        return formula_x, formula_y


if __name__ == '__main__':
    main()
