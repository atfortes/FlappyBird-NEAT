import pygame as pg
import random


class Pipe:
    GAP = 200
    VEL = 5

    def __init__(self, start_x, x, min_y, max_y, pipe_img):
        self.passed = False
        self.img = pipe_img
        self.start_x = start_x
        self.x = x
        self.pipe_bottom = self.img
        self.pipe_top = pg.transform.flip(self.img, False, True)
        self.MIN_Y = min_y
        self.MAX_Y = max_y
        self.set_ys()

    def set_ys(self):
        self.y_bottom = random.randint(self.MIN_Y + self.GAP, self.MAX_Y)
        self.y_top = self.y_bottom - self.GAP - self.img.get_height()

    def move(self):
        self.x -= self.VEL
        if self.x < -self.img.get_width():
            self.passed = False
            self.x = self.start_x
            self.set_ys()

        if self.x < 200 - self.img.get_width() and not self.passed:
            self.passed = True
            return 1
        return 0

    def draw(self, window):
        window.blit(self.pipe_bottom, (self.x, self.y_bottom))
        window.blit(self.pipe_top, (self.x, self.y_top))

    def collision(self, bird):
        bird_mask = bird.mask()
        mask_bottom = pg.mask.from_surface(self.pipe_bottom)
        mask_top = pg.mask.from_surface(self.pipe_top)

        offset_bottom = (self.x - bird.x, self.y_bottom - round(bird.y))
        offset_top = (self.x - bird.x, self.y_top - round(bird.y))

        point_bottom = bird_mask.overlap(mask_bottom, offset_bottom)
        point_top = bird_mask.overlap(mask_top, offset_top)

        return point_bottom and len(point_bottom) > 1 or point_top and len(point_top) > 1
