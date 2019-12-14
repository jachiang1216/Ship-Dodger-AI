import pygame
import random
from os import path
import neat
import os
import math
from properties import *

class Obstacle(pygame.sprite.Sprite):
    GAP = 150
    VEL = 5

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img_dir = path.join(path.dirname(__file__), 'img')
        platform_img = pygame.image.load(path.join(img_dir, "platform.png")).convert()
        self.image = platform_img
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.gap = 100
        self.image.set_colorkey(BLACK)

    def update(self):
        self.rect.y += self.VEL