import pygame
import random
from os import path
import neat
import os
import math
from properties import *


class Wall:
    VEL = 5

    def __init__(self, x):
        img_dir = path.join(path.dirname(__file__), 'img')
        wall_img = pygame.image.load(path.join(img_dir, "wall.png")).convert()
        self.x = x
        self.y1 = 0
        self.HEIGHT = wall_img.get_height()
        self.IMG = wall_img
        self.y2 = self.HEIGHT

    def move(self):
        self.y1 += self.VEL
        self.y2 += self.VEL

        if self.y1 > HEIGHT:
            self.y1 = self.y2 - self.HEIGHT

        if self.y2 > HEIGHT:
           self.y2 = self.y1 - self.HEIGHT

    def draw(self,window):
        window.blit(self.IMG, (self.x, self.y1))
        window.blit(self.IMG, (self.x, self.y2))