import random

from const import *
from utils import *

IMAGE:dict[str,pygame.Surface] = get_all_image()
class Could:
    def __init__(self,speed_x:int):
        self.x = 0 if speed_x<=0 else WIDTH
        self.y = random.randint(0,HEIGHT)
        self.transform = random.randint(5,10)
        self.image_name = 'could'+str(random.randint(1,2))
        self.image = pygame.transform.scale(IMAGE[self.image_name],\
            (IMAGE[self.image_name].get_width()*self.transform,\
                IMAGE[self.image_name].get_height()*self.transform))
        self.image = pygame.transform.flip(self.image,True,False) if self.x ==0 else self.image
    def move(self,speed_x:int):
        self.x -= speed_x
        
    def draw(self,surface:pygame.Surface):
        surface.blit(self.image,(self.x,self.y))