import pygame
import random
from os import path
import neat
import os
import math
from properties import *



class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        img_dir = path.join(path.dirname(__file__), 'img')
        player_up_img = pygame.image.load(path.join(img_dir, "spaceShips_Up.png")).convert()
        self.image = pygame.transform.scale(player_up_img, (50, 50))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = WIDTH / 2
        self.rect.bottom = HEIGHT - 50
        self.rect.y = HEIGHT - 100
        self.speedx = 0
        self.speedy = 0

    def moveLeft(self):
        self.speedx = -5
        self.rect.x += self.speedx


    def moveRight(self):
        self.speedx = 5
        self.rect.x += self.speedx

    def update(self):
        self.speedx = 0
        self.rect.x += self.speedx
        if self.rect.x < 29:
            self.rect.x = 29
        if self.rect.x > 524:
            self.rect.x = 524