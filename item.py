import pygame.transform

from utils import *

IMAGE:dict[str,pygame.Surface] = get_all_image()
class Item(pygame.sprite.Sprite):
    def __init__(self,item_name:str,center_x:int,bottom:int,num:int=1):
        super().__init__()
        self.item_name:str = item_name
        self.image = pygame.transform.scale(IMAGE[self.item_name],ITEM_TRANSFORM)
        self.rect = self.image.get_rect()
        self.rect.bottom = bottom
        self.rect.centerx = center_x
        self.speed_y = 0
        self.max_speed = -30
        self.num = num

    def update(self):
        self.speed_y -= GRAVITY
        if self.speed_y <= self.max_speed:
            self.speed_y = self.max_speed
        self.rect.y -= self.speed_y
        if self.rect.top >= HEIGHT:
            self.kill()
