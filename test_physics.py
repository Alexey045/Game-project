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
            self.animations_right = [load_image('walk1.png', DATA_FILE, -1), load_image('walk2.png', DATA_FILE, -1),
                                     load_image('walk3.png', DATA_FILE, -1)]
            self.animations_right = [load_image('walk-1.png', DATA_FILE, -1), load_image('walk-2.png', DATA_FILE, -1),
                                     load_image('walk-3.png', DATA_FILE, -1)]
            self.sprite = load_image('stand1.png', DATA_FILE, -1)
            self.player_location = [10, HEIGHT - self.sprite.get_height() - 48]
            self.body = level.CreateDynamicBody(
                angle=0, position=(self.get_box2d_coordinates()),
                shapes=b.b2PolygonShape(box=(self.get_box2d_size())))  # 1 = 20 pixel
            self.x, self.y = 0, 0
            self.check_jump = 0
            self.stand = True
            self.dir = 1
            self.left = False
            self.right = False
            self.run = False
            self.j_check = False
            self.start = True

        def get_box2d_coordinates(self):
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

        def get_box2d_size(self):
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
                        self.stand = False
                        self.check_jump = 0
            if events.type == KEYUP:
                if events.key == K_RIGHT:
                    self.moving_right = False
                if events.key == K_LEFT:
                    self.moving_left = False

        def change_dir(self):  # ToDo
            if self.body.linearVelocity[0] > 0:
                self.dir = 1
                self.run = True
            elif self.body.linearVelocity[0] < 0:
                self.dir = -1
                self.run = True
            if self.body.linearVelocity[0] == 0:
                self.run = False

        def check(self):
            if self.moving_left:
                if self.x > -13:
                    self.x -= 1
            if self.moving_right:
                if self.x < 13:
                    self.x += 1
            if not self.j_check and not self.jump and not self.start:
                if self.dir == 1:
                    self.sprite = load_image('jump1.png', DATA_FILE, -1)
                elif self.dir == -1:
                    self.sprite = load_image('jump-1.png', DATA_FILE, -1)
                self.j_check = True
            if len(self.body.contacts) != 0:
                if self.check_jump != 8:
                    self.check_jump += 1
                if self.check_jump == 8 and self.body.linearVelocity[1] == 0:
                    self.jump = True
                    self.j_check = False
                    self.start = False
                    if not self.run:
                        if self.dir == 1:
                            self.sprite = load_image('stand1.png', DATA_FILE, -1)
                        elif self.dir == -1:
                            self.sprite = load_image('stand-1.png', DATA_FILE, -1)
                    elif self.run:
                        pass
                        """if self.dir == 1:
                            self.sprite = load_image('stand1.png', DATA_FILE, -1)
                        elif self.dir == -1:
                            self.sprite = load_image('stand-1.png', DATA_FILE, -1)"""

        def draw_polygons(self, py_screen):
            for fixture in self.body.fixtures:
                shape = fixture.shape
                vertices = [self.body.transform * v * 10 for v in shape.vertices]
                vertices = [(v[0], 240 - v[1]) for v in vertices]
                pygame.draw.polygon(py_screen, (255, 255, 255), vertices)

        def death(self):  # ToDo
            if self.player_location[1] + self.sprite.get_height() >= HEIGHT:
                return False
            else:
                return True

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
    my_map = Map('test.tmx', world, DATA_FILE, HEIGHT)
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
        person.change_dir()
        running = person.death()
        # camera.update(player)
        screen.fill(SKY)
        my_map.render(screen)
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


def get_box2d_size(image, last, first):
    size_x = 0.05 * ((image.get_width() - 1) * (last - first + 1)) + 0.1
    size_x += int(size_x / 0.85) * 0.05 - 0.05
    size_y = 0.05 * (image.get_height() - 1)
    return size_x, size_y


def draw_polygons(screen, i):
    for fixture in i.fixtures:
        shape = fixture.shape
        vertices = [i.transform * v * 10 for v in shape.vertices]
        vertices = [(v[0], 240 - v[1]) for v in vertices]
        pygame.draw.polygon(screen, (255, 255, 255), vertices)


class Map:
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
                            self.set_collision(get_box2d_size(image, last_x, first_x),
                                               self.get_box2d_coordinates(image, first_x, y, self.HEIGHT, last_x,
                                                                          first_x))
                        elif self.map.get_tile_image(x + 1, y, 0) is None:
                            last_x = x
                            first = False
                            self.set_collision(get_box2d_size(image, last_x, first_x),
                                               self.get_box2d_coordinates(image, first_x, y, self.HEIGHT, last_x,
                                                                          first_x))
                        else:
                            first = True
                    screen.blit(image, (x * self.tile_width, y * self.tile_height))
        self.col = False

    def set_collision(self, sizes, coordinates):
        self.world.CreateStaticBody(position=coordinates,
                                    shapes=b.b2PolygonShape(box=sizes))

    def get_box2d_coordinates(self, image, x, y, HEIGHT, last, first):
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
