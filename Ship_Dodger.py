# Asteroid AI Learning Game

import pygame
import random
from os import path
import neat
import os
from properties import *
import math
import Player
import Wall
import Obstacle

img_dir = path.join(path.dirname(__file__), 'img')
sound_dir = path.join(path.dirname(__file__), 'sound')

pygame.init()
pygame.mixer.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ship Dodger AI")
clock = pygame.time.Clock()

font_name = pygame.font.match_font('arial')

# Image Graphics
background = pygame.image.load( path.join(img_dir, "space.png")).convert()
background_rect = background.get_rect()
platform_img = pygame.image.load(path.join(img_dir, "platform.png")).convert()

# Music/Sounds
music = pygame.mixer.Sound(path.join(sound_dir, 'KingOfTheDesert.ogg'))
music.play(loops=-1)


def draw_text(surf, text, size, x, y):

    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.top = y
    text_rect.left = x
    surf.blit(text_surface, text_rect)



all_sprites = pygame.sprite.Group()
obstacle_sprites = pygame.sprite.Group()
generation = 0


def main(genomes, config):

    nets = []
    ge = []
    players = []
    walls = [Wall.Wall(-30), Wall.Wall(WIDTH-25)]
    obstacles = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        players.append(Player.Player())
        g.fitness = 0
        ge.append(g)

    for player in players:
        all_sprites.add(player)

    score = 0
    ctr = 0
    GAP = 150
    PLATFORM_IMG_WIDTH = 746
    # Game Loop
    running = True
    previous_elapse_time = -1
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                # PLAYER CONTROLS
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.speedx = -5
                elif event.key == pygame.K_RIGHT:
                    player.speedx = 5
            # PLAYER CONTROLS

        for wall in walls:
            wall.move()

        rem = []

        for obstacle in obstacles:
            # If Obstacle goes off screen
            if obstacle.rect.y > HEIGHT-20:
                rem.append(obstacle)


        if ctr % 70 == 0:
            x = random.randrange(-700, -344)
            obstacle = Obstacle.Obstacle(x, 0)
            obstacles.append(obstacle)
            all_sprites.add(obstacle)
            obstacle_sprites.add(obstacle)
            x2 = x + GAP + PLATFORM_IMG_WIDTH
            obstacle = Obstacle.Obstacle(x2, 0)
            obstacles.append(obstacle)
            all_sprites.add(obstacle)
            obstacle_sprites.add(obstacle)


        for r in rem:
            obstacles.remove(r)
            all_sprites.remove(r)
            obstacle_sprites.remove(r)
            score += 5
            ge[x].fitness += 5

        ctr += 1

        if len(players) < 1:
            for obstacle in obstacles:
                all_sprites.remove(obstacle)
                obstacle_sprites.remove(obstacle)
            generation += 1
            break
        # UPDATE
        for obstacle in obstacles:
            for x, player in enumerate(players):
                    collisions = pygame.sprite.spritecollide(player, obstacle_sprites, False)
                    if collisions:
                        players.pop(x)
                        all_sprites.remove(player)
                        nets.pop(x)
                        ge[x].fitness -= 5
                        ge.pop(x)

        ctr2 = 2
        for obstacle in obstacles:
            if obstacle.rect.y > HEIGHT/2.5 and obstacle.rect.y - obstacle.rect.height< player.rect.y:
                for x, player in enumerate(players):
                        output = nets[x].activate((player.rect.x,abs(player.rect.x - (obstacle.rect.x + obstacle.rect.width)), abs(player.rect.x - (obstacle.rect.x + obstacle.rect.width + GAP))))
                        if output[0] > 0.5:
                            player.moveLeft()
                        elif output[1] > 0.5:
                            player.moveRight()
            else:
                pass
            ctr2 += 1

        draw_window(window, score, generation, walls)



def draw_window(window, score, generation, walls):
    window.blit(background, background_rect)
    draw_text(window, "Generation: "+str(generation), 22, WIDTH/3, 10)
    draw_text(window, "Score: "+str(score), 22, 2*WIDTH/3, 10)

    for wall in walls:
        wall.draw(window)
    all_sprites.update()
    all_sprites.draw(window)
    pygame.display.update()


def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)
    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main, 50)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "feedforward.txt")
    run(config_path)


