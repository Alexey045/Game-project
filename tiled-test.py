import os
import sys
import pygame
import pytmx
from pygame.locals import *

WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 320, 240
FPS = 60
DATA_FILE = 'data'
TILE_SIZE = 16


def load_image(name, color_key=None):
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


def link_file(name):
    if not isinstance(name, str):
        raise TypeError('file name must be str type')
    fullname = os.path.join(DATA_FILE, name)
    if os.path.exists(fullname):
        return fullname
    else:
        raise FileNotFoundError(f'Cannot find image: {name}')


class Labyrinth:
    def __init__(self, filename):
        self.map = pytmx.load_pygame(
            link_file(filename))  # внутри map файла прописаны пути к
        # ассетам. можно изменить вручную, или через tiled
        # print(self.map.tiledgidmap[self.map.get_tile_gid(1, 1, 0)])
        if self.map.tiledgidmap[self.map.get_tile_gid(1, 1, 0)] == 4:  # ToDo
            print('yes')
        self.height = self.map.height
        self.width = self.map.width
        self.tile_height = self.map.tileheight
        self.tile_width = self.map.tilewidth
        # self.free_tiles = free_tiles

    def get_tile_id(self, pos):
        return self.map.tiledgidmap[self.map.get_tile_gid(*pos, 0)]

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                image = self.map.get_tile_image(x, y, 0)
                if image is not None:
                    image.get_height()
                    image.get_width()
                    # x * self.tile_width, y * self.tile_height
                    screen.blit(image, (x * self.tile_width, y * self.tile_height))


class Hero:
    def __init__(self, pos):
        self.x, self.y = pos

    def get_pos(self):
        return self.x, self.y

    def set_pos(self, pos):
        self.x, self.y = pos

    def render(self, screen):
        pass

    def movement(self):
        pass


class Enemy(Hero):
    def __init__(self, pos):
        super().__init__(pos)
        self.x, self.y = pos

    def movement(self):
        pass


def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    labyrinth = Labyrinth('test.tmx')
    clock = pygame.time.Clock()
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        screen.fill((119, 128, 225))
        labyrinth.render(screen)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
