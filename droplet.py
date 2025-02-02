import random

import pygame

from const import *
from utils import *

IMAGE:dict[str,pygame.Surface] = get_all_image()
class Droplet:
    def __init__(self,surface:pygame.Surface):
        
        self.x = random.randint(-100, WIDTH + 100)
        self.y = random.randint(-100, -50)
        self.size = random.randint(1, 2)
        self.surface = surface
        #self.image = IMAGE['droplet']

    def move(self,is_ending:bool,speed_x:int):
        self.speed_x = speed_x
        self.y += 10
        self.x -= self.speed_x

        if self.x < 0 or self.x > WIDTH or self.y > HEIGHT:

            if  not is_ending:
                self.x = random.randint(-100, WIDTH + 100)
                self.y = random.randint(-100, -50)
                self.speedy = random.randint(4, 10)
                self.size = random.randint(1, 2)
        if is_ending:
            del self

    def draw(self):
        #self.surface.blit(self.image,(int(self.x), int(self.y)))
        pygame.draw.rect(self.surface, '#99f2ff',
        pygame.Rect(self.x,self.y,self.size,self.size))