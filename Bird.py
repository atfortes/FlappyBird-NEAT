import pygame as pg


class Bird:
    TILT_VEL = 10
    MAX_TILT_UP = 25
    MAX_TILT_DOWN = -80
    ANIMATION_TIME = 5

    def __init__(self, x, y, bird_imgs):
        self.imgs = bird_imgs
        self.x = x
        self.y = y
        self.height = y
        self.img = self.imgs[0]
        self.img_count = 1
        self.tilt = 0
        self.vel = 0
        self.time = 0

    def jump(self):
        self.time = 0
        self.vel = -8.5
        self.height = self.y

    def move(self):
        self.time += 1

        # terminal velocity
        dist = min(self.vel*self.time + self.time**2, 16)

        self.y += dist if dist >= 0 else dist-2

        if dist < 0 or self.y < self.height - 30:
            self.tilt = self.MAX_TILT_UP
        elif self.tilt > self.MAX_TILT_DOWN:
            self.tilt -= self.TILT_VEL

    def draw(self, window):

        switcher = {
            0: self.imgs[0],
            1: self.imgs[1],
            2: self.imgs[2],
            3: self.imgs[1],
            4: self.imgs[0]
        }
        self.img = switcher.get(self.img_count // self.ANIMATION_TIME)
        self.img_count = self.img_count + 1 if self.img_count // self.ANIMATION_TIME < 4 else 1

        if self.tilt < 0:
            self.img = self.imgs[1]
            self.img_count = self.ANIMATION_TIME*2

        rotated_image = pg.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)

        window.blit(rotated_image, new_rect.topleft)

    def mask(self):
        return pg.mask.from_surface(self.img)
