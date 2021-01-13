import os
import sys
from abc import ABC, abstractmethod
from pygame.locals import *
import pygame
import pytmx
import Box2D as b
import pygame_gui


def main():
    pygame.mixer.pre_init()
    pygame.init()
    pygame.font.init()

    vec = pygame.math.Vector2
    py_world = pygame.Surface((1600, 240))

    manager_menu = pygame_gui.UIManager((320, 240))
    manager_death = pygame_gui.UIManager((320, 240))
    manager_win = pygame_gui.UIManager((320, 240))

    class Hero:
        def __init__(self, level):
            self.jump = False
            self.moving_left = False
            self.moving_right = False
            self.animations_right = [load_image('walk1.png', DATA_FILE, -1),
                                     load_image('walk2.png', DATA_FILE, -1),
                                     load_image('walk3.png', DATA_FILE, -1),
                                     load_image('walk2.png', DATA_FILE, -1),
                                     load_image('walk1.png', DATA_FILE, -1),
                                     load_image('walk2.png', DATA_FILE, -1),
                                     load_image('walk3.png', DATA_FILE, -1),
                                     load_image('walk2.png', DATA_FILE, -1),
                                     load_image('walk1.png', DATA_FILE, -1),
                                     load_image('walk2.png', DATA_FILE, -1),
                                     load_image('walk3.png', DATA_FILE, -1),
                                     load_image('walk2.png', DATA_FILE, -1)]
            self.animations_left = [load_image('walk-1.png', DATA_FILE, -1),
                                    load_image('walk-2.png', DATA_FILE, -1),
                                    load_image('walk-3.png', DATA_FILE, -1),
                                    load_image('walk-2.png', DATA_FILE, -1),
                                    load_image('walk-1.png', DATA_FILE, -1),
                                    load_image('walk-2.png', DATA_FILE, -1),
                                    load_image('walk-3.png', DATA_FILE, -1),
                                    load_image('walk-2.png', DATA_FILE, -1),
                                    load_image('walk-1.png', DATA_FILE, -1),
                                    load_image('walk-2.png', DATA_FILE, -1),
                                    load_image('walk-3.png', DATA_FILE, -1),
                                    load_image('walk-2.png', DATA_FILE, -1)
                                    ]
            self.sprite = load_image('stand1.png', DATA_FILE, -1)
            self.start_pos = (10, HEIGHT - self.sprite.get_height() - 48)
            self.player_location = [10, HEIGHT - self.sprite.get_height() - 48]
            self.body = level.CreateDynamicBody(
                angle=0, position=(self.get_box2d_coordinates()),
                shapes=b.b2PolygonShape(box=(self.get_box2d_size())))  # 1 = 20 pixel
            self.start_box2d = self.get_box2d_coordinates()
            self.x, self.y = 0, 0
            self.check_jump = 0
            self.anim_count = 0
            self.stand = True
            self.dir = 1
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
                if events.key == K_RIGHT or events.key == K_d:
                    self.moving_right = True
                if events.key == K_LEFT or events.key == K_a:
                    self.moving_left = True
                if events.key == K_UP or events.key == K_w:
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

        def change_dir(self):
            if self.body.linearVelocity[0] > 0:
                self.dir = 1
                self.run = True
            elif self.body.linearVelocity[0] < 0:
                self.dir = -1
                self.run = True
            if self.body.linearVelocity[0] == 0:
                self.anim_count = 0
                self.run = False

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

        def win(self):
            if self.player_location[0] >= (py_world.get_width() - (16 * 10.5)):
                return True
            else:
                return False

    class Menu:
        def __init__(self, man):
            self.manager = man
            self.layer = pygame.Surface((320, 240))
            self.label = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((70, 30), (180, 60)), text='Super Yandex Proj.',
                manager=self.manager
            )
            self.switch = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((130, 90), (60, 60)),
                text="Start",
                manager=self.manager
            )

    class Death:
        def __init__(self, man):
            self.manager = man
            self.layer = pygame.Surface((320, 240))
            self.label = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((70, 30), (180, 60)), text='YOU DIED',
                manager=self.manager)

    class Win:
        def __init__(self, man):
            self.manager = man
            self.layer = pygame.Surface((320, 240))
            self.label = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((70, 30), (180, 60)), text='YOU WIN!!!',
                manager=self.manager)

    class Camera:
        def __init__(self, player):
            self.player = player
            self.offset = vec(0, 0)
            self.offset_float = vec(0, 0)
            self.w, self.h = 320, 240
            self.CONST = vec(-self.w / 2 + self.player.sprite.get_width() / 2,
                             -self.player.sprite.get_height() + 20)

        def scroll(self):
            self.method.scroll()

        def set_method(self, method):
            self.method = method

    class CamScroll(ABC):
        def __init__(self, cam, player):
            self.player = player
            self.camera = cam

        @abstractmethod
        def scroll(self):
            pass

    class Follow(CamScroll):
        def __init__(self, cam, player):
            CamScroll.__init__(self, cam, player)

        def scroll(self):
            self.camera.offset_float.x += (
                    self.player.player_location[0] - self.camera.offset_float.x + self.camera.CONST.x)
            self.camera.offset.x, self.camera.offset.y = int(self.camera.offset_float.x), 0

    class Border(CamScroll):
        def __init__(self, cam, player):
            CamScroll.__init__(self, cam, player)

        def scroll(self):
            self.camera.offset_float.x += (
                    self.player.player_location[0] - self.camera.offset_float.x + self.camera.CONST.x)
            self.camera.offset.x, self.camera.offset.y = int(self.camera.offset_float.x), 0
            self.camera.offset.x = max(self.player.player_location, self.camera.offset.x)
            self.camera.offset.x = min(self.camera.offset.x,
                                       self.player.player_location + self.player.sprite - self.camera.w)

    class Auto(CamScroll):
        def __init__(self, cam, player):
            CamScroll.__init__(self, cam, player)

        def scroll(self):
            self.camera.offset.x += 1

    WIDTH = 320
    HEIGHT = 240
    DATA_FILE = 'data'
    SIZE = (WIDTH, HEIGHT)
    SKY = (119, 128, 225)

    flag = pygame.SCALED | pygame.FULLSCREEN
    screen = pygame.display.set_mode(SIZE, flag)
    pygame.display.set_caption('Super Yandex proj.')
    clock = pygame.time.Clock()

    pygame.mixer.music.load(link_file('ambient.wav', DATA_FILE))
    pygame.mixer.music.play(-1)
    jump_sound = pygame.mixer.Sound(link_file('jump.wav', DATA_FILE))
    death_sound = pygame.mixer.Sound(link_file('death.wav', DATA_FILE))
    win_sound = pygame.mixer.Sound(link_file('jump.wav', DATA_FILE))

    world = b.b2World()
    world.gravity = (0, -100)
    world.CreateStaticBody(position=(0, -5), shapes=b.b2PolygonShape(box=(70, 5)))
    world.CreateStaticBody(position=(-5, 0), shapes=b.b2PolygonShape(box=(5.05, 100)))

    menu = Menu(manager_menu)
    death = Death(manager_death)
    win = Win(manager_win)

    person = Hero(world)
    my_map = Map('main1.tmx', world, DATA_FILE, HEIGHT)
    camera = Camera(person)
    follow = Follow(camera, person)
    Auto(camera, person)
    Border(camera, person)

    camera.set_method(follow)
    music = False
    start_menu = True
    running = True
    while running:
        delta_time = 17 / 1000.0
        person.merge()
        person.awake()
        person.get_x_y()

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return
            if event.type == QUIT:
                return
            if not start_menu:
                person.movement(event)
            if start_menu:
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == menu.switch:
                            start_menu = False
                            music = True
            manager_menu.process_events(event)

        menu.manager.update(delta_time)
        death.manager.update(delta_time)
        win.manager.update(delta_time)

        person.check()
        person.set_x_y()
        person.change_dir()

        if music:
            pygame.mixer.music.load(link_file('disco.wav', DATA_FILE))
            pygame.mixer.music.play(-1, 0, 3000)
            music = False

        if person.anim_count + 1 >= 60:
            person.anim_count = 0
        elif not person.jump and not person.start:
            if person.dir == 1:
                person.sprite = load_image('jump1.png', DATA_FILE, -1)
            elif person.dir == -1:
                person.sprite = load_image('jump-1.png', DATA_FILE, -1)
            person.j_check = True
        elif person.moving_right:
            person.sprite = person.animations_right[person.anim_count // 5]
            person.anim_count += 1
        elif person.moving_left:
            person.sprite = person.animations_left[person.anim_count // 5]
            person.anim_count += 1

        camera.scroll()

        screen.fill(SKY)
        py_world.fill(SKY)

        my_map.render(py_world)
        screen.blit(py_world, [0 - camera.offset.x, 0])
        screen.blit(person.sprite, [person.player_location[0] - camera.offset.x, person.player_location[1]])

        if start_menu:
            menu.layer.fill(SKY)
            menu.manager.draw_ui(menu.layer)
            screen.blit(menu.layer, [0, 0])

        if not person.death():
            pygame.mixer.music.stop()
            death.layer.fill(SKY)
            death.manager.draw_ui(death.layer)
            screen.blit(death.layer, [0, 0])

        if person.win():  # ToDo
            pygame.mixer.music.stop()
            win.layer.fill(SKY)
            win.manager.draw_ui(win.layer)
            screen.blit(win.layer, [0, 0])

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


def link_file(name, DATA_FILE):
    if not isinstance(name, str):
        raise TypeError('file name must be str type')
    fullname = os.path.join(DATA_FILE, name)
    if os.path.exists(fullname):
        return fullname
    else:
        raise FileNotFoundError(f'Cannot find image: {name}')


def get_box2d_size(image, last, first):
    size_x = 0.05 * ((image.get_width() - 1) * (last - first + 1))
    size_x += int(size_x / 0.85) * 0.05 + 0.05
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

    def change_map(self, map_name, DATAFILE):
        self.map = pytmx.load_pygame(link_file(map_name, DATAFILE))

    def render(self, screen):
        first_x = 0
        first_sprite = False
        for y in range(self.height):
            for x in range(self.width):
                image = self.map.get_tile_image(x, y, 0)
                if image is not None:
                    if not first_sprite:
                        first_x = x
                        first_sprite = True
                    if self.col:
                        if x == self.width - 1:
                            last_x = x
                            first_sprite = False
                            self.set_collision(get_box2d_size(image, last_x, first_x),
                                               self.get_box2d_coordinates(image, first_x, y, self.HEIGHT,
                                                                          last_x,
                                                                          first_x))
                        elif self.map.get_tile_image(x + 1, y, 0) is None:
                            last_x = x
                            first_sprite = False
                            self.set_collision(get_box2d_size(image, last_x, first_x),
                                               self.get_box2d_coordinates(image, first_x, y, self.HEIGHT,
                                                                          last_x,
                                                                          first_x))
                        else:
                            first_sprite = True
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
