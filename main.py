import os
import pygame as pg
from pygame.locals import *
from Ground import Ground
from Bird import Bird
from Pipe import Pipe

pg.init()
pg.font.init()
pg.event.set_allowed([QUIT, KEYDOWN])

WIN_WIDTH = 570
WIN_HEIGHT = 900
GROUND_Y = 750
SCORE_FONT = pg.font.SysFont("vemana2000", 80)
DISPLAY_SURF = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT), DOUBLEBUF, 16)
pg.display.set_caption("Flappy Bird")


def loadify(img_name):
    return pg.image.load(img_name).convert_alpha()


BG_IMG = pg.transform.scale2x(loadify(os.path.join("images", "bg.png")))
GROUND_IMG = pg.transform.scale2x(loadify(os.path.join("images", "base.png")))
PIPE_IMG = pg.transform.scale2x(loadify(os.path.join("images", "pipe.png")))
BIRD_IMGS = [pg.transform.scale2x(loadify(os.path.join("images", "bird" + str(x) + ".png")))
             for x in range(1, 4)]


def draw_window(window, ground, bird, pipes, score):

    window.blit(BG_IMG, (0, -100))
    bird.draw(window)
    for pipe in pipes:
        pipe.draw(window)
    ground.draw(window)

    # score
    score_label = SCORE_FONT.render(str(score), True, (255, 255, 255))
    window.blit(score_label, (WIN_WIDTH / 2 - score_label.get_width() / 2, 100))

    pg.display.update((0, 0, WIN_WIDTH, WIN_HEIGHT))


def main(score):

    clock = pg.time.Clock()
    ground = Ground(GROUND_Y, GROUND_IMG)
    pipes = [Pipe(WIN_WIDTH, WIN_WIDTH, 50, GROUND_Y - 50, PIPE_IMG),
             Pipe(WIN_WIDTH, WIN_WIDTH + (WIN_WIDTH - PIPE_IMG.get_width()) // 2 + PIPE_IMG.get_width(),
                  50, GROUND_Y - 50, PIPE_IMG)]
    bird = Bird(200, 300, BIRD_IMGS)

    run = True
    started = False
    lost = False

    while run:
        clock.tick(30)
        pg.time.delay(10)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    if not started:
                        started = True
                        score = 0
                    bird.jump()

        if started:
            bird.move()
            for pipe in pipes:
                score += pipe.move()
                if pipe.collision(bird):
                    return score
            if bird.y > GROUND_Y - bird.img.get_height():
                return score

        ground.move()
        draw_window(DISPLAY_SURF, ground, bird, pipes, score)

    pg.quit()
    quit()


if __name__ == "__main__":
    result = 0
    while True:
        result = main(result)
