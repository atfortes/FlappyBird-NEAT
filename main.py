import os
import pickle

import neat
import pygame as pg
from pygame.locals import *
from Ground import Ground
from Bird import Bird
from Pipe import Pipe

pg.init()
pg.font.init()
pg.event.set_allowed([QUIT, KEYDOWN])

GEN = -1
WIN_WIDTH = 570
WIN_HEIGHT = 900
GROUND_Y = 750
SCORE_FONT = pg.font.SysFont("vemana2000", 80)
GEN_FONT = pg.font.SysFont("arial.ttf", 40)
DISPLAY_SURF = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT), DOUBLEBUF, 16)
pg.display.set_caption("Flappy Bird")


def loadify(img_name):
    return pg.image.load(img_name).convert_alpha()


BG_IMG = pg.transform.scale2x(loadify(os.path.join("images", "bg.png")))
GROUND_IMG = pg.transform.scale2x(loadify(os.path.join("images", "base.png")))
PIPE_IMG = pg.transform.scale2x(loadify(os.path.join("images", "pipe.png")))
BIRD_IMGS = [pg.transform.scale2x(loadify(os.path.join("images", "bird" + str(x) + ".png")))
             for x in range(1, 4)]


def draw_window(window, ground, birds, pipes, score, gen, birds_alive):
    window.blit(BG_IMG, (0, -100))
    for bird in birds:
        bird.draw(window)
    for pipe in pipes:
        pipe.draw(window)
    ground.draw(window)

    # score
    score_label = SCORE_FONT.render(str(score), True, (255, 255, 255))
    window.blit(score_label, (WIN_WIDTH / 2 - score_label.get_width() / 2, 100))

    # gen
    gen_label = GEN_FONT.render("Gen: " + str(gen), True, (255, 255, 255))
    window.blit(gen_label, (10, 10))

    # birds alive
    birds_alive_label = GEN_FONT.render("Alive: " + str(birds_alive), True, (255, 255, 255))
    window.blit(birds_alive_label, (10, 10 + gen_label.get_height()))

    pg.display.update((0, 0, WIN_WIDTH, WIN_HEIGHT))


def calculate_fitness(score, lifespan):
    return 1 + score**2 + lifespan/20


def kill_bird(birds, nets, ge, i):
    birds.pop(i)
    nets.pop(i)
    ge.pop(i)


def main(genomes, config, score=0):
    global GEN
    GEN += 1

    clock = pg.time.Clock()
    ground = Ground(GROUND_Y, GROUND_IMG)
    pipes = [Pipe(WIN_WIDTH, WIN_WIDTH, 100, GROUND_Y - 100, PIPE_IMG),
             Pipe(WIN_WIDTH, WIN_WIDTH + (WIN_WIDTH - PIPE_IMG.get_width()) // 2 + PIPE_IMG.get_width(),
                  100, GROUND_Y - 100, PIPE_IMG)]

    nets = []
    ge = []
    birds = []
    lifespan = 0

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(200, 300, BIRD_IMGS))
        g.fitness = 0
        ge.append(g)

    while True:
        clock.tick(30)
        pg.time.delay(10)
        lifespan += 1
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

        if not birds:
            return

        pipe_to_check = 0
        first_pipe_diff = pipes[0].x + PIPE_IMG.get_width() - birds[0].x
        second_pipe_diff = pipes[1].x + PIPE_IMG.get_width() - birds[0].x
        if 0 < second_pipe_diff < first_pipe_diff or first_pipe_diff < 0:
            pipe_to_check = 1

        # move birds
        for i, bird in enumerate(birds):
            bird.move()

            y_top = pipes[pipe_to_check].y_bottom - pipes[pipe_to_check].GAP
            output = nets[i].activate((bird.vel,
                                       pipes[pipe_to_check].x - bird.x,
                                       pipes[pipe_to_check].y_bottom - bird.y,
                                       y_top - bird.y))

            if output[0] > 0.5:
                bird.jump()

        # check ground and sky collisions
        for i, bird in enumerate(birds):
            if bird.y > GROUND_Y - bird.img.get_height() or bird.y < 0:
                ge[i].fitness = calculate_fitness(score, lifespan)
                kill_bird(birds, nets, ge, i)

        # check pipe collisions
        for pipe in pipes:
            pipe_scored = pipe.move()

            for i, bird in enumerate(birds):
                if pipe.collision(bird):
                    ge[i].fitness = calculate_fitness(score, lifespan)
                    kill_bird(birds, nets, ge, i)

            score += pipe_scored

        ground.move()
        draw_window(DISPLAY_SURF, ground, birds, pipes, score, GEN, len(birds))

        # should be a winner already
        if score > 49:
            for g in ge:
                g.fitness = calculate_fitness(score, lifespan)
            pickle.dump(nets[0], open("winner.pickle", "wb"))
            break


def run_neat(neat_config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                neat_config_path)

    # create the population
    p = neat.Population(config)

    # add a stdout reporter to show progress
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # run for up to 30 generations
    winner = p.run(main, 30)

    # show final stats
    print('\nWinner:\n{!s}'.format(winner))


if __name__ == "__main__":
    config_path = os.path.join(os.path.dirname(__file__), "neat-config.txt")
    run_neat(config_path)
